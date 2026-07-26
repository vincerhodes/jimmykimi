#!/usr/bin/env python3
"""site_audit.py — crawl a website and report dead links + per-page SEO basics.

Per page: exactly one <h1>, <h2> count, <title>, meta description, canonical
tag, viewport meta, images missing alt, response time, redirect chains,
mixed content (http assets on https pages). Site-wide: dead links (internal
+ external), duplicate titles, duplicate content, and a 0-100 health score.

Stdlib only. Usage:
    python3 site_audit.py <url> [--max-pages N] [--depth N] [--no-external]
                          [--timeout SECS] [--slow-threshold SECS] [--json]
"""

import argparse
import concurrent.futures
import hashlib
import html.parser
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree
from collections import deque

USER_AGENT = "site-audit/2.0 (+https://skills.sh; dead-link & SEO checker)"
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "ftp:")
HTML_TYPES = ("text/html", "application/xhtml")
MAX_REDIRECTS = 10


class FetchResult:
    def __init__(self, status, content_type, body, elapsed, chain):
        self.status = status            # int, 0 = network error
        self.content_type = content_type
        self.body = body
        self.elapsed = elapsed          # seconds for the full request
        self.chain = chain              # list of URLs visited (incl. final)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Disables automatic redirects so fetch() can record the chain itself."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect())
REDIRECT_CODES = (301, 302, 303, 307, 308)


def fetch(url, timeout, method="GET"):
    """Fetch URL, following redirects manually. Returns FetchResult."""
    chain = [url]
    current = url
    start = time.time()
    while True:
        req = urllib.request.Request(current, method=method,
                                     headers={"User-Agent": USER_AGENT})
        try:
            with _opener.open(req, timeout=timeout) as resp:
                body = b"" if method == "HEAD" else resp.read(2_000_000)
                return FetchResult(resp.status, resp.headers.get("Content-Type", ""),
                                   body, time.time() - start, chain)
        except urllib.error.HTTPError as e:
            location = e.headers.get("Location") if e.headers else None
            if e.code in REDIRECT_CODES and location:
                if len(chain) > MAX_REDIRECTS:
                    return FetchResult(508, "", b"", time.time() - start, chain)
                current = urllib.parse.urljoin(current, location)
                chain.append(current)
                if e.code == 303:
                    method = "GET"
                continue
            return FetchResult(e.code, e.headers.get("Content-Type", "") if e.headers else "",
                               b"", time.time() - start, chain)
        except Exception as e:
            return FetchResult(0, "", str(e).encode(), time.time() - start, chain)


def check_link(url, timeout):
    """HEAD first, fall back to GET on 405/501/network error. Return status int."""
    r = fetch(url, timeout, method="HEAD")
    if r.status in (405, 501) or r.status == 0:
        r = fetch(url, timeout, method="GET")
    return r.status


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_description = None
        self.canonical = None
        self.has_viewport = False
        self.h1_texts = []
        self.h2_count = 0
        self.imgs_missing_alt = 0
        self.links = []            # absolute <a href> URLs
        self.http_assets = []      # http:// asset URLs (mixed content check)
        self.body_text = []        # for duplicate-content hash
        self.base_url = ""
        self._capture = None       # "title" | "h1"
        self._buf = []
        self._skip_text = 0        # inside script/style
        self._in_title = 0         # inside <title> (excluded from content hash)

    def _abs(self, url):
        return urllib.parse.urljoin(self.base_url, url)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self._skip_text += 1
        if tag == "title":
            self._capture, self._buf = "title", []
            self._in_title += 1
        elif tag == "h1":
            self._capture, self._buf = "h1", []
        elif tag == "h2":
            self.h2_count += 1
        elif tag == "meta":
            name = attrs.get("name", "").lower()
            if name == "description":
                self.meta_description = attrs.get("content", "").strip() or None
            elif name == "viewport":
                self.has_viewport = True
        elif tag == "link":
            if attrs.get("rel", "").lower() == "canonical" and attrs.get("href"):
                self.canonical = self._abs(attrs["href"].strip())
            href = attrs.get("href", "")
            if href.startswith("http://"):
                self.http_assets.append(self._abs(href))
        elif tag == "img":
            if "alt" not in attrs or not attrs.get("alt", "").strip():
                self.imgs_missing_alt += 1
            src = attrs.get("src", "")
            if src.startswith("http://"):
                self.http_assets.append(self._abs(src))
        elif tag in ("script", "iframe"):
            src = attrs.get("src", "")
            if src.startswith("http://"):
                self.http_assets.append(self._abs(src))
        elif tag == "a":
            href = attrs.get("href", "").strip()
            if href and not href.startswith(SKIP_SCHEMES) and href != "#":
                absolute = self._abs(href)
                if absolute.startswith(("http://", "https://")):
                    self.links.append(absolute)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_text:
            self._skip_text -= 1
        if tag == "title" and self._in_title:
            self._in_title -= 1
        if self._capture and tag == self._capture:
            text = " ".join("".join(self._buf).split())
            if self._capture == "title":
                self.title = text
            else:
                self.h1_texts.append(text)
            self._capture, self._buf = None, []

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)
        if not self._skip_text and not self._in_title:
            self.body_text.append(data)

    def content_hash(self):
        text = " ".join("".join(self.body_text).split()).lower()
        return hashlib.sha256(text.encode()).hexdigest()[:16]


def normalize(url):
    """Strip fragment; lowercase scheme/host; default path '/'."""
    parts = urllib.parse.urlsplit(url)
    path = parts.path or "/"
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                                    path, parts.query, ""))


def sitemap_urls(root, timeout):
    """Try /sitemap.xml; return list of page URLs (best effort)."""
    urls = []
    r = fetch(urllib.parse.urljoin(root, "/sitemap.xml"), timeout)
    if r.status != 200 or not r.body:
        return urls
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    def locs(xml_bytes):
        try:
            tree = xml.etree.ElementTree.fromstring(xml_bytes)
        except xml.etree.ElementTree.ParseError:
            return [], []
        pages = [l.text.strip() for l in
                 (tree.findall(".//s:url/s:loc", ns) or tree.findall(".//url/loc"))
                 if l.text]
        indexes = [l.text.strip() for l in
                   (tree.findall(".//s:sitemap/s:loc", ns) or tree.findall(".//sitemap/loc"))
                   if l.text]
        return pages, indexes

    pages, indexes = locs(r.body)
    urls.extend(pages)
    for idx in indexes:  # one level of sitemap index
        r2 = fetch(idx, timeout)
        if r2.status == 200 and r2.body:
            p2, _ = locs(r2.body)
            urls.extend(p2)
    return urls


def crawl(start_url, max_pages, max_depth, check_external, timeout):
    origin = urllib.parse.urlsplit(start_url).netloc.lower()
    start_url = normalize(start_url)

    pages = {}        # normalized url -> PageParser
    fetch_meta = {}   # normalized url -> FetchResult (for time/redirects)
    page_links = {}   # normalized url -> list of raw link urls

    frontier = deque([(start_url, 0)])
    seen = {start_url}
    for u in sitemap_urls(start_url, timeout):
        n = normalize(u)
        if urllib.parse.urlsplit(n).netloc.lower() == origin and n not in seen:
            seen.add(n)
            frontier.append((n, max_depth))

    while frontier and len(pages) < max_pages:
        url, depth = frontier.popleft()
        r = fetch(url, timeout)
        if r.status != 200 or not any(t in r.content_type for t in HTML_TYPES):
            continue
        parser = PageParser()
        parser.base_url = url
        try:
            parser.feed(r.body.decode("utf-8", errors="replace"))
        except Exception:
            pass
        pages[url] = parser
        fetch_meta[url] = r
        page_links[url] = parser.links
        if depth < max_depth:
            for link in parser.links:
                n = normalize(link)
                if (urllib.parse.urlsplit(n).netloc.lower() == origin
                        and n not in seen and len(seen) < max_pages * 4):
                    seen.add(n)
                    frontier.append((n, depth + 1))

    # Check unique links concurrently (fragments stripped)
    to_check = set()
    for links in page_links.values():
        for link in links:
            if check_external or urllib.parse.urlsplit(link).netloc.lower() == origin:
                to_check.add(urllib.parse.urlsplit(link)._replace(fragment="").geturl())

    link_status = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(check_link, u, timeout): u for u in to_check}
        for fut in concurrent.futures.as_completed(futures):
            link_status[futures[fut]] = fut.result()

    return pages, fetch_meta, page_links, link_status, origin


def is_dead(status):
    return status == 0 or status >= 400


def build_report(start_url, pages, fetch_meta, page_links, link_status, origin,
                 slow_threshold):
    dead = []
    for page, links in sorted(page_links.items()):
        for link in sorted(set(links)):
            key = urllib.parse.urlsplit(link)._replace(fragment="").geturl()
            status = link_status.get(key)
            if status is not None and is_dead(status):
                dead.append((page, link, status))

    seo = []
    titles = {}
    hashes = {}
    redirects = []  # (requested, chain) with >1 hop
    is_https_site = start_url.startswith("https://")

    for page, p in sorted(pages.items()):
        titles.setdefault(p.title, []).append(page)
        hashes.setdefault(p.content_hash(), []).append(page)
        meta = fetch_meta[page]
        if len(meta.chain) > 2:  # requested -> at least one redirect -> final
            redirects.append((page, meta.chain))

        issues = []
        if len(p.h1_texts) == 0:
            issues.append("NO H1")
        elif len(p.h1_texts) > 1:
            issues.append(f"{len(p.h1_texts)}x H1")
        if not p.title:
            issues.append("no title")
        if not p.meta_description:
            issues.append("no meta desc")
        if not p.canonical:
            issues.append("no canonical")
        elif normalize(p.canonical) != page:
            issues.append("canonical->other")
        if not p.has_viewport:
            issues.append("no viewport")
        if p.imgs_missing_alt:
            issues.append(f"{p.imgs_missing_alt} img no alt")
        if is_https_site and p.http_assets:
            issues.append(f"{len(p.http_assets)} mixed content")
        if meta.elapsed > slow_threshold:
            issues.append(f"slow ({meta.elapsed:.1f}s)")
        seo.append({
            "page": page,
            "title": p.title or "(none)",
            "h1_count": len(p.h1_texts),
            "h2_count": p.h2_count,
            "meta_desc": bool(p.meta_description),
            "canonical": p.canonical or "(none)",
            "time_s": round(meta.elapsed, 2),
            "redirect_hops": len(meta.chain) - 1,
            "imgs_missing_alt": p.imgs_missing_alt,
            "mixed_content": p.http_assets if is_https_site else [],
            "issues": issues,
        })

    dup_titles = {t: ps for t, ps in titles.items() if t and len(ps) > 1}
    dup_content = {h: ps for h, ps in hashes.items() if len(ps) > 1}

    score = health_score(dead, seo, dup_titles, dup_content, redirects)
    return {"dead_links": dead, "seo": seo, "duplicate_titles": dup_titles,
            "duplicate_content": dup_content, "redirects": redirects,
            "health_score": score}


def health_score(dead, seo, dup_titles, dup_content, redirects):
    """0-100 heuristic rollup. Start at 100, deduct per issue class."""
    def cap(n, per, ceiling):
        return min(n * per, ceiling)

    no_h1 = sum(1 for s in seo if s["h1_count"] == 0)
    multi_h1 = sum(1 for s in seo if s["h1_count"] > 1)
    no_title = sum(1 for s in seo if s["title"] == "(none)")
    no_meta = sum(1 for s in seo if not s["meta_desc"])
    no_canon = sum(1 for s in seo if s["canonical"] == "(none)")
    no_viewport = sum(1 for s in seo if "no viewport" in s["issues"])
    mixed = sum(1 for s in seo if s["mixed_content"])
    slow = sum(1 for s in seo if any(i.startswith("slow") for i in s["issues"]))
    missing_alt = sum(s["imgs_missing_alt"] for s in seo)

    deductions = (
        cap(len(dead), 5, 30) +
        cap(no_h1, 5, 20) +
        cap(multi_h1, 2, 10) +
        cap(no_title + len(dup_titles), 3, 10) +
        cap(no_meta, 2, 10) +
        cap(no_canon, 1, 5) +
        (10 if no_viewport else 0) +
        cap(mixed, 5, 15) +
        cap(slow, 3, 10) +
        cap(len(redirects), 2, 10) +
        cap(len(dup_content), 5, 10) +
        cap(missing_alt, 1, 5)
    )
    return max(0, 100 - deductions)


def render_markdown(start_url, pages, report, elapsed):
    dead = report["dead_links"]
    seo = report["seo"]
    dups_t = report["duplicate_titles"]
    dups_c = report["duplicate_content"]
    redirects = report["redirects"]

    out = []
    out.append(f"# Site audit: {start_url}")
    out.append(f"\n**Health score: {report['health_score']}/100** — "
               f"crawled {len(pages)} pages in {elapsed:.0f}s, "
               f"{len(dead)} dead link(s), "
               f"{sum(1 for s in seo if s['issues'])} page(s) with issues.\n")

    out.append("## Dead links\n")
    if not dead:
        out.append("None found. ✅\n")
    else:
        out.append("| Source page | Broken link | Status |")
        out.append("|---|---|---|")
        for page, link, status in dead:
            out.append(f"| {page} | {link} | {'network error' if status == 0 else status} |")
    out.append("")

    out.append("## Per-page SEO\n")
    out.append("| Page | Title | H1 | H2s | Meta desc | Canonical | Time | Issues |")
    out.append("|---|---|---|---|---|---|---|---|")
    for s in seo:
        title = s["title"][:40] + ("…" if len(s["title"]) > 40 else "")
        canon = "yes" if s["canonical"] != "(none)" else "NO"
        out.append(f"| {s['page']} | {title} | {s['h1_count']} | {s['h2_count']}"
                   f" | {'yes' if s['meta_desc'] else 'NO'} | {canon}"
                   f" | {s['time_s']}s | {', '.join(s['issues']) or 'ok'} |")
    out.append("")

    if redirects:
        out.append("## Redirect chains\n")
        out.append("| Requested | Hops | Final URL |")
        out.append("|---|---|---|")
        for requested, chain in redirects:
            out.append(f"| {requested} | {len(chain) - 1} | {chain[-1]} |")
        out.append("")

    if dups_t:
        out.append("## Duplicate titles\n")
        for t, ps in dups_t.items():
            out.append(f"- \"{t}\": {', '.join(ps)}")
        out.append("")

    if dups_c:
        out.append("## Duplicate content (identical body text)\n")
        for h, ps in dups_c.items():
            out.append(f"- {', '.join(ps)}")
        out.append("")

    out.append("---")
    out.append("Health score is a heuristic: deductions for dead links, heading/title/meta "
               "problems, missing canonical/viewport, mixed content, slow pages, redirect "
               "chains, and duplicate content.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Dead-link + SEO site audit")
    ap.add_argument("url", help="Root URL, e.g. https://example.com")
    ap.add_argument("--max-pages", type=int, default=100)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--no-external", action="store_true",
                    help="Only check internal links")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--slow-threshold", type=float, default=1.5,
                    help="Seconds before a page is flagged slow (default 1.5)")
    ap.add_argument("--json", action="store_true", help="JSON output instead of Markdown")
    args = ap.parse_args()

    start = time.time()
    pages, fetch_meta, page_links, link_status, origin = crawl(
        args.url, args.max_pages, args.depth, not args.no_external, args.timeout)
    report = build_report(args.url, pages, fetch_meta, page_links, link_status,
                          origin, args.slow_threshold)
    elapsed = time.time() - start

    if not pages:
        print("ERROR: no HTML pages crawled — check the URL is reachable.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps({
            "url": args.url, "pages_crawled": len(pages),
            "health_score": report["health_score"],
            "dead_links": [{"source": p, "link": l, "status": s}
                           for p, l, s in report["dead_links"]],
            "seo": [{k: v for k, v in s.items() if k != "mixed_content" or True}
                    for s in report["seo"]],
            "redirects": [{"requested": r, "chain": c} for r, c in report["redirects"]],
            "duplicate_titles": report["duplicate_titles"],
            "duplicate_content": report["duplicate_content"],
        }, indent=2))
    else:
        print(render_markdown(args.url, pages, report, elapsed))

    has_issues = (report["dead_links"] or any(s["issues"] for s in report["seo"])
                  or report["duplicate_titles"] or report["duplicate_content"])
    sys.exit(2 if has_issues else 0)


if __name__ == "__main__":
    main()

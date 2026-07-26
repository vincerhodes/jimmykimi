---
name: site-audit
description: Crawl a website and report dead links plus per-page SEO (H1, H2, title, meta description, canonical, viewport, image alt, page speed, redirect chains, mixed content, duplicates) with a 0-100 health score.
whenToUse: When the user asks to check a site for dead/broken links, audit SEO, verify H1/H2 tags on every page, or get a site health score
---

# Site Audit

Crawl a live website and produce a Markdown report covering:

- **Dead links** — every `<a href>` checked (internal + external), grouped by source page with HTTP status
- **Per-page SEO** — H1 count (flags missing or multiple), H2 count, `<title>`, meta description, canonical tag, viewport meta, images missing alt text
- **Performance** — response time per page, flags pages over a threshold (default 1.5s)
- **Redirect chains** — pages reached via >1 hop, with the final URL
- **Mixed content** — `http://` assets (img/script/link/iframe) on `https://` pages
- **Duplicates** — duplicate titles and duplicate body content across pages
- **Health score** — 0–100 heuristic rollup of all the above

## Usage

Run the bundled script (Python 3, stdlib only, no dependencies):

```bash
python3 ~/.agents/skills/site-audit/site_audit.py <url>
```

Options:
- `--max-pages N` (default 100) — crawl cap
- `--depth N` (default 3) — link-follow depth from the root
- `--no-external` — only check internal links (much faster)
- `--timeout SECS` (default 10)
- `--slow-threshold SECS` (default 1.5) — page response time flag
- `--json` — machine-readable output instead of Markdown

Pages are discovered from `/sitemap.xml` (if present) plus same-origin BFS from the root URL.

Exit codes: `0` = clean, `1` = crawl failed, `2` = issues found.

## Workflow

1. Run the script against the target URL. For large sites start with `--no-external`, then do a full run including external links.
2. Summarise the report for the user: health score, dead-link count and worst offenders, pages missing H1/H2, slowest pages.
3. Offer to fix issues in the codebase (map URLs back to source files/templates).

## Notes

- Only HTML pages are audited; non-HTML assets are link-checked but not parsed.
- JavaScript-rendered content is not seen — the audit reflects the raw HTML response. If the site is a client-rendered SPA, note this caveat.
- The health score is a heuristic for prioritisation, not a Google metric.
- Be polite: the script fetches sequentially for pages (8-way parallel only for link checks). Don't point it at sites you don't own without care.

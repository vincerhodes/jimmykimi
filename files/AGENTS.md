# Jimmy — Global Context

## About Me
- Developer across multiple projects (currently: Browzr, Jimfolio)
- Value comprehensive planning before implementation
- Prefer concise, direct responses

## Planning-First Rule
Every non-trivial task begins with a planning folder.
Before writing implementation code: create planning/ with 00-master-plan.md.
Only begin Phase 1 after the plan is reviewed and confirmed.

## Planning Document Standard
Planning docs must be executable by any LLM without prior conversation context.
- Exact file paths, not "the config file"
- Exact commands to run, not "install it"
- Explicit constraints (what to preserve, what NOT to do)
- Acceptance criteria must be shell-testable where possible
- No assumed shared context — treat executing model as stateless

## Response Style
- Terse. No preamble, no summaries of what you just did.
- If you read a file, don't narrate that you're about to read a file.
- If there's nothing to add after a tool call, say nothing.

## Sub-Agent Routing
- Routine reads/exploration → `explore` subagent
- Multi-file implementation → `coder` subagent
- Architecture / design analysis → `plan` subagent
- Workers return tight `file:line` summaries, never full file dumps

## Cross-Project Rules
- Never push directly to main — always branch + PR
- Check for a planning/ folder before starting implementation
- Run security scan before any PR that touches auth or user input

## Email
- ALWAYS CC `you@yourdomain.com` on anything sent from `ai@yourdomain.com` (emailmcp) — every recipient, every message, no exceptions.

## Git Commits
- Auto-commit WITHOUT asking when all of these hold:
  1. The changes belong to the current approved task (never sweep up user WIP or unrelated dirty files).
  2. Build/tests covering the change are green (run them first if the project has them; if a project has no tests, a green build suffices).
  3. One logical change per commit, Conventional Commits format.
- Pushing is also auto-approved under the same conditions (green tests, on-task changes) — push the current branch to its remote without asking.
- Never push to main directly (branch + PR still applies); creating PRs still needs explicit approval each time.
- If any condition fails (red tests, mixed/unrelated changes), stop and ask instead of committing.

## Hetzner
- Infra managed via `/skill:hetzner-infra` (OpenTofu; example repo at ~/dev/hetzner-infra)
- API token at ~/.config/hetzner-infra/token (never in repos)
- Prices have risen a lot — never quote from memory, fetch /v1/pricing live (skill has the command)

## Cloudflare (DNS for all domains, added 2026-07-19)
- API token at `~/.config/cloudflare/token` (all-zones DNS-edit scope, chmod 600, never in repos).
- Zones: `yourdomain.com` = `<cloudflare-zone-id>`; also your-second-domain.com, your-third-domain.com (IDs via `GET /zones`).
- API base `https://api.cloudflare.com/client/v4` — behind GFW but reachable; use `curl -x http://127.0.0.1:7897` anyway if flaky.
- Add app CNAME: `POST /zones/<zone>/dns_records {"type":"CNAME","name":"<app>","content":"cname.vercel-dns.com","proxied":false,"ttl":1}`.
- `proxied` MUST be false for Vercel CNAMEs (orange-cloud proxy in front of Vercel breaks TLS).
- Lesson: Cloudflare zone-import scans can MISS records — after any NS flip/import, diff records against reality before calling it done (2026-07-19 incident: 3 live apps NXDOMAIN).

## Network: GFW + Clash Verge (mihomo) on this machine
- Machine is behind the GFW. Clash Verge Rev + mihomo, Nexitally subscription, system-proxy mode.
- `curl` ignores the system proxy — always `curl -x http://127.0.0.1:7897` (mixed port) for blocked sites.
- GFW-poisoned: `*.vercel.app`, `vercel-dns.com` (kills Vercel custom-domain TLS locally), OpenRouter API.
  NOT blocked: `vercel.com`, `api.vercel.com`, GitHub.
- mihomo API via unix socket: `curl --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/{rules,proxies,connections,dns/query?name=...}`
- Clash Verge Rev merge quirks (this version): `prepend-rules` in Merge.yaml is NOT interpreted (deep-merged verbatim).
  Rule overrides go in the profile's rules-extend file (`~/.local/share/io.github.clash-verge-rev.clash-verge-rev/profiles/<id>.yaml`,
  `prepend:`/`append:`/`delete:` lists). Currently active: `rliOO7wLrfar.yaml` with `DOMAIN-SUFFIX,yourdomain.com,Proxies`.
  Changes apply only after re-clicking the subscription profile in the GUI.
- Nexitally tunnel breaks TLS to `*.yourdomain.com` custom Vercel domains specifically (relay-side DNS poisons
  the vercel-dns.com CNAME chain); `*.vercel.app` aliases work through the same node. Use the vercel.app alias for testing.
- External 200 check that works: `curl -x http://127.0.0.1:7897 "https://api.hackertarget.com/httpheaders/?q=<domain>"`
- Vercel MCP OAuth token doubles as a REST API Bearer token: `~/.kimi-code/credentials/mcp/vercel-*-tokens.json` → `access_token`.
  Works for api.vercel.com (project create, env vars, deploys, domains) — no `vercel login` needed. Expires hourly.
- ALL Vercel projects are git-linked (Vercel GitHub App installed 2026-07-26) — this is the DEFAULT for every
  project going forward: when creating a new Vercel project, link it to its GitHub repo immediately.
  Monorepo apps link to `vincerhodes/your-monorepo` with `rootDirectory=apps/<app>`; standalone apps
  (standalone app repos — private; source at ~/dev/<name>) link to their own repos, no rootDirectory. Merges to main auto-deploy affected apps (Vercel
  skips builds when rootDirectory unchanged); branch pushes trigger previews.
  Link API: `POST /v9/projects/<id>/link {"type":"github","repo":"vincerhodes/<repo>"}`
  + `PATCH /v9/projects/<id> {"rootDirectory":"apps/<app>"}` (monorepo only). Manual CLI deploy as fallback:
  `cd apps/<app> && npx vercel@latest deploy --prod --yes --token <access_token>` (use `HTTPS_PROXY=http://127.0.0.1:7897`).
  `*.vercel.app` deployment URLs are behind Vercel SSO deployment protection — verify gates/custom behavior
  on the custom domain via `api.hackertarget.com/httpheaders/?q=app.yourdomain.com` instead.
- Crema gate: `CREMA_PASSWORD` env on Vercel (prod+preview) enables the site-wide password (middleware → `/login`).

## Context Management
- At 50% context: invoke `/skill:context-save` before compaction
- New task after compaction: re-read planning/00-master-plan.md first
- **Proactively recommend a fresh chat at breakpoints.** When context is getting heavy AND we're at a
  natural seam — a phase just finished, a task shipped, about to start something new — recommend a
  fresh session rather than pushing on. Prefer a clean break over a degraded long session.
- **Never cut mid-task.** Do NOT suggest a new session in the middle of an edit, a debug loop, or an
  unfinished phase — finish the coherent unit of work first, then recommend the break at the seam.
- **Default break action is `/skill:respawn`, not `/skill:handoff`.** At a seam, run respawn — it
  hands off, primes the auto-resume marker, and `/clear` restarts fresh with auto-resume. Use plain
  `/skill:handoff` only when stopping entirely or moving machine.
- At session start, if `planning/.respawn-pending` exists: a respawn was primed — delete the marker
  and invoke `/skill:resume-from-handoff` immediately (re-enable caveman at the recorded level).

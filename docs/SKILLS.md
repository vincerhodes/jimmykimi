# Skills Catalog — 27 user-scope skills

Installed to `~/.agents/skills/` — verbatim copies in [`../skills/`](../skills/). Each is a directory with a `SKILL.md` (some have supporting scripts/docs).

## Caveman family (token compression)

| Skill | What it does |
|---|---|
| `caveman` | Ultra-compressed "caveman speak" communication mode (~75% token cut). Intensity levels: lite / full / ultra (default), plus wenyan-lite/full/ultra (compressed classical Chinese) |
| `caveman-commit` | Ultra-compressed Conventional Commits generator — subject ≤50 chars, body only when the "why" isn't obvious |
| `caveman-compress` | Compress memory files (CLAUDE.md, AGENTS.md, todos) into caveman format, with validation + benchmark scripts (Python) |
| `caveman-help` | Quick-reference card for all caveman modes and commands |
| `caveman-review` | One-line-per-issue code review comments (location, problem, fix) |

## Session & context management

| Skill | What it does |
|---|---|
| `context-save` | Save session context to disk before compaction, at >50% context, or when switching tasks |
| `handoff` | Write/update the living `planning/HANDOFF.md` so a fresh session can resume cleanly |
| `resume-from-handoff` | Resume a build from `planning/HANDOFF.md` — read guardrails, verify green build, pick up next phase |
| `respawn` | Handoff + prime auto-resume marker + `/clear` — fresh session in the same window that auto-resumes |

## TDD family

| Skill | What it does |
|---|---|
| `tdd-cycle` | Full red-green-refactor orchestration with coverage gates; `--incremental` or `--suite` modes |
| `tdd-red` | Write failing tests first (AAA structure, happy path + edge + error cases) |
| `tdd-green` | Minimal production code to make failing tests pass — no premature optimisation |
| `tdd-refactor` | Atomic refactors with the suite staying green |

## Review & quality

| Skill | What it does |
|---|---|
| `pr-review` | Review current branch vs main — first-pass review then security pass, combined verdict |
| `security-scan` | Security findings by severity with `file:line` and remediation (required before PRs touching auth/user input) |
| `code-review-checklist` | Checklist for PR reviews and pre-commit self-review |
| `smart-debug` | Root-cause debugging — reproduce, confirm hypothesis, minimal fix, verify with the suite |
| `site-audit` | Crawl a website: dead links, per-page SEO (H1/H2/title/meta/canonical/alt/speed/redirects), 0–100 health score |

## Git & planning

| Skill | What it does |
|---|---|
| `git-conventional-commits` | Conventional Commits conventions |
| `planning-workflow` | Scaffold a `planning/` folder (`00-master-plan.md` etc.) before any implementation |

## Communication / email

| Skill | What it does |
|---|---|
| `email-nordy` | Email a collaborator in NZ lingo via `emailmcp`, always CC Jimmy; coding work gets Claude Code prompts |
| `send-project-intro` | Project intro/summary email to the team, built from planning files |
| `send-project-update` | Structured project update email (recent git changes, needs-testing, confirmed-working) |
| `expenses-summary` | Process the expenses inbox via `inboxmcp` into a Xero-ready summary email, then file processed mail |

## Infrastructure & references

| Skill | What it does |
|---|---|
| `hetzner-infra` | Provision/manage Hetzner Cloud VPS servers with OpenTofu (API token lives outside repos) |
| `openrouter-typescript-sdk` | Reference for the OpenRouter TS SDK using the callModel pattern (300+ models) |
| `find-skills` | Discover and install new agent skills |

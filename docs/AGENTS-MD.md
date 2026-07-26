# AGENTS.md — the behavioral core

Source file: [`../files/AGENTS.md`](../files/AGENTS.md) → installed to `~/.kimi-code/AGENTS.md`

This is the global instruction file kimi reads at every session start, in every project. It encodes the working conventions the whole setup is built around. The file itself is the source of truth — this page is the guided tour.

## The rules it encodes

**Planning-first.** Every non-trivial task begins with a `planning/` folder and a `00-master-plan.md`. Implementation starts only after the plan is reviewed. Planning docs must be executable by a *stateless* LLM: exact file paths, exact commands, shell-testable acceptance criteria, explicit "do NOT touch" constraints.

**Response style.** Terse. No preamble, no "I'm about to read a file" narration, no summaries of what was just done.

**Sub-agent routing.** Exploration → `explore` subagent; multi-file implementation → `coder`; architecture/design → `plan`. Workers return tight `file:line` summaries, never full file dumps.

**Cross-project rules.** Never push to main directly (branch + PR). Check for a `planning/` folder before implementing. Security scan before any PR touching auth or user input.

**Git commits.** Auto-commit/push without asking *only* when: the changes belong to the current approved task, tests/build are green, and it's one logical Conventional Commit. Anything mixed or red → stop and ask. PR creation always needs explicit approval.

**Context management.** `/skill:context-save` at 50% context; re-read the master plan after compaction; recommend a fresh session at natural seams (never mid-task); default break action is `/skill:respawn`; at session start, honor a `planning/.respawn-pending` marker by invoking `resume-from-handoff`.

**Infrastructure notes.** The file also carries hard-won operational lessons as reference data for future sessions: Hetzner/OpenTofu layout, Cloudflare DNS automation (`proxied` must be false for Vercel CNAMEs; zone-import scans can miss records), Vercel git-linking conventions (monorepo `rootDirectory`, link API calls), and local network workarounds (proxy usage for blocked endpoints).

## Why it matters for recreation

The skills and hooks are machinery; this file is the policy layer that ties them together — e.g. the respawn skill primes the marker, `respawn-resume.sh` prints the hint, but it's the AGENTS.md marker-check rule that guarantees the resume actually happens. Install it verbatim and the conventions come with it.

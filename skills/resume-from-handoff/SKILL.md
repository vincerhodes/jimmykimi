---
name: resume-from-handoff
description: Resume a build/session from planning/HANDOFF.md — read guardrails, verify the build is green, pick up at the next phase.
whenToUse: At the start of a fresh session when the user says "resume from handoff" or "pick up where we left off", or after a respawn
---

# Resume From Handoff

Re-enter an in-progress project from its living handoff doc so a fresh session
continues exactly where the last one stopped — no re-derivation, no guessing.

## Steps

1. **Locate the handoff.** Look for `planning/HANDOFF.md` (fallback: `HANDOFF.md`
   at repo root, then any `**/HANDOFF.md`). If none exists, tell the user and
   offer to run `/skill:handoff` conventions in reverse — do not invent state.
2. **Read the required context, in order:**
   - `planning/HANDOFF.md` — where we are, decisions, next-phase checklist.
   - `AGENTS.md` (project) — guardrails and hard rules.
   - The specific planning doc(s) the handoff names for the phase being entered
     (the handoff should point at them; read those, not all of them).
3. **Verify the tree matches the handoff.** `git status --porcelain`,
   `git branch --show-current`, `git log --oneline -5`. Confirm the branch and
   last commit line up with what the handoff claims. Flag any drift.
4. **Run the verify-on-entry commands** the handoff specifies (e.g.
   `make build && make test && make harness`). If the handoff gives none, run the
   project's standard build/test. All must be green before building on top.
   If red, stop and report — the handoff's "done" claims are suspect.
5. **Confirm the entry point.** State back to the user, in 3–5 lines: current
   phase, what's done, the exact next task from the handoff's entry checklist,
   and any open decision that gates it. Then ask whether to proceed with that
   next task or something else.

## Guards

- Trust the docs over memory, but trust the actual build state over the docs.
  If `make test` fails on a "done" phase, surface that before doing anything.
- Do not start implementing until the verify step is green and the user has
  confirmed the next task — the handoff may predate a decision the user has
  since changed.
- Re-read the phase's planning doc even if a recalled memory summarises it;
  memories can be stale.

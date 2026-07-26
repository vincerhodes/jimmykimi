---
name: respawn
description: Hand off and restart fresh in the same window — runs handoff, primes an auto-resume marker, then /clear auto-resumes.
whenToUse: When the user says "respawn", "uber resume", "handoff and clear", or at a clean seam with heavy context
---

# Respawn

Replaces the old ritual (handoff → exit → relaunch → resume) with:
`/skill:respawn` → `/clear` → any message. Everything else is automatic.

## Steps

1. **Detect caveman state FIRST, before anything else.** Judge from the current
   conversation whether caveman mode is active and at what level
   (`lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra`), or `off` if not
   active. Do this now because the handoff step is long and the judgement is
   about *this* conversation.
2. **Run the handoff.** Invoke the `handoff` skill and complete it fully —
   including its "is now a good time?" judgement. If it concludes this is a bad
   handoff point, or it aborts (dirty tree it can't resolve, red tests), stop
   here: report why, and do NOT prime the marker.
3. **Prime the auto-resume marker** (only after the handoff finished cleanly):
   ```sh
   mkdir -p planning && printf 'caveman=%s\n' '<level-or-off>' > planning/.respawn-pending
   ```
4. **Tell the user, then stop:**
   > Respawn primed. Type `/clear` now, then send any message (e.g. `go`) —
   > the fresh session auto-resumes from the handoff
   > [+ re-enables caveman `<level>`].

## How the second half works (reference)

`~/.kimi-code/hooks/respawn-resume.sh` runs on `SessionStart` with matcher
`startup` (which `/clear` triggers). If `planning/.respawn-pending` exists and
is under 60 minutes old, it deletes the marker and injects instructions into the
fresh context: re-enable caveman at the recorded level, then run
`resume-from-handoff`. Stale markers are silently discarded, and the marker is
project-local, so an ordinary `/clear` (or one in another project) resumes
nothing. A matching AGENTS.md rule covers the same path as a fallback.

## Guards

- Never prime the marker if the handoff was aborted or incomplete — a marker
  without a fresh HANDOFF.md makes the next session resume stale state.
- Don't run the handoff twice; if the user invokes `/skill:respawn` right after
  a manual `/skill:handoff` and nothing has changed, skip to step 3.

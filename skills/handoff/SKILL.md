---
name: handoff
description: Write or update the living handoff doc (planning/HANDOFF.md) so a fresh session can resume cleanly.
whenToUse: When the user says "write a handoff", "hand off", "wrap up for now", or before ending a session mid-project
---

# Handoff

Produce a handoff that a stateless future session (any LLM, no prior context)
can execute from. Four steps, in order. Do not skip step 1.

## 1. Is now a good time to hand off?

Judge the tradeoff before writing anything, and say your verdict out loud:

- **Good point:** a phase/task is complete, tests are green, the tree is
  logically consistent (no half-applied refactor), and the *next* task is
  cleanly separable. Hand off.
- **Bad point:** mid-edit, tests red, a decision half-made, or the next step is
  only meaningful with reasoning that lives in this session's context. Either
  finish the small remaining bit first, or capture the in-flight reasoning
  explicitly in the handoff so it isn't lost.
- **Context-efficiency angle:** if context is getting heavy (~50%+) but work is
  at a clean seam, handing off now and resuming fresh is *cheaper and safer*
  than pushing further in a degraded window — prefer it. If context is light and
  the task is nearly done, just finish it; a handoff has overhead too.

State: "Good handoff point because …" or "Not ideal yet — recommend X first."
If not ideal, get user agreement before proceeding.

## 2. Push outstanding work, confirm porcelain

- `git status --porcelain` and `git branch --show-current`.
- Commit anything outstanding that belongs in this unit of work (respect the
  project's git rules — branch + PR vs. direct-to-main; check AGENTS.md). Write
  a real Conventional-Commit message.
- Push the branch (and open/update the PR if that's the project's workflow).
- Re-run `git status --porcelain` and confirm **empty** (clean tree). A handoff
  over a dirty tree is a broken handoff — the resume step can't trust the docs.
- If the project has a merge-before-handoff rule, honour it.

## 3. Write the handoff document

Update `planning/HANDOFF.md` (create it if absent). It is a *living* doc —
edit the existing one, don't append duplicates. Keep it executable by a
stateless model. Required sections:

```markdown
# Handoff — <project> build state

> Living doc for resuming in a fresh session. Read this + AGENTS.md + the
> Doc(s) named below for the phase you're entering. Last updated <date/phase>.

## Where we are
- Phase-by-phase status (done / in-progress), each with the concrete artifact.
- Branch + commit the state corresponds to.

## Verify on entry
​```sh
<exact commands to prove the state is green — build/test/harness>
​```

## Decisions taken (not otherwise recorded in code)
- <decision> — <why>, with date for anything dated.

## Repo map
- One-line-per-path orientation to the source of truth.

## Key contracts for the next phase
- The function/module signatures the next session will build against.

## <Next phase> entry checklist
1. The exact next task, and what gates it.
2. …

## Open questions / not done
- Explicit list of placeholders, deferrals, and unresolved items.
```

Convert relative dates to absolute. Exact paths and commands, not "the config
file". Note what must NOT be broken (hard rules, clamps, placeholders).

## 4. Confirm next steps + outstanding user actions

Close with a short message to the user covering:

- **Resume command:** "Next session, run `/skill:resume-from-handoff`."
- **The single next task** and any decision that gates it.
- **Outstanding *user* actions** only you can't do — e.g. a login
  (`gcloud auth login`), a manual sign-off, a dataset/licensing decision, a
  secret to provide, a PR to review/merge. List them explicitly; if none, say so.
- Confirm the tree is clean and pushed (result of step 2).

## Guards

- Never claim a phase is "done" in the handoff if its tests aren't green — say
  what's actually true.
- Don't fabricate contracts or file paths; verify them against the tree.
- Keep it a single living doc; stale handoffs mislead the resume step.

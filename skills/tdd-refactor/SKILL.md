---
name: tdd-refactor
description: TDD refactor phase — safely refactor green code in atomic steps; tests must stay green.
whenToUse: After tdd-green, when the suite is green and the implementation needs cleaning up
arguments:
  - code
---

# TDD Refactor

TDD **refactor phase** — improve the code while every test stays green.

First, capture the baseline with Bash:
`(npm test 2>&1 || pytest 2>&1 || go test ./... 2>&1) | tail -15`

**GATE:** the baseline must be green before you start. If it's red, stop — finish `/skill:tdd-green`
first. Refactoring on a red suite has no safety net.

Run in two steps.

**Step 1 — `plan` subagent** (advisory, read-only): identify what's actually worth changing.
Brief it with the code in question. Ask for the highest-impact smells only, in
What / Why / Trade-offs / Alternatives / Risk format:
- Duplication, long methods, large classes, long parameter lists
- Feature envy, primitive obsession, dead code
- SOLID violations that are causing real pain (not theoretical ones)
- Genuine performance bottlenecks — **profiled, not guessed**

Tell it explicitly: recommend only refactorings that pay for themselves. No pattern-for-pattern's-sake,
no speculative abstraction. If the code is fine, say the code is fine.

**Step 2 — `coder` subagent**: apply the agreed refactorings.
- Small atomic changes; re-run the suite after each one
- Behaviour must not change — refactoring and feature work never mix
- If a change turns the suite red, revert that change immediately and report it
- Do not touch the tests except to keep them compiling; coverage must not drop

**Guards:** never modify a test to accommodate a refactor. If a refactor genuinely requires a test to
change, that's a behaviour change — stop and flag it. If the suite goes red and the cause isn't
obvious, use `/skill:smart-debug` rather than guessing.

After both agents return, present:
- What was changed and why (file:line)
- Suite status — must still be 100% green
- What was deliberately left alone, and why
- Any remaining technical debt worth tracking

Code to refactor: $code

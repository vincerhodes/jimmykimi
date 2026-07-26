---
name: tdd-green
description: TDD green phase — minimal production code to make failing tests pass. No premature optimisation.
whenToUse: After tdd-red, when failing tests exist and need minimal passing implementation
arguments:
  - tests
---

# TDD Green

TDD **green phase** — write the minimal production code that makes the failing tests pass.

First, capture the current failures with Bash:
`(npm test 2>&1 || pytest 2>&1 || go test ./... 2>&1) | tail -25`

Delegate to a `coder` subagent. Brief it with the failing output and these rules:

1. **Read the failing tests first.** The tests are the specification. Understand exactly what they
   assert before writing anything.
2. **Minimal code that could possibly work.** Hard-coded returns are acceptable early. Generalise only
   when a second test forces it (triangulation).
3. **Nothing beyond the tests.** No extra features, no error handling for cases no test exercises, no
   design patterns, no optimisation. All of that is `/skill:tdd-refactor`.
4. **One test at a time.** Make the simplest failing test pass, re-run, move to the next.
5. **Do not modify the tests to make them pass.** If a test looks wrong, stop and say so — don't
   quietly edit it.
6. **Re-run the full suite at the end** — confirm all green and no existing test regressed.

The agent should report: files changed (file:line), what each change does, the final suite result
(pass/fail counts), and any shortcut or technical debt taken deliberately for the refactor phase.

If a test still fails and the *test itself* is wrong rather than the code, do not patch production
code around it — report it and use `/skill:smart-debug`.

After it returns, present:
- Suite status (all green / still failing)
- Files changed and why
- Shortcuts taken, to be cleaned up in `/skill:tdd-refactor`
- Next step: `/skill:tdd-refactor`

Tests to make pass: $tests

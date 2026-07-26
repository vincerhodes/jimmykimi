---
name: tdd-cycle
description: Full red-green-refactor TDD orchestration with coverage gates; --incremental or --suite modes.
whenToUse: When building a feature end-to-end test-first, or when the user asks for a full TDD cycle
arguments:
  - feature
---

# TDD Cycle

Full **red-green-refactor** cycle with strict discipline. You orchestrate; the subagents do the work.

First, detect the setup with Bash:
- Test framework: `ls package.json pytest.ini pyproject.toml go.mod Cargo.toml 2>/dev/null | head -3`
- Suite status: `(npm test 2>&1 || pytest 2>&1 || go test ./... 2>&1) | tail -10`

Each phase is a **gate** — do not advance until it passes. If discipline breaks, stop, say which gate
was violated, and go back.

## Phase 1 — Specify (`plan` subagent)
Analyse the requirement. Produce acceptance criteria, edge cases, and test scenarios. No code.
**Gate:** every requirement maps to at least one test scenario.

## Phase 2 — RED (`coder` subagent)
Write the failing tests from that spec. Behaviour, not implementation. Happy path + edge cases + error
paths. Run them.
**Gate:** all new tests fail, and fail for the *right* reason (missing implementation, not import or
syntax errors). A test that passes now is a broken test.

Then have an `explore` subagent do a fast pass over the failures to confirm none are false positives.

## Phase 3 — GREEN (`coder` subagent)
Minimal production code to make the tests pass. Nothing beyond what the tests demand. Do not edit the
tests to make them pass.
**Gate:** 100% of the suite green, no existing test regressed. If a test fails because the *test* is
wrong, use `/skill:smart-debug` — do not patch production code around it.

## Phase 4 — REFACTOR (`plan` → `coder`)
Plan subagent identifies the high-impact smells (read-only, What/Why/Trade-offs/Alternatives/Risk).
Coder applies them in small atomic steps, re-running the suite after each.
**Gate:** suite still 100% green; behaviour unchanged.

## Phase 5 — Integration (`coder`)
Failing integration tests first (component interaction, contracts, data flow), then the integration
code to pass them. Same red-then-green discipline.
**Gate:** integration suite green.

## Phase 6 — Verify (`explore`, + `/skill:security-scan` if it touches auth or user input)
Final review pass. Security scan is **mandatory** if the change touches authentication, authorization,
or user input — that's the standing cross-project rule.

## Coverage gates
- Line coverage ≥ 80%
- Branch coverage ≥ 75%
- Critical path coverage 100%

## Modes
- `--incremental` — one test at a time: write one failing test, pass only that, refactor, repeat.
  Prefer this. It's the actual discipline.
- `--suite` — all tests for the feature first, then implement, then refactor.

## Anti-patterns — stop if you catch any of these
- Implementation written before the test
- A test that passed the moment it was written
- A test edited to make it pass
- Refactoring mixed into a feature change
- The refactor phase skipped because it was green

## Report at the end
Phases completed, tests added, files changed (file:line), final suite + coverage, security findings if
any, and anything left undone.

Feature: $feature

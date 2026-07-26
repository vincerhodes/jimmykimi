---
name: tdd-red
description: TDD red phase — write failing tests (AAA, happy path + edge + error cases) before production code.
whenToUse: When starting a feature test-first, when the user asks for failing tests, or as phase 1 of a TDD cycle
arguments:
  - requirement
---

# TDD Red

TDD **red phase** — write failing tests that define the expected behaviour. No production code.

First, detect the project setup with Bash:
- Test framework: `ls package.json pytest.ini pyproject.toml go.mod Cargo.toml 2>/dev/null | head -3`
- Existing tests: `find . -type d \( -name node_modules -o -name .git \) -prune -o -type f \( -name "*.test.*" -o -name "*_test.go" -o -name "test_*.py" -o -name "*.spec.*" \) -print 2>/dev/null | head -10`

Then delegate to a `coder` subagent. Brief it with the requirement below and these rules:

1. **Read first** — the code under test (if it exists) and the existing tests, so the new tests match
   the project's framework, conventions, and fixtures. Do not introduce a new test framework.
2. **Define behaviour, not implementation** — test observable behaviour. No testing of private
   internals or trivial getters.
3. **Cover** the happy path, edge cases (empty, null, zero, boundary, max), and error paths.
4. **One behaviour per test.** Arrange-Act-Assert. Descriptive names (`should_X_when_Y`). Tests must
   be isolated — no interdependencies, no cascading failures.
5. **Meaningful test data** — not `foo`/`bar`.
6. **Run the suite and confirm the new tests FAIL** — and fail for the *right* reason (missing
   implementation, not a syntax or import error). A test that passes immediately is a bug in the test.

**Guard:** do NOT write or modify production code in this phase. That's `/skill:tdd-green`.

The agent should report: test files added, what each covers, and the failure output proving they fail
correctly. Not full file dumps.

After it returns, present:
- Number of tests added and what they cover
- Confirmation they fail for the right reasons (quote the failure)
- Anything ambiguous in the requirement that the tests had to assume
- Next step: `/skill:tdd-green`

Requirement: $requirement

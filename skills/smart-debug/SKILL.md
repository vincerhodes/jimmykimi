---
name: smart-debug
description: Root-cause debugging — reproduce, confirm hypothesis, minimal fix, verify with the suite.
whenToUse: When there is a failing test, a reported bug, or an error to diagnose and fix
arguments:
  - issue
---

# Smart Debug

Diagnose and fix a bug, root cause first.

First, gather context with Bash:
- Current directory: `pwd`
- Recent changes: `git diff HEAD --stat 2>/dev/null | tail -10`
- Recent commits: `git log --oneline -5 2>/dev/null`

Delegate to a `coder` subagent. Brief it with the issue below, the recent changes above,
and its standard method:

1. **Reproduce first.** Capture the actual failure — stack trace, failing assertion, log output. Do
   not theorise before you've seen it fail.
2. **Hypothesis, then confirm.** Form a hypothesis and verify it by reading the actual code path.
3. **Fix the cause, not the symptom.** Smallest change that addresses the root cause. No opportunistic
   refactoring while you're in there.
4. **Verify.** Re-run the failing case *and* the surrounding suite to confirm no regression.

**Escalation:** if the root cause turns out to be a design flaw rather than a local bug, stop and
hand to a `plan` subagent for a design recommendation rather than patching around it.

**If the issue is performance-related**, brief the coder to profile before changing anything —
measure, find the actual bottleneck, then optimise only what the profile implicates, and measure again
to prove the improvement. Guessing at bottlenecks is not debugging. If the bottleneck is architectural
(N+1 queries, wrong data structure at the core, a sync call that should be async), escalate to the
`plan` subagent.

The agent should report: root cause in one line, the fix (file:line + what changed), and the
verification output. Not full file dumps.

Issue: $issue

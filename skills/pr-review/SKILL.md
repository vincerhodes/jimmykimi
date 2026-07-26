---
name: pr-review
description: Review current branch vs main — first-pass review then security pass, combined verdict.
whenToUse: Before merging a branch, when the user asks to review the current branch or PR
---

# PR Review

Review all changes on the current branch vs main.

First, gather the context with Bash:
- Branch: `git branch --show-current`
- Base branch: `git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}' || echo "main"`
- Commit summary: `git log main...HEAD --oneline 2>/dev/null || git log origin/main...HEAD --oneline 2>/dev/null`
- Diff stat: `git diff main...HEAD --stat 2>/dev/null || git diff origin/main...HEAD --stat 2>/dev/null`
- Full diff: `git diff main...HEAD 2>/dev/null || git diff origin/main...HEAD 2>/dev/null`

Then run two passes in sequence:

**Step 1 — first pass (`explore` subagent):** quick pass for obvious issues.
Brief it with the full diff. Ask for CRITICAL / WARNING / SUGGESTION categorised output.

**Step 2 — security pass (`coder` subagent, read-only — no edits):**
Brief it with the full diff, focusing on any code that handles user input, auth, database
queries, or filesystem operations.

After both passes complete, produce a combined summary:
- Overall assessment (Ready / Needs work / Major issues)
- Blocked issues (if any)
- Suggested improvements (if any)
- Security findings (if any)

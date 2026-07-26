---
name: git-conventional-commits
description: Conventional commit message conventions for writing or reviewing git commits.
whenToUse: When writing or reviewing a git commit message
disableModelInvocation: true
---

# Conventional Commits

Format: <type>(<scope>): <description>

Types: feat, fix, refactor, docs, test, chore, perf, ci, style, revert

Rules:
- Subject line ≤ 72 characters
- Present tense ("add feature" not "added feature")
- No period at end of subject
- Body: explain WHY, not WHAT
- Footer: "Closes #123" or "Fixes #123"
- Breaking changes: "BREAKING CHANGE:" in footer

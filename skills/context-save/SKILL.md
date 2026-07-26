---
name: context-save
description: Save session context to disk before compaction, at >50% context, or when switching tasks.
whenToUse: When context usage is above 50%, before a compaction, before ending a session mid-task, or when switching to a completely new task
---

# Context Save

Save session state to disk so reasoning survives compaction.

## What to save

Write to `quality_reports/session_logs/YYYY-MM-DD-HH-MM.md`:

```markdown
# Session Log — YYYY-MM-DD HH:MM

## Current task
<what we're working on>

## Decisions made this session
- <decision> — <why>

## Files modified
- <path> — <what changed>

## Next steps
- <step 1>

## Open questions
- <question>
```

## When to invoke

- Context usage > 50%
- Before compaction
- Before ending a session mid-task
- When switching to a completely new task

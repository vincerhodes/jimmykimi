---
name: planning-workflow
description: Scaffold a planning/ folder for a new project or feature before any implementation.
whenToUse: At the start of any non-trivial project or feature, before any implementation code is written
arguments:
  - project_name
---

# Planning Workflow

Every non-trivial task begins with a planning folder before any implementation.

Project/feature: $project_name

## Structure

```
planning/
├── 00-master-plan.md       Required. Phases, objectives, acceptance criteria.
├── 01-<component>.md       One file per major component.
└── ...
```

## Rules

1. Plan before code. No implementation until planning/ exists and is reviewed.
2. Each phase must have: objective, deliverables (file paths), acceptance criteria.
3. Phases: minimum 2, maximum 6.
4. Mark assumptions: `ASSUMPTION: <text>`
5. Mark open questions: `OPEN: <text>`
6. Human reviews plan before Phase 1 begins.

## Master Plan Template (00-master-plan.md)

```markdown
# <Project> — Master Plan

> Status: Planning | In Progress | Complete
> Date: YYYY-MM-DD
> Objective: one sentence

## Phases

### Phase 1 — <Name>
**Why first:** <dependency reasoning>
**Deliverables:**
- file/path/here
**Acceptance criteria:** <testable conditions>

## Document Index
| File | Purpose |
```

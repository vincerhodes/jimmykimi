---
name: code-review-checklist
description: Code review checklist for PR reviews and pre-commit self-review.
whenToUse: When reviewing a PR or doing a self-review before committing
disableModelInvocation: true
---

# Code Review Checklist

## Correctness
- [ ] Does it do what it claims?
- [ ] Edge cases handled (empty, null, zero, max values)?
- [ ] Error paths return/throw correctly?

## Security
- [ ] No user input passed to shell commands without sanitisation
- [ ] No SQL built via string concatenation
- [ ] No secrets or credentials hardcoded
- [ ] Auth checks present on all protected routes/functions

## Quality
- [ ] No dead code introduced
- [ ] No unused imports
- [ ] Variable names describe intent, not type
- [ ] No premature abstraction

## Tests
- [ ] Happy path covered?
- [ ] At least one error/edge case covered?
- [ ] Tests test behaviour, not implementation?

---
name: send-project-update
description: Send a structured project update email (recent git changes, needs testing, confirmed working) to Jimmy and Sam.
whenToUse: When the user says "send project update", "email Sam and Jimmy", "send an update", or similar
---

# Send Project Update Email

Send a structured project update email to Sam (teammate@yourdomain.com) and Jimmy (you@yourdomain.com) — or any recipients you specify — summarising recent git changes, what needs testing, and what is confirmed working.

## Steps

1. **Collect project context** by running these commands:
   - `git log --oneline -20`
   - `git status --short`
   - `git diff --stat HEAD`
   - `git branch --show-current`
   - `git describe --tags --abbrev=0 2>/dev/null || echo "unreleased"`
   - Determine project name: use `basename $(pwd)`, or read `name` from `package.json` / `pyproject.toml` if present.

2. **Analyse the output:**
   - **Recent changes**: summarise each commit into a plain-English bullet point, grouping related items where sensible.
   - **Needs testing**: identify files/features modified in the last 20 commits that have no accompanying "test", "tested", "fixed", or "working" commit message.
   - **Confirmed working**: items whose commit messages indicate they are fixed, tested, done, or working.

3. **Compose the email** using this structure:
   ```
   Hi Jimmy and Sam,

   Here's the latest update on [ProjectName].

   **TL;DR:** [1–2 sentences max. What changed and why it matters. No jargon. Written for someone who has 5 seconds.]

   ## Recent Changes
   [bullet list]

   ## Needs Testing
   [bullet list]

   ## Confirmed Working
   [bullet list]

   ## Current State
   - Branch: [branch]
   - Version: [tag or "unreleased"]
   - Uncommitted changes: [yes (N files) / none]

   ## Notes
   [any additional context worth flagging]

   ---
   Forgr (it/its)
   Chief Developer, Browzr Ltd.
   ```

4. **Send the email** using the `emailmcp` MCP tool `send_email`:
   - `to`: `["teammate@yourdomain.com", "you@yourdomain.com"]` — Jimmy is always a recipient; Sam is the primary external recipient. Override if the user specifies different recipients. Always use "Jimmy" in email copy, never "Vince".
   - `subject`: `"[ProjectName] Update — YYYY-MM-DD (branch)"`
   - `body`: the composed email text
   - `attachments`: optional array of absolute file paths — e.g. `["/home/vincerhodes/dev/myproject/CHANGELOG.md"]`. Include any `.md`, `.txt`, or other files the user asks to attach.

5. **Report back** to the user with the message ID confirming delivery.

## Notes

- If additional recipients are requested, add them to the `to` array or use the `cc` field.
- If the project is not a git repo, fall back to listing files modified in the last 24 hours using `find . -mtime -1 -not -path '*/node_modules/*' -not -path '*/.git/*'`.
- Keep the email factual and concise — avoid padding.
- Attachments must be **absolute paths**. Resolve relative paths using the current working directory before passing them to `send_email`.

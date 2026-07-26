---
name: send-project-intro
description: Send a project intro/summary email to Sam and Jimmy, using planning files for context.
whenToUse: When the user says "send intro email", "email Sam and Jimmy about the project", "send a summary to the team", or similar
---

# Send Project Intro/Summary Email

Send a comprehensive project email to Sam (teammate@yourdomain.com) and Jimmy (you@yourdomain.com) covering what the project is, current status, features, monetisation plan, and next steps. Assumes Sam may not have full context.

## Steps

1. **Determine project name** using `basename $(pwd)`, or read `name` from `package.json` / `pyproject.toml` if present.

2. **Read context files** (skip gracefully if a file doesn't exist):
   - `planning/PRD.md` — feature list and requirements
   - `planning/00-master-plan.md` — build status and phases
   - `README.md` — setup and deployment notes
   - Any additional files the user specifies

3. **Compose the email** using this structure:
   ```
   Hi Jimmy and Sam,

   Here's an overview of [ProjectName].

   ## What Is It?
   [1–2 paragraph plain-English description. Assume Sam may not know the project.]

   ## Current Status
   [e.g. "Built and running locally. Ready for internal testing / pre-launch."]

   ## Features
   [bullet list from PRD or master plan]

   ## Monetisation Plan
   [if applicable — pricing model, tiers, revenue approach]

   ## What's Next
   [upcoming phases, blockers, decisions needed]

   ## Notes
   [any context worth flagging — e.g. infrastructure, dependencies, open questions]

   ---
   AI Assistant
   ```

4. **Send the email** using the `emailmcp` MCP tool `send_email`:
   - `to`: `["teammate@yourdomain.com", "you@yourdomain.com"]`
   - `subject`: something descriptive, e.g. `"Introducing [ProjectName] — [tagline]"` or `"[ProjectName] — Project Summary"`
   - `body`: the composed email text
   - `attachments`: optional — include any files the user asks to attach (absolute paths only)

5. **Report back** with the message ID confirming delivery.

## Notes

- If planning files are missing, use README.md and any other available docs.
- Keep the tone clear and informative — Sam may be reading this cold.
- Override recipients if the user specifies different ones.
- Attachments must be absolute paths.

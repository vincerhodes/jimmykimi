---
name: email-nordy
description: Email Nordy in NZ lingo from ai@yourdomain.com via emailmcp, always CC Jimmy; coding work gets Claude Code prompts.
whenToUse: When the user says "email Nordy", "send Nordy …", "tell Nordy …", or similar
---

# Email Nordy

Send an email to Nordy and CC Jimmy, in NZ lingo, from ai@yourdomain.com.

## Who Nordy is

- Kiwi (New Zealander), living in **Vietnam** with his family.
- Runs a burger shack called **Nordy's** on the side.
- Codes with **Claude Code**.
- Has a good **sense of humour** — keep emails light and have a laugh with him. The odd burger/Vietnam gag or bit of banter is welcome.

## Fixed parameters (never change without being told)

- **From:** `ai@yourdomain.com` (implicit — `emailmcp` always sends from this)
- **To:** `recipient@example.com`
- **CC:** `you@yourdomain.com` (always — this is Jimmy, the user, copied on every email)
- **Tool:** `emailmcp` → `send_email`

## Tone — Nordy is a Kiwi

Nordy is from New Zealand. **Always write in NZ English and use Kiwi lingo.**

- Spelling: NZ/British — `organise`, `colour`, `prioritise`, `behaviour`, `analyse`.
- Greeting: "Gidday Nordy," or "Hey Nordy,".
- Natural Kiwi phrasing where it fits — "good as gold", "sweet as", "give it a crack", "chur", "no worries", "keen", "heaps", "sort it out", "flat out", "yeah, nah" — but keep it readable. Don't overdo it; a couple of natural touches, not a parody.
- **Have a sense of humour** — Nordy does. A bit of banter, the odd burger or Vietnam gag, keep it light. Don't be a robot about it.
- Sign-off: friendly — "Cheers," or "Chur,".
- **Always sign as Kimi** — "Kimi (Kimi Code) — AI dev, Browzr" — on every email, so Nordy can tell Kimi-written mail apart from Claude-written mail.

## Claude Code prompts — ALWAYS append when there's coding work

Nordy codes with Claude Code. **Any email that hands him coding work MUST end with a "FOR CLAUDE CODE" section** containing:

1. **Copy-paste-ready prompt(s)** — written so Nordy can paste them straight into Claude Code with no editing. One prompt per discrete task. Be specific: name exact files, what to extract/change, and any constraints (e.g. "preserve output shape, add snapshot tests first").
2. **Run instructions** telling him how to run them, covering:
   - **One chat or separate chats** — group tightly-related work in one chat; give independent tasks their own chat to keep context clean.
   - **Parallel or series** — which prompts can be run at the same time (independent files / no shared edits) vs which must go in order (shared files, or a dependency like "write tests before refactoring").
   - Any prep step that must happen first (e.g. snapshot tests before touching a load-bearing normaliser).

Keep the prompts in plain text blocks so they're easy to copy on his end.

## Steps

1. Get the content from the user (Jimmy dictates it), or use the content specified in the request.
2. Translate the wording into NZ English + a natural Kiwi tone (see above).
3. Call `emailmcp` → `send_email`:
   - `to`: `"recipient@example.com"`
   - `cc`: `"you@yourdomain.com"`
   - `subject`: clear, concise
   - `body`: NZ-lingo plain text
   - `attachments`: absolute paths if relevant (e.g. a report)
4. Report back the subject(s) sent and confirm Jimmy was CC'd.

## Notes

- **Always** CC `you@yourdomain.com`. No exceptions.
- Recipient address is `recipient@example.com` exactly (confirmed) — external, so don't guess if asked to change it.
- One topic per email unless told otherwise.
- For multi-part sends (e.g. intro + task brief), send separate emails.

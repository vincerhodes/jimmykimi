---
name: expenses-summary
description: Process expenses@yourdomain.com inbox into a UK Xero-ready summary email, then file processed mail to Clauded.
whenToUse: When the user says "process expenses", "summarise expenses", "run expenses workflow", or similar
---

# Expenses Summary Workflow

Process the expenses@yourdomain.com inbox and produce a UK Xero-ready expense report email.

## Steps

### 1. Fetch all inbox messages

Call `inboxmcp` → `list_messages` with `limit: 100`. If the inbox has more than 100 messages, call again with increasing offsets until all UIDs are collected. Note every UID returned — these are the messages to process.

### 2. Fetch full content of each message

For each UID, call `inboxmcp` → `get_message`. From the body (plain text preferred, HTML fallback), extract:

- **Date** — use the original receipt date if visible in the body, otherwise fall back to the email date field. Format as DD/MM/YYYY for UK Xero.
- **Supplier** — the company that issued the receipt (e.g. "OpenRouter, Inc.", "Exafunction, Inc.").
- **Reference** — the receipt or invoice number (e.g. "#1345-0721").
- **Description** — the service or product (e.g. "API usage credits", "AI compute credits"). Be specific if the receipt mentions a plan or tier.
- **Currency** — as stated on the receipt (USD, GBP, EUR, etc.).
- **Gross amount** — total charged including any local taxes shown on the receipt.
- **Net amount** — amount before any taxes. If no tax shown, gross = net.
- **VAT / tax notes** — these are US-based digital service suppliers with no UK VAT registration. For UK Xero, classify as: `No VAT` (tax code `NO VAT`). If the business is VAT-registered and the amount is significant, note that reverse charge VAT may apply — flag for accountant review.

If a message body cannot be parsed (HTML-only with no readable text), note the UID and subject as "Unparseable — manual review required".

### 3. Compose the summary email

Structure:

```
Subject: Expenses Summary — [DD Month YYYY] ([N] items)

Hi Jimmy and Sam,

Here is a summary of [N] expenses processed from the expenses@yourdomain.com inbox, formatted for entry into Xero.

All suppliers below are non-UK entities providing digital services. No UK VAT has been charged. If the business is VAT-registered, reverse charge VAT may apply — please confirm with your accountant.

---

EXPENSE ENTRIES

| # | Date       | Supplier              | Reference      | Description              | Currency | Net Amount | VAT      | Gross Amount |
|---|------------|-----------------------|----------------|--------------------------|----------|------------|----------|--------------|
| 1 | DD/MM/YYYY | Supplier Name         | #REF-0000      | Description of service   | USD      | 0.00       | No VAT   | 0.00         |
...

---

TOTALS BY CURRENCY

USD: $[total]
GBP: £[total]
[other currencies as applicable]

---

XERO ENTRY NOTES

- Account: Computer & IT Subscriptions (or Technology Expenses — confirm with accountant)
- Tax Rate: No VAT
- Contact: Create a Xero Contact for each unique supplier if not already present
- Tracking: [leave blank unless you have Xero tracking categories set up]

---

ITEMS REQUIRING MANUAL REVIEW

[list any unparseable or ambiguous items here with UID and subject]

---

Forgr (it/its)
Chief Developer, Browzr Ltd.
```

Use actual tabular data. Do not use placeholder values — every row must be populated from the parsed receipts.

### 4. Send the email

Call `emailmcp` → `send_email`:
- `to`: `["teammate@yourdomain.com", "you@yourdomain.com"]`
- `subject`: `"Expenses Summary — [DD Month YYYY] ([N] items)"`
- `body`: the composed email text

### 5. Move processed messages to Clauded

For each UID that was successfully processed (parsed or flagged), call `inboxmcp` → `move_message`:
- `uid`: the message UID
- `targetFolder`: `"INBOX.Clauded"`
- `createIfMissing`: `true` (on the first call only — folder is created automatically if absent)

Move them one at a time. Do not batch. If a move fails, log the UID and continue — do not abort the whole run.

### 6. Report back

Tell the user:
- How many messages were processed
- How many were moved to Clauded
- Any that failed to move or parse
- The email message ID confirming delivery

## Notes

- Forwarded receipts (Fwd:) are common — extract the inner receipt data, not the forwarding wrapper.
- If the receipt is in HTML and bodyText is empty, use bodyHtml and strip tags mentally to find amounts and dates.
- Currency conversion is NOT required — list each currency separately in the totals.
- Do not invent or estimate amounts. If an amount cannot be found, mark the row as "Amount not found — manual review".
- Always use "Jimmy" in email copy, never "Vince".

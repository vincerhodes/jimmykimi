# MCP Servers

Source file: [`../files/mcp.json`](../files/mcp.json) (sanitized) → installed to `~/.kimi-code/mcp.json`

6 servers configured. Two need secrets supplied at install time; two are private local projects; two work anywhere.

| Server | Type | Launch | Needs |
|---|---|---|---|
| `vercel` | remote | `"url": "https://mcp.vercel.com"` | OAuth via browser on first use |
| `context7` | local npx | `npx -y @upstash/context7-mcp` | nothing — works anywhere node exists |
| `supabase` | local npx | `npx -y @supabase/mcp-server-supabase@latest --access-token …` | personal access token (`sbp_…`) |
| `emailmcp` | local node | `node ~/dev/emailmcp/dist/server.js` | private local project + its own env |
| `emailmcp-kickoff` | local node | same binary, SMTP creds passed via `env` | private local project + SMTP credentials |
| `inboxmcp` | local node | `node ~/dev/inboxmcp/dist/server.js` | private local project + its own env |

## vercel

Remote MCP server for the Vercel platform: projects, deployments, build/runtime logs, domains, web analytics, toolbar threads, purchase flows. Auth is OAuth — first use opens a browser flow and the token is cached under `~/.kimi-code/credentials/mcp/`.

Handy trick: the cached OAuth token doubles as a Vercel REST API Bearer token (expires hourly) for direct `api.vercel.com` calls — no `vercel login` needed.

## context7

Up-to-date library/framework documentation lookup (resolve library ID → query docs). Zero config.

## supabase

Postgres/Supabase management: schema listing, raw SQL, logs, advisors, migrations, type generation. The `enabledTools` allowlist pins it to read + SQL tools only. Requires a personal access token from https://supabase.com/dashboard/account/tokens — **this is the one secret in mcp.json**; it's a placeholder in this repo.

## emailmcp / emailmcp-kickoff

Send email through a self-hosted MCP server (private, unpublished node project). Two instances of the same binary with different identities, differentiated by env vars — the second instance (`emailmcp-kickoff`) shows the pattern: SMTP host/port/user/pass plus `FROM_ADDRESS`/`FROM_NAME` passed via the `env` block. The default instance picks up its own credentials from the project's local env file.

## inboxmcp

Read/search/file an IMAP inbox (companion private project) — used by the `expenses-summary` skill to process expense emails and file them to an archive folder.

## New-machine notes

- `emailmcp`, `emailmcp-kickoff`, `inboxmcp` only make sense if the built `dist/server.js` files exist locally — delete those entries otherwise (the recreate guide handles this).
- `REPLACE_WITH_HOME` placeholders → the machine's actual `$HOME`.
- Everything secret is a `REPLACE_WITH_*` placeholder in this repo; the real values are entered once at install time and never committed.

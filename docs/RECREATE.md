# Recreating This Setup on a New Machine

Human-readable guide. For the machine-executable version (a prompt you paste into a fresh kimi session that performs the install itself), see [`BOOTSTRAP.md`](BOOTSTRAP.md).

## Layout on a configured machine

```
~/.kimi-code/
├── config.toml      # model, provider, permissions, hooks   ← files/config.toml
├── tui.toml         # client/UI preferences                 ← files/tui.toml
├── mcp.json         # MCP server definitions                ← files/mcp.json (placeholders resolved)
├── AGENTS.md        # global agent instructions             ← files/AGENTS.md
├── hooks/           # 5 event hooks                         ← files/hooks/
└── bin/kimi         # the CLI itself (installed separately, not in this repo)

~/.agents/skills/    # 27 user-scope skills                  ← skills/
```

Not copied (machine-local): `credentials/`, `oauth/`, `sessions/`, `logs/`, `device_id`, `workspaces.json`, `user-history/`.

## Prerequisites

1. **Kimi Code CLI** installed (`kimi --version` works, or `~/.kimi-code/bin/kimi`).
2. **Node.js** (`node` + `npx`) — required for the MCP servers.
3. **`jq` or `python3`** — the hooks use jq with a python3 fallback; at least one must exist.

## Step 1 — Config files

```bash
mkdir -p ~/.kimi-code/hooks ~/.agents/skills
cp files/config.toml ~/.kimi-code/config.toml
cp files/tui.toml ~/.kimi-code/tui.toml
cp files/AGENTS.md ~/.kimi-code/AGENTS.md
cp files/hooks/*.sh ~/.kimi-code/hooks/
chmod +x ~/.kimi-code/hooks/*.sh
cp -r skills/* ~/.agents/skills/
```

If any destination already exists, back it up before overwriting.

## Step 2 — MCP config (resolve placeholders)

`files/mcp.json` has placeholders. Edit a **temp copy**, never the repo file:

1. `REPLACE_WITH_HOME` → your `$HOME` (3 occurrences: emailmcp, emailmcp-kickoff, inboxmcp).
   - These three servers point at **private local projects** (`~/dev/emailmcp`, `~/dev/inboxmcp`). If they don't exist on this machine, delete those entries entirely — the setup works fine without them (you lose the email skills that depend on them).
2. `emailmcp-kickoff` env: `REPLACE_WITH_SMTP_USER` / `REPLACE_WITH_SMTP_PASSWORD` / `REPLACE_WITH_FROM_ADDRESS` / `REPLACE_WITH_FROM_NAME` → real SMTP credentials for the second sending identity. Delete the block if unused.
3. `REPLACE_WITH_SUPABASE_ACCESS_TOKEN` → a personal access token from https://supabase.com/dashboard/account/tokens (starts with `sbp_`).
4. Validate: `python3 -m json.tool < edited-mcp.json > /dev/null` then `cp` it to `~/.kimi-code/mcp.json`.

`vercel` and `context7` need nothing — vercel auths via browser OAuth on first use, context7 is keyless.

## Step 3 — Verify

```bash
bash -n ~/.kimi-code/hooks/*.sh          # all 5 parse
ls ~/.agents/skills | wc -l              # 27
ls ~/.kimi-code                          # config.toml tui.toml AGENTS.md mcp.json hooks
```

Then **restart kimi and run `/login`** (OAuth is per-machine and can't be copied). Sanity check: ask kimi to list its skills and MCP servers.

## Secrets inventory (everything you must supply, nothing stored here)

| Secret | Where it goes | How you get it |
|---|---|---|
| Kimi OAuth | `~/.kimi-code/oauth/` (automatic) | `/login` in the CLI |
| Vercel OAuth | `~/.kimi-code/credentials/mcp/` (automatic) | browser flow on first vercel MCP use |
| Supabase token | `mcp.json` arg | supabase.com/dashboard/account/tokens |
| SMTP creds (kickoff identity) | `mcp.json` env block | your mail provider |
| emailmcp/inboxmcp own env | inside those private projects | not in this repo |
| Hetzner token | `~/.config/hetzner-infra/token` | Hetzner console (hetzner-infra skill) |
| Cloudflare token | `~/.config/cloudflare/token` (chmod 600) | Cloudflare dashboard |

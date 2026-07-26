# BOOTSTRAP — Kimi Code machine setup

> **Prompt for a fresh kimi session.** The user has cloned `jimmykimi` and launched you in the repo root. Execute every step below in order. Ask the user only where marked **[ASK]**. Do not skip the verification step.

Confirm the bundle exists (`ls files skills docs`) before starting; if the user launched you elsewhere, ask for the repo path.

## Prerequisites (check, don't install)

1. `kimi --version` works (if not on PATH, check `~/.kimi-code/bin/kimi`). If kimi isn't installed at all, stop and tell the user to install it first.
2. `node --version` and `npx --version` work — required for the MCP servers. If missing, tell the user to install Node.js before continuing.
3. `jq --version` OR `python3 --version` works — the hooks use jq with a python3 fallback; at least one must exist.

## Step 1 — Install config files

Run exactly:

```bash
mkdir -p ~/.kimi-code/hooks ~/.agents/skills
cp files/config.toml ~/.kimi-code/config.toml
cp files/tui.toml ~/.kimi-code/tui.toml
cp files/AGENTS.md ~/.kimi-code/AGENTS.md
cp files/hooks/*.sh ~/.kimi-code/hooks/
chmod +x ~/.kimi-code/hooks/*.sh
cp -r skills/* ~/.agents/skills/
```

If any destination file already exists, **stop and ask the user** before overwriting — they may have local config worth keeping.

## Step 2 — Install MCP config

`files/mcp.json` contains placeholders. Resolve them in this order, editing a **temp copy** (never the repo file — never leave secrets in the repo):

1. **[ASK]** "Do the `emailmcp` and `inboxmcp` projects exist on this machine?" (Private local node projects, expected at `~/dev/emailmcp/dist/server.js` and `~/dev/inboxmcp/dist/server.js`.)
   - If **yes**: replace all three `REPLACE_WITH_HOME` placeholders with the user's actual `$HOME`. Verify the `dist/server.js` files exist; if one is missing, warn and remove that server's entry.
   - If **no**: delete the `emailmcp`, `emailmcp-kickoff`, and `inboxmcp` entries entirely, and skip question 2.
2. **[ASK]** (only if emailmcp exists) "Do you use the second sending identity (`emailmcp-kickoff`)? If yes, paste its SMTP user, password, from-address, and from-name." Replace the four `REPLACE_WITH_SMTP_*` / `REPLACE_WITH_FROM_*` placeholders. If not used, delete the `emailmcp-kickoff` entry.
3. **[ASK]** "Paste your Supabase access token" (from https://supabase.com/dashboard/account/tokens, starts with `sbp_`). Replace `REPLACE_WITH_SUPABASE_ACCESS_TOKEN`.
   - If the user doesn't have it handy: leave the placeholder, install anyway, and flag at the end that the supabase MCP server will fail until they edit `~/.kimi-code/mcp.json`.
4. `vercel` and `context7` need no substitution.
5. Validate the result parses (`python3 -m json.tool`), then:

```bash
cp <temp-copy> ~/.kimi-code/mcp.json && rm <temp-copy>
```

## Step 3 — Verify

1. `bash -n` each of the 5 hook scripts — all must parse.
2. Confirm `ls ~/.agents/skills | wc -l` is **27**.
3. Confirm `~/.kimi-code/` contains: `config.toml`, `tui.toml`, `AGENTS.md`, `mcp.json`, `hooks/` with 5 executable `.sh` files.
4. Tell the user: **restart kimi, then run `/login`** to complete OAuth (credentials are per-machine and can't be copied). The `vercel` MCP server auths via browser on first use.
5. After restart, sanity-check by asking kimi to list its skills and MCP servers.

## Done means

- All files in place, hooks executable, mcp.json valid JSON with real values (or clearly-flagged pending placeholders).
- A short final report: what was installed, which MCP servers are active vs skipped, and the `/login` reminder.

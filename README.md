# jimmykimi

Full documentation and backup of Jimmy's [Kimi Code](https://www.kimi.com/code) CLI setup — config, hooks, MCP servers, global agent instructions, and all 27 custom skills — plus a machine-executable guide to recreate the whole environment from scratch.

**No secrets in this repo.** All tokens, passwords, and credentials are replaced with `REPLACE_WITH_*` placeholders. Machine-local state (sessions, logs, OAuth files) is intentionally excluded.

## Repo layout

| Path | Contents |
|---|---|
| `files/config.toml` | Model/provider config, permission deny-rules, hook registrations |
| `files/tui.toml` | TUI client preferences (theme, notifications, editor) |
| `files/mcp.json` | All 6 MCP server definitions, **sanitized** with placeholders |
| `files/AGENTS.md` | Global agent instructions — the behavioral core of the setup |
| `files/hooks/` | 5 bash event hooks (safety guardrails, auto-format, session logging, respawn) |
| `skills/` | All 27 user-scope skills, verbatim (installed to `~/.agents/skills/`) |
| `docs/` | The full write-up, split by topic — start below |

## Documentation

- [`docs/CONFIG.md`](docs/CONFIG.md) — config.toml & tui.toml explained: models, provider, permissions, hooks
- [`docs/MCP-SERVERS.md`](docs/MCP-SERVERS.md) — the 6 MCP servers, what each does, what each needs
- [`docs/SKILLS.md`](docs/SKILLS.md) — catalog of all 27 custom skills
- [`docs/AGENTS-MD.md`](docs/AGENTS-MD.md) — the global instruction file and the conventions it encodes
- [`docs/RECREATE.md`](docs/RECREATE.md) — full guide to recreate this setup on a new machine (human-readable)
- [`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md) — the same as a prompt you hand to a fresh kimi session to execute the install itself

## TL;DR recreate

```bash
mkdir -p ~/.kimi-code/hooks ~/.agents/skills
cp files/config.toml files/tui.toml files/AGENTS.md ~/.kimi-code/
cp files/hooks/*.sh ~/.kimi-code/hooks/ && chmod +x ~/.kimi-code/hooks/*.sh
# edit files/mcp.json placeholders (Supabase token, SMTP creds, $HOME paths), then:
cp files/mcp.json ~/.kimi-code/mcp.json
cp -r skills/* ~/.agents/skills/
```

Then restart kimi and run `/login` (OAuth is per-machine). Full detail in [`docs/RECREATE.md`](docs/RECREATE.md).

## What's deliberately NOT here

- OAuth credentials (`~/.kimi-code/oauth/`, `credentials/`) — re-login per machine
- Supabase access token, SMTP password — placeholders only; supply at install time
- `emailmcp` / `inboxmcp` server source — private local node projects; this repo only documents how they're wired
- Sessions, history, logs, `device_id`, `workspaces.json` — machine-local state

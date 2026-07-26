# Configuration — `config.toml` & `tui.toml`

Source files: [`../files/config.toml`](../files/config.toml), [`../files/tui.toml`](../files/tui.toml)
Installed to: `~/.kimi-code/config.toml`, `~/.kimi-code/tui.toml`

## Models & provider

Default model is `kimi-code/k3` (1M context, thinking, image/video input). Four models are defined, all routed through the `managed:kimi-code` provider at `https://api.kimi.com/coding/v1`:

| Model | Display name | Context | Notes |
|---|---|---|---|
| `k3` | K3 | 1M | default; efforts low/high/max |
| `k3-256k` | K3-256k | 256k | no video input |
| `kimi-for-coding` | K2.7 Coding | 256k | |
| `kimi-for-coding-highspeed` | K2.7 Coding Highspeed | 256k | |

Auth is OAuth (`/login`), stored on file at `oauth/kimi-code` — there is **no API key** anywhere in the config. Thinking is enabled globally at `high` effort.

`moonshot_search` and `moonshot_fetch` services back the WebSearch/FetchURL tools, using the same OAuth credential.

## Permission deny rules (hard floor)

These hold even in yolo mode — the always-on backstop:

```toml
[[permission.rules]]
decision = "deny"
pattern = "Bash(rm -rf*)"

[[permission.rules]]
decision = "deny"
pattern = "Bash(git push --force*main*)"

[[permission.rules]]
decision = "deny"
pattern = "Bash(git reset --hard*)"
```

The `safety-check.sh` hook blocks a wider set interactively (exit 2 = block); these three rules are the floor underneath it.

## Hooks (5 registered)

| Event | Matcher | Script | Timeout |
|---|---|---|---|
| PreToolUse | Bash | `safety-check.sh` | 5s |
| PostToolUse | Edit\|Write | `auto-format.sh` | 15s |
| Stop | — | `session-log.sh` | 5s |
| PostCompact | — | `post-compact.sh` | 5s |
| SessionStart | startup | `respawn-resume.sh` | 5s |

All hooks are bash, read a JSON payload on **stdin** (fields extracted via `jq`, with a `python3` fallback), and are **fail-open** (exit 0 on internal error) except the safety check, which blocks by design.

- **`safety-check.sh`** (PreToolUse/Bash) — exits **2 (block)** with a stderr reason when the command matches: `rm -rf` on root or relative paths, `DROP/TRUNCATE TABLE|DATABASE|SCHEMA`, force-push to main/master, `git reset --hard`, `--no-verify`, `--passWithNoTests`, writes to `.env.production`, broad `pkill -9`.
- **`auto-format.sh`** (PostToolUse/Edit|Write) — formats by extension: prettier for ts/tsx/js/jsx/mjs/cjs/json, black for py, gofmt for go. Silent no-op if the formatter isn't installed.
- **`session-log.sh`** (Stop) — appends a timestamped "Turn complete" line to `<cwd>/quality_reports/session_logs/<session_id>.log`.
- **`post-compact.sh`** (PostCompact) — prints a "re-read planning/00-master-plan.md" reminder if that file exists. (PostCompact stdout may not reach the model; the AGENTS.md re-read rule is the real mechanism.)
- **`respawn-resume.sh`** (SessionStart/startup) — second half of the `respawn` skill. If `<cwd>/planning/.respawn-pending` exists and is <60 min old, prints resume instructions (re-enable caveman at the recorded level, invoke `resume-from-handoff`). Stale markers are deleted.

## tui.toml

Theme `auto`, desktop notifications on but only when the terminal is unfocused, editor defers to `$VISUAL`/`$EDITOR`, CLI auto-update enabled.

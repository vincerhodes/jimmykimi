#!/usr/bin/env bash
# ~/.kimi-code/hooks/safety-check.sh
# PreToolUse hook for the Bash tool. Exit 2 blocks the call and shows the message to the model.
# Ported from ~/.claude/hooks/safety-check.sh — same stdin JSON contract (.tool_input.command),
# same exit-code semantics (2 = block, stderr is the reason).

set -uo pipefail

PAYLOAD="$(cat)"

if command -v jq >/dev/null 2>&1; then
  COMMAND="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.command // empty' 2>/dev/null)"
else
  COMMAND="$(printf '%s' "$PAYLOAD" | python3 -c "
import json,sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
print((d.get('tool_input') or {}).get('command') or '')
" 2>/dev/null)"
fi

[[ -z "${COMMAND:-}" ]] && exit 0

check_pattern() {
  local pattern="$1"
  local message="$2"
  # `--` ends option parsing: without it, a pattern starting with `--` (e.g. --no-verify,
  # --passWithNoTests) is swallowed by grep as a flag and silently never matches.
  if printf '%s' "$COMMAND" | grep -qE -- "$pattern"; then
    echo "BLOCKED: $message" >&2
    echo "Command: $COMMAND" >&2
    echo "To proceed, run this command manually in your terminal." >&2
    exit 2
  fi
}

# Destructive filesystem operations
check_pattern 'rm\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+/(\s|$)' "rm -rf on root path is blocked"
check_pattern 'rm\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+\.(\s|/|$)' "rm -rf on current/relative path is blocked"

# Database destructive operations
check_pattern '(DROP\s+TABLE|TRUNCATE\s+TABLE|DROP\s+DATABASE|DROP\s+SCHEMA)' "Destructive DB operation blocked"

# Git destructive operations
check_pattern 'git\s+push\s+.*--force.*\s+(main|master)' "Force push to main/master blocked"
check_pattern 'git\s+reset\s+--hard' "git reset --hard blocked — use git stash or confirm manually"

# Verification bypass
check_pattern 'git\s+(commit|push)\s+.*--no-verify' "--no-verify bypasses the commit hooks"
check_pattern '--passWithNoTests' "--passWithNoTests turns an empty suite into a green one. Blocked."

# Sensitive files
check_pattern '(>|>>|tee)\s+\.env\.production' "Write to .env.production blocked"

# Broad process killing
check_pattern 'pkill\s+-9\s+[^0-9]' "Broad pkill -9 blocked — be specific about PID"

exit 0

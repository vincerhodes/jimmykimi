#!/usr/bin/env bash
# ~/.kimi-code/hooks/auto-format.sh
# PostToolUse hook (Edit|Write). Formats the file just written.
# Ported from ~/.claude/hooks/auto-format.sh — reads .tool_input.file_path from the stdin JSON
# payload instead of the CLAUDE_FILE_PATH env var. Silent-fail: a missing formatter breaks nothing.

set -uo pipefail

PAYLOAD="$(cat)"

if command -v jq >/dev/null 2>&1; then
  FILE="$(printf '%s' "$PAYLOAD" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"
else
  FILE="$(printf '%s' "$PAYLOAD" | python3 -c "
import json,sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
print((d.get('tool_input') or {}).get('file_path') or '')
" 2>/dev/null)"
fi

if [[ -z "${FILE:-}" || ! -f "$FILE" ]]; then
  exit 0
fi

EXT="${FILE##*.}"

case "$EXT" in
  ts|tsx|js|jsx|mjs|cjs)
    npx prettier --write "$FILE" 2>/dev/null || true
    ;;
  json)
    npx prettier --write "$FILE" 2>/dev/null || true
    ;;
  py)
    python3 -m black "$FILE" 2>/dev/null || true
    ;;
  go)
    gofmt -w "$FILE" 2>/dev/null || true
    ;;
  *)
    # No formatter for this type, exit cleanly
    ;;
esac

exit 0

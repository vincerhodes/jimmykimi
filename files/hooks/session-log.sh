#!/usr/bin/env bash
# ~/.kimi-code/hooks/session-log.sh
# Stop hook. Appends a timestamp marker to the session log.
# Ported from ~/.claude/hooks/session-log.sh — reads session_id/cwd from the stdin JSON payload
# instead of CLAUDE_SESSION_ID/CLAUDE_PROJECT_DIR env vars.

set -uo pipefail

PAYLOAD="$(cat)"

if command -v jq >/dev/null 2>&1; then
  CWD="$(printf '%s' "$PAYLOAD" | jq -r '.cwd // empty' 2>/dev/null)"
  SESSION_ID="$(printf '%s' "$PAYLOAD" | jq -r '.session_id // empty' 2>/dev/null)"
else
  read -r CWD SESSION_ID <<< "$(printf '%s' "$PAYLOAD" | python3 -c "
import json,sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
print(d.get('cwd') or '', d.get('session_id') or '')
" 2>/dev/null)"
fi

LOG_DIR="${CWD:-$PWD}/quality_reports/session_logs"
SESSION_ID="${SESSION_ID:-unknown}"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Append turn marker to session log
LOGFILE="$LOG_DIR/${SESSION_ID}.log"
echo "[$TIMESTAMP] Turn complete" >> "$LOGFILE"

exit 0

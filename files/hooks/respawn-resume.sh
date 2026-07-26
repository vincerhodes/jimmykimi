#!/usr/bin/env bash
# ~/.kimi-code/hooks/respawn-resume.sh
# SessionStart(startup) hook — second half of /skill:respawn.
# If respawn primed a marker before the /clear, inject resume instructions into the
# fresh session's context. Stale markers (>60 min) are discarded.
# Ported from ~/.claude/hooks/respawn-resume.sh — reads cwd from the stdin JSON payload.

set -uo pipefail

PAYLOAD="$(cat)"

if command -v jq >/dev/null 2>&1; then
  CWD="$(printf '%s' "$PAYLOAD" | jq -r '.cwd // empty' 2>/dev/null)"
else
  CWD="$(printf '%s' "$PAYLOAD" | python3 -c "
import json,sys
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
print(d.get('cwd') or '')
" 2>/dev/null)"
fi

MARKER="${CWD:-$PWD}/planning/.respawn-pending"
[ -f "$MARKER" ] || exit 0

# Stale marker from an aborted respawn — discard silently.
if [ -z "$(find "$MARKER" -mmin -60 2>/dev/null)" ]; then
  rm -f "$MARKER"
  exit 0
fi

CAVEMAN=$(sed -n 's/^caveman=//p' "$MARKER")
# Marker intentionally left in place: hook stdout is NOT injected into the fresh
# session's context (verified 2026-07-19), so the AGENTS.md fallback
# ("marker exists → delete it, invoke /skill:resume-from-handoff") is the guaranteed
# resume path and must be able to see it. Stale markers are still discarded above.

echo "RESPAWN: this fresh session was triggered by the respawn skill. On the user's next message, before anything else:"
if [ -n "$CAVEMAN" ] && [ "$CAVEMAN" != "off" ]; then
  echo "1. Invoke the caveman skill at level '$CAVEMAN' (/skill:caveman $CAVEMAN) and keep it active for the whole session."
  echo "2. Invoke the resume-from-handoff skill (/skill:resume-from-handoff) and follow it fully."
else
  echo "1. Invoke the resume-from-handoff skill (/skill:resume-from-handoff) and follow it fully."
fi
echo "Treat the user's next message as 'go' unless it says otherwise."

exit 0

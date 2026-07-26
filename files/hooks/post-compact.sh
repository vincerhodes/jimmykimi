#!/usr/bin/env bash
# ~/.kimi-code/hooks/post-compact.sh
# PostCompact hook — prints a reminder to re-read the master plan after context compaction.
# Ported from ~/.claude/hooks/post-compact.sh — reads cwd from the stdin JSON payload.
# Note: PostCompact is observation-only in Kimi Code, so this reminder may not reach the model;
# the AGENTS.md "re-read planning/00-master-plan.md after compaction" rule is the real mechanism.

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

PLAN="${CWD:-$PWD}/planning/00-master-plan.md"
if [[ -f "$PLAN" ]]; then
  echo "PostCompact: re-read planning/00-master-plan.md before continuing."
fi
exit 0

#!/usr/bin/env bash
set -euo pipefail
PROMPT="${*:-}"
if [[ -z "$PROMPT" ]]; then
  echo "Usage: redteam_consult.sh 'question for redteam'" >&2
  exit 2
fi
exec /opt/data/.local/bin/hermes --profile redteam chat -q "$PROMPT"

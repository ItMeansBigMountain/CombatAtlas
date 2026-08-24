#!/usr/bin/env bash
set -euo pipefail
HERMES=/opt/data/.local/bin/hermes
WORKDIR=/opt/data/HeRmEz
LOG=/opt/data/HeRmEz/projects/KANBAN_DISPATCH.log
mkdir -p "$(dirname "$LOG")"
cd "$WORKDIR"
OUT="$($HERMES kanban dispatch --max 2 --json 2>&1 || true)"
printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$OUT" >> "$LOG"
# Stay silent for cron delivery; the board/log are durable surfaces.
exit 0

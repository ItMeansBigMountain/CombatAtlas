#!/usr/bin/env bash
set -euo pipefail

cd /opt/data/HeRmEz/projects/viral-clip-radar

# Discovery: keep the existing creator-watchlist behavior, but capture output so
# this wrapper can decide whether there is anything new to process.
DISCOVERY_OUTPUT="$(python3 scripts/poll_watchlist.py --limit 15 --quiet-if-empty)"

if [[ -z "${DISCOVERY_OUTPUT//[[:space:]]/}" ]]; then
  # Stay silent when there is nothing new; no_agent cron jobs deliver non-empty stdout.
  exit 0
fi

printf '%s\n' "$DISCOVERY_OUTPUT"
printf '\n---\nStarting clip/render/upload pipeline for newly discovered Viral Radar item(s)...\n'

# The daily uploader selects the freshest not-yet-public manifest clip, renders it,
# uploads public to YouTube, and logs the returned YouTube response. FORCE_UPLOAD
# allows this discovery-triggered lane to run even if the noon daily lane already ran.
FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py

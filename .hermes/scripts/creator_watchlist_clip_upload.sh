#!/usr/bin/env bash
set -euo pipefail

cd /opt/data/HeRmEz/projects/viral-clip-radar

# Use private user-provided YouTube cookies for source acquisition when present.
# Only the path is exported; cookie values stay in /opt/data/secrets with 0600 perms.
if [[ -f /opt/data/secrets/youtube-cookies/youtube-cookies.txt ]]; then
  export YOUTUBE_COOKIES_FILE=/opt/data/secrets/youtube-cookies/youtube-cookies.txt
  export YTDLP_COOKIES_FILE=/opt/data/secrets/youtube-cookies/youtube-cookies.txt
  export YOUTUBE_COOKIES=/opt/data/secrets/youtube-cookies/youtube-cookies.txt
fi

# Discovery: find newly available videos from the configured creator watchlist.
DISCOVERY_OUTPUT="$(python3 scripts/poll_watchlist.py --limit 15 --quiet-if-empty)"

if [[ -z "${DISCOVERY_OUTPUT//[[:space:]]/}" ]]; then
  # Stay silent when there is nothing new; no_agent cron jobs deliver non-empty stdout.
  exit 0
fi

printf '%s\n' "$DISCOVERY_OUTPUT"
printf '\n---\nStarting strict Viral Radar procedure: discovered creator video -> >=10 clips -> upload those exact clips...\n'

# Extract the exact plans discovered by the data pipeline. Each plan is processed
# independently so every found influencer video gets its own minimum clip batch.
PRIORITY_PLANS="$(printf '%s\n' "$DISCOVERY_OUTPUT" | awk '/^  Plan: /{sub(/^  Plan: /, ""); print}' | paste -sd ':' -)"

# Viral Radar influencer clips always upload to Classical Echos. Override any
# inherited token from faceless/newsletter jobs.
export YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
export VIRAL_RADAR_MIN_UPLOADS="${VIRAL_RADAR_MIN_UPLOADS:-10}"
export VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM="${VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM:-10}"
export VIRAL_RADAR_MAX_CLIPS_PER_SOURCE="${VIRAL_RADAR_MAX_CLIPS_PER_SOURCE:-50}"
export VIRAL_RADAR_DAILY_UPLOAD_CAP="${VIRAL_RADAR_DAILY_UPLOAD_CAP:-100}"
export VIRAL_RADAR_STRICT_DISCOVERED_ONLY=1
# Do not let old queued/stale clips satisfy the minimum for a new discovered video.
export VIRAL_RADAR_UPLOAD_QUEUE_FIRST=0

FAILURES=0
IFS=':' read -r -a PLANS <<< "$PRIORITY_PLANS"
if [[ -z "$PRIORITY_PLANS" ]]; then
  PLANS=("")
fi

for PLAN in "${PLANS[@]}"; do
  if [[ -n "$PLAN" ]]; then
    export VIRAL_RADAR_PRIORITY_PLANS="$PLAN"
    printf '\n---\nProcessing discovered plan: %s\n' "$PLAN"
  else
    unset VIRAL_RADAR_PRIORITY_PLANS
  fi
  if ! FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py; then
    FAILURES=$((FAILURES + 1))
  fi
done

if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi

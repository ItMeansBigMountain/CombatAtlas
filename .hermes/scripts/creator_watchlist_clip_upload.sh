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

# Discovery: keep the existing creator-watchlist behavior, but capture output so
# this wrapper can decide whether there is anything new to process.
DISCOVERY_OUTPUT="$(python3 scripts/poll_watchlist.py --limit 15 --quiet-if-empty)"

if [[ -z "${DISCOVERY_OUTPUT//[[:space:]]/}" ]]; then
  # Stay silent when there is nothing new; no_agent cron jobs deliver non-empty stdout.
  exit 0
fi

printf '%s\n' "$DISCOVERY_OUTPUT"
printf '\n---\nStarting clip/render/upload pipeline for newly discovered Viral Radar item(s)...\n'

# Prioritize the exact plans that this poll discovered. If a plan only has
# source_metadata.json, viral_radar_daily_upload.py will auto-create a minimal
# clip_manifest.json and attempt immediate source -> vertical render -> public
# upload. This keeps this cron as a true discovery-triggered publish lane.
PRIORITY_PLANS="$(printf '%s\n' "$DISCOVERY_OUTPUT" | awk '/^  Plan: /{sub(/^  Plan: /, ""); print}' | paste -sd ':' -)"
if [[ -n "$PRIORITY_PLANS" ]]; then
  export VIRAL_RADAR_PRIORITY_PLANS="$PRIORITY_PLANS"
fi

# The uploader selects the freshest not-yet-public manifest clip, renders it,
# uploads public to YouTube, and logs the returned YouTube response. FORCE_UPLOAD
# allows this discovery-triggered lane to run even if the noon daily lane already ran.
# Run once per discovered plan so discovery does not stop after one influencer.
# Long-form seeding now defaults to at least 3 clips per video.
# Viral Radar influencer clips always upload to Classical Echos. Override any
# inherited token from faceless/newsletter jobs.
export YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json
export VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM="${VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM:-3}"
PLAN_COUNT="$(printf '%s\n' "$PRIORITY_PLANS" | awk -F: '{print NF}')"
if [[ -z "$PRIORITY_PLANS" ]]; then
  PLAN_COUNT=1
fi
FAILURES=0
for ((i=1; i<=PLAN_COUNT; i++)); do
  if ! FORCE_UPLOAD=1 python3 /opt/data/scripts/viral_radar_daily_upload.py; then
    FAILURES=$((FAILURES + 1))
  fi
done
if [[ "$FAILURES" -gt 0 ]]; then
  exit 1
fi

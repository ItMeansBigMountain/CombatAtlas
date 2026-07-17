#!/usr/bin/env bash
set -u

ROOT="/opt/data/HeRmEz/projects/viral-clip-radar"
PYTHON="/opt/hermes/.venv/bin/python3"
RUNNER="/opt/data/scripts/viral_radar_daily_upload.py"

# Hard separation guard: this backlog processor may only operate on Viral Radar.
if [[ ! -d "$ROOT/CLIP_PLANS" || ! -f "$ROOT/scripts/upload_to_youtube.py" ]]; then
  printf '{"status":"blocked_invalid_viral_radar_root","root":"%s"}\n' "$ROOT"
  exit 1
fi

queue_count=$(find "$ROOT/UPLOAD_QUEUE" -maxdepth 1 -type f -name '*.upload.json' 2>/dev/null | wc -l | tr -d ' ')
min_uploads=10
if [[ "$queue_count" =~ ^[0-9]+$ ]] && (( queue_count > min_uploads )); then
  min_uploads="$queue_count"
fi

output=$(mktemp)
trap 'rm -f "$output"' EXIT

set +e
FORCE_UPLOAD=1 \
VIRAL_RADAR_UPLOAD_QUEUE_FIRST=1 \
VIRAL_RADAR_STRICT_DISCOVERED_ONLY=1 \
VIRAL_RADAR_MIN_UPLOADS="$min_uploads" \
VIRAL_RADAR_MAX_SOURCE_ATTEMPTS=50 \
VIRAL_RADAR_DAILY_UPLOAD_CAP=100 \
"$PYTHON" "$RUNNER" >"$output" 2>&1
rc=$?
set -e

remaining_queue=$(find "$ROOT/UPLOAD_QUEUE" -maxdepth 1 -type f -name '*.upload.json' 2>/dev/null | wc -l | tr -d ' ')
hold_queue=$(find "$ROOT/UPLOAD_QUEUE_HOLD" -maxdepth 1 -type f -name '*.upload.json' 2>/dev/null | wc -l | tr -d ' ')

printf 'Viral Radar backlog processor\n'
printf 'status: %s\n' "$([[ $rc -eq 0 ]] && printf completed || printf blocked_or_failed)"
printf 'queue_before: %s\n' "$queue_count"
printf 'queue_after: %s\n' "$remaining_queue"
printf 'hold_queue: %s\n' "$hold_queue"
printf 'pipeline_exit: %s\n' "$rc"
printf '%s\n' '--- pipeline tail ---'
tail -n 120 "$output"

exit "$rc"

#!/usr/bin/env bash
set -euo pipefail
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
# Faceless/Daily Stoic videos upload to A F (fareed320).
export YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-fareed320/youtube_upload_token.json
exec /opt/hermes/.venv/bin/python scripts/newsletter_batch_upload.py --profile all-personal --limit 10

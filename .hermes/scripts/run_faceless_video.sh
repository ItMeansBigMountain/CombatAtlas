#!/usr/bin/env bash
set -euo pipefail
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
# Faceless/newsletter videos always upload to Trapiistan/Sosai.
export YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json
exec python3 scripts/run_trend_video.py

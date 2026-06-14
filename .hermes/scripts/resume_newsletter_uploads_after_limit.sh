#!/usr/bin/env bash
set -euo pipefail
export NEWSLETTER_UPLOAD_MANIFEST=/opt/data/HeRmEz/projects/faceless-youtube-channel/PENDING_UPLOAD_AFTER_LIMIT_20260613.json
/opt/hermes/.venv/bin/python /opt/data/scripts/upload_rendered_newsletter_videos.py

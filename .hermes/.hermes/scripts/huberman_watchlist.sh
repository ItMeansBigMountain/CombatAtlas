#!/usr/bin/env bash
set -euo pipefail
cd /opt/data/HeRmEz/projects/viral-clip-radar
python3 scripts/poll_watchlist.py --limit 15 --quiet-if-empty

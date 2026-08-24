#!/usr/bin/env bash
set -euo pipefail
exec /usr/bin/python3 /opt/data/scripts/expire_kanban_corruption_forensics.py --apply --retention-days 30

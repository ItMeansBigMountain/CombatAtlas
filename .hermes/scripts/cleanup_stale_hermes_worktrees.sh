#!/usr/bin/env bash
set -euo pipefail
exec python3 /opt/data/scripts/cleanup_stale_hermes_worktrees.py --apply

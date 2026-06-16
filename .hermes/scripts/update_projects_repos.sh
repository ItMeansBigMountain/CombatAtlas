#!/usr/bin/env bash
set -euo pipefail
ROOT="/opt/data/HeRmEz/projects"
LOG_DIR="$ROOT/_ops/update-logs"
mkdir -p "$LOG_DIR"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$LOG_DIR/projects-update-$TS.log"
{
  echo "# Project repo update $TS"
  echo "ROOT=$ROOT"
  echo
  find "$ROOT" -mindepth 1 -maxdepth 3 -type d -name .git -prune | while read -r gitdir; do
    repo="$(dirname "$gitdir")"
    echo "## $repo"
    git -C "$repo" remote -v || true
    git -C "$repo" status --short || true
    if git -C "$repo" remote get-url origin >/dev/null 2>&1; then
      git -C "$repo" fetch --all --prune || true
      branch="$(git -C "$repo" branch --show-current || true)"
      if [ -n "$branch" ]; then
        git -C "$repo" status -sb || true
      fi
    fi
    echo
  done
} | tee "$LOG"
echo "$LOG"

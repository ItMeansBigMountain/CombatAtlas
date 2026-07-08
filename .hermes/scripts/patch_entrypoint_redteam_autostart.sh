#!/usr/bin/env bash
set -euo pipefail

ENTRYPOINT=${1:-/entrypoint.sh}

if [[ ! -f "$ENTRYPOINT" ]]; then
  echo "entrypoint_not_found: $ENTRYPOINT" >&2
  exit 1
fi

DEFAULT_BLOCK='if [[ -f /opt/data/config.yaml ]]; then
  if ! pgrep -f "hermes gateway run" >/dev/null 2>&1; then
    gosu hermes nohup hermes gateway run >>/opt/data/logs/gateway.log 2>&1 </dev/null &
  fi
fi'

REDTEAM_BLOCK='if [[ -f /opt/data/config.yaml ]]; then
  if ! pgrep -f "hermes -p redteam gateway run" >/dev/null 2>&1; then
    gosu hermes nohup hermes -p redteam gateway run >>/opt/data/logs/gateway-redteam.log 2>&1 </dev/null &
  fi
fi'

if grep -F 'hermes -p redteam gateway run' "$ENTRYPOINT" >/dev/null; then
  echo "already_patched: $ENTRYPOINT"
  exit 0
fi

python3 - "$ENTRYPOINT" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1])
text = p.read_text()
anchor = '''if [[ -f /opt/data/config.yaml ]]; then
  if ! pgrep -f "hermes gateway run" >/dev/null 2>&1; then
    gosu hermes nohup hermes gateway run >>/opt/data/logs/gateway.log 2>&1 </dev/null &
  fi
fi'''
red = '''

if [[ -f /opt/data/config.yaml ]]; then
  if ! pgrep -f "hermes -p redteam gateway run" >/dev/null 2>&1; then
    gosu hermes nohup hermes -p redteam gateway run >>/opt/data/logs/gateway-redteam.log 2>&1 </dev/null &
  fi
fi'''
if anchor not in text:
    raise SystemExit('default_gateway_anchor_not_found')
p.write_text(text.replace(anchor, anchor + red))
PY

if command -v zsh >/dev/null 2>&1; then
  zsh -n "$ENTRYPOINT"
elif command -v sh >/dev/null 2>&1; then
  sh -n "$ENTRYPOINT"
fi

echo "patched: $ENTRYPOINT"

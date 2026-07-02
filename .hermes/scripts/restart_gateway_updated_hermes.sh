#!/usr/bin/env bash
set -euo pipefail
export HERMES_HOME=/opt/data
export HOME=/opt/data
export PATH=/opt/data/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LOG=/opt/data/logs/gateway-restart-updated-hermes.log
mkdir -p /opt/data/logs
if kill -0 11 2>/dev/null; then
  echo "Stopping old gateway PID 11" >>"$LOG"
  kill 11 || true
  sleep 5
fi
# Kill any remaining old /opt/hermes gateway processes owned by this user.
pkill -u "$(id -u)" -f '/opt/hermes/.venv/.*/hermes gateway run|/opt/hermes/.venv/bin/hermes gateway run' 2>/dev/null || true
sleep 2
nohup /opt/data/.local/bin/hermes gateway run >>"$LOG" 2>&1 &
echo $! >/opt/data/logs/gateway-updated-hermes.pid
sleep 8
/opt/data/.local/bin/hermes gateway status >>"$LOG" 2>&1 || true
ps -p "$(cat /opt/data/logs/gateway-updated-hermes.pid)" -o pid,user,cmd >>"$LOG" 2>&1 || true
cat "$LOG"

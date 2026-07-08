#!/usr/bin/env bash
set -euo pipefail

# Silent watchdog: keep redteam profile gateway running after Docker/container resets.
# The default gateway is started by /entrypoint.sh; this ensures the second profile starts too.
LOG=/opt/data/logs/gateway-redteam.log
mkdir -p /opt/data/logs

if pgrep -f 'hermes -p redteam gateway run' >/dev/null 2>&1; then
  exit 0
fi

# Remove stale pid/lock only if no matching process exists.
rm -f /opt/data/profiles/redteam/gateway.pid /opt/data/profiles/redteam/gateway.lock 2>/dev/null || true

nohup /opt/data/.local/bin/hermes -p redteam gateway run >>"$LOG" 2>&1 </dev/null &

# Give it a moment to write state. Stay silent on success; emit on failure so cron alerts.
sleep 5
if pgrep -f 'hermes -p redteam gateway run' >/dev/null 2>&1; then
  exit 0
fi

echo '{"status":"redteam_gateway_start_failed","log":"/opt/data/logs/gateway-redteam.log"}'
exit 1

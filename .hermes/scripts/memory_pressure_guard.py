#!/usr/bin/env python3
"""Alert once on VPS memory pressure; never kills processes."""
from __future__ import annotations

import json
import os
from pathlib import Path

STATE = Path('/opt/data/runtime-state/memory-guard.json')
STATE.parent.mkdir(parents=True, exist_ok=True)


def meminfo() -> dict[str, int]:
    out = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        parts = value.strip().split()
        if parts and parts[0].isdigit():
            out[key] = int(parts[0]) * 1024
    return out


def process_snapshot() -> tuple[int, list[dict[str, object]]]:
    total = 0
    rows = []
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cmd = (entry / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='ignore')
            if not any(name in cmd for name in ('tsserver.js', 'typescript-language-server', 'pyright', 'gradle', 'runelite')):
                continue
            status = {}
            for line in (entry / 'status').read_text().splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    status[key] = value.strip()
            rss_kib = int(status.get('VmRSS', '0 kB').split()[0])
            rss = rss_kib * 1024
            total += rss
            rows.append({'pid': int(entry.name), 'rss_mib': round(rss / 1048576), 'cmd': cmd[:140]})
        except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
            continue
    rows.sort(key=lambda row: int(row['rss_mib']), reverse=True)
    return total, rows[:8]


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {'alerting': False}


def save_state(value: dict) -> None:
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, sort_keys=True))
    os.chmod(tmp, 0o600)
    tmp.replace(STATE)


def main() -> None:
    mi = meminfo()
    total = mi.get('MemTotal', 1)
    available = mi.get('MemAvailable', 0)
    available_pct = available * 100 / total
    dev_rss, rows = process_snapshot()
    critical = available < 768 * 1048576 or available_pct < 10 or dev_rss > 3 * 1073741824
    previous = load_state()

    if critical and not previous.get('alerting'):
        print('⚠️ VPS memory guard: pressure is critical.')
        print(f'- Available: {available / 1073741824:.2f} GiB ({available_pct:.1f}%)')
        print(f'- Development-process RSS: {dev_rss / 1073741824:.2f} GiB')
        for row in rows[:5]:
            print(f"- PID {row['pid']}: {row['rss_mib']} MiB — {row['cmd']}")
        print('- Alert only: no process was stopped automatically.')
    elif not critical and previous.get('alerting'):
        print('✅ VPS memory recovered above the guard threshold.')
        print(f'- Available: {available / 1073741824:.2f} GiB ({available_pct:.1f}%)')
        print(f'- Development-process RSS: {dev_rss / 1073741824:.2f} GiB')

    save_state({'alerting': critical})


if __name__ == '__main__':
    main()

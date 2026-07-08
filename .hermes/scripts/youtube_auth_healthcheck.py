#!/usr/bin/env python3
"""Silent YouTube/Workspace auth healthcheck for recurring social-video crons.

No secrets are printed. Default mode is watchdog style: stdout is empty when all
checks pass, and contains an actionable alert only on failure. Use --verbose for
manual diagnostics.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path('/opt/data/HeRmEz')
REAUTH = Path('/opt/data/scripts/google_reauth_workflow.py')
METRICS = Path('/opt/data/scripts/youtube_metrics_monitor.py')
SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
VIRAL_UPLOADER = Path('/opt/data/HeRmEz/projects/viral-clip-radar/scripts/upload_to_youtube.py')
FACELESS_NEWSLETTER = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/newsletter_batch_upload.py')
VIRAL_DAILY = Path('/opt/data/scripts/viral_radar_daily_upload.py')
CREATOR_WRAPPER = Path('/opt/data/scripts/creator_watchlist_clip_upload.sh')
FACELESS_WRAPPER = Path('/opt/data/scripts/run_faceless_video.sh')

EXPECTED = {
    'trapiistan': {
        'channel_id': 'UCsxzQlusqwmMUdjMvKAJDfA',
        'title': 'Sosai Oyama',
        'token': '/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json',
    },
    'classicalechos': {
        'channel_id': 'UCcIpxiU2CLEsBdHcc7_lcyA',
        'title': 'Classical Echos',
        'token': '/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json',
    },
    'fareed320': {
        'channel_id': 'PENDING_FAREED320_CHANNEL_ID',
        'title': 'fareed320 YouTube failover',
        'token': '/opt/data/secrets/youtube-fareed320/youtube_upload_token.json',
        'optional_until_verified': True,
    },
}

REQUIRED_SNIPPETS = {
    str(FACELESS_NEWSLETTER): [
        '/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json',
        'UCsxzQlusqwmMUdjMvKAJDfA',
    ],
    str(FACELESS_WRAPPER): [
        'YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json',
    ],
    str(VIRAL_UPLOADER): [
        "/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json",
        "UCcIpxiU2CLEsBdHcc7_lcyA",
        "/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json",
        "UCsxzQlusqwmMUdjMvKAJDfA",
        "Classical Echos upload limit hit; failed over to",
        "youtube-fareed320",
    ],
    str(VIRAL_DAILY): [
        '/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json',
        'cross-lane token defaults caused recurring',
    ],
    str(CREATOR_WRAPPER): [
        'YOUTUBE_UPLOAD_TOKEN=/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json',
        'VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM',
    ],
    str(SHARED_UPLOADER): [
        '--expect-channel-id',
        'blocked_wrong_channel_token',
    ],
}

RECENT_ERROR_PATTERNS = [
    'invalid_grant',
    'blocked_wrong_channel_token',
    'ModuleNotFoundError: No module named',
    'provider timeout',
    'Fallback chain was exhausted',
]


def run_json(cmd: list[str], timeout: int = 120) -> tuple[bool, dict | str]:
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    if p.returncode != 0:
        return False, (p.stderr or p.stdout)[-2000:]
    try:
        return True, json.loads(p.stdout)
    except Exception:
        return False, p.stdout[-2000:]


def check_youtube_profiles() -> list[str]:
    problems: list[str] = []
    for profile, exp in EXPECTED.items():
        token = Path(exp['token'])
        if not token.is_file():
            if exp.get('optional_until_verified'):
                continue
            problems.append(f'{profile}: missing token file {token}')
            continue
        ok, data = run_json([sys.executable, str(REAUTH), 'verify', 'youtube', profile])
        if not ok:
            if exp.get('optional_until_verified'):
                continue
            problems.append(f'{profile}: verify failed: {data}')
            continue
        if not data.get('valid'):
            problems.append(f'{profile}: token not valid')
        if not data.get('channel_match'):
            problems.append(f"{profile}: channel mismatch; expected {exp['channel_id']}, got {data.get('channels')}")
        scopes = set(data.get('scopes') or [])
        needed = {'https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly'}
        missing = sorted(needed - scopes)
        if missing:
            problems.append(f'{profile}: missing scopes {missing}')
    return problems


def check_code_guards() -> list[str]:
    problems: list[str] = []
    for path_s, snippets in REQUIRED_SNIPPETS.items():
        path = Path(path_s)
        if not path.exists():
            problems.append(f'missing guard file: {path}')
            continue
        text = path.read_text(errors='ignore')
        for snippet in snippets:
            if snippet not in text:
                problems.append(f'{path}: missing guard snippet {snippet!r}')
    return problems


def check_python_deps() -> list[str]:
    problems: list[str] = []
    code = 'import googleapiclient, google.oauth2.credentials; print("ok")'
    for py in ['/opt/hermes/.venv/bin/python3', sys.executable]:
        if not Path(py).exists():
            continue
        p = subprocess.run([py, '-c', code], text=True, capture_output=True)
        if p.returncode != 0 and py == '/opt/hermes/.venv/bin/python3':
            problems.append(f'Hermes uploader Python missing Google deps: {py}: {(p.stderr or p.stdout)[-500:]}')
    return problems


def check_metrics() -> list[str]:
    problems: list[str] = []
    if not METRICS.exists():
        return ['missing metrics monitor script']
    ok, data = run_json([sys.executable, str(METRICS), '--json'], timeout=180)
    if not ok:
        problems.append(f'metrics monitor failed/unparsed: {data}')
    elif data.get('status') not in (None, 'ok'):
        problems.append(f"metrics monitor status={data.get('status')}: {data.get('errors')}")
    return problems


def check_recent_cron_errors() -> list[str]:
    problems: list[str] = []
    outdir = Path('/opt/data/cron/output')
    if not outdir.exists():
        return problems
    files = sorted(outdir.glob('*.txt'), key=lambda p: p.stat().st_mtime, reverse=True)[:80]
    hits = []
    for path in files:
        text = path.read_text(errors='ignore')[-12000:]
        for pat in RECENT_ERROR_PATTERNS:
            if pat in text:
                hits.append(f'{path.name}: {pat}')
                break
    # Historical output can contain already-fixed problems; report only in verbose.
    if hits:
        problems.append('recent cron logs contain notable auth/provider patterns: ' + '; '.join(hits[:12]))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--ignore-recent-log-history', action='store_true', default=True)
    ap.add_argument('--include-recent-log-history', action='store_true')
    args = ap.parse_args()

    checks = {
        'youtube_profiles': check_youtube_profiles(),
        'code_guards': check_code_guards(),
        'python_deps': check_python_deps(),
        'metrics': check_metrics(),
    }
    if args.include_recent_log_history:
        checks['recent_cron_logs'] = check_recent_cron_errors()

    problems = [f'{section}: {problem}' for section, items in checks.items() for problem in items]
    if problems or args.verbose:
        payload = {
            'status': 'blocked_auth_hardening' if problems else 'ok',
            'problems': problems,
            'checks': checks if args.verbose else None,
            'next_steps': [
                'If a YouTube profile fails, run: python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url <profile>',
                'Exchange callback with: python3 /opt/data/scripts/google_reauth_workflow.py youtube-exchange <profile> <localhost callback URL> --verify',
                'Then rerun: python3 /opt/data/scripts/youtube_auth_healthcheck.py --verbose',
            ] if problems else [],
        }
        print(json.dumps(payload, indent=2))
    return 1 if problems else 0


if __name__ == '__main__':
    raise SystemExit(main())

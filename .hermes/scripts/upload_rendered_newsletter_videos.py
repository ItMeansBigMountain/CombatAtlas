#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

MANIFEST = Path(os.environ.get('NEWSLETTER_UPLOAD_MANIFEST', '/opt/data/HeRmEz/projects/faceless-youtube-channel/REVIEW_FINAL_PRODUCTS_20260613.json'))
UPLOAD_SCRIPT = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel/UPLOADS/youtube_uploads.jsonl')
RUN_LOG = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel/UPLOADS/rendered_newsletter_upload_run_20260613.jsonl')
SUMMARY = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel/UPLOADS/rendered_newsletter_upload_summary_20260613.json')
GMAIL_TOKEN = Path('/opt/data/google_profiles/fareed320/google_token.json')
CALENDAR_TOKEN = Path('/opt/data/google_profiles/trapiistan/google_token.json')
SUPPORT_BLOCK = """More from me: https://linktr.ee/sosai.oyama
Support the channel: https://buymeacoffee.com/affanfareev
Cash App: https://cash.app/$sosaioyama
Venmo: https://venmo.com/u/SosaiOyama"""


def creds(path: Path):
    c = Credentials.from_authorized_user_file(str(path))
    if not c.valid and c.expired and c.refresh_token:
        c.refresh(Request())
        path.write_text(c.to_json())
        path.chmod(0o600)
    return c


def gmail_service():
    return build('gmail', 'v1', credentials=creds(GMAIL_TOKEN), cache_discovery=False)


def calendar_service():
    return build('calendar', 'v3', credentials=creds(CALENDAR_TOKEN), cache_discovery=False)


def safe_title(subject: str) -> str:
    title = re.sub(r'\s+', ' ', subject).strip()
    # Keep API-safe title length and avoid #Shorts because these are 2-minute videos.
    return title[:95]


def description(subject: str) -> str:
    return f"My read: turn this signal into proof today.\n\n{SUPPORT_BLOCK}"


def upload_video(path: Path, title: str, desc: str) -> dict:
    cmd = [
        sys.executable, str(UPLOAD_SCRIPT), str(path),
        '--title', title,
        '--description', desc,
        '--privacy', 'public',
        '--project', 'classical-echos-newsletter-backlog',
        '--log-jsonl', str(UPLOAD_LOG),
        '--delete-after-upload',
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout)[-2000:])
    start = r.stdout.find('{')
    if start < 0:
        raise RuntimeError(f'Could not parse uploader JSON: {r.stdout[-1000:]}')
    return json.loads(r.stdout[start:])


def create_calendar_event(subject: str, url: str):
    now = dt.datetime.now(dt.UTC)
    svc = calendar_service()
    body = {
        'summary': f'Published: {subject[:55]}',
        'description': f'Classical Echos newsletter video published public.\n{url}',
        'start': {'dateTime': now.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': (now + dt.timedelta(minutes=10)).isoformat(), 'timeZone': 'UTC'},
    }
    event = svc.events().insert(calendarId='primary', body=body).execute()
    return event.get('id')


def trash_source_email(workspace: Path):
    source = workspace / 'source.json'
    if not source.exists():
        return None
    meta = json.loads(source.read_text())
    msg_id = meta.get('id')
    if not msg_id or msg_id == 'fixture':
        return None
    gmail_service().users().messages().trash(userId='me', id=msg_id).execute()
    return msg_id


def main():
    items = json.loads(MANIFEST.read_text())
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    uploaded = []
    failed = []
    for idx, item in enumerate(items, 1):
        subject = item['subject']
        video = Path(item['path'])
        workspace = Path(item['workspace'])
        rec = {'index': idx, 'subject': subject, 'path': str(video), 'started_utc': dt.datetime.now(dt.UTC).isoformat()}
        print(f'[{idx}/{len(items)}] Uploading: {subject}', flush=True)
        try:
            if not video.exists():
                raise FileNotFoundError(str(video))
            result = upload_video(video, safe_title(subject), description(subject))
            url = result.get('url') or (f"https://youtu.be/{result.get('video_id')}" if result.get('video_id') else '')
            event_id = create_calendar_event(subject, url)
            trashed = trash_source_email(workspace)
            shutil.rmtree(workspace, ignore_errors=True)
            rec.update({'status': 'uploaded', 'url': url, 'video_id': result.get('video_id'), 'privacy': result.get('privacy'), 'calendar_event_id': event_id, 'trashed_email_id': trashed, 'finished_utc': dt.datetime.now(dt.UTC).isoformat()})
            uploaded.append(rec)
            print(f'  OK {url}', flush=True)
        except Exception as exc:
            rec.update({'status': 'failed', 'error': str(exc)[:2000], 'finished_utc': dt.datetime.now(dt.UTC).isoformat()})
            failed.append(rec)
            print(f'  FAILED {exc}', flush=True)
        with RUN_LOG.open('a') as f:
            f.write(json.dumps(rec) + '\n')
    summary = {'uploaded_count': len(uploaded), 'failed_count': len(failed), 'uploaded': uploaded, 'failed': failed, 'run_log': str(RUN_LOG), 'finished_utc': dt.datetime.now(dt.UTC).isoformat()}
    SUMMARY.write_text(json.dumps(summary, indent=2))
    print(json.dumps({'uploaded_count': len(uploaded), 'failed_count': len(failed), 'summary': str(SUMMARY)}, indent=2))


if __name__ == '__main__':
    main()

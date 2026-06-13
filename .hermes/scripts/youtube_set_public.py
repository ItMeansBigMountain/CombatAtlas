#!/usr/bin/env python3
from __future__ import annotations
import json, sys, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN = pathlib.Path('/opt/data/secrets/youtube-main/youtube_upload_token.json')
VIDEO_IDS = sys.argv[1:]
if not VIDEO_IDS:
    raise SystemExit('usage: youtube_set_public.py VIDEO_ID ...')

# Try broad enough scopes for metadata/status update; the stored token may or may not include them.
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]
creds = Credentials.from_authorized_user_file(str(TOKEN), scopes=SCOPES)
if not creds.valid and creds.expired and creds.refresh_token:
    creds.refresh(Request())
    TOKEN.write_text(creds.to_json())
    TOKEN.chmod(0o600)

yt = build('youtube', 'v3', credentials=creds, cache_discovery=False)
results = []
for vid in VIDEO_IDS:
    try:
        current = yt.videos().list(part='snippet,status', id=vid).execute()
        items = current.get('items', [])
        if not items:
            results.append({'video_id': vid, 'status': 'not_found_or_no_access'})
            continue
        item = items[0]
        snippet = item['snippet']
        status = item.get('status', {})
        status['privacyStatus'] = 'public'
        status.pop('publishAt', None)
        body = {
            'id': vid,
            'snippet': {
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'tags': snippet.get('tags', []),
                'categoryId': snippet.get('categoryId', '22'),
            },
            'status': status,
        }
        updated = yt.videos().update(part='snippet,status', body=body).execute()
        results.append({'video_id': vid, 'status': 'updated', 'privacy': updated.get('status', {}).get('privacyStatus'), 'url': f'https://youtu.be/{vid}'})
    except Exception as e:
        results.append({'video_id': vid, 'status': 'error', 'error': str(e)[:500]})
print(json.dumps(results, indent=2))

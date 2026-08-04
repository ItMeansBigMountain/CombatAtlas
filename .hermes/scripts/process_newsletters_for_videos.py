#!/usr/bin/env python3
"""
Process newsletters from a specific Gmail profile and generate faceless YouTube videos.
Uses Pexels API for stock footage instead of Sora.
"""

import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.request
import urllib.parse
from pathlib import Path

# Add hermes-agent to path
sys.path.insert(0, '/opt/data/hermes-agent')

ROOT = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel')
SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'newsletter_youtube_uploads.jsonl'
PROJECT = 'faceless-youtube-newsletters'
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
TOKEN_BASE = Path('/opt/data/google_profiles')

# Pexels configuration
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY') or os.getenv('PEXELS_API_KEY')


def load_dotenv(path: Path = Path('/opt/data/.env')) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors='ignore').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def elevenlabs_key() -> str | None:
    return os.getenv('EllevenLabsKey') or os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')


def pexels_available() -> bool:
    return bool(PEXELS_API_KEY)


def sh(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout.strip()


def slugify(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')[:70] or 'newsletter-video'


def gmail_service(profile: str):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    
    token = TOKEN_BASE / profile / 'google_token.json'
    creds = Credentials.from_authorized_user_file(str(token))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token.write_text(creds.to_json())
        os.chmod(token, 0o600)
    return build('gmail', 'v1', credentials=creds, cache_discovery=False)


def get_newsletter_messages(service, max_results=10):
    """Search for newsletter messages in the inbox."""
    results = service.users().messages().list(
        userId='me',
        q='in:inbox label:fareed320 OR from:fareed320@gmail.com',
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    return messages


def get_message_details(service, msg_id):
    """Get full message details."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg.get('payload', {})
    
    headers = {h['name'].lower(): h['value'] for h in payload.get('headers', [])}
    
    def decode_part(part):
        data = part.get('body', {}).get('data')
        if not data:
            return ''
        raw = base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))
        return raw.decode('utf-8', errors='replace')
    
    def walk_parts(part):
        yield part
        for child in part.get('parts', []) or []:
            yield from walk_parts(child)
    
    body = ''
    for part in walk_parts(payload):
        mime = part.get('mimeType', '')
        text = decode_part(part)
        if mime == 'text/plain' and text:
            body = text
            break
        elif mime == 'text/html' and text:
            body = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    
    return {
        'id': msg_id,
        'threadId': msg.get('threadId'),
        'from': headers.get('from', ''),
        'subject': headers.get('subject', ''),
        'date': headers.get('date', ''),
        'body': body[:2000]  # Limit body length
    }


def search_pexels_videos(query: str, per_page: int = 3) -> list[str]:
    """Search Pexels for video clips matching a query."""
    if not PEXELS_API_KEY:
        return []
    
    url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&per_page={per_page}"
    req = urllib.request.Request(url, headers={'Authorization': PEXELS_API_KEY})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            videos = []
            for vid in data.get('videos', []):
                for v in vid.get('video_files', []):
                    if v.get('width', 0) >= 1080 and 'mp4' in v.get('file_type', ''):
                        videos.append(v['link'])
                        break
            return videos[:3]
    except Exception as e:
        print(f"Pexels search error: {e}", file=sys.stderr)
        return []


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Process newsletters and generate videos')
    parser.add_argument('--profile', default='fareed320', help='Gmail profile to use')
    parser.add_argument('--max', type=int, default=5, help='Max number of newsletters to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed without generating')
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE")
        print(f"Profile: {args.profile}")
        print(f"Max messages: {args.max}")
        return 0
    
    # Check prerequisites
    has_voice = bool(elevenlabs_key())
    has_pexels = pexels_available()
    
    print(f"ElevenLabs: {'✓' if has_voice else '✗'}")
    print(f"Pexels: {'✓' if has_pexels else '✗'}")
    
    if not has_voice:
        print("ERROR: ElevenLabs key not configured")
        return 1
    
    if not has_pexels:
        print("WARNING: Pexels key not configured, using fallback visuals")
    
    # Connect to Gmail
    try:
        service = gmail_service(args.profile)
    except Exception as e:
        print(f"Failed to connect to Gmail: {e}")
        return 1
    
    # Get messages
    messages = get_newsletter_messages(service, max_results=args.max)
    print(f"Found {len(messages)} messages")
    
    for msg_ref in messages:
        msg_id = msg_ref['id']
        print(f"\nProcessing message {msg_id}...")
        
        details = get_message_details(service, msg_id)
        print(f"Subject: {details['subject']}")
        
        # Generate a topic from the subject
        topic = details['subject'][:80]
        
        # Try to find stock footage
        stock_clips = []
        if has_pexels:
            keywords = re.findall(r'\b\w+\b', topic.lower())[:3]
            for kw in keywords:
                clips = search_pexels_videos(kw, per_page=1)
                stock_clips.extend(clips)
        
        print(f"Found {len(stock_clips)} stock clips")
        
        # Here you would call the existing pipeline
        # For now, just log what would be done
        print(f"Would generate video for: {topic}")
        print(f"Stock clips: {stock_clips[:2]}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
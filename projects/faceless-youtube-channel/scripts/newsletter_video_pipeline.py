#!/usr/bin/env python3
"""Create/upload faceless YouTube videos from selected Gmail newsletter messages.

This is intentionally deterministic and source-preserving: it extracts the
newsletter subject/snippet/body, renders a short commentary-style text video,
uploads via the shared YouTube uploader, and only trashes the source Gmail
message after YouTube returns a video ID.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import os
import re
import subprocess
import textwrap
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from creator_links import support_block

ROOT = Path(__file__).resolve().parents[1]
SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'newsletter_youtube_uploads.jsonl'
PROJECT = 'faceless-youtube-newsletters'
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
TOKEN_BASE = Path('/opt/data/google_profiles')


def load_dotenv(path: Path = Path('/opt/data/.env')) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors='ignore').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('\"').strip("'"))


def ai_video_provider_available() -> bool:
    return any(os.getenv(k) for k in ['COMFY_CLOUD_API_KEY','FAL_KEY','FAL_API_KEY','REPLICATE_API_TOKEN','RUNWAY_API_KEY','PIKA_API_KEY','LUMA_API_KEY'])


def elevenlabs_available() -> bool:
    return bool(os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY'))


def sh(cmd: list[str], *, cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout.strip()


def slugify(text: str) -> str:
    return (re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')[:70] or 'newsletter-video')


def gmail_service(profile: str):
    token = TOKEN_BASE / profile / 'google_token.json'
    creds = Credentials.from_authorized_user_file(str(token), scopes=[GMAIL_SCOPE])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token.write_text(creds.to_json())
        os.chmod(token, 0o600)
    return build('gmail', 'v1', credentials=creds, cache_discovery=False)


def header(payload: dict, name: str) -> str:
    for h in payload.get('headers', []):
        if h.get('name', '').lower() == name.lower():
            return h.get('value', '')
    return ''


def decode_part(part: dict) -> str:
    data = part.get('body', {}).get('data')
    if not data:
        return ''
    raw = base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))
    return raw.decode('utf-8', errors='replace')


def walk_parts(part: dict):
    yield part
    for child in part.get('parts', []) or []:
        yield from walk_parts(child)


def text_from_message(msg: dict) -> str:
    payload = msg.get('payload', {})
    texts, htmls = [], []
    for part in walk_parts(payload):
        mime = part.get('mimeType', '')
        body = decode_part(part)
        if not body:
            continue
        if mime == 'text/plain':
            texts.append(body)
        elif mime == 'text/html':
            htmls.append(body)
    text = '\n'.join(texts) if texts else '\n'.join(htmls)
    text = re.sub(r'<(script|style).*?</\1>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'[\u200b\u200c\u200d\ufeff\u034f]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_message(profile: str, msg_id: str) -> dict:
    g = gmail_service(profile)
    msg = g.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg.get('payload', {})
    return {
        'profile': profile,
        'id': msg_id,
        'threadId': msg.get('threadId'),
        'from': header(payload, 'From'),
        'subject': header(payload, 'Subject'),
        'date': header(payload, 'Date'),
        'snippet': msg.get('snippet', ''),
        'body': text_from_message(msg),
    }


def split_subject(subject: str) -> list[str]:
    subject = re.sub(r'[\U00010000-\U0010ffff]', '', subject)
    parts = [p.strip(' -–—|') for p in re.split(r',|\||;|–|—', subject) if p.strip()]
    return parts[:4] or [subject[:80]]


def build_scenes(src: dict) -> list[dict]:
    subject = src['subject']
    parts = split_subject(subject)
    sender = re.sub(r'<.*?>', '', src['from']).strip() or 'newsletter'
    body = src.get('body') or src.get('snippet') or subject
    clean = body[:900]
    if len(clean) > 500:
        # Keep first few complete-ish sentences only.
        sents = re.split(r'(?<=[.!?])\s+', clean)
        clean = ' '.join(sents[:4])[:650]
    main = parts[0]
    second = parts[1] if len(parts) > 1 else 'the hidden systems angle'
    third = parts[2] if len(parts) > 2 else 'what operators should watch next'
    return [
        {'title': 'NEWSLETTER SIGNAL', 'body': f'{sender} flagged this: {main}. The point is not the headline; it is the system changing underneath it.'},
        {'title': 'WHAT CHANGED', 'body': f'{clean}'},
        {'title': 'THE SECOND-ORDER MOVE', 'body': f'{second} matters because infrastructure, payments, AI agents, and attention are starting to merge into one operating layer.'},
        {'title': 'OPERATOR TAKEAWAY', 'body': f'Do not just consume this. Turn it into a reusable asset: a note, a workflow, a prompt, a client offer, or a tiny product experiment.'},
        {'title': 'WATCH NEXT', 'body': f'Watch {third}. If adoption gets easier or cheaper, the opportunity moves from information to execution speed.'},
        {'title': 'TODAY\'S REP', 'body': 'Pick one signal from your inbox. Build one small proof from it before the next newsletter arrives. Subscribe for more operator-grade signal.'},
    ]


def ffmpeg_quote_path(p: Path) -> str:
    return str(p).replace('\\', '/').replace("'", "\\'")


def render_scene(work: Path, idx: int, scene: dict) -> Path:
    scene_dir = work / 'scenes'
    scene_dir.mkdir(exist_ok=True)
    title_file = scene_dir / f'{idx:02d}_title.txt'
    body_file = scene_dir / f'{idx:02d}_body.txt'
    voice_file = scene_dir / f'{idx:02d}_voice.txt'
    audio = scene_dir / f'{idx:02d}.wav'
    video = scene_dir / f'{idx:02d}.mp4'
    title_file.write_text(scene['title'], encoding='utf-8')
    body_file.write_text('\n'.join(textwrap.wrap(scene['body'], width=48)), encoding='utf-8')
    voice_file.write_text(f"{scene['title']}. {scene['body']}", encoding='utf-8')
    sh(['ffmpeg', '-y', '-hide_banner', '-f', 'lavfi', '-i', f'flite=textfile={voice_file}:voice=slt', '-ar', '44100', str(audio)])
    duration = float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(audio)])) + 0.6
    vf = (
        f"drawtext=textfile='{ffmpeg_quote_path(title_file)}':fontcolor=0xF5F5F5:fontsize=70:x=(w-text_w)/2:y=210:font=DejaVuSans-Bold,"
        f"drawtext=textfile='{ffmpeg_quote_path(body_file)}':fontcolor=0xD0D6E0:fontsize=44:x=(w-text_w)/2:y=390:line_spacing=15:font=DejaVuSans,"
        "drawtext=text='NEWSLETTER TO OPERATOR SIGNAL':fontcolor=0x7C8799:fontsize=28:x=70:y=h-90:font=DejaVuSans,"
        f"drawtext=text='{idx:02d}/06':fontcolor=0x7C8799:fontsize=28:x=w-150:y=h-90:font=DejaVuSans"
    )
    sh(['ffmpeg','-y','-hide_banner','-f','lavfi','-i',f'color=c=0x0B0F14:s=1920x1080:d={duration:.2f}','-i',str(audio),'-vf',vf,'-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(video)])
    return video


def render_video(work: Path, scenes: list[dict]) -> Path:
    rendered = [render_scene(work, i, s) for i, s in enumerate(scenes, 1)]
    concat = work / 'concat.txt'
    concat.write_text(''.join(f"file {p.resolve()}\n" for p in rendered), encoding='utf-8')
    out = work / 'final.mp4'
    sh(['ffmpeg','-y','-hide_banner','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(out)])
    return out


def upload(video: Path, title: str, description: str, privacy: str) -> dict:
    output = sh([
        'python3', str(SHARED_UPLOADER), str(video),
        '--title', title[:95],
        '--description', description,
        '--tags', 'self improvement,discipline,motivation,technology,news',
        '--privacy', privacy,
        '--project', PROJECT,
        '--log-jsonl', str(UPLOAD_LOG),
        '--delete-after-upload',
    ])
    text = output.strip()
    marker = text.rfind('{\n  "status"')
    if marker != -1:
        return json.loads(text[marker:])
    return json.loads(text)


def trash_source(profile: str, msg_id: str) -> dict:
    g = gmail_service(profile)
    return g.users().messages().trash(userId='me', id=msg_id).execute()


def main() -> int:
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument('--message', action='append', required=True, help='profile:message_id')
    ap.add_argument('--privacy', choices=['private','unlisted','public'], default='public')
    args = ap.parse_args()
    if not elevenlabs_available() or not ai_video_provider_available():
        missing = []
        if not elevenlabs_available():
            missing.append('ElevenLabs key')
        if not ai_video_provider_available():
            missing.append('AI video/B-roll provider key (Comfy Cloud/Fal/Replicate/Runway/Pika/Luma)')
        raise SystemExit('Refusing to render/upload low-quality static placeholder. Missing: ' + ', '.join(missing))
    results = []
    for spec in args.message:
        profile, msg_id = spec.split(':', 1)
        src = get_message(profile, msg_id)
        stamp = dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')
        work = ROOT / 'videos' / f"{stamp}-{slugify(src['subject'])}"
        work.mkdir(parents=True, exist_ok=True)
        (work / 'source_email.json').write_text(json.dumps({k:v for k,v in src.items() if k != 'body'} | {'body_excerpt': src['body'][:1500]}, indent=2), encoding='utf-8')
        scenes = build_scenes(src)
        (work / 'script.md').write_text('\n\n'.join(f"## {s['title']}\n{s['body']}" for s in scenes), encoding='utf-8')
        video = render_video(work, scenes)
        safe_sender = re.sub(r'<[^>]*>', '', src['from']).strip()
        safe_subject = re.sub(r'[^\x20-\x7E]+', '', src['subject']).strip()
        safe_date = re.sub(r'[^\x20-\x7E]+', '', src['date']).strip()
        title = re.sub(r'[^\x20-\x7E]+', '', f"Inbox Signal: {split_subject(src['subject'])[0]}")[:95]
        description = f"{safe_subject}\n\nMy read on this: don't just collect the headline. Take the useful signal, build one proof from it, and move before everyone else calls it obvious.{support_block()}"
        up = upload(video, title, description, args.privacy)
        trashed = None
        if up.get('video_id'):
            trashed = trash_source(profile, msg_id)
        result = {'source': {k: src[k] for k in ['profile','id','from','subject','date']}, 'workspace': str(work), 'upload': up, 'source_email_trashed_after_verified_upload': bool(trashed), 'trash_result_id': (trashed or {}).get('id')}
        (work / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        results.append(result)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

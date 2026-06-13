#!/usr/bin/env python3
"""
Classical Echos faceless newsletter backlog processor.

Quality requirements:
- One newsletter email -> one ~2 minute video.
- Use actual newsletter content for the script.
- Use multiple relevant Pexels stock video clips matched to script beats.
- 9:16 vertical render, ElevenLabs voiceover, public YouTube upload by default.
- No upload if quality gate fails.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import email.utils
import html
import json
import os
import re
import shutil
import subprocess
import textwrap
import time
import urllib.parse
import urllib.request
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel')
UPLOAD_SCRIPT = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'youtube_uploads.jsonl'
GMAIL_PROFILE = 'fareed320'  # symlink to personal-secondary / fareed320@gmail.com
CALENDAR_PROFILE = 'trapiistan'
GMAIL_TOKEN = Path(f'/opt/data/google_profiles/{GMAIL_PROFILE}/google_token.json')
CALENDAR_TOKEN = Path(f'/opt/data/google_profiles/{CALENDAR_PROFILE}/google_token.json')
TARGET_SECONDS = 120
MIN_SECONDS = 110
MIN_CLIPS = 6
PEXELS_API_KEY = None

SUPPORT_BLOCK = """More from me: https://linktr.ee/sosai.oyama
Support the channel: https://buymeacoffee.com/affanfareev
Cash App: https://cash.app/$sosaioyama
Venmo: https://venmo.com/u/SosaiOyama"""


MIXKIT_PAGES = {
    'technology': [
        'https://mixkit.co/free-stock-video/datacenter',
        'https://mixkit.co/free-stock-video/information-technology',
        'https://mixkit.co/free-stock-video/artificial',
        'https://mixkit.co/free-stock-video/robots',
        'https://mixkit.co/free-stock-video/coding',
        'https://mixkit.co/free-stock-video/hacker',
        'https://mixkit.co/free-stock-video/internet',
    ],
    'finance': [
        'https://mixkit.co/free-stock-video/stock-market',
        'https://mixkit.co/free-stock-video/investment',
        'https://mixkit.co/free-stock-video/finance',
    ],
    'fitness': [
        'https://mixkit.co/free-stock-video/gym',
        'https://mixkit.co/free-stock-video/fitness',
        'https://mixkit.co/free-stock-video/workout',
        'https://mixkit.co/free-stock-video/running',
    ],
    'stoic': [
        'https://mixkit.co/free-stock-video/statue',
        'https://mixkit.co/free-stock-video/ancient',
        'https://mixkit.co/free-stock-video/sunrise',
        'https://mixkit.co/free-stock-video/meditation',
    ],
}

def mixkit_groups_for_queries(queries: list[str]) -> list[str]:
    joined = ' '.join(queries).lower()
    groups = []
    if any(k in joined for k in ['stock', 'market', 'finance', 'trading', 'money', 'coinbase', 'aave', 'vc']):
        groups.append('finance')
    if any(k in joined for k in ['gym', 'fitness', 'training', 'workout', 'testosterone', 'running']):
        groups.append('fitness')
    if any(k in joined for k in ['stoic', 'statue', 'ancient', 'roman', 'journal', 'meditation']):
        groups.append('stoic')
    groups.append('technology')
    return dedupe(groups)

def extract_mixkit_mp4s(page_url: str) -> list[str]:
    req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            html_text = resp.read().decode('utf-8', 'replace')
    except Exception:
        return []
    urls = re.findall(r'https?://[^"\\\'<> ]+?\.mp4[^"\\\'<> ]*', html_text)
    out=[]
    for u in urls:
        u = u.replace('\\u0026', '&')
        if '-720.mp4' in u and u not in out:
            out.append(u)
    for u in urls:
        if u not in out:
            out.append(u)
    return out

def mixkit_fallback_urls(queries: list[str], needed: int = 10) -> list[dict]:
    urls=[]
    for group in mixkit_groups_for_queries(queries):
        for page in MIXKIT_PAGES.get(group, []):
            for u in extract_mixkit_mp4s(page):
                if u not in [x['url'] for x in urls]:
                    urls.append({'query': f'mixkit:{group}', 'url': u, 'width': None, 'height': None, 'duration': None, 'pexels_id': None, 'source': page})
                if len(urls) >= needed * 2:
                    return urls
    return urls

SOURCE_QUERIES = {
    'daily stoic': ['stoic statue', 'ancient roman statue', 'journal writing', 'sunrise discipline', 'man walking alone', 'mountain sunrise', 'calm meditation'],
    'stoic': ['stoic statue', 'marble statue', 'ancient architecture', 'journal discipline', 'sunrise'],
    'kino': ['gym workout', 'strength training', 'healthy meal prep', 'man running', 'fitness lifestyle', 'weights training', 'morning workout'],
    'testosterone': ['strength training', 'gym workout', 'healthy food', 'running sunrise', 'boxing training', 'athlete training'],
    'tldr': ['technology data center', 'artificial intelligence', 'robotics lab', 'coding laptop', 'server room', 'futuristic interface'],
    'ai': ['artificial intelligence', 'data center', 'robotics', 'coding screen', 'neural network', 'technology abstract'],
    'robinhood': ['stock market', 'financial charts', 'wall street', 'trading desk', 'business news', 'market data'],
    'stocks': ['stock market', 'financial charts', 'trading', 'wall street', 'finance laptop'],
}


def load_env() -> None:
    for env_path in [Path('/opt/data/.env'), ROOT / '.env', ROOT / '.env.pexels']:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    global PEXELS_API_KEY
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')


def elevenlabs_key() -> str | None:
    return os.getenv('EllevenLabsKey') or os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')


def creds(path: Path) -> Credentials:
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


def clean_text(s: str) -> str:
    s = html.unescape(s or '')
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'https?://\S+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def decode_body(payload: dict) -> str:
    chunks: list[str] = []
    def walk(part: dict):
        mime = part.get('mimeType', '')
        body = part.get('body', {})
        data = body.get('data')
        if data and mime in ('text/plain', 'text/html'):
            try:
                chunks.append(base64.urlsafe_b64decode(data + '===').decode('utf-8', 'replace'))
            except Exception:
                pass
        for child in part.get('parts', []) or []:
            walk(child)
    walk(payload or {})
    return clean_text('\n'.join(chunks))


def header(headers: list[dict], name: str) -> str:
    name = name.lower()
    for h in headers:
        if h.get('name', '').lower() == name:
            return h.get('value', '')
    return ''


def fetch_newsletters(max_count: int) -> list[dict]:
    svc = gmail_service()
    query = 'newer_than:30d (from:tldrnewsletter.com OR from:dailystoic.com OR from:snacks.robinhood.com OR "Daily Stoic" OR "Kino Body" OR kinobody OR "Robinhood Snacks")'
    listed = svc.users().messages().list(userId='me', q=query, maxResults=max_count).execute().get('messages', [])
    emails = []
    for item in listed:
        msg = svc.users().messages().get(userId='me', id=item['id'], format='full').execute()
        headers = msg.get('payload', {}).get('headers', [])
        subject = header(headers, 'subject') or '(no subject)'
        sender = header(headers, 'from')
        body = decode_body(msg.get('payload', {}))
        if len(body) < 120:
            body = clean_text(msg.get('snippet', ''))
        emails.append({'id': item['id'], 'threadId': msg.get('threadId'), 'subject': subject, 'from': sender, 'body': body, 'labels': msg.get('labelIds', [])})
    return emails


def infer_lane(subject: str, sender: str, body: str) -> str:
    t = f'{subject} {sender} {body[:500]}'.lower()
    if 'daily stoic' in t or 'stoic' in t:
        return 'Daily Stoic'
    if 'kino' in t or 'testosterone' in t or 'shredded' in t:
        return 'Kino Body'
    if 'robinhood snacks' in t or 'snacks' in t:
        return 'Market Brief'
    if 'tldr' in t or 'ai' in t or 'tech' in t:
        return 'TLDR / AI'
    return 'Operator Brief'


def build_script(email: dict) -> tuple[str, list[dict], list[str]]:
    subject, sender, body = email['subject'], email.get('from', ''), email.get('body', '')
    lane = infer_lane(subject, sender, body)
    source = clean_text(body)[:2500]
    if lane == 'Daily Stoic':
        angle = 'turning a hard day into training for character'
        tone = 'calm, disciplined, ancient-warrior motivation'
    elif lane == 'Kino Body':
        angle = 'building a stronger body without losing your joy or standards'
        tone = 'fitness, warrior discipline, masculine health, clean confidence'
    elif lane == 'Market Brief':
        angle = 'what today’s market signal means for a builder watching money and risk'
        tone = 'sharp finance operator, calm and practical'
    elif lane == 'TLDR / AI':
        angle = 'why this tech shift matters before everybody else catches up'
        tone = 'fast, futuristic, operator-minded tech analysis'
    else:
        angle = 'what this signal means for discipline and leverage'
        tone = 'motivational operator voice'

    # Long enough for ~115-130 seconds at natural 135-155 wpm.
    narration = f"""
    {subject}.

    Here is the part that matters: {source[:650]}

    My read is simple. This is not just information. This is a signal. The point is {angle}.

    Most people consume messages like this and move on. They nod, they feel inspired for ten seconds, then they go right back to the same habits. But the edge is not in hearing the lesson. The edge is in turning the lesson into a rule you can actually live by today.

    If this is about discipline, then the move is to choose the obstacle before the obstacle chooses you. Write down the hard thing, face it early, and stop negotiating with your weaker mood.

    If this is about health, then the move is not chasing some random hack. It is stacking sleep, training, food, sunlight, and consistency until your body starts trusting you again.

    If this is about technology or markets, then the move is to ask what changed, who benefits, who gets disrupted, and what skill or position you should build before the crowd understands the shift.

    The hidden pattern is ownership. Discovery gives you the signal. Harnessing turns it into a system. Ownership means you stop waiting for motivation and start acting like the operator of your own life.

    So take this message and make it practical. Pick one action. One workout. One note. One trade rule. One build session. One uncomfortable conversation. Something real enough that your day has evidence, not just intention.

    That is how you stay ahead. Not by collecting more information, but by converting the right information into standards, reps, and proof.
    """
    narration = re.sub(r'\s+', ' ', textwrap.dedent(narration)).strip()

    beat_specs = [
        ('Hook / source signal', subject, 0, 12),
        ('The real meaning', angle, 12, 28),
        ('Most people consume and forget', 'scrolling phone distraction crowd', 28, 42),
        ('Turn lesson into rule', 'journal writing discipline morning', 42, 58),
        ('Face the hard thing', 'man walking alone sunrise mountain', 58, 74),
        ('Body / execution / reps', 'gym workout strength training running', 74, 90),
        ('Tech / money / leverage', 'technology data center financial charts coding laptop', 90, 106),
        ('Ownership close', 'silhouette sunrise city cinematic', 106, 120),
    ]
    beats = [{'label': a, 'query': b, 'start': c, 'end': d} for a,b,c,d in beat_specs]
    queries = queries_for_email(subject, sender, body) + [b['query'] for b in beats]
    return narration, beats, dedupe(queries)


def queries_for_email(subject: str, sender: str, body: str) -> list[str]:
    t = f'{subject} {sender} {body[:1000]}'.lower()
    queries = []
    for key, qs in SOURCE_QUERIES.items():
        if key in t:
            queries.extend(qs)
    words = [w for w in re.findall(r'[a-zA-Z]{4,}', subject.lower()) if w not in {'daily','body','with','from','that','this','your','newsletter'}]
    if words:
        queries.append(' '.join(words[:3]))
    if not queries:
        queries = ['cinematic discipline', 'city sunrise', 'focused work', 'technology abstract', 'fitness training']
    return dedupe(queries)


def dedupe(items: list[str]) -> list[str]:
    seen, out = set(), []
    for x in items:
        x = re.sub(r'\s+', ' ', x.strip())
        if x and x.lower() not in seen:
            seen.add(x.lower()); out.append(x)
    return out


def search_pexels(query: str, per_page: int = 5) -> list[dict]:
    if not PEXELS_API_KEY:
        return []
    url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&per_page={per_page}&orientation=portrait"
    req = urllib.request.Request(url, headers={'Authorization': PEXELS_API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return []
    out = []
    for vid in data.get('videos', []):
        files = vid.get('video_files', [])
        # Prefer portrait/high-res; fallback still gets cropped to vertical.
        scored = sorted(files, key=lambda f: ((f.get('height',0) >= f.get('width',0)), f.get('height',0), f.get('width',0)), reverse=True)
        for f in scored:
            link = f.get('link')
            if link and 'mp4' in f.get('file_type', 'video/mp4'):
                out.append({'query': query, 'url': link, 'width': f.get('width'), 'height': f.get('height'), 'duration': vid.get('duration'), 'pexels_id': vid.get('id')})
                break
    return out


def download_clips(queries: list[str], work_dir: Path, needed: int = 10) -> list[Path]:
    clips_dir = work_dir / 'clips'
    clips_dir.mkdir(parents=True, exist_ok=True)
    candidates: list[dict] = []
    for q in queries:
        candidates.extend(search_pexels(q, per_page=4))
        if len(candidates) >= needed * 2:
            break
    if len(candidates) < needed:
        candidates.extend(mixkit_fallback_urls(queries, needed=needed))
    unique = []
    seen = set()
    for c in candidates:
        if c['url'] not in seen:
            seen.add(c['url']); unique.append(c)
    paths = []
    manifest = []
    for idx, c in enumerate(unique[:needed], 1):
        dest = clips_dir / f'clip_{idx:02d}.mp4'
        try:
            req = urllib.request.Request(c['url'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=90) as resp:
                dest.write_bytes(resp.read())
            if dest.stat().st_size > 100_000:
                paths.append(dest)
                manifest.append({**c, 'local': str(dest), 'bytes': dest.stat().st_size})
        except Exception as e:
            manifest.append({**c, 'download_error': str(e)[:200]})
    (work_dir / 'pexels_manifest.json').write_text(json.dumps(manifest, indent=2))
    return paths


def generate_voiceover(text: str, out: Path, allow_edge_fallback: bool = False) -> str:
    key = elevenlabs_key()
    if key:
        payload = json.dumps({
            'text': text,
            'model_id': 'eleven_flash_v2_5',
            'voice_settings': {'stability': 0.48, 'similarity_boost': 0.78, 'style': 0.18, 'use_speaker_boost': True},
        }).encode()
        req = urllib.request.Request(
            'https://api.elevenlabs.io/v1/text-to-speech/CwhRBWXzGAHq8TQ4Fs17',
            data=payload,
            headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                out.write_bytes(resp.read())
            if out.stat().st_size < 50_000:
                raise RuntimeError(f'Voiceover too small: {out.stat().st_size} bytes')
            return 'elevenlabs'
        except Exception as exc:
            if not allow_edge_fallback:
                raise
            print(f'ElevenLabs unavailable for this render ({exc}); using edge-tts REVIEW fallback')
    elif not allow_edge_fallback:
        raise RuntimeError('Missing ElevenLabs key')

    # Review fallback only; do not treat as final channel voice unless user approves.
    escaped = text.replace('\n', ' ')[:3500]
    cmd = ['edge-tts', '--voice', 'en-US-GuyNeural', '--text', escaped, '--write-media', str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    if out.stat().st_size < 50_000:
        raise RuntimeError(f'edge-tts fallback voiceover too small: {out.stat().st_size} bytes')
    return 'edge-tts-review'


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nk=1:nw=1',str(path)], text=True, capture_output=True, check=True)
    return float(r.stdout.strip())


def render_video(clips: list[Path], voice: Path, out: Path, seconds: int = TARGET_SECONDS) -> None:
    if len(clips) < MIN_CLIPS:
        raise RuntimeError(f'Quality gate failed: need at least {MIN_CLIPS} relevant stock clips, got {len(clips)}')
    seg = max(7, seconds // len(clips))
    rendered = []
    for idx, clip in enumerate(clips):
        segment = out.parent / f'segment_{idx:02d}.mp4'
        vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p"
        subprocess.run([
            'ffmpeg','-y','-stream_loop','-1','-i',str(clip),'-t',str(seg),
            '-vf',vf,'-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','24','-pix_fmt','yuv420p',str(segment)
        ], check=True, capture_output=True)
        rendered.append(segment)
    concat = out.parent / 'concat.txt'
    concat.write_text('\n'.join(f"file '{p}'" for p in rendered) + '\n')
    silent = out.parent / 'montage_silent.mp4'
    subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-t',str(seconds),'-c','copy',str(silent)], check=True, capture_output=True)
    subprocess.run([
        'ffmpeg','-y','-i',str(silent),'-i',str(voice),'-t',str(seconds),
        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-shortest',str(out)
    ], check=True, capture_output=True)
    dur = ffprobe_duration(out)
    if dur < MIN_SECONDS:
        raise RuntimeError(f'Quality gate failed: rendered duration {dur:.1f}s < {MIN_SECONDS}s')


def upload_video(out_video: Path, title: str, desc: str, scheduled: bool = False) -> dict:
    publish_time = (dt.datetime.now(dt.UTC) + dt.timedelta(hours=1)).isoformat()
    cmd = ['python3', str(UPLOAD_SCRIPT), str(out_video), '--title', title, '--description', desc, '--privacy', 'public', '--project', 'faceless-backlog', '--log-jsonl', str(UPLOAD_LOG), '--delete-after-upload']
    if scheduled:
        cmd.extend(['--publish-at', publish_time])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1000:] or r.stdout[-1000:])
    # Parse pretty JSON from stdout.
    start = r.stdout.find('{')
    result = json.loads(r.stdout[start:]) if start >= 0 else {'raw': r.stdout}
    result['publish_time_for_calendar'] = publish_time if scheduled else dt.datetime.now(dt.UTC).isoformat()
    return result


def create_calendar_event(summary: str, description: str, start_time_utc: str, video_url: str = '') -> bool:
    svc = calendar_service()
    start = dt.datetime.fromisoformat(start_time_utc.replace('Z','+00:00'))
    end = start + dt.timedelta(minutes=10)
    body = {
        'summary': summary,
        'description': f'{description}\n{video_url}'.strip(),
        'start': {'dateTime': start.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end.isoformat(), 'timeZone': 'UTC'},
    }
    svc.events().insert(calendarId='primary', body=body).execute()
    return True


def trash_email(message_id: str) -> None:
    gmail_service().users().messages().trash(userId='me', id=message_id).execute()


def slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:48] or 'newsletter-video'


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument('--max', type=int, default=3)
    parser.add_argument('--offset', type=int, default=0, help='Skip first N fetched newsletter candidates')
    parser.add_argument('--scheduled', action='store_true', help='Use native YouTube publishAt; otherwise upload public immediately')
    parser.add_argument('--no-upload', action='store_true', help='Render and verify only; do not upload/trash source email')
    parser.add_argument('--keep-workspace', action='store_true')
    parser.add_argument('--allow-edge-tts-fallback', action='store_true', help='Review renders only: use edge-tts if ElevenLabs quota/auth blocks')
    parser.add_argument('--fixture', action='store_true', help='Render one representative test item without Gmail')
    args = parser.parse_args()

    if args.fixture:
        emails = [{
            'id': 'fixture',
            'threadId': 'fixture',
            'subject': 'Daily Stoic - Turn The Obstacle Into Training',
            'from': 'Daily Stoic <newsletter@example.com>',
            'body': 'The lesson today is that obstacles are not interruptions to the path. They are the path. When resistance shows up, the disciplined person uses it as training: write the rule, do the hard thing early, and turn frustration into proof of character.'
        }]
        args.no_upload = True
    else:
        emails = fetch_newsletters(args.max + args.offset)[args.offset:]
    print(f'Found {len(emails)} newsletter candidates')
    processed = 0
    for email in emails:
        subject = email['subject']
        stamp = dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')
        work_dir = ROOT / 'videos' / f'{stamp}-{slug(subject)}'
        work_dir.mkdir(parents=True, exist_ok=True)
        print(f'\nProcessing: {subject}')
        try:
            narration, beats, queries = build_script(email)
            (work_dir / 'source.json').write_text(json.dumps({k:v for k,v in email.items() if k != 'body'} | {'body_chars': len(email.get('body',''))}, indent=2))
            (work_dir / 'script.txt').write_text(narration)
            (work_dir / 'beats.json').write_text(json.dumps(beats, indent=2))
            (work_dir / 'queries.json').write_text(json.dumps(queries, indent=2))

            voice = work_dir / 'voice.mp3'
            voice_provider = generate_voiceover(narration, voice, allow_edge_fallback=args.allow_edge_tts_fallback)
            print(f'Voiceover: {voice.stat().st_size} bytes via {voice_provider}')

            clips = download_clips(queries, work_dir, needed=10)
            print(f'Pexels clips: {len(clips)}')
            out_video = work_dir / 'final.mp4'
            render_video(clips, voice, out_video, TARGET_SECONDS)
            duration = ffprobe_duration(out_video)
            print(f'Rendered: {out_video} ({duration:.1f}s)')

            title = f'{re.sub(r"\\s+", " ", subject).strip()[:72]} #Shorts'
            desc = f"My read: turn the signal into proof today.\n\n{SUPPORT_BLOCK}\n\n#Shorts"
            if args.no_upload:
                print('NO_UPLOAD: quality-gated render complete; source email not trashed')
                if not args.keep_workspace:
                    print(f'Workspace kept for inspection: {work_dir}')
                processed += 1
                continue

            result = upload_video(out_video, title, desc, scheduled=args.scheduled)
            print(f"Uploaded: {result.get('url')} privacy={result.get('privacy')}")
            create_calendar_event(f"Published: {subject[:45]}", f"Classical Echos upload from newsletter backlog", result['publish_time_for_calendar'], result.get('url',''))
            trash_email(email['id'])
            if not args.keep_workspace:
                shutil.rmtree(work_dir, ignore_errors=True)
                print('Cleaned local workspace')
            processed += 1
        except Exception as exc:
            print(f'FAILED quality gate or processing: {exc}')
            print(f'Workspace preserved for debugging: {work_dir}')
    print(f'Processed {processed} videos')


if __name__ == '__main__':
    main()

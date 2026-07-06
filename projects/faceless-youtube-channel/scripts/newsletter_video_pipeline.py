#!/usr/bin/env python3
"""
Modified faceless YouTube pipeline to use Pexels for stock footage instead of Sora.
Processes newsletter topics and generates videos using Pexels API for B-roll.
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

# Configuration
ROOT = Path('/opt/data/HeRmEz/projects/faceless-youtube-channel')
SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'newsletter_youtube_uploads.jsonl'
PROJECT = 'faceless-youtube-newsletters'
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
TOKEN_BASE = Path('/opt/data/google_profiles')
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

def sh(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout.strip()

def slugify(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')[:70] or 'faceless-video'

def elevenlabs_key() -> str | None:
    return os.getenv('EllevenLabsKey') or os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')

def pexels_available() -> bool:
    return bool(PEXELS_API_KEY)

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
    
    parser = argparse.ArgumentParser(description='Generate faceless videos from newsletter topics')
    parser.add_argument('--topic', required=True, help='Topic or headline to base video on')
    parser.add_argument('--profile', default='fareed320', help='Gmail profile to use')
    parser.add_argument('--max', type=int, default=1, help='Max number of videos to generate')
    parser.add_argument('--dry-run', action='store_true', help='Dry run without actual generation')
    args = parser.parse_args()
    
    print(f"🔧 Processing topic: '{args.topic}'")
    
    # Extract keywords for stock footage search
    keywords = re.findall(r'\b\w+\b', args.topic.lower())[:3]
    print(f"🔎 Keywords for stock search: {keywords}")
    
    all_clips = []
    for kw in keywords:
        clips = search_pexels_videos(kw, per_page=2)
        all_clips.extend(clips)
        print(f"📹 Found {len(clips)} clips for '{kw}': {clips[:1]}")
    
    if not all_clips:
        print("⚠️  No stock clips found - continuing with placeholder visuals")
    
    # Generate script content
    script_lines = [
        "# Generated script from newsletter topic",
        "",
        "## Title Sequence",
        "This video explores how to turn everyday challenges into opportunities for growth.",
        "",
        "## Main Body",
        "The core principle is that disciplined action creates momentum, even when motivation fades.",
        "",
        "## Call to Action",
        "Take one small action today that aligns with your long-term goals."
    ]
    
    # Create workspace
    stamp = dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')
    work_dir = ROOT / f"videos/{stamp}-{slugify(args.topic)}"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # Save script
    (work_dir / 'script.md').write_text('\n'.join(script_lines), encoding='utf-8')
    
    # Generate voiceover
    voice_file = work_dir / 'voice.wav'
    spoken_text = "Today we discuss turning challenges into opportunities for growth."
    # Use elevenlabs to generate speech
    def generate_speech(text, out_path):
        key = elevenlabs_key()
        if not key:
            print("❌ No ElevenLabs key found")
            return False
        import urllib.request, json
        payload = json.dumps({
            "text": text,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {"stability": 0.42, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{os.getenv('ELEVENLABS_VOICE_ID', 'CwhRBWXzGAHq8TQ4Fs17')}",
            data=payload,
            headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"}
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                out_path.write_bytes(resp.read())
            return out_path.exists() and out_path.stat().st_size > 1000
        except Exception as e:
            print(f"ElevenLabs error: {e}")
            return False
    
    generate_speech(spoken_text, voice_file)
    
    # If we have stock clips, download them
    downloaded_clips = []
    for clip_url in all_clips:
        try:
            clip_path = work_dir / Path(clip_url).name
            sh(['curl', '-sSL', '-o', str(clip_path), clip_url])
            downloaded_clips.append(str(clip_path))
        except Exception as e:
            print(f"Failed to download clip {clip_url}: {e}")
    
    # Render final video using ffmpeg (simplified single clip + audio)
    if downloaded_clips:
        # Simple concat of first clip with audio
        concat_txt = work_dir / 'concat.txt'
        with open(concat_txt, 'w') as f:
            f.write(f"file '{downloaded_clips[0]}'\n")
            f.write(f"file '{voice_file}'\n")
        out_video = work_dir / 'final.mp4'
        sh([
            'ffmpeg', '-y', '-i', str(downloaded_clips[0]), '-i', str(voice_file),
            '-c', 'copy', str(out_video)
        ])
        print(f"✅ Generated video: {out_video}")
    else:
        # Fallback: use only voice with static image
        print("⚠️  No clips downloaded, generating static video with voiceover only")
        # Placeholder 1080x1920 black screen
        placeholder = work_dir / 'placeholder.mp4'
        sh([
            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=30',
            '-i', str(voice_file), '-c', 'copy', str(placeholder)
        ])
        out_video = placeholder
        print(f"✅ Generated placeholder video: {out_video}")
    
    # If not dry-run, upload
    if not args.dry_run:
        title = f"{args.topic[:50]}... #Shorts"
        description = "My read on this topic:\n\nTurn challenges into opportunities. Build one proof today.\n\n#Shorts"
        upload_cmd = [
            'python3', str(SHARED_UPLOADER), str(out_video),
            '--title', title,
            '--description', description,
            '--tags', 'discipline,self improvement,motivation,shorts',
            '--privacy', 'public',
            '--token', '/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json',
            '--expect-channel-id', 'UCsxzQlusqwmMUdjMvKAJDfA',
            '--project', PROJECT,
            '--log-jsonl', str(UPLOAD_LOG),
            '--delete-after-upload'
        ]
        print(f"📤 Uploading video: {out_video}")
        try:
            upload_result = subprocess.run(upload_cmd, capture_output=True, text=True)
            print(f"Upload exit code: {upload_result.returncode}")
            print("Upload output:", upload_result.stdout[:200])
            if upload_result.returncode == 0:
                print("✅ Upload successful")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
    
    print("🏁 Processing complete")

if __name__ == '__main__':
    main()
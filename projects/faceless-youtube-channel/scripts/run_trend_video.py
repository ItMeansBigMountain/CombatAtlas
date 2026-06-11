#!/usr/bin/env python3
"""One-command faceless trend-to-video pipeline.

Creates a short discipline/self-improvement faceless video from a trend/topic,
renders kinetic text slides with FFmpeg + flite TTS, and optionally uploads to
YouTube as private through the shared HeRmEz uploader.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import textwrap
import shutil
import urllib.request
from pathlib import Path

PROJECT = 'faceless-youtube-channel'
ROOT = Path(__file__).resolve().parents[1]
SHARED_UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'youtube_uploads.jsonl'


def sh(cmd: list[str], *, cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout.strip()


def slugify(text: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')
    return s[:70] or 'trend-video'


def fetch_hn_trend() -> dict:
    url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10'
    try:
        with urllib.request.urlopen(url, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        hits = data.get('hits') or []
        for hit in hits:
            title = hit.get('title') or hit.get('story_title')
            if title:
                return {
                    'source': 'Hacker News front page',
                    'title': title,
                    'url': hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    'points': hit.get('points'),
                    'comments': hit.get('num_comments'),
                }
    except Exception as exc:
        return {'source': 'fallback', 'title': 'AI distraction is training people to avoid hard work', 'url': '', 'error': str(exc)}
    return {'source': 'fallback', 'title': 'AI distraction is training people to avoid hard work', 'url': ''}


def build_script(topic: str, source: dict) -> list[dict]:
    trend = source.get('title') or topic
    return [
        {
            'title': 'THE TREND IS NOT THE POINT',
            'body': f"Today everybody is reacting to: {trend}. But the real lesson is not the headline. It is what your attention does after the headline grabs you.",
        },
        {
            'title': 'ATTENTION IS A BANK ACCOUNT',
            'body': 'Every scroll is a withdrawal. Every focused block is a deposit. Most men are not broke because they lack ideas. They are broke because their attention leaks all day.',
        },
        {
            'title': 'DISCIPLINE IS BORING ON PURPOSE',
            'body': 'The boring reps are the filter. Ten minutes of planning. One clean meal. One uncomfortable workout. One application. One page. That is how a chaotic life gets rebuilt.',
        },
        {
            'title': 'USE THE TREND, DO NOT BECOME IT',
            'body': 'Read the trend. Extract the lesson. Then leave. If the internet gives you a signal, turn it into an action before it turns into another hour of consumption.',
        },
        {
            'title': 'TODAY\'S MOVE',
            'body': 'Pick one thing you have been avoiding. Set a fifteen minute timer. No music hunting. No perfect setup. Start ugly and finish the rep.',
        },
        {
            'title': 'PRIVATE STANDARD',
            'body': 'Nobody needs to clap for the first version. The standard is simple: produce before you consume. Repeat until your life has evidence.',
        },
    ]


def write_script_md(path: Path, scenes: list[dict], source: dict) -> None:
    lines = ['# Video Script', '', f"Source: {source.get('source','manual')}", f"Trend: {source.get('title','')}", f"URL: {source.get('url','')}", '']
    for i, scene in enumerate(scenes, 1):
        lines += [f"## Scene {i}: {scene['title']}", '', scene['body'], '']
    path.write_text('\n'.join(lines), encoding='utf-8')


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
    duration = float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', str(audio)]))
    duration += 0.6

    vf = (
        f"drawtext=textfile='{ffmpeg_quote_path(title_file)}':fontcolor=0xF5F5F5:fontsize=72:"
        "x=(w-text_w)/2:y=220:font=DejaVuSans-Bold,"
        f"drawtext=textfile='{ffmpeg_quote_path(body_file)}':fontcolor=0xD0D6E0:fontsize=46:"
        "x=(w-text_w)/2:y=410:line_spacing=16:font=DejaVuSans,"
        "drawtext=text='FACELESS DISCIPLINE SYSTEM':fontcolor=0x7C8799:fontsize=28:x=70:y=h-90:font=DejaVuSans,"
        f"drawtext=text='{idx:02d}/06':fontcolor=0x7C8799:fontsize=28:x=w-150:y=h-90:font=DejaVuSans"
    )
    sh([
        'ffmpeg', '-y', '-hide_banner',
        '-f', 'lavfi', '-i', f'color=c=0x0B0F14:s=1920x1080:d={duration:.2f}',
        '-i', str(audio),
        '-vf', vf,
        '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', str(video)
    ])
    return video


def render_video(work: Path, scenes: list[dict]) -> Path:
    rendered = [render_scene(work, i, scene) for i, scene in enumerate(scenes, 1)]
    concat = work / 'concat.txt'
    concat.write_text(''.join(f"file {p.resolve()}\n" for p in rendered), encoding='utf-8')
    out = work / 'final.mp4'
    sh(['ffmpeg', '-y', '-hide_banner', '-f', 'concat', '-safe', '0', '-i', str(concat), '-c', 'copy', str(out)])
    sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'json', str(out)])
    return out


def upload(video: Path, title: str, description: str, tags: str, dry_run: bool) -> dict:
    cmd = [
        'python3', str(SHARED_UPLOADER), str(video),
        '--title', title,
        '--description', description,
        '--tags', tags,
        '--privacy', 'public',
        '--project', PROJECT,
        '--log-jsonl', str(UPLOAD_LOG),
        '--delete-after-upload',
    ]
    if dry_run:
        cmd.append('--dry-run')
    output = sh(cmd)
    try:
        return json.loads(output)
    except Exception:
        return {'raw': output}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--topic', default='')
    p.add_argument('--upload', action='store_true', help='Upload private to YouTube after rendering')
    p.add_argument('--dry-run-upload', action='store_true')
    args = p.parse_args()

    source = {'source': 'manual', 'title': args.topic, 'url': ''} if args.topic else fetch_hn_trend()
    topic = args.topic or source['title']
    stamp = dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')
    work = ROOT / 'videos' / f"{stamp}-{slugify(topic)}"
    work.mkdir(parents=True, exist_ok=True)

    scenes = build_script(topic, source)
    write_script_md(work / 'script.md', scenes, source)
    (work / 'source.json').write_text(json.dumps(source, indent=2), encoding='utf-8')
    video = render_video(work, scenes)

    title = 'Stop Letting Trends Steal Your Discipline'
    description = (
        'Private faceless automation pilot. Built from a live trend signal and reframed as a discipline/self-improvement lesson.\n\n'
        f"Source signal: {source.get('title','manual')}\n{source.get('url','')}"
    )
    result = {'workspace': str(work), 'video': str(video), 'uploaded': False}
    if args.upload or args.dry_run_upload:
        result['upload'] = upload(video, title, description, 'discipline,self improvement,faceless youtube,focus', args.dry_run_upload)
        result['uploaded'] = not args.dry_run_upload
        if args.upload and not args.dry_run_upload:
            shutil.rmtree(work, ignore_errors=True)
            result['workspace_deleted_after_upload'] = str(work)
    if work.exists():
        (work / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

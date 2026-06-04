#!/usr/bin/env python3
"""Render a simple narrated text video with FFmpeg flite + drawtext."""
from __future__ import annotations

import argparse
import json
import subprocess
import textwrap
from pathlib import Path


def sh(cmd: list[str]) -> str:
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--body', required=True)
    ap.add_argument('--footer', default='PRIVATE REVIEW DRAFT')
    ap.add_argument('--size', default='1080x1920')
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / (out.stem + '_render')
    work.mkdir(exist_ok=True)
    title_file = work / 'title.txt'
    body_file = work / 'body.txt'
    voice_file = work / 'voice.txt'
    audio = work / 'voice.wav'
    title_file.write_text(args.title, encoding='utf-8')
    width = 30 if args.size.startswith('1080x1920') else 48
    body_file.write_text('\n'.join(textwrap.wrap(args.body, width=width)), encoding='utf-8')
    voice_file.write_text(args.title + '. ' + args.body, encoding='utf-8')
    sh(['ffmpeg','-y','-hide_banner','-f','lavfi','-i',f'flite=textfile={voice_file}:voice=slt','-ar','44100',str(audio)])
    duration = float(sh(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)])) + 1.0
    vf = (
        f"drawtext=textfile='{title_file}':fontcolor=0xF5F5F5:fontsize=58:x=(w-text_w)/2:y=260:font=DejaVuSans-Bold,"
        f"drawtext=textfile='{body_file}':fontcolor=0xD0D6E0:fontsize=42:x=(w-text_w)/2:y=560:line_spacing=18:font=DejaVuSans,"
        f"drawtext=text='{args.footer}':fontcolor=0x7C8799:fontsize=26:x=(w-text_w)/2:y=h-170:font=DejaVuSans"
    )
    sh(['ffmpeg','-y','-hide_banner','-f','lavfi','-i',f'color=c=0x0B0F14:s={args.size}:d={duration:.2f}','-i',str(audio),'-vf',vf,'-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(out)])
    meta = json.loads(sh(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(out)]))
    print(json.dumps({'out': str(out), 'meta': meta}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

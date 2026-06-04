#!/usr/bin/env python3
"""Faceless channel: better voice + real graphic scenes + private upload + cleanup.

Uses ElevenLabs when ELEVENLABS_API_KEY is available in env or /opt/data/.env.
Renders vertical Shorts-style kinetic scenes with diagram/B-roll style graphics.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import textwrap
import urllib.request
from pathlib import Path

PROJECT = "faceless-youtube-channel"
ROOT = Path(__file__).resolve().parents[1]
SHARED_UPLOADER = Path("/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py")
UPLOAD_LOG = ROOT / "UPLOADS" / "youtube_uploads.jsonl"
DEFAULT_VOICE = os.getenv("ELEVENLABS_VOICE_ID") or "21m00Tcm4TlvDq8ikWAM"  # Rachel


def load_dotenv(path: Path = Path("/opt/data/.env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def sh(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout.strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")[:70] or "faceless-video"


def fftext(path: Path) -> str:
    return str(path).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def build_scenes(topic: str) -> list[dict]:
    return [
        {
            "title": "AI DIDN'T MAKE YOU LAZY",
            "body": "It exposed the system you already had. If your day had no rules, faster tools only make the chaos move faster.",
            "visual": "phone_scroll",
        },
        {
            "title": "TOOLS MULTIPLY DISCIPLINE",
            "body": "A builder gets leverage from AI. A consumer gets another dopamine slot machine. Same tool. Different standard.",
            "visual": "leverage",
        },
        {
            "title": "THE REAL FILTER IS OUTPUT",
            "body": "Don't measure prompts. Measure shipped work. Did you publish, apply, train, write, or build something that can be seen?",
            "visual": "output_meter",
        },
        {
            "title": "BUILD A BORING RULE",
            "body": "Before you open the internet, write the single deliverable for the day. One sentence. One target. One finish line.",
            "visual": "checklist",
        },
        {
            "title": "TODAY'S STANDARD",
            "body": "Use AI for one hard thing you were avoiding. Then close it. The win is not using the tool. The win is having evidence.",
            "visual": "evidence",
        },
    ]


def elevenlabs_tts(text: str, out: Path) -> bool:
    key = os.getenv("ELEVENLABS_API_KEY") or os.getenv("XI_API_KEY") or os.getenv("ELEVEN_API_KEY")
    if not key:
        return False
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{DEFAULT_VOICE}"
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.42, "similarity_boost": 0.75, "style": 0.35, "use_speaker_boost": True},
    }).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            out.write_bytes(resp.read())
        return out.exists() and out.stat().st_size > 1000
    except Exception as exc:
        (out.parent / "elevenlabs_error.txt").write_text(str(exc), encoding="utf-8")
        return False


def fallback_tts(text: str, out: Path) -> None:
    txt = out.with_suffix(".txt")
    txt.write_text(text, encoding="utf-8")
    sh(["ffmpeg", "-y", "-hide_banner", "-f", "lavfi", "-i", f"flite=textfile={txt}:voice=slt", "-ar", "44100", str(out)])


def graphic_filters(idx: int, title_file: Path, body_file: Path, visual: str, duration: float) -> str:
    base = [
        "scale=1080:1920",
        "drawbox=x=0:y=0:w=1080:h=1920:color=0x071018:t=fill",
        "drawbox=x=54:y=72:w=972:h=1740:color=0x111827@0.88:t=fill",
        "drawbox=x=54:y=72:w=972:h=1740:color=0x334155:t=3",
        f"drawtext=textfile='{fftext(title_file)}':font=DejaVuSans-Bold:fontcolor=0xF8FAFC:fontsize=66:x=80:y=140:line_spacing=8",
        f"drawtext=textfile='{fftext(body_file)}':font=DejaVuSans:fontcolor=0xCBD5E1:fontsize=42:x=86:y=1320:line_spacing=18",
        "drawtext=text='FACELESS DISCIPLINE':font=DejaVuSans-Bold:fontcolor=0x38BDF8:fontsize=28:x=82:y=1762",
    ]
    if visual == "phone_scroll":
        base += [
            "drawbox=x=340:y=430:w=400:h=640:color=0x0F172A:t=fill",
            "drawbox=x=340:y=430:w=400:h=640:color=0xE2E8F0:t=5",
            "drawbox=x=382:y=500+mod(t*120\\,420):w=316:h=78:color=0xEF4444@0.85:t=fill",
            "drawbox=x=382:y=610+mod(t*95\\,360):w=316:h=78:color=0xF97316@0.85:t=fill",
            "drawbox=x=382:y=720+mod(t*75\\,300):w=316:h=78:color=0x22C55E@0.85:t=fill",
            "drawtext=text='SCROLL':font=DejaVuSans-Bold:fontcolor=white:fontsize=48:x=394:y=890",
        ]
    elif visual == "leverage":
        base += [
            "drawbox=x=180:y=880:w=720:h=22:color=0x94A3B8:t=fill",
            "drawbox=x=220:y=910:w=70:h=210:color=0xF97316:t=fill",
            "drawbox=x=700:y=620:w=110:h=500:color=0x38BDF8:t=fill",
            "drawtext=text='CONSUME':font=DejaVuSans-Bold:fontcolor=0xF97316:fontsize=38:x=150:y=1160",
            "drawtext=text='BUILD':font=DejaVuSans-Bold:fontcolor=0x38BDF8:fontsize=52:x=700:y=560",
        ]
    elif visual == "output_meter":
        base += [
            "drawbox=x=160:y=620:w=760:h=90:color=0x334155:t=fill",
            "drawbox=x=160:y=620:w=760*min(t/5\\,1):h=90:color=0x22C55E:t=fill",
            "drawtext=text='OUTPUT > PROMPTS':font=DejaVuSans-Bold:fontcolor=white:fontsize=54:x=190:y=740",
            "drawbox=x=250:y=920:w=580:h=260:color=0x0F172A:t=fill",
            "drawtext=text='SHIPPED WORK':font=DejaVuSans-Bold:fontcolor=0xFACC15:fontsize=56:x=300:y=1020",
        ]
    elif visual == "checklist":
        for n, y in enumerate([520, 660, 800, 940], 1):
            base += [
                f"drawbox=x=190:y={y}:w=70:h=70:color=0x22C55E:t=4",
                f"drawtext=text='✓':font=DejaVuSans-Bold:fontcolor=0x22C55E:fontsize=64:x=202:y={y-8}",
                f"drawbox=x=310:y={y+24}:w={420+n*70}:h=18:color=0x64748B:t=fill",
            ]
    else:
        base += [
            "drawbox=x=170:y=540:w=740:h=450:color=0x020617:t=fill",
            "drawbox=x=220:y=610:w=640:h=80:color=0x38BDF8:t=fill",
            "drawbox=x=220:y=750:w=500:h=80:color=0x22C55E:t=fill",
            "drawbox=x=220:y=890:w=350:h=80:color=0xFACC15:t=fill",
            "drawtext=text='EVIDENCE':font=DejaVuSans-Bold:fontcolor=white:fontsize=72:x=260:y=1060",
        ]
    base += [f"drawbox=x=80:y=1810:w=920*{idx}/5:h=10:color=0x38BDF8:t=fill"]
    return ",".join(base)


def render_scene(work: Path, idx: int, scene: dict) -> Path:
    sd = work / "scenes"; sd.mkdir(exist_ok=True)
    title = sd / f"{idx:02d}_title.txt"
    body = sd / f"{idx:02d}_body.txt"
    title.write_text("\n".join(textwrap.wrap(scene["title"], 16)), encoding="utf-8")
    body.write_text("\n".join(textwrap.wrap(scene["body"], 34)), encoding="utf-8")
    audio = sd / f"{idx:02d}.mp3"
    spoken = f"{scene['title']}. {scene['body']}"
    if not elevenlabs_tts(spoken, audio):
        audio = sd / f"{idx:02d}.wav"
        fallback_tts(spoken, audio)
    duration = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(audio)])) + 0.6
    vf = graphic_filters(idx, title, body, scene["visual"], duration)
    out = sd / f"{idx:02d}.mp4"
    sh(["ffmpeg", "-y", "-hide_banner", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:d={duration:.2f}", "-i", str(audio), "-vf", vf, "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", str(out)])
    return out


def render(work: Path, scenes: list[dict]) -> Path:
    parts = [render_scene(work, i, s) for i, s in enumerate(scenes, 1)]
    concat = work / "concat.txt"
    concat.write_text("".join(f"file {p.resolve()}\n" for p in parts), encoding="utf-8")
    out = work / "final.mp4"
    sh(["ffmpeg", "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(out)])
    return out


def upload(video: Path, title: str, description: str) -> dict:
    raw = sh(["python3", str(SHARED_UPLOADER), str(video), "--title", title, "--description", description, "--tags", "discipline,self improvement,AI,faceless shorts", "--privacy", "private", "--project", PROJECT, "--log-jsonl", str(UPLOAD_LOG), "--delete-after-upload"])
    return json.loads(raw)


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser()
    p.add_argument("--topic", default="AI tools make lazy people lazier unless they build a discipline system")
    p.add_argument("--upload", action="store_true")
    p.add_argument("--keep-workspace", action="store_true")
    args = p.parse_args()

    stamp = dt.datetime.now(dt.UTC).strftime("%Y%m%d-%H%M%S")
    work = ROOT / "videos" / f"{stamp}-{slugify(args.topic)}"
    work.mkdir(parents=True, exist_ok=True)
    scenes = build_scenes(args.topic)
    (work / "script.json").write_text(json.dumps({"topic": args.topic, "scenes": scenes}, indent=2), encoding="utf-8")
    video = render(work, scenes)
    probe = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-show_entries", "format=duration,size", "-of", "json", str(video)]))
    result = {"workspace": str(work), "video": str(video), "probe": probe, "uploaded": False, "elevenlabs_key_present": bool(os.getenv("ELEVENLABS_API_KEY") or os.getenv("XI_API_KEY") or os.getenv("ELEVEN_API_KEY"))}
    if args.upload:
        result["upload"] = upload(video, "AI Did Not Make You Lazy — It Exposed You", "Private faceless channel upload with ElevenLabs voice and graphic/diagram scenes. Topic: " + args.topic)
        result["uploaded"] = True
        if not args.keep_workspace:
            shutil.rmtree(work, ignore_errors=True)
            result["workspace_deleted_after_upload"] = str(work)
    elif not args.keep_workspace:
        result["cleanup_note"] = "workspace retained because upload was not requested"
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

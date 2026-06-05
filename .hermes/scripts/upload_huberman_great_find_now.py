#!/usr/bin/env python3
"""Clip the Huberman motivation video into fresh shorts and upload private now."""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path("/opt/data/HeRmEz/projects/viral-clip-radar")
PLAN = ROOT / "CLIP_PLANS" / f"{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}-huberman-motivation-great-find"
SOURCE = ROOT / "SOURCES" / "huberman-motivation-great-find" / "vA50EK70whE.mp4"
ARCHIVE_MP4 = "https://archive.org/download/youtube-vA50EK70whE/vA50EK70whE.mp4"
SOURCE_URL = "https://www.youtube.com/watch?v=vA50EK70whE"
ARCHIVE_SOURCE = "https://archive.org/details/youtube-vA50EK70whE"
VTT = ROOT / "CLIP_PLANS" / "2026-05-31-huberman-motivation-drive" / "vA50EK70whE.en-US.vtt"
RENDER = ROOT / "scripts" / "render_clip_manifest.py"
UPLOAD = ROOT / "scripts" / "upload_to_youtube.py"

CLIPS = [
    {
        "slug": "motivation-is-pleasure-plus-pain",
        "start": "00:12:10",
        "end": "00:12:58",
        "hook": "Motivation is pleasure plus pain — that is why comfort kills drive.",
        "title": "Motivation Is Pleasure Plus Pain #Shorts",
    },
    {
        "slug": "social-media-dopamine-trap",
        "start": "00:17:40",
        "end": "00:18:29",
        "hook": "Social media hijacks dopamine because the reward keeps moving.",
        "title": "The Social Media Dopamine Trap #Shorts",
    },
    {
        "slug": "craving-is-pain-in-disguise",
        "start": "00:20:15",
        "end": "00:21:03",
        "hook": "Craving is part pleasure, part pain — and pain eventually wins.",
        "title": "Craving Is Pain In Disguise #Shorts",
    },
    {
        "slug": "working-too-late-kills-drive",
        "start": "00:52:59",
        "end": "00:53:50",
        "hook": "Working too late can suppress tomorrow's drive before the day starts.",
        "title": "Working Too Late Kills Tomorrow's Drive #Shorts",
    },
    {
        "slug": "dont-celebrate-every-win",
        "start": "01:14:14",
        "end": "01:15:04",
        "hook": "Enjoy your wins — but not every win needs a dopamine spike.",
        "title": "Do Not Celebrate Every Win #Shorts",
    },
]


def run(cmd: list[str], timeout: int = 900) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def parse_json_output(text: str) -> dict:
    text = text.strip()
    for marker in ("\n{", "{"):
        idx = text.rfind(marker) if marker.startswith("\n") else text.find(marker)
        if idx != -1:
            try:
                return json.loads(text[idx:].strip())
            except json.JSONDecodeError:
                pass
    raise ValueError(f"could not parse JSON from output: {text[-500:]}")


def seconds(ts: str) -> float:
    parts = ts.replace(",", ".").split(":")
    if len(parts) == 3:
        h, m, s = parts
    else:
        h, m, s = 0, parts[0], parts[1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def srt_time(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60); t -= m * 60
    s = int(t); ms = int(round((t - s) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_vtt(path: Path) -> list[tuple[float, float, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    blocks = re.split(r"\n\s*\n", text)
    cues = []
    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        time_line = next((ln for ln in lines if "-->" in ln), None)
        if not time_line:
            continue
        start_raw, end_raw = [part.strip().split()[0] for part in time_line.split("-->", 1)]
        caption = " ".join(ln for ln in lines if "-->" not in ln and not ln.startswith(("WEBVTT", "Kind:", "Language:")))
        caption = re.sub(r"<[^>]+>", "", caption).strip()
        if caption:
            cues.append((seconds(start_raw), seconds(end_raw), caption))
    return cues


def write_subtitles(cues: list[tuple[float, float, str]], clip: dict) -> str:
    outdir = PLAN / "subtitles"
    outdir.mkdir(parents=True, exist_ok=True)
    start = seconds(clip["start"])
    end = seconds(clip["end"])
    selected = [(max(a, start) - start, min(b, end) - start, txt) for a, b, txt in cues if b > start and a < end]
    srt = []
    for i, (a, b, txt) in enumerate(selected, 1):
        srt.append(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n")
    path = outdir / f"{clip['slug']}.srt"
    path.write_text("\n".join(srt), encoding="utf-8")
    return f"subtitles/{clip['slug']}.srt"


def ensure_source() -> None:
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if SOURCE.exists() and SOURCE.stat().st_size > 1000:
        return
    tmp = SOURCE.with_suffix(".mp4.part")
    with urllib.request.urlopen(ARCHIVE_MP4, timeout=300) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out)
    tmp.replace(SOURCE)


def build_manifest() -> Path:
    PLAN.mkdir(parents=True, exist_ok=True)
    cues = parse_vtt(VTT)
    manifest_clips = []
    for clip in CLIPS:
        subtitle = write_subtitles(cues, clip)
        manifest_clips.append({
            "file": f"EXPORTS/huberman-great-find/{clip['slug']}.mp4",
            "captioned_file": f"EXPORTS/huberman-great-find/{clip['slug']}.mp4",
            "start": clip["start"],
            "end": clip["end"],
            "hook": clip["hook"],
            "subtitle": subtitle,
        })
    manifest = {
        "source_file": str(SOURCE.relative_to(ROOT)),
        "source_url": SOURCE_URL,
        "archive_source": ARCHIVE_SOURCE,
        "source_title": "How to Increase Motivation & Drive",
        "creator": "Andrew Huberman / Huberman Lab",
        "rights_note": "Transformative vertical clips with captions, hook framing, attribution, and private-first upload for review.",
        "clips": manifest_clips,
    }
    path = PLAN / "clip_manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PLAN / "source_metadata.json").write_text(json.dumps({
        "source_url": SOURCE_URL,
        "archive_source": ARCHIVE_SOURCE,
        "source_title": manifest["source_title"],
        "creator": manifest["creator"],
        "created_at": dt.datetime.now(dt.UTC).isoformat(),
        "clip_count": len(CLIPS),
    }, indent=2) + "\n", encoding="utf-8")
    return path


def upload_clip(video: Path, clip: dict) -> dict:
    description = (
        "Private Viral Clip Radar upload for review. Source: Andrew Huberman / Huberman Lab, "
        "How to Increase Motivation & Drive. Original source: https://www.youtube.com/watch?v=vA50EK70whE. "
        "Archive mirror used for reliable VPS rendering. Transformative additions: vertical crop, burned captions, hook framing, and attribution.\n\n#Shorts"
    )
    proc = run([
        sys.executable, str(UPLOAD),
        "--file", str(video),
        "--title", clip["title"],
        "--description", description,
        "--tags", "shorts,Huberman,dopamine,motivation,self control,viral radar,clip analysis",
        "--privacy", "private",
    ], timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(json.dumps({
            "stage": "upload",
            "video": str(video),
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }, indent=2))
    return parse_json_output(proc.stdout)


def main() -> int:
    ensure_source()
    manifest = build_manifest()
    proc = run([sys.executable, str(RENDER), str(manifest), "--suffix=-great-find"], timeout=1200)
    if proc.returncode != 0:
        print(json.dumps({"status": "failed_render", "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:]}, indent=2))
        return proc.returncode
    rendered = parse_json_output(proc.stdout)
    uploads = []
    for item, clip in zip(rendered.get("rendered", []), CLIPS):
        uploads.append({"clip": clip["slug"], "upload": upload_clip(Path(item["output"]), clip), "render": item})
    print(json.dumps({
        "status": "ok",
        "plan": str(PLAN),
        "manifest": str(manifest),
        "rendered_count": len(rendered.get("rendered", [])),
        "uploads": uploads,
        "source_cleanup": rendered.get("source_cleanup"),
        "cleanup": "source deleted after render; exports deleted after confirmed YouTube upload IDs",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

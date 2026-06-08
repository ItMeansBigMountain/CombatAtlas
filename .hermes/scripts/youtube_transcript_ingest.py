#!/usr/bin/env python3
"""Fetch a YouTube transcript and save review artifacts for Hermes content workflows.

This is the repeatable path for "don't make me paste transcript chunks into Discord".
It wraps the youtube-content skill's fetch_transcript.py helper and writes durable
artifacts for Viral Radar / faceless YouTube planning.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

FETCHER = Path("/opt/data/skills/media/youtube-content/scripts/fetch_transcript.py")
DEFAULT_OUT = Path("/opt/data/HeRmEz/projects/viral-clip-radar/CLIP_PLANS")
FACELESS_IDEAS = Path("/opt/data/HeRmEz/projects/faceless-youtube-channel/STATE/source_transcripts")

KEYWORDS = [
    "one second", "worst days", "habit", "gratitude", "meditation", "exercise",
    "push-up", "learning", "social", "flirting", "rut", "potential", "discipline",
    "dopamine", "relapse", "momentum", "mental health", "happiness", "anxiety",
]


def slugify(value: str, max_len: int = 80) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value[:max_len].strip("-") or "youtube-video")


def extract_video_id(url_or_id: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})", url_or_id)
    if m:
        return m.group(1)
    m = re.search(r"^[a-zA-Z0-9_-]{11}$", url_or_id.strip())
    if m:
        return m.group(0)
    return hashlib.sha1(url_or_id.encode()).hexdigest()[:11]


def ts(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def run_fetcher(url: str, languages: str | None) -> dict[str, Any]:
    if not FETCHER.exists():
        raise SystemExit(f"fetch_transcript.py not found at {FETCHER}")
    cmd = [sys.executable, str(FETCHER), url, "--timestamps"]
    if languages:
        cmd.extend(["--language", languages])
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    if proc.returncode != 0:
        detail = proc.stdout.strip() or proc.stderr.strip()
        raise SystemExit(f"transcript fetch failed: {detail}")
    data = json.loads(proc.stdout)
    if data.get("error"):
        raise SystemExit(f"transcript fetch failed: {data['error']}")
    return data


def strip_vtt_payload(payload: str) -> str:
    lines: list[str] = []
    last = ""
    for raw in payload.splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        if "-->" in line or re.match(r"^\d+$", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = line.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
        line = re.sub(r"\s+", " ", line).strip()
        if line and line != last:
            lines.append(line)
            last = line
    return " ".join(lines)


def run_ytdlp_fallback(url: str, languages: str | None) -> dict[str, Any]:
    """Try yt-dlp subtitles when youtube-transcript-api is blocked by cloud IP."""
    langs = languages or "en"
    with tempfile.TemporaryDirectory(prefix="yt-sub-") as td:
        out_tpl = str(Path(td) / "%(id)s.%(ext)s")
        cmd = [
            "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", langs, "--sub-format", "vtt", "-o", out_tpl, url,
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout).strip()
            raise SystemExit(f"transcript fetch failed via API and yt-dlp fallback: {detail}")
        files = sorted(Path(td).glob("*.vtt"), key=lambda p: p.stat().st_size, reverse=True)
        if not files:
            raise SystemExit("transcript fetch failed: yt-dlp did not find subtitles/captions for this video")
        payload = files[0].read_text(encoding="utf-8", errors="replace")
        full_text = strip_vtt_payload(payload)
        video_id = extract_video_id(url)
        return {
            "video_id": video_id,
            "segment_count": None,
            "duration": "unknown",
            "full_text": full_text,
            "timestamped_text": full_text,
            "source_method": "yt-dlp-subtitles-fallback",
        }


def load_segments_from_fetcher(url: str, languages: str | None) -> dict[str, Any]:
    try:
        return run_fetcher(url, languages)
    except SystemExit as exc:
        msg = str(exc)
        if "blocking requests from your IP" in msg or "RequestBlocked" in msg or "IpBlocked" in msg:
            return run_ytdlp_fallback(url, languages)
        raise


def find_candidate_moments(timestamped: str, max_items: int = 12) -> list[dict[str, str]]:
    moments = []
    for line in timestamped.splitlines():
        low = line.lower()
        hits = [k for k in KEYWORDS if k in low]
        if hits:
            m = re.match(r"^(\S+)\s+(.*)$", line)
            moments.append({
                "timestamp": m.group(1) if m else "",
                "reason": ", ".join(hits[:3]),
                "text": (m.group(2) if m else line)[:240],
            })
    return moments[:max_items]


def write_artifacts(url: str, creator: str, title: str, data: dict[str, Any], out_root: Path) -> Path:
    video_id = data.get("video_id") or extract_video_id(url)
    date = dt.datetime.now(dt.UTC).date().isoformat()
    name = f"{date}-{slugify(creator, 24)}-{slugify(title or video_id, 58)}-{video_id}"
    plan = out_root / name
    plan.mkdir(parents=True, exist_ok=True)
    (plan / "transcript_timestamped.txt").write_text(data.get("timestamped_text", ""), encoding="utf-8")
    (plan / "transcript_full.txt").write_text(data.get("full_text", ""), encoding="utf-8")

    moments = find_candidate_moments(data.get("timestamped_text", ""))
    metadata = {
        "source_url": url,
        "video_id": video_id,
        "creator": creator,
        "title": title,
        "ingested_at": dt.datetime.now(dt.UTC).isoformat(),
        "segment_count": data.get("segment_count"),
        "duration": data.get("duration"),
        "candidate_status": "needs_human_or_agent_clip_selection",
        "transformative_standard": "Add hook/context/captions/analysis and source attribution. Do not raw reupload.",
        "candidate_moments": moments,
    }
    (plan / "source_metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    bullets = "\n".join(f"- **{m['timestamp']}** — {m['text']} _(signal: {m['reason']})_" for m in moments) or "- No keyword moments found yet; review transcript manually."
    (plan / "edit_notes.md").write_text(f"""# Transcript Ingest — {title or video_id}

- Creator: {creator}
- Source: {url}
- Duration: {data.get('duration')}
- Status: needs clip selection + transformative framing

## Candidate moments

{bullets}

## Clip rules

1. Add a punchy hook in the first 1–2 seconds.
2. Add captions and context/analysis.
3. Attribute the source creator.
4. Render 9:16 Shorts/Reels format.
5. Upload private-first when using YouTube.
""", encoding="utf-8")

    FACELESS_IDEAS.mkdir(parents=True, exist_ok=True)
    (FACELESS_IDEAS / f"{name}.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest YouTube transcript into Viral Radar / faceless workflow artifacts")
    ap.add_argument("url", help="YouTube URL or video ID")
    ap.add_argument("--creator", default="unknown-creator")
    ap.add_argument("--title", default="")
    ap.add_argument("--language", default="en", help="Comma-separated transcript language fallback, e.g. en,tr. Use empty string for auto.")
    ap.add_argument("--out-root", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    languages = args.language or None
    data = load_segments_from_fetcher(args.url, languages)
    plan = write_artifacts(args.url, args.creator, args.title, data, Path(args.out_root))
    print(json.dumps({
        "ok": True,
        "plan": str(plan),
        "video_id": data.get("video_id"),
        "duration": data.get("duration"),
        "segment_count": data.get("segment_count"),
        "candidate_moments": len(find_candidate_moments(data.get("timestamped_text", ""))),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

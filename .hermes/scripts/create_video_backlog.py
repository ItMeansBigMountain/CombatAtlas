#!/usr/bin/env python3
"""Create a scheduled YouTube release backlog across HeRmEz video projects.

Backlog policy:
- upload with YouTube publishAt so videos release in peak Central-time windows;
- delete generated MP4/workspaces only after returned upload IDs;
- preserve logs/manifests/metadata/backlog calendar.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

FACELESS = Path("/opt/data/HeRmEz/projects/faceless-youtube-channel")
VIRAL = Path("/opt/data/HeRmEz/projects/viral-clip-radar")
SHARED_UPLOADER = Path("/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py")
BACKLOG_DIR = Path("/opt/data/HeRmEz/projects/_ops/social-growth/backlog")
BACKLOG_LOG = BACKLOG_DIR / "scheduled_release_backlog.jsonl"

FACILESS_TOPICS = [
    "The day gets easier when the rule is written before the phone opens",
    "Nobody is coming to save your discipline; build the system anyway",
    "Your dopamine problem is really a standards problem",
    "No degree is not a death sentence if your receipts are public",
    "The fastest way to stop wasting your potential is to pick one proof task",
]

VIRAL_MANIFEST = VIRAL / "CLIP_PLANS" / "2026-05-31-huberman-motivation-drive" / "clip_manifest.json"
HUBERMAN_SOURCE = VIRAL / "SOURCES" / "huberman-motivation" / "fallback-source.mp4"
HUBERMAN_ARCHIVE_MP4 = "https://archive.org/download/youtube-vA50EK70whE/vA50EK70whE.mp4"


def run(cmd: list[str], cwd: Path, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)


def parse_json_output(text: str) -> dict:
    text = text.strip()
    for marker in ("\n{", "{"):
        idx = text.rfind(marker) if marker.startswith("\n") else text.find(marker)
        if idx != -1:
            candidate = text[idx:].strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass
    raise ValueError(f"could not parse JSON output: {text[-500:]}")


def peak_slots(start_date: dt.date, count: int, *, local_hour: int, local_minute: int, every_days: int = 1) -> list[dict]:
    tz = ZoneInfo("America/Chicago")
    out = []
    d = start_date
    for _ in range(count):
        local = dt.datetime(d.year, d.month, d.day, local_hour, local_minute, tzinfo=tz)
        utc = local.astimezone(dt.UTC)
        out.append({"local": local.isoformat(), "utc": utc.strftime("%Y-%m-%dT%H:%M:%SZ")})
        d += dt.timedelta(days=every_days)
    return out


def upload_scheduled(video: Path, *, title: str, description: str, tags: str, project: str, log_jsonl: Path, publish_at: str) -> dict:
    cmd = [
        sys.executable, str(SHARED_UPLOADER), str(video),
        "--title", title,
        "--description", description,
        "--tags", tags,
        "--privacy", "private",
        "--publish-at", publish_at,
        "--project", project,
        "--log-jsonl", str(log_jsonl),
        "--delete-after-upload",
    ]
    proc = run(cmd, video.parent, timeout=600)
    if proc.returncode != 0:
        raise RuntimeError(json.dumps({
            "stage": "upload_scheduled",
            "video": str(video),
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }, indent=2))
    return parse_json_output(proc.stdout)


def slug_title(topic: str) -> str:
    words = topic.replace(";", "").split()
    return " ".join(words[:10]).strip().title()


def build_faceless_backlog(start_date: dt.date) -> list[dict]:
    runner = FACELESS / "scripts" / "run_graphic_video.py"
    slots = peak_slots(start_date, len(FACILESS_TOPICS), local_hour=14, local_minute=45)
    results = []
    for topic, slot in zip(FACILESS_TOPICS, slots):
        proc = run([sys.executable, str(runner), "--topic", topic, "--keep-workspace"], FACELESS, timeout=900)
        if proc.returncode != 0:
            raise RuntimeError(json.dumps({"stage": "faceless_render", "topic": topic, "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:]}, indent=2))
        payload = parse_json_output(proc.stdout)
        video = Path(payload["video"])
        title = f"{slug_title(topic)} #Shorts"
        description = (
            "Scheduled faceless discipline/self-improvement Short. "
            "Graphic/diagram scenes, burned-in text, and private scheduled release from the HeRmEz backlog. "
            f"Topic: {topic}\n\n#Shorts"
        )
        upload = upload_scheduled(
            video,
            title=title[:95],
            description=description,
            tags="discipline,self improvement,faceless shorts,systems,dopamine,first gen men",
            project="faceless-youtube-channel",
            log_jsonl=FACELESS / "UPLOADS" / "youtube_uploads.jsonl",
            publish_at=slot["utc"],
        )
        work = Path(payload["workspace"])
        shutil.rmtree(work, ignore_errors=True)
        record = {"project": "faceless-youtube-channel", "topic": topic, "title": title[:95], "publish_slot": slot, "upload": upload, "workspace_deleted": str(work)}
        append_record(record)
        results.append(record)
    return results


def ensure_huberman_source() -> Path:
    HUBERMAN_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if HUBERMAN_SOURCE.exists() and HUBERMAN_SOURCE.stat().st_size > 1000:
        return HUBERMAN_SOURCE
    tmp = HUBERMAN_SOURCE.with_suffix(".mp4.part")
    with urllib.request.urlopen(HUBERMAN_ARCHIVE_MP4, timeout=300) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out)
    tmp.replace(HUBERMAN_SOURCE)
    return HUBERMAN_SOURCE


def build_viral_backlog(start_date: dt.date) -> list[dict]:
    source = ensure_huberman_source()
    render = VIRAL / "scripts" / "render_clip_manifest.py"
    proc = run([sys.executable, str(render), str(VIRAL_MANIFEST), "--source", str(source), "--suffix=-backlog"], VIRAL, timeout=1200)
    if proc.returncode != 0:
        raise RuntimeError(json.dumps({"stage": "viral_render", "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:]}, indent=2))
    payload = parse_json_output(proc.stdout)
    manifest = json.loads(VIRAL_MANIFEST.read_text(encoding="utf-8"))
    clips_by_stem = {Path(c.get("file", "")).stem: c for c in manifest.get("clips", [])}
    slots = peak_slots(start_date, len(payload.get("rendered", [])), local_hour=19, local_minute=15, every_days=2)
    results = []
    for item, slot in zip(payload.get("rendered", []), slots):
        video = Path(item["output"])
        base_stem = video.stem.replace("-backlog", "")
        clip = clips_by_stem.get(base_stem, {})
        hook = clip.get("hook") or base_stem.replace("-", " ").title()
        title = f"{hook.split('.')[0][:78]} #Shorts"
        description = (
            "Scheduled Viral Clip Radar Short. Source: Andrew Huberman / Huberman Lab, How to Increase Motivation & Drive. "
            "Source URL: https://www.youtube.com/watch?v=vA50EK70whE. "
            "Internet Archive mirror used because VPS YouTube download hit bot checks. "
            "Transformative additions: vertical crop, captions, hook overlay/context, and attribution.\n\n#Shorts"
        )
        upload = upload_scheduled(
            video,
            title=title,
            description=description,
            tags="shorts,Huberman,dopamine,motivation,self control,viral radar,clip analysis",
            project="viral-clip-radar",
            log_jsonl=VIRAL / "UPLOADS" / "youtube_uploads.jsonl",
            publish_at=slot["utc"],
        )
        record = {"project": "viral-clip-radar", "clip": base_stem, "title": title, "publish_slot": slot, "upload": upload}
        append_record(record)
        results.append(record)
    return results


def append_record(record: dict) -> None:
    BACKLOG_DIR.mkdir(parents=True, exist_ok=True)
    with BACKLOG_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"created_at": dt.datetime.now(dt.UTC).isoformat(), **record}, separators=(",", ":")) + "\n")


def write_calendar(records: list[dict]) -> Path:
    BACKLOG_DIR.mkdir(parents=True, exist_ok=True)
    path = BACKLOG_DIR / f"release-calendar-{dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')}.md"
    lines = ["# Scheduled Release Backlog", "", "All times include Central local slot + exact UTC `publishAt` sent to YouTube.", ""]
    for rec in sorted(records, key=lambda r: r["publish_slot"]["utc"]):
        upload = rec["upload"]
        lines.append(f"- {rec['publish_slot']['local']} / `{rec['publish_slot']['utc']}` — **{rec['project']}** — {rec.get('title') or rec.get('topic') or rec.get('clip')} — {upload.get('url')} — privacy `{upload.get('privacy')}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    tomorrow = dt.datetime.now(ZoneInfo("America/Chicago")).date() + dt.timedelta(days=1)
    records = []
    records.extend(build_faceless_backlog(tomorrow))
    records.extend(build_viral_backlog(tomorrow))
    calendar = write_calendar(records)
    print(json.dumps({"status": "ok", "created_count": len(records), "calendar": str(calendar), "log": str(BACKLOG_LOG), "records": records}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

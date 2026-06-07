#!/usr/bin/env python3
"""Daily public faceless YouTube Shorts upload pipeline for cron.

Runs the project renderer/uploader, logs through the project upload log, and lets
run_graphic_video.py delete generated workspace assets after a confirmed upload.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/opt/data/HeRmEz/projects/faceless-youtube-channel")
SCRIPT = ROOT / "scripts" / "run_graphic_video.py"
TOPICS = [
    "Fatherless men need systems, not motivation",
    "Dopamine is quietly killing your comeback",
    "AI did not make you lazy; it exposed your standards",
    "No degree, no excuse: build receipts before confidence",
    "Before you open the internet, write one standard for the day",
    "Food, weed, and scrolling are symptoms of a missing system",
    "A chaotic life gets rebuilt by boring rules",
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


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
    raise ValueError("could not parse JSON output")


def main() -> int:
    local_day = dt.datetime.now(ZoneInfo("America/Chicago")).date().isoformat()
    marker = ROOT / "STATE" / f"faceless_daily_upload_{local_day}.done"
    if marker.exists() and os.getenv("FORCE_UPLOAD") != "1":
        print(json.dumps({
            "job": "faceless_daily_upload",
            "status": "skipped_already_ran_today",
            "local_day": local_day,
            "marker": str(marker),
            "override": "set FORCE_UPLOAD=1 to bypass",
        }, indent=2))
        return 0
    researched_topic = os.getenv("FACELESS_TOPIC", "").strip()
    idx = dt.datetime.now(dt.UTC).toordinal() % len(TOPICS)
    topic = researched_topic or TOPICS[idx]
    research_json = os.getenv("FACELESS_RESEARCH_JSON", "").strip()
    if research_json:
        (ROOT / "STATE").mkdir(parents=True, exist_ok=True)
        (ROOT / "STATE" / f"research_{local_day}.json").write_text(research_json, encoding="utf-8")
    cmd = [sys.executable, str(SCRIPT), "--topic", topic, "--upload"]
    proc = run(cmd)
    if proc.returncode != 0:
        print(json.dumps({
            "job": "faceless_daily_upload",
            "status": "failed",
            "topic": topic,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }, indent=2))
        return proc.returncode
    try:
        payload = parse_json_output(proc.stdout)
    except Exception:
        payload = {"raw_stdout": proc.stdout[-3000:]}
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({
        "completed_at": dt.datetime.now(dt.UTC).isoformat(),
        "topic": topic,
        "result": payload,
    }, indent=2), encoding="utf-8")
    print(json.dumps({
        "job": "faceless_daily_upload",
        "status": "ok",
        "topic": topic,
        "result": payload,
        "cleanup": "generated per-video workspace deleted after successful public upload unless --keep-workspace is used",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Collect lightweight YouTube performance metrics for social-video cron jobs.

Reads project upload logs, fetches public video statistics when YOUTUBE_API_KEY is
available, and writes durable performance learnings that future cron runs can use
for topic/title/hook selection. If the API key is missing, it still writes a
credential/action note instead of failing the content pipeline.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import statistics
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/opt/data/HeRmEz/projects")
PROJECTS = {
    "faceless-youtube-channel": ROOT / "faceless-youtube-channel" / "UPLOADS" / "youtube_uploads.jsonl",
    "viral-clip-radar": ROOT / "viral-clip-radar" / "UPLOADS" / "youtube_uploads.jsonl",
}
LEARNINGS = ROOT / "_ops" / "social-growth" / "PERFORMANCE_LEARNINGS.md"
API = "https://www.googleapis.com/youtube/v3/videos"


def load_dotenv(path: Path = Path("/opt/data/.env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def read_uploads(path: Path) -> list[dict]:
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("video_id"):
            rows.append(row)
    return rows


def chunks(xs: list[str], n: int = 50):
    for i in range(0, len(xs), n):
        yield xs[i:i+n]


def fetch_stats(video_ids: list[str]) -> dict[str, dict]:
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        return {}
    out = {}
    for batch in chunks(sorted(set(video_ids))):
        params = urllib.parse.urlencode({
            "part": "snippet,statistics,status",
            "id": ",".join(batch),
            "key": key,
        })
        with urllib.request.urlopen(f"{API}?{params}", timeout=30) as resp:
            data = json.load(resp)
        for item in data.get("items", []):
            out[item.get("id")] = item
    return out


def words(text: str) -> list[str]:
    stop = {"shorts", "the", "and", "you", "your", "this", "that", "with", "from", "public", "viral"}
    return [w for w in re.findall(r"[a-zA-Z]{4,}", text.lower()) if w not in stop]


def summarize(project_rows: dict[str, list[dict]], stats: dict[str, dict]) -> str:
    now = dt.datetime.now(dt.UTC).isoformat()
    lines = ["# Social Video Performance Learnings", "", f"Last updated: `{now}`", ""]
    if not stats:
        lines += [
            "## Metrics status",
            "",
            "- `YOUTUBE_API_KEY` was not available, so this run could not fetch live view/like/comment metrics.",
            "- Upload logs were still parsed so cron jobs can avoid duplicate video IDs/titles.",
            "- To enable the learning loop, add a YouTube Data API v3 key as `YOUTUBE_API_KEY` in `/opt/data/.env`.",
            "",
        ]
    for project, rows in project_rows.items():
        public_rows = [r for r in rows if r.get("privacy") == "public"]
        lines += [f"## {project}", "", f"- Uploads logged: {len(rows)} total; {len(public_rows)} public."]
        scored = []
        for row in public_rows:
            item = stats.get(row.get("video_id"))
            if not item:
                continue
            st = item.get("statistics", {})
            views = int(st.get("viewCount", 0) or 0)
            likes = int(st.get("likeCount", 0) or 0)
            comments = int(st.get("commentCount", 0) or 0)
            score = views + likes * 5 + comments * 12
            scored.append((score, views, likes, comments, row))
        scored.sort(reverse=True, key=lambda x: x[0])
        if scored:
            median_views = statistics.median([x[1] for x in scored])
            lines.append(f"- Median public views in latest snapshot: {median_views}.")
            lines.append("- Current winners to study:")
            for score, views, likes, comments, row in scored[:5]:
                lines.append(f"  - {views} views / {likes} likes / {comments} comments — {row.get('title')} — {row.get('url')}")
            counter = Counter()
            for _, _, _, _, row in scored[:10]:
                counter.update(words((row.get("title") or "") + " " + (row.get("description") or "")))
            if counter:
                lines.append("- Hook/title words showing up in better performers: " + ", ".join(w for w, _ in counter.most_common(12)) + ".")
        elif public_rows:
            lines.append("- Live metrics unavailable for public videos in this snapshot; use upload-log dedupe only until API metrics are configured.")
        lines.append("")
    lines += [
        "## Operating rule for future cron runs",
        "",
        "- Before generating the next video, read this file and avoid repeating low-signal titles/hooks.",
        "- Double down on topics whose public videos beat the channel median views and comments.",
        "- Treat missing metrics as a setup issue, not as proof the content failed.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    load_dotenv()
    project_rows = {name: read_uploads(path) for name, path in PROJECTS.items()}
    ids = [r["video_id"] for rows in project_rows.values() for r in rows if r.get("video_id")]
    stats = fetch_stats(ids)
    snapshot_at = dt.datetime.now(dt.UTC).isoformat()
    for project, rows in project_rows.items():
        out = ROOT / project / "ANALYTICS" / "youtube_metrics.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as f:
            for row in rows:
                vid = row.get("video_id")
                if vid in stats:
                    f.write(json.dumps({"snapshot_at": snapshot_at, "project": project, "upload": row, "youtube": stats[vid]}, separators=(",", ":")) + "\n")
    LEARNINGS.parent.mkdir(parents=True, exist_ok=True)
    LEARNINGS.write_text(summarize(project_rows, stats), encoding="utf-8")
    payload = {
        "status": "ok",
        "youtube_api_key_present": bool(os.getenv("YOUTUBE_API_KEY")),
        "video_ids_seen": len(set(ids)),
        "stats_fetched": len(stats),
        "learnings": str(LEARNINGS),
    }
    print(json.dumps(payload, indent=2) if args.json else LEARNINGS.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Daily public Viral Clip Radar Shorts upload pipeline for cron.

Uses the currently reviewed NASA/JPL manifest as the safe evergreen upload lane:
official NASA source -> vertical captioned render -> public YouTube upload ->
log upload IDs -> delete generated exports and source media.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/opt/data/HeRmEz/projects/viral-clip-radar")
MANIFEST = ROOT / "CLIP_PLANS" / "2026-06-03-nasa-batch-shorts" / "clip_manifest.json"
RENDER = ROOT / "scripts" / "render_clip_manifest.py"
UPLOAD = ROOT / "scripts" / "upload_to_youtube.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def ensure_source(manifest: dict) -> Path:
    source = ROOT / manifest["source_file"]
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists() and source.stat().st_size > 1000:
        return source
    url = manifest.get("fallback_source_url")
    if not url:
        raise RuntimeError("manifest source missing and no fallback_source_url present")
    tmp = source.with_suffix(source.suffix + ".part")
    with urllib.request.urlopen(url, timeout=180) as resp, tmp.open("wb") as out:
        shutil.copyfileobj(resp, out)
    tmp.replace(source)
    return source


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


def upload_rendered(rendered: list[dict], manifest: dict) -> list[dict]:
    uploads = []
    suffix = dt.datetime.now(dt.UTC).strftime("%Y%m%d")
    for item in rendered:
        output = Path(item["output"])
        hook = ""
        for clip in manifest.get("clips", []):
            if Path(clip.get("file", "")).stem in output.stem or Path(clip.get("captioned_file", "")).stem in output.stem:
                hook = str(clip.get("hook") or "")
                break
        title_seed = hook.split(":")[0].strip() or output.stem.replace("-", " ").title()
        title = f"{title_seed[:74]} #Shorts"
        description = (
            "Public Viral Clip Radar automated upload. Source: NASA/JPL-Caltech, "
            f"{manifest.get('source_title','Perseverance landing footage')}. "
            f"Original source: {manifest.get('source_url','')}. "
            "Transformative additions: vertical edit, burned captions, hook/context framing, and source attribution. "
            f"Cron cohort: viral-radar-{suffix}.\n\n#Shorts"
        )
        cmd = [
            sys.executable, str(UPLOAD),
            "--file", str(output),
            "--title", title,
            "--description", description,
            "--tags", "shorts,viral radar,NASA,Mars,Perseverance,clip analysis",
            "--privacy", "public",
        ]
        proc = run(cmd)
        if proc.returncode != 0:
            raise RuntimeError(json.dumps({
                "upload_failed_for": str(output),
                "returncode": proc.returncode,
                "stdout_tail": proc.stdout[-2000:],
                "stderr_tail": proc.stderr[-2000:],
            }, indent=2))
        uploads.append(parse_json_output(proc.stdout))
    return uploads


def main() -> int:
    local_day = dt.datetime.now(ZoneInfo("America/Chicago")).date().isoformat()
    marker = ROOT / "STATE" / f"viral_radar_daily_upload_{local_day}.done"
    if marker.exists() and os.getenv("FORCE_UPLOAD") != "1":
        print(json.dumps({
            "job": "viral_radar_daily_upload",
            "status": "skipped_already_ran_today",
            "local_day": local_day,
            "marker": str(marker),
            "override": "set FORCE_UPLOAD=1 to bypass",
        }, indent=2))
        return 0
    manifest = load_manifest()
    try:
        source = ensure_source(manifest)
        render_proc = run([sys.executable, str(RENDER), str(MANIFEST), "--suffix=-cron"])
        if render_proc.returncode != 0:
            print(json.dumps({
                "job": "viral_radar_daily_upload",
                "status": "failed_render",
                "source": str(source),
                "returncode": render_proc.returncode,
                "stdout_tail": render_proc.stdout[-2000:],
                "stderr_tail": render_proc.stderr[-2000:],
            }, indent=2))
            return render_proc.returncode
        render_payload = parse_json_output(render_proc.stdout)
        uploads = upload_rendered(render_payload.get("rendered", []), manifest)
        result = {
            "job": "viral_radar_daily_upload",
            "status": "ok",
            "manifest": str(MANIFEST),
            "rendered_count": len(render_payload.get("rendered", [])),
            "uploads": uploads,
            "source_cleanup": render_payload.get("source_cleanup"),
            "cleanup": "source video deleted by renderer when safe; rendered exports deleted by uploader after successful public upload",
        }
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps({
            "completed_at": dt.datetime.now(dt.UTC).isoformat(),
            "result": result,
        }, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({
            "job": "viral_radar_daily_upload",
            "status": "failed",
            "error": str(exc),
        }, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

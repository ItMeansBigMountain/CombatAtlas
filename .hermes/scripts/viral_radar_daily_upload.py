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
DEFAULT_MANIFEST = ROOT / "CLIP_PLANS" / "2026-06-04-huberman-motivation-great-find" / "clip_manifest.json"
MANIFEST = Path(os.getenv("VIRAL_RADAR_MANIFEST", str(DEFAULT_MANIFEST)))
RENDER = ROOT / "scripts" / "render_clip_manifest.py"
UPLOAD = ROOT / "scripts" / "upload_to_youtube.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def clip_key(manifest_path: Path, clip: dict) -> str:
    return f"{manifest_path}:{Path(clip.get('captioned_file') or clip.get('file') or clip.get('hook','clip')).stem}"


def uploaded_public_keys() -> set[str]:
    log = ROOT / "UPLOADS" / "youtube_uploads.jsonl"
    keys = set()
    if not log.exists():
        return keys
    for line in log.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("privacy") != "public":
            continue
        path = str(row.get("video_path") or "")
        title = str(row.get("title") or "")
        stem = Path(path).stem.replace("-cron", "").replace("-daily", "")
        if stem:
            keys.add(stem)
        keys.add(title.lower())
    return keys


def select_daily_manifest_clip() -> tuple[Path, dict, dict]:
    forced_index = os.getenv("VIRAL_RADAR_CLIP_INDEX", "").strip()
    manifests = [MANIFEST] if os.getenv("VIRAL_RADAR_MANIFEST") else sorted((ROOT / "CLIP_PLANS").glob("*/clip_manifest.json"), reverse=True)
    seen = uploaded_public_keys()
    fallback = None
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        clips = manifest.get("clips") or []
        if forced_index:
            clip = clips[int(forced_index)]
            return manifest_path, manifest, clip
        for clip in clips:
            stem = Path(clip.get("captioned_file") or clip.get("file") or "").stem
            hook = str(clip.get("hook") or "").lower()
            candidate = (manifest_path, manifest, clip)
            fallback = fallback or candidate
            if stem not in seen and hook not in seen:
                return candidate
    if fallback and os.getenv("VIRAL_RADAR_ALLOW_DUPLICATE") == "1":
        return fallback
    raise RuntimeError("no fresh reviewed manifest clips available; add/review a new clip manifest or set VIRAL_RADAR_ALLOW_DUPLICATE=1 explicitly")


def write_single_clip_manifest(manifest_path: Path, manifest: dict, clip: dict, local_day: str) -> Path:
    outdir = ROOT / "TMP" / "daily-cron-manifests" / local_day
    outdir.mkdir(parents=True, exist_ok=True)
    single = dict(manifest)
    clip_copy = dict(clip)
    if clip_copy.get("subtitle") and not Path(str(clip_copy["subtitle"])).is_absolute():
        subtitle_path = manifest_path.parent / str(clip_copy["subtitle"])
        if subtitle_path.exists():
            clip_copy["subtitle"] = str(subtitle_path)
    single["clips"] = [clip_copy]
    single["selected_from_manifest"] = str(manifest_path)
    out = outdir / f"{Path(clip_copy.get('captioned_file') or clip_copy.get('file') or 'clip').stem}.json"
    out.write_text(json.dumps(single, indent=2), encoding="utf-8")
    return out


def ensure_source(manifest: dict) -> Path:
    source = ROOT / manifest["source_file"]
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists() and source.stat().st_size > 1000:
        return source
    url = manifest.get("fallback_source_url")
    if not url and manifest.get("archive_source"):
        vid = str(manifest.get("source_url", "")).split("v=")[-1].split("&")[0]
        if vid:
            url = f"https://archive.org/download/youtube-{vid}/{vid}.mp4"
    if not url:
        raise RuntimeError("manifest source missing and no fallback_source_url/archive_source present")
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


def upload_rendered(rendered: list[dict], manifest: dict, selected_clip: dict | None = None) -> list[dict]:
    uploads = []
    suffix = dt.datetime.now(dt.UTC).strftime("%Y%m%d")
    for item in rendered:
        output = Path(item["output"])
        hook = ""
        for clip in ([selected_clip] if selected_clip else manifest.get("clips", [])):
            if Path(clip.get("file", "")).stem in output.stem or Path(clip.get("captioned_file", "")).stem in output.stem:
                hook = str(clip.get("hook") or "")
                break
        title_seed = hook.split(":")[0].strip() or output.stem.replace("-", " ").title()
        title = f"{title_seed[:74]} #Shorts"
        description = (
            f"Public Viral Clip Radar automated upload. Source: {manifest.get('creator','source creator')}, "
            f"{manifest.get('source_title','source footage')}. "
            f"Original source: {manifest.get('source_url','')}. "
            "Transformative additions: vertical edit, burned captions, hook/context framing, and source attribution. "
            f"Cron cohort: viral-radar-{suffix}.\n\n#Shorts"
        )
        cmd = [
            sys.executable, str(UPLOAD),
            "--file", str(output),
            "--title", title,
            "--description", description,
            "--tags", "shorts,viral radar,clip analysis,self improvement,dopamine,motivation",
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
    try:
        manifest_path, manifest, selected_clip = select_daily_manifest_clip()
        single_manifest = write_single_clip_manifest(manifest_path, manifest, selected_clip, local_day)
        source = ensure_source(manifest)
        render_proc = run([sys.executable, str(RENDER), str(single_manifest), "--suffix=-daily"])
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
        uploads = upload_rendered(render_payload.get("rendered", []), manifest, selected_clip)
        result = {
            "job": "viral_radar_daily_upload",
            "status": "ok",
            "manifest": str(single_manifest),
            "selected_from_manifest": str(manifest_path),
            "selected_hook": selected_clip.get("hook"),
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

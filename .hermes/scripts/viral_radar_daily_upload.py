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
SEED_LATEST = ROOT / "scripts" / "seed_latest_longform_manifests.py"
EXTERNAL_PROVIDER = ROOT / "scripts" / "external_clip_provider.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["YOUTUBE_UPLOAD_TOKEN"] = os.getenv("YOUTUBE_UPLOAD_TOKEN") or "/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json"
    cookie_path = "/opt/data/secrets/youtube-cookies/youtube-cookies.txt"
    if Path(cookie_path).is_file():
        env.setdefault("YOUTUBE_COOKIES_FILE", cookie_path)
        env.setdefault("YTDLP_COOKIES_FILE", cookie_path)
        env.setdefault("YOUTUBE_COOKIES", cookie_path)
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env)


def seed_latest_manifests() -> dict:
    """Refresh queue from Google/YouTube APIs every job before selecting a clip."""
    if not SEED_LATEST.exists():
        return {"status": "missing_seed_script", "path": str(SEED_LATEST)}
    proc = run([sys.executable, str(SEED_LATEST), "--clips-per-video", "2", "--max-videos-per-channel", "50"])
    if proc.returncode != 0:
        return {"status": "seed_failed", "returncode": proc.returncode, "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:]}
    try:
        return parse_json_output(proc.stdout)
    except Exception:
        return {"status": "seed_output_unparsed", "stdout_tail": proc.stdout[-2000:]}


def external_clip_fallback(manifest_path: Path, manifest: dict, selected_clip: dict) -> dict:
    """Use official clipping/import APIs instead of direct YouTube downloading.

    This avoids the VPS/headless `yt-dlp` bot-verification path. Providers may
    return a finished local MP4 immediately or a submitted/pending job for a
    later cron poll.
    """
    if not EXTERNAL_PROVIDER.exists():
        return {"attempted": False, "reason": "external provider script missing", "path": str(EXTERNAL_PROVIDER)}
    clips = manifest.get("clips") or []
    try:
        clip_index = clips.index(selected_clip)
    except ValueError:
        clip_index = 0
    proc = run([
        sys.executable, str(EXTERNAL_PROVIDER), str(manifest_path),
        "--clip-index", str(clip_index),
        "--poll-seconds", os.getenv("VIRAL_RADAR_PROVIDER_POLL_SECONDS", "0"),
    ])
    if proc.returncode != 0:
        return {"attempted": True, "status": "failed", "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:]}
    try:
        return parse_json_output(proc.stdout)
    except Exception:
        return {"attempted": True, "status": "unparsed", "stdout_tail": proc.stdout[-2000:]}


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


def _creator_name(manifest: dict) -> str:
    return str(manifest.get("creator") or manifest.get("channel") or "unknown").strip()


def _is_evergreen_fallback_creator(manifest: dict) -> bool:
    creator = _creator_name(manifest).lower()
    title = str(manifest.get("source_title") or "").lower()
    return (
        "nasa" in creator
        or creator == "unknown"
        or "huberman / huberman lab" in creator
        or "how to increase motivation" in title
    )


def recent_uploaded_creators(limit: int = 8) -> list[str]:
    logs = [ROOT / "UPLOADS" / "viral_radar_enriched_uploads.jsonl", ROOT / "UPLOADS" / "youtube_uploads.jsonl"]
    creators: list[str] = []
    lines = []
    for log in logs:
        if log.exists():
            lines.extend(log.read_text(encoding="utf-8", errors="ignore").splitlines())
    for line in reversed(lines):
        try:
            row = json.loads(line)
        except Exception:
            continue
        creator = str(row.get("creator") or row.get("source_creator") or "").strip()
        if not creator:
            # Older rows did not log creator. Infer from title/description only as
            # a weak de-dupe hint; new rows should include explicit creator.
            blob = (str(row.get("title") or "") + " " + str(row.get("description") or "")).lower()
            for name in ["huberman", "chris williamson", "kinobody", "hormozi", "hamza", "gg33", "belmar", "tate"]:
                if name in blob:
                    creator = name
                    break
        if creator:
            creators.append(creator.lower())
        if len(creators) >= limit:
            break
    return creators


def iter_candidate_manifest_clips() -> list[tuple[Path, dict, dict]]:
    """Return candidate clips in creator-diverse priority order.

    Cron must publish a finished clip, not merely identify a source. Try every
    influencer in the pool before repeating the same creator. Source-ready
    candidates still rank higher inside each creator so the job can complete.
    """
    forced_index = os.getenv("VIRAL_RADAR_CLIP_INDEX", "").strip()
    manifests = [MANIFEST] if os.getenv("VIRAL_RADAR_MANIFEST") else sorted((ROOT / "CLIP_PLANS").glob("*/clip_manifest.json"), reverse=True)
    seen = uploaded_public_keys()
    fresh: list[tuple[Path, dict, dict]] = []
    fallback: list[tuple[Path, dict, dict]] = []
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        creator_l = _creator_name(manifest).lower()
        if "zerkaa" in creator_l:
            continue
        if _is_evergreen_fallback_creator(manifest) and os.getenv("VIRAL_RADAR_ALLOW_EVERGREEN_FALLBACK") != "1":
            # The user's current queue is influencer clips. Do not silently fill
            # blocked creator slots with NASA/unknown/old Huberman evergreen clips.
            continue
        clips = manifest.get("clips") or []
        if forced_index:
            if clips:
                return [(manifest_path, manifest, clips[int(forced_index)])]
            continue
        for clip in clips:
            stem = Path(clip.get("captioned_file") or clip.get("file") or "").stem
            hook = str(clip.get("hook") or "").lower()
            candidate = (manifest_path, manifest, clip)
            if stem not in seen and hook not in seen:
                fresh.append(candidate)
            else:
                fallback.append(candidate)

    # If a source is not local/source-ready, trying multiple clips from the same
    # manifest only repeats the same blocked downloader path. Keep the first clip
    # per remote-only source for the expensive acquisition pass; source-ready
    # manifests can still publish their remaining clips normally.
    def dedupe_remote_sources(items: list[tuple[Path, dict, dict]]) -> list[tuple[Path, dict, dict]]:
        out: list[tuple[Path, dict, dict]] = []
        seen_remote: set[str] = set()
        for candidate in items:
            _manifest_path, manifest, _clip = candidate
            source_file = ROOT / str(manifest.get("source_file", ""))
            source_ready = source_file.exists() and source_file.stat().st_size > 1000
            key = str(manifest.get("source_url") or manifest.get("source_file") or _manifest_path)
            if not source_ready and key in seen_remote:
                continue
            if not source_ready:
                seen_remote.add(key)
            out.append(candidate)
        return out

    fresh = dedupe_remote_sources(fresh)
    fallback = dedupe_remote_sources(fallback)

    recent_creators = set(recent_uploaded_creators())

    def source_ready_score(candidate: tuple[Path, dict, dict]) -> int:
        _manifest_path, manifest, _clip = candidate
        source_file = ROOT / str(manifest.get("source_file", ""))
        if source_file.exists() and source_file.stat().st_size > 1000:
            return 0
        if manifest.get("fallback_source_url") or manifest.get("archive_source"):
            return 1
        return 2

    def diversity_score(candidate: tuple[Path, dict, dict]) -> tuple[int, int, str]:
        _manifest_path, manifest, _clip = candidate
        creator = _creator_name(manifest).lower()
        repeated = 1 if any(c and c in creator for c in recent_creators) else 0
        return (repeated, source_ready_score(candidate), creator)

    fresh.sort(key=diversity_score)
    fallback.sort(key=diversity_score)
    if fresh:
        return fresh + fallback
    if fallback:
        return fallback
    raise RuntimeError("no reviewed manifest clips available; add/review a new clip manifest")


def select_daily_manifest_clip() -> tuple[Path, dict, dict]:
    return iter_candidate_manifest_clips()[0]


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
    source_url = manifest.get("source_url")
    direct_video_url = False
    if url:
        # Only raw-download actual media/archive URLs. Facebook/YouTube page URLs
        # return HTML if fetched with urllib, which creates corrupt .mp4 files.
        url_l = str(url).lower()
        direct_video_url = any(url_l.split("?", 1)[0].endswith(ext) for ext in (".mp4", ".mov", ".m4v", ".webm")) or "archive.org/download" in url_l
        if direct_video_url:
            tmp = source.with_suffix(source.suffix + ".part")
            with urllib.request.urlopen(url, timeout=180) as resp, tmp.open("wb") as out:
                shutil.copyfileobj(resp, out)
            tmp.replace(source)
            return source

    if source_url and os.getenv("VIRAL_RADAR_DISABLE_DIRECT_YOUTUBE_DOWNLOAD") != "1":
        downloader = ROOT / "scripts" / "download_youtube_source.py"
        logdir = ROOT / "LOGS" / "daily_youtube_source_download" / str(manifest.get("source_video_id") or "unknown")
        cmd = [
            sys.executable, str(downloader), source_url,
            "--outdir", str(source.parent),
            "--logdir", str(logdir),
            "--skip-cleanup",
            "--no-ytdlp",
            "--try-pytubefix",
            "--oauth",
            "--pytubefix-client", os.getenv("PYTUBEFIX_CLIENTS", "WEB"),
            "--try-pytube",
        ]
        if manifest.get("fallback_source_url") and direct_video_url:
            cmd += ["--fallback-url", str(manifest["fallback_source_url"])]
        proc = run(cmd)
        if proc.returncode != 0:
            raise RuntimeError(json.dumps({
                "source_download_failed": source_url,
                "stdout_tail": proc.stdout[-2000:],
                "stderr_tail": proc.stderr[-2000:],
                "logs": str(logdir),
            }, indent=2))
        payload = parse_json_output(proc.stdout)
        downloaded = Path(payload.get("path", ""))
        if downloaded.exists():
            downloaded.replace(source)
            return source
    if source_url:
        raise RuntimeError("direct YouTube/Rumble downloading is disabled by VIRAL_RADAR_DISABLE_DIRECT_YOUTUBE_DOWNLOAD=1; use external provider APIs or local/Drive source media")
    raise RuntimeError("manifest source missing and no fallback/local source is available")


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
        upload_payload = parse_json_output(proc.stdout)
        upload_payload["creator"] = manifest.get("creator") or manifest.get("channel") or "source creator"
        upload_payload["source_url"] = manifest.get("source_url", "")
        uploads.append(upload_payload)
        # Append enriched row because the shared uploader log historically did
        # not include source creator, which caused the cron to repeat Huberman.
        enriched_log = ROOT / "UPLOADS" / "viral_radar_enriched_uploads.jsonl"
        enriched_log.parent.mkdir(parents=True, exist_ok=True)
        with enriched_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(upload_payload, ensure_ascii=False) + "\n")
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
        seed_result = seed_latest_manifests()
        candidates = iter_candidate_manifest_clips()
        max_attempts = int(os.getenv("VIRAL_RADAR_MAX_SOURCE_ATTEMPTS", "8"))
        source_failures = []
        for manifest_path, manifest, selected_clip in candidates[:max_attempts]:
            single_manifest = write_single_clip_manifest(manifest_path, manifest, selected_clip, local_day)
            try:
                source = ensure_source(manifest)
                if source_failures and _is_evergreen_fallback_creator(manifest) and os.getenv("VIRAL_RADAR_ALLOW_EVERGREEN_FALLBACK") != "1":
                    source_failures.append({
                        "manifest": str(single_manifest),
                        "selected_from_manifest": str(manifest_path),
                        "selected_hook": selected_clip.get("hook"),
                        "source_url": manifest.get("source_url"),
                        "skipped_reason": "evergreen Huberman/NASA fallback suppressed so cron does not keep publishing the same influencer while other influencer sources are blocked",
                    })
                    continue
                break
            except Exception as source_exc:
                failure = {
                    "manifest": str(single_manifest),
                    "selected_from_manifest": str(manifest_path),
                    "selected_hook": selected_clip.get("hook"),
                    "source_error": str(source_exc),
                    "source_url": manifest.get("source_url"),
                }
                source_failures.append(failure)
                if os.getenv("VIRAL_RADAR_USE_EXTERNAL_PROVIDER") == "1":
                    provider_result = external_clip_fallback(manifest_path, manifest, selected_clip)
                    provider_path_raw = str(provider_result.get("path") or "")
                    provider_path = Path(provider_path_raw) if provider_path_raw else Path("/__no_provider_clip__")
                    if provider_path.is_file() and provider_path.stat().st_size > 1000:
                        uploads = upload_rendered([{"output": str(provider_path)}], manifest, selected_clip)
                        result = {
                            "job": "viral_radar_daily_upload",
                            "status": "ok_external_provider",
                            "manifest": str(single_manifest),
                            "selected_from_manifest": str(manifest_path),
                            "selected_hook": selected_clip.get("hook"),
                            "seed_result": seed_result,
                            "prior_source_failures": source_failures[:-1],
                            "external_provider": provider_result,
                            "uploads": uploads,
                            "cleanup": "external provider MP4 preserved for audit; upload logged after verified YouTube response",
                        }
                        marker.parent.mkdir(parents=True, exist_ok=True)
                        marker.write_text(json.dumps({
                            "completed_at": dt.datetime.now(dt.UTC).isoformat(),
                            "result": result,
                        }, indent=2), encoding="utf-8")
                        print(json.dumps(result, indent=2))
                        return 0
                    failure["external_provider"] = provider_result
                continue
        else:
            print(json.dumps({
                "job": "viral_radar_daily_upload",
                "status": "blocked_source_all_candidates",
                "seed_result": seed_result,
                "attempted_candidates": len(source_failures),
                "source_failures": source_failures,
                "next_step": "No usable source media after trying multiple manifests. Add YouTube cookies/residential proxy/local MP4 source, or use the pytubefix/yt-dlp direct downloader path. Opus Clips is intentionally disabled. This exits nonzero so cron no longer reports discovery-only work as success.",
            }, indent=2))
            return 2

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
            "seed_result": seed_result,
            "prior_source_failures": source_failures,
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

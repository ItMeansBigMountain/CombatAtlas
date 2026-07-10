#!/usr/bin/env python3
"""Daily public Viral Radar influencer Shorts upload pipeline for cron.

Procedure: discover videos from the configured creator watchlist, clip the exact
found influencer video into multiple vertical Shorts, and upload those clips.
Do not use NASA/space/unknown placeholder filler to satisfy minimums.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import re
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("/opt/data/HeRmEz/projects/viral-clip-radar")
UPLOAD_QUEUE = ROOT / "UPLOAD_QUEUE"
DEFAULT_MANIFEST = ROOT / "CLIP_PLANS" / "2026-06-04-huberman-motivation-great-find" / "clip_manifest.json"
MANIFEST = Path(os.getenv("VIRAL_RADAR_MANIFEST", str(DEFAULT_MANIFEST)))
RENDER = ROOT / "scripts" / "render_clip_manifest.py"
UPLOAD = ROOT / "scripts" / "upload_to_youtube.py"
SEED_LATEST = ROOT / "scripts" / "seed_latest_longform_manifests.py"
EXTERNAL_PROVIDER = ROOT / "scripts" / "external_clip_provider.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    # Viral Radar influencer clips prefer Classical Echos. If that channel hits
    # YouTube's account upload limit, the upload wrapper may fail over to the
    # Trapiistan/Sosai token so rendered real creator clips can keep publishing.
    # Override inherited faceless/newsletter token values for the primary lane.
    env["YOUTUBE_UPLOAD_TOKEN"] = "/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json"
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
    min_clips = os.getenv("VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM", os.getenv("VIRAL_RADAR_MIN_UPLOADS", "10"))
    env = os.environ.copy()
    # Viral Radar discovery/read scopes should use the same Classical Echos lane
    # token as upload unless an explicit discovery override is provided. Do not
    # fall back to Trapiistan here; cross-lane token defaults caused recurring
    # wrong-channel/auth confusion.
    env["YOUTUBE_UPLOAD_TOKEN"] = os.getenv("YOUTUBE_DISCOVERY_TOKEN") or "/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json"
    proc = subprocess.run(
        [sys.executable, str(SEED_LATEST), "--clips-per-video", min_clips, "--max-videos-per-channel", "50"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=env,
    )
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


def normalized_upload_key(value: str) -> str:
    stem = Path(str(value or "")).stem.lower()
    for suffix in ("-captioned-daily", "-captioned-cron", "-captioned", "-daily", "-cron"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return stem.strip()


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
        stem = normalized_upload_key(path)
        if stem:
            keys.add(stem)
        if title:
            keys.add(title.lower().strip())
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
    priority_manifests = priority_plan_manifests()
    priority_set = set(priority_manifests)
    strict_discovered_only = os.getenv("VIRAL_RADAR_STRICT_DISCOVERED_ONLY", "1") != "0"
    if os.getenv("VIRAL_RADAR_MANIFEST"):
        manifests = [MANIFEST]
    elif priority_manifests and strict_discovered_only:
        # User procedure: for discovery-triggered runs, clip/upload the actual
        # videos found by the Viral Radar data pipeline. Do not fall back to old
        # manifests/placeholders just to hit a quota/minimum.
        manifests = priority_manifests
    else:
        manifests = priority_manifests + [
            p for p in sorted((ROOT / "CLIP_PLANS").glob("*/clip_manifest.json"), reverse=True)
            if p not in priority_set
        ]
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
            stem = normalized_upload_key(clip.get("captioned_file") or clip.get("file") or "")
            hook = str(clip.get("hook") or "").lower().strip()
            candidate = (manifest_path, manifest, clip)
            if stem and stem in seen:
                continue
            if hook and hook in seen:
                continue
            fresh.append(candidate)

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

    if not priority_manifests:
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


def slugify(value: str, max_len: int = 72) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return (value[:max_len].strip("-") or "clip")


def parse_time_to_seconds(value: str | None, fallback: int = 45) -> int:
    if not value:
        return fallback
    try:
        parts = [float(p) for p in str(value).split(":")]
        if len(parts) == 3:
            return int(parts[0] * 3600 + parts[1] * 60 + parts[2])
        if len(parts) == 2:
            return int(parts[0] * 60 + parts[1])
        return int(parts[0])
    except Exception:
        return fallback


def format_seconds(seconds: int) -> str:
    seconds = max(1, int(seconds))
    return f"00:{seconds // 60:02d}:{seconds % 60:02d}"

def _clean_words(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'’-]{2,}", text.lower())
    stop = {
        "this", "that", "with", "from", "they", "them", "what", "when", "where", "were", "your", "youre",
        "about", "after", "before", "have", "has", "had", "into", "over", "under", "because", "there",
        "their", "would", "could", "should", "people", "someone", "thing", "things", "really", "going",
        "will", "just", "dont", "doesnt", "isnt", "cant", "than", "then", "also", "very",
    }
    return [w.strip("'’-") for w in words if w not in stop]


def make_public_packaging(creator: str, source_title: str, window_text: str, idx: int = 1) -> dict[str, str]:
    seed = re.sub(r"\s+", " ", (window_text or source_title or "")).strip()
    words = []
    for w in _clean_words(seed):
        if w not in words:
            words.append(w)
        if len(words) >= 4:
            break
    title_l = source_title.lower()
    seed_l = seed.lower()
    if any(x in title_l or x in seed_l for x in ["sex", "dating", "women", "men", "desire", "attraction", "bedroom"]):
        templates = ["The Desire Gap Nobody Admits", "Why Attraction Gets Messy Fast", "The Bedroom Truth People Dodge", "Men, Women, and the Awkward Truth"]
    elif any(x in title_l or x in seed_l for x in ["money", "business", "sales", "entrepreneur", "broke", "rich"]):
        templates = ["The Money Mistake That Looks Smart", "Why Most Hustlers Stay Broke", "The Business Trap Nobody Warns You About", "This Is Where Winners Separate"]
    elif any(x in title_l or x in seed_l for x in ["fat", "muscle", "fitness", "hormone", "diet", "body"]):
        templates = ["The Body Hack Nobody Wants to Hear", "Why Your Fitness Plan Feels Rigged", "The Physique Lie That Keeps You Stuck", "This Is Why Discipline Gets Ugly"]
    else:
        templates = ["The Uncomfortable Truth Hiding Here", "This Sounds Wrong Until It Clicks", "The Part They Say Quietly", "Why This Hits Harder Than Expected"]
    angle = templates[(idx - 1) % len(templates)]
    clean_source = re.sub(r"[^A-Za-z0-9 ,'-]", " ", source_title).strip()
    clean_source = re.sub(r"\s+", " ", clean_source)
    if words:
        public_subtitle = " / ".join(w.title() for w in words[:3])
        specific = " ".join(w.title() for w in words[:4])
    else:
        public_subtitle = clean_source[:54] or f"Moment {idx}"
        specific = clean_source[:42] or f"Moment {idx}"
    creator_prefix = re.sub(r"[^A-Za-z0-9 ]", " ", creator).strip().split()
    creator_prefix = " ".join(creator_prefix[:2])
    base_title = f"{creator_prefix}: {specific}" if creator_prefix else specific
    public_title = f"{base_title} — {angle}"
    return {"hook": public_title[:118], "public_title": public_title[:90], "public_subtitle": public_subtitle[:90]}


def build_relevant_hashtags(*texts: str, max_topic_tags: int = 5) -> list[str]:
    """Build description hashtags from title/transcript/context, not static filler."""
    blob = " ".join(t for t in texts if t).lower()
    tag_rules = [
        (("sex", "dating", "women", "men", "desire", "attraction", "bedroom", "relationships"), ["DatingAdvice", "Relationships", "Attraction", "MaleFemaleDynamics"]),
        (("money", "business", "sales", "entrepreneur", "broke", "rich", "profit", "customer"), ["Business", "Entrepreneurship", "Sales", "MoneyMindset"]),
        (("fat", "fatloss", "muscle", "fitness", "hormone", "diet", "body", "testosterone", "lean"), ["Fitness", "FatLoss", "Muscle", "Hormones"]),
        (("discipline", "confidence", "mindset", "focus", "motivation", "habits", "self improvement"), ["SelfImprovement", "Mindset", "Discipline", "Motivation"]),
        (("dog", "calm", "assertive", "cesar", "training"), ["DogTraining", "CalmEnergy", "Leadership"]),
        (("numerology", "lifepath", "astrology", "spiritual"), ["Numerology", "LifePath", "Spirituality"]),
        (("dopamine", "brain", "neuroscience", "huberman", "sleep", "protocol"), ["Neuroscience", "Huberman", "Health", "Dopamine"]),
    ]
    tokens = set(re.findall(r"[a-z0-9]+", blob))
    def matches(needle: str) -> bool:
        return (" " in needle and needle in blob) or needle in tokens

    topic_tags: list[str] = []
    for needles, tags in tag_rules:
        if any(matches(n) for n in needles):
            for tag in tags:
                if tag not in topic_tags:
                    topic_tags.append(tag)
    for w in _clean_words(blob):
        if len(topic_tags) >= max_topic_tags:
            break
        if len(w) >= 4:
            tag = re.sub(r"[^A-Za-z0-9]", "", w.title())[:28]
            if tag and tag not in topic_tags and tag.lower() not in {"shorts", "viral", "radar"}:
                topic_tags.append(tag)
    return ["Shorts", *topic_tags[:max_topic_tags], "ViralRadar"]


def build_youtube_tags(hashtags: list[str]) -> str:
    tags = ["shorts", "viral radar", "clip analysis"]
    for tag in hashtags:
        plain = re.sub(r"(?<!^)([A-Z])", r" \1", tag).lower().strip()
        if plain not in tags:
            tags.append(plain)
    return ",".join(tags[:12])


def auto_clip_manifest_from_plan(plan_dir: Path) -> Path | None:
    """Create a minimal reviewed manifest for a newly discovered watchlist plan.

    The watchlist poller creates source_metadata.json immediately. This lets the
    discovery cron clip/render/upload the found video right away instead of
    waiting for a separate manual manifest pass. The render still adds a hook
    overlay and the uploader adds source attribution, so this is not a raw
    reupload.
    """
    manifest_path = plan_dir / "clip_manifest.json"
    if manifest_path.exists():
        return manifest_path
    metadata_path = plan_dir / "source_metadata.json"
    if not metadata_path.exists():
        return None
    meta = json.loads(metadata_path.read_text(encoding="utf-8"))
    video_id = str(meta.get("video_id") or "").strip()
    source_url = str(meta.get("url") or meta.get("source_url") or "").strip()
    title = str(meta.get("title") or "Creator clip").strip()
    creator = str(meta.get("channel_name") or meta.get("creator") or meta.get("channel") or "Creator").strip()
    if not video_id and "youtu" in source_url:
        video_id = source_url.rsplit("/", 1)[-1].split("?", 1)[0].split("&", 1)[0]
    if not source_url:
        return None
    duration = parse_time_to_seconds(str(meta.get("duration") or meta.get("duration_seconds") or ""), 45)
    stem = slugify(f"{creator}-{title}", 64)
    min_clips = max(10, int(os.getenv("VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM", os.getenv("VIRAL_RADAR_MIN_UPLOADS", "10"))))
    max_clips = min(50, max(min_clips, int(os.getenv("VIRAL_RADAR_MAX_CLIPS_PER_SOURCE", "50"))))
    is_short_source = "/shorts/" in source_url or duration <= 75
    # Shorts cannot always provide 3 distinct moments, but every long-form source
    # must produce at least 3 and may produce up to 50 based on duration/opportunity.
    clip_count = 1 if is_short_source else min(max(min_clips, max(3, duration // 300)), max_clips)
    clip_len = min(max(duration, 12), 58) if is_short_source else 45
    clips = []
    usable_span = max(clip_len, duration - clip_len)
    for idx in range(clip_count):
        if is_short_source:
            start_seconds = 0
        elif clip_count == 1:
            start_seconds = max(0, min(duration - clip_len, duration // 3))
        else:
            # Spread candidate clips across the source so long interviews produce
            # multiple distinct uploads. Transcript-aware seeded manifests can
            # override these with better exact moments; this is the fallback.
            start_seconds = int((usable_span * idx) / max(1, clip_count - 1))
            start_seconds = max(0, min(start_seconds, max(0, duration - clip_len)))
        end_seconds = min(duration, start_seconds + clip_len)
        label = f"auto-{idx+1:02d}"
        packaging = make_public_packaging(creator, title, str(meta.get("description") or ""), idx + 1)
        clips.append({
            "file": f"EXPORTS/{stem}-{label}.mp4",
            "captioned_file": f"EXPORTS/{stem}-{label}-captioned.mp4",
            "start": format_seconds(start_seconds),
            "end": format_seconds(end_seconds),
            "hook": packaging["hook"],
            "public_title": packaging["public_title"],
            "public_subtitle": packaging["public_subtitle"],
            "context": f"{packaging['public_subtitle']} from {title}",
        })
    manifest = {
        "creator": creator,
        "source_title": title,
        "source_url": source_url,
        "source_video_id": video_id or stem,
        "source_file": f"SOURCES/{video_id or stem}/source.mp4",
        "auto_generated_from_watchlist": True,
        "clips": clips,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path


def priority_plan_manifests() -> list[Path]:
    raw = os.getenv("VIRAL_RADAR_PRIORITY_PLANS", "").strip()
    if not raw:
        return []
    manifests: list[Path] = []
    for item in raw.split(os.pathsep):
        if not item.strip():
            continue
        plan = Path(item.strip())
        if not plan.is_absolute():
            plan = ROOT / plan
        manifest = plan if plan.name == "clip_manifest.json" else auto_clip_manifest_from_plan(plan)
        if manifest and manifest.exists() and manifest not in manifests:
            manifests.append(manifest)
    return manifests


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


def local_upload_day() -> str:
    return dt.datetime.now(ZoneInfo("America/Chicago")).date().isoformat()


def daily_upload_cap() -> int:
    # Official YouTube Data API docs list videos.insert at 100 calls/day in the
    # Video Uploads bucket. User preference is to probe up to that documented
    # ceiling and only stop when YouTube actually rate-limits the channel; failed
    # uploads are queued for the next workflow run.
    return max(1, int(os.getenv("VIRAL_RADAR_DAILY_UPLOAD_CAP", "100")))


def uploaded_count_for_day(day: str | None = None) -> int:
    day = day or local_upload_day()
    log = ROOT / "UPLOADS" / "youtube_uploads.jsonl"
    if not log.exists():
        return 0
    count = 0
    for line in log.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
            uploaded_at = row.get("uploaded_at")
            if not uploaded_at:
                continue
            row_day = dt.datetime.fromisoformat(uploaded_at).astimezone(ZoneInfo("America/Chicago")).date().isoformat()
            if row_day == day and row.get("privacy") == "public":
                count += 1
        except Exception:
            continue
    return count


def upload_capacity_remaining() -> int:
    return max(0, daily_upload_cap() - uploaded_count_for_day())


def queue_failed_upload(output: Path, *, title: str, description: str, tags: str, manifest: dict, selected_clip: dict | None, proc: subprocess.CompletedProcess[str]) -> dict:
    UPLOAD_QUEUE.mkdir(parents=True, exist_ok=True)
    signature = (str(manifest.get("source_url") or ""), str((selected_clip or {}).get("hook") or ""), title)
    for existing_meta in UPLOAD_QUEUE.glob("*.upload.json"):
        try:
            existing = json.loads(existing_meta.read_text(encoding="utf-8"))
            existing_sig = (str(existing.get("source_url") or ""), str(existing.get("selected_hook") or ""), str(existing.get("title") or ""))
            if existing_sig == signature:
                if output.exists():
                    output.unlink()
                return {"queued_file": str(existing.get("file") or ""), "queue_metadata": str(existing_meta), "queued_for_next_run": True, "duplicate_queue_item": True}
        except Exception:
            continue
    queued_file = UPLOAD_QUEUE / output.name
    if output.exists() and output.resolve() != queued_file.resolve():
        if queued_file.exists():
            queued_file = UPLOAD_QUEUE / f"{dt.datetime.now(dt.UTC).strftime('%Y%m%d%H%M%S')}-{output.name}"
        shutil.move(str(output), str(queued_file))
    meta = {
        "queued_at": dt.datetime.now(dt.UTC).isoformat(),
        "file": str(queued_file),
        "title": title,
        "description": description,
        "tags": tags,
        "privacy": "public",
        "creator": manifest.get("creator") or manifest.get("channel") or "source creator",
        "source_url": manifest.get("source_url", ""),
        "source_title": manifest.get("source_title", ""),
        "selected_hook": (selected_clip or {}).get("hook"),
        "last_error": {
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
            "blocked_upload_quota": "exceeded the number of videos" in (proc.stderr + proc.stdout).lower(),
        },
    }
    meta_path = queued_file.with_suffix(queued_file.suffix + ".upload.json")
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"queued_file": str(queued_file), "queue_metadata": str(meta_path), "queued_for_next_run": True}


def append_enriched_upload(upload_payload: dict, manifest: dict) -> None:
    upload_payload["creator"] = manifest.get("creator") or manifest.get("channel") or "source creator"
    upload_payload["source_url"] = manifest.get("source_url", "")
    enriched_log = ROOT / "UPLOADS" / "viral_radar_enriched_uploads.jsonl"
    enriched_log.parent.mkdir(parents=True, exist_ok=True)
    with enriched_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(upload_payload, ensure_ascii=False) + "\n")


def upload_pending_queue(limit: int | None = None) -> list[dict]:
    uploads: list[dict] = []
    if not UPLOAD_QUEUE.exists():
        return uploads
    metas = sorted(UPLOAD_QUEUE.glob("*.upload.json"), key=lambda p: p.stat().st_mtime)
    if limit is not None:
        metas = metas[:max(0, limit)]
    for meta_path in metas:
        if upload_capacity_remaining() <= 0:
            break
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        file_path = Path(meta.get("file") or "")
        if not file_path.exists():
            meta_path.unlink(missing_ok=True)
            continue
        proc = run([
            sys.executable, str(UPLOAD),
            "--file", str(file_path),
            "--title", str(meta.get("title") or file_path.stem)[:95],
            "--description", str(meta.get("description") or ""),
            "--tags", str(meta.get("tags") or "shorts,viral radar"),
            "--privacy", str(meta.get("privacy") or "public"),
        ])
        if proc.returncode != 0:
            meta["last_attempt_at"] = dt.datetime.now(dt.UTC).isoformat()
            meta["last_error"] = {"returncode": proc.returncode, "stdout_tail": proc.stdout[-2000:], "stderr_tail": proc.stderr[-2000:], "blocked_upload_quota": "exceeded the number of videos" in (proc.stderr + proc.stdout).lower()}
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            break
        payload = parse_json_output(proc.stdout)
        payload["creator"] = meta.get("creator") or "source creator"
        payload["source_url"] = meta.get("source_url") or ""
        uploads.append(payload)
        enriched_log = ROOT / "UPLOADS" / "viral_radar_enriched_uploads.jsonl"
        enriched_log.parent.mkdir(parents=True, exist_ok=True)
        with enriched_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        meta_path.unlink(missing_ok=True)
    return uploads


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
        context = str(
            (selected_clip or {}).get("summary")
            or (selected_clip or {}).get("context")
            or manifest.get("transcript_summary")
            or manifest.get("source_description")
            or ""
        ).strip()
        public_title = str((selected_clip or {}).get("public_title") or "").strip()
        public_subtitle = str((selected_clip or {}).get("public_subtitle") or "").strip()
        title_seed = public_title or hook.strip() or output.stem.replace("-", " ").title()
        # Hashtags belong in tags/description, not the title. Never publish internal
        # planning labels like "the part people will replay".
        title = re.sub(r"\s*#\w+", "", title_seed).replace("the part people will replay", "").strip()[:95]
        if not title:
            creator_name = str(manifest.get('creator') or 'Creator').strip()
            source_name = re.sub(r"[^A-Za-z0-9 ,'-]", " ", str(manifest.get('source_title') or output.stem)).strip()
            title = f"{creator_name}: {source_name}"[:95]
        context_line = public_subtitle or context[:600]
        source_url = str(manifest.get('source_url') or '').strip()
        description_parts = [title]
        if context_line:
            description_parts += ["", context_line]
        description_parts += [
            "",
            "Source:",
            f"{manifest.get('creator','source creator')} — {manifest.get('source_title','source footage')}",
        ]
        if source_url:
            # Keep the original URL on its own line so YouTube renders it as a clear hyperlink.
            description_parts += ["", "Original source:", source_url]
        hashtags = build_relevant_hashtags(
            title,
            public_subtitle,
            context,
            hook,
            str(manifest.get('source_title') or ''),
            str((selected_clip or {}).get('transcript_excerpt') or ''),
            str(manifest.get('transcript_summary') or ''),
        )
        description_parts += [
            "",
            "Edited with vertical framing, burned captions, context, and source attribution.",
            "",
            " ".join(f"#{tag}" for tag in hashtags),
        ]
        description = "\n".join(description_parts)
        cmd = [
            sys.executable, str(UPLOAD),
            "--file", str(output),
            "--title", title,
            "--description", description,
            "--tags", build_youtube_tags(hashtags),
            "--privacy", "public",
        ]
        tags = build_youtube_tags(hashtags)
        if upload_capacity_remaining() <= 0:
            proc = subprocess.CompletedProcess(cmd, 1, "", f"daily upload safety cap reached: {uploaded_count_for_day()}/{daily_upload_cap()}")
            queued = queue_failed_upload(output, title=title, description=description, tags=tags, manifest=manifest, selected_clip=selected_clip, proc=proc)
            raise RuntimeError(json.dumps({
                "upload_deferred_for": str(output),
                "queued_for_next_run": True,
                **queued,
                "daily_upload_cap": daily_upload_cap(),
                "uploaded_today": uploaded_count_for_day(),
                "reason": "daily_upload_safety_cap_reached",
            }, indent=2))
        proc = run(cmd)
        if proc.returncode != 0:
            queued = queue_failed_upload(output, title=title, description=description, tags=tags, manifest=manifest, selected_clip=selected_clip, proc=proc)
            error_blob = proc.stderr[-4000:] + proc.stdout[-1000:]
            raise RuntimeError(json.dumps({
                "upload_failed_for": str(output),
                "returncode": proc.returncode,
                "stdout_tail": proc.stdout[-2000:],
                "stderr_tail": proc.stderr[-2000:],
                "queued_for_next_run": True,
                **queued,
                "blocked_upload_quota": "exceeded the number of videos" in error_blob.lower(),
            }, indent=2))
        upload_payload = parse_json_output(proc.stdout)
        append_enriched_upload(upload_payload, manifest)
        uploads.append(upload_payload)
    return uploads


def main() -> int:
    local_day = dt.datetime.now(ZoneInfo("America/Chicago")).date().isoformat()
    marker = ROOT / "STATE" / f"viral_radar_daily_upload_{local_day}.done"
    queue_has_items = UPLOAD_QUEUE.exists() and any(UPLOAD_QUEUE.glob("*.upload.json"))
    if marker.exists() and os.getenv("FORCE_UPLOAD") != "1" and not queue_has_items:
        print(json.dumps({
            "job": "viral_radar_daily_upload",
            "status": "skipped_already_ran_today",
            "local_day": local_day,
            "marker": str(marker),
            "override": "set FORCE_UPLOAD=1 to bypass",
        }, indent=2))
        return 0
    try:
        min_uploads = max(10, int(os.getenv("VIRAL_RADAR_MIN_UPLOADS", os.getenv("VIRAL_RADAR_MIN_CLIPS_PER_LONGFORM", "10"))))
        upload_queue_first = os.getenv("VIRAL_RADAR_UPLOAD_QUEUE_FIRST", "1") != "0"
        queued_uploads = upload_pending_queue(limit=min_uploads) if upload_queue_first else []
        seed_result = seed_latest_manifests()
        candidates = iter_candidate_manifest_clips()
        max_attempts = max(min_uploads, int(os.getenv("VIRAL_RADAR_MAX_SOURCE_ATTEMPTS", "50")))
        source_failures = []
        render_failures = []
        uploaded_batches = []
        all_uploads = list(queued_uploads)
        rendered_total = 0
        source_cleanup = []
        used_sources: set[str] = set()

        for manifest_path, manifest, selected_clip in candidates[:max_attempts]:
            if len(all_uploads) >= min_uploads:
                break
            single_manifest = write_single_clip_manifest(manifest_path, manifest, selected_clip, local_day)
            try:
                source = ensure_source(manifest)
                used_sources.add(str(source))
                if source_failures and _is_evergreen_fallback_creator(manifest) and os.getenv("VIRAL_RADAR_ALLOW_EVERGREEN_FALLBACK") != "1":
                    source_failures.append({
                        "manifest": str(single_manifest),
                        "selected_from_manifest": str(manifest_path),
                        "selected_hook": selected_clip.get("hook"),
                        "source_url": manifest.get("source_url"),
                        "skipped_reason": "evergreen Huberman/NASA fallback suppressed so cron does not keep publishing the same influencer while other influencer sources are blocked",
                    })
                    continue
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
                        all_uploads.extend(uploads)
                        uploaded_batches.append({
                            "mode": "external_provider",
                            "manifest": str(single_manifest),
                            "selected_from_manifest": str(manifest_path),
                            "selected_hook": selected_clip.get("hook"),
                            "uploads": uploads,
                            "external_provider": provider_result,
                        })
                    else:
                        failure["external_provider"] = provider_result
                continue

            render_proc = run([sys.executable, str(RENDER), str(single_manifest), "--suffix=-daily", "--keep-source"])
            if render_proc.returncode != 0:
                render_failures.append({
                    "manifest": str(single_manifest),
                    "selected_from_manifest": str(manifest_path),
                    "selected_hook": selected_clip.get("hook"),
                    "source": str(source),
                    "returncode": render_proc.returncode,
                    "stdout_tail": render_proc.stdout[-2000:],
                    "stderr_tail": render_proc.stderr[-2000:],
                })
                continue
            render_payload = parse_json_output(render_proc.stdout)
            uploads = upload_rendered(render_payload.get("rendered", []), manifest, selected_clip)
            rendered_total += len(render_payload.get("rendered", []))
            all_uploads.extend(uploads)
            source_cleanup.extend(render_payload.get("source_cleanup") or [])
            uploaded_batches.append({
                "manifest": str(single_manifest),
                "selected_from_manifest": str(manifest_path),
                "selected_hook": selected_clip.get("hook"),
                "rendered_count": len(render_payload.get("rendered", [])),
                "uploads": uploads,
            })

        if len(all_uploads) < min_uploads:
            print(json.dumps({
                "job": "viral_radar_daily_upload",
                "status": "blocked_min_uploads_not_met",
                "min_uploads": min_uploads,
                "uploaded_count": len(all_uploads),
                "queued_replay_uploaded_count": len(queued_uploads),
                "remaining_queue_count": len(list(UPLOAD_QUEUE.glob("*.upload.json"))) if UPLOAD_QUEUE.exists() else 0,
                "seed_result": seed_result,
                "uploaded_batches": uploaded_batches,
                "source_failures": source_failures,
                "render_failures": render_failures,
                "next_step": "Cron must publish at least the configured minimum. Add source-ready manifests/cookies/proxy/local MP4s, or increase candidate source reliability.",
            }, indent=2))
            return 2

        result = {
            "job": "viral_radar_daily_upload",
            "status": "ok",
            "min_uploads": min_uploads,
            "uploaded_count": len(all_uploads),
            "queued_replay_uploaded_count": len(queued_uploads),
            "remaining_queue_count": len(list(UPLOAD_QUEUE.glob("*.upload.json"))) if UPLOAD_QUEUE.exists() else 0,
            "seed_result": seed_result,
            "prior_source_failures": source_failures,
            "render_failures": render_failures,
            "rendered_count": rendered_total,
            "uploaded_batches": uploaded_batches,
            "uploads": all_uploads,
            "source_cleanup": source_cleanup,
            "cleanup": "rendered exports deleted by uploader after successful public upload; sources kept during batch so multiple clips can be produced from the same long-form source",
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


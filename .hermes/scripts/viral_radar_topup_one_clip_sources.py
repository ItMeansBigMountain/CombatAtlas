#!/usr/bin/env python3
"""Top up Viral Radar sources that only received one public upload.

Finds source_url groups in viral_radar_enriched_uploads.jsonl with fewer than the
requested minimum and uploads additional clips from their existing manifest until
that source reaches the target. Intended for user-requested backfill after old
one-clip Viral Radar runs.
"""
from __future__ import annotations
import datetime as dt
import importlib.util
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/opt/data/HeRmEz/projects/viral-clip-radar')
PIPELINE_PATH = Path('/opt/data/scripts/viral_radar_daily_upload.py')
LOG = ROOT / 'UPLOADS' / 'viral_radar_enriched_uploads.jsonl'

TARGET_MIN = max(10, int(os.getenv('VIRAL_RADAR_TOPUP_MIN_PER_SOURCE', '10')))
MAX_PER_SOURCE = min(50, max(TARGET_MIN, int(os.getenv('VIRAL_RADAR_MAX_CLIPS_PER_SOURCE', '50'))))
MAX_SOURCES = int(os.getenv('VIRAL_RADAR_TOPUP_MAX_SOURCES', '999'))
MAX_UPLOADS = int(os.getenv('VIRAL_RADAR_TOPUP_MAX_UPLOADS', '999'))
INCLUDE_SHORTS = os.getenv('VIRAL_RADAR_TOPUP_INCLUDE_SHORTS') == '1'

spec = importlib.util.spec_from_file_location('vr_pipeline', PIPELINE_PATH)
vr = importlib.util.module_from_spec(spec)
sys.modules['vr_pipeline'] = vr
assert spec and spec.loader
spec.loader.exec_module(vr)


def rows() -> list[dict]:
    out=[]
    if LOG.exists():
        for line in LOG.read_text(encoding='utf-8', errors='ignore').splitlines():
            try: out.append(json.loads(line))
            except Exception: pass
    return out


def is_short_source(url: str, manifest: dict) -> bool:
    if '/shorts/' in url:
        return True
    dur = manifest.get('duration_seconds') or manifest.get('source_duration_seconds') or 0
    try:
        return int(float(dur)) <= 75 and int(float(dur)) > 0
    except Exception:
        return False


def source_counts() -> dict[str, list[dict]]:
    by=defaultdict(list)
    for r in rows():
        src = r.get('source_url')
        if src:
            by[src].append(r)
    return by


def find_manifests_by_source() -> dict[str, Path]:
    found={}
    for p in ROOT.glob('CLIP_PLANS/*/clip_manifest.json'):
        try: m=json.loads(p.read_text(encoding='utf-8'))
        except Exception: continue
        src = str(m.get('source_url') or '').strip()
        if src and src not in found:
            found[src]=p
    return found


def clip_signature(clip: dict) -> str:
    return str(clip.get('captioned_file') or clip.get('file') or clip.get('hook') or '')


def already_uploaded_clip_indices(manifest: dict, uploaded_count: int) -> set[int]:
    # Old enriched logs did not preserve clip indexes. Treat the first N manifest
    # clips as already consumed for that source, then top up from later windows.
    return set(range(max(0, uploaded_count)))


def seconds_to_ts(seconds: int) -> str:
    seconds = max(0, int(seconds))
    return f"00:{seconds // 60:02d}:{seconds % 60:02d}" if seconds < 3600 else f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"


def ffprobe_duration(path: Path) -> int:
    proc = vr.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nk=1:nw=1', str(path)])
    try:
        return max(1, int(float(proc.stdout.strip())))
    except Exception:
        return 180


def expand_clips_if_needed(manifest: dict, source: Path, target: int) -> None:
    clips = manifest.setdefault('clips', [])
    if len(clips) >= target:
        return
    duration = ffprobe_duration(source)
    clip_len = min(55, max(20, duration // max(target + 1, 4)))
    usable = max(clip_len, duration - clip_len)
    creator = manifest.get('creator') or manifest.get('channel') or 'Creator'
    source_title = manifest.get('source_title') or manifest.get('title') or 'Source video'
    stem = vr.slugify(f"{creator}-{source_title}", 64)
    existing = len(clips)
    for idx in range(existing, target):
        if target == 1:
            start = 0
        else:
            start = int((usable * idx) / max(1, target - 1))
            start = max(0, min(start, max(0, duration - clip_len)))
        end = min(duration, start + clip_len)
        packaging = vr.make_public_packaging(str(creator), str(source_title), str(manifest.get('transcript_summary') or source_title), idx + 1)
        clips.append({
            'file': f'EXPORTS/{stem}-topup-auto-{idx+1:02d}.mp4',
            'captioned_file': f'EXPORTS/{stem}-topup-auto-{idx+1:02d}-captioned.mp4',
            'start': seconds_to_ts(start),
            'end': seconds_to_ts(end),
            'hook': packaging['hook'],
            'public_title': packaging['public_title'],
            'public_subtitle': packaging['public_subtitle'],
            'context': f"{packaging['public_subtitle']} from {source_title}",
        })


def main() -> int:
    local_day = dt.datetime.now(ZoneInfo('America/Chicago')).date().isoformat()
    counts = source_counts()
    manifests = find_manifests_by_source()
    candidates=[]
    for src, uploaded in sorted(counts.items(), key=lambda kv: len(kv[1])):
        if len(uploaded) >= TARGET_MIN:
            continue
        mp = manifests.get(src)
        if not mp:
            continue
        m = json.loads(mp.read_text(encoding='utf-8'))
        if vr._is_evergreen_fallback_creator(m) and os.getenv('VIRAL_RADAR_ALLOW_EVERGREEN_FALLBACK') != '1':
            # User correction: do not top up NASA/space/placeholder evergreen filler.
            # Viral Radar should upload real influencer clips or nothing.
            continue
        if is_short_source(src, m) and not INCLUDE_SHORTS:
            continue
        clips = m.get('clips') or []
        if not clips:
            continue
        candidates.append((src, len(uploaded), mp, m))
    results=[]
    total_uploads=0
    for src, have, mp, manifest in candidates[:MAX_SOURCES]:
        needed = min(MAX_PER_SOURCE, TARGET_MIN) - have
        if needed <= 0:
            continue
        source_result={'source_url': src, 'creator': manifest.get('creator') or manifest.get('channel'), 'source_title': manifest.get('source_title'), 'had': have, 'needed': needed, 'manifest': str(mp), 'uploads': [], 'failures': []}
        try:
            source = vr.ensure_source(manifest)
        except Exception as exc:
            source_result['failures'].append({'stage':'source','error':str(exc)})
            results.append(source_result)
            continue
        expand_clips_if_needed(manifest, source, min(MAX_PER_SOURCE, TARGET_MIN))
        consumed = already_uploaded_clip_indices(manifest, have)
        clips = manifest.get('clips') or []
        for idx, clip in enumerate(clips):
            if total_uploads >= MAX_UPLOADS or len(source_result['uploads']) >= needed:
                break
            if idx in consumed:
                continue
            try:
                single = vr.write_single_clip_manifest(mp, manifest, clip, local_day)
                render_proc = vr.run([sys.executable, str(vr.RENDER), str(single), '--suffix=-topup', '--keep-source'])
                if render_proc.returncode != 0:
                    source_result['failures'].append({'stage':'render','clip_index':idx,'hook':clip.get('hook'),'stderr_tail':render_proc.stderr[-1200:]})
                    continue
                render_payload = vr.parse_json_output(render_proc.stdout)
                uploads = vr.upload_rendered(render_payload.get('rendered', []), manifest, clip)
                source_result['uploads'].extend(uploads)
                total_uploads += len(uploads)
            except Exception as exc:
                source_result['failures'].append({'stage':'upload','clip_index':idx,'hook':clip.get('hook'),'error':str(exc)[:1200]})
        results.append(source_result)
        if total_uploads >= MAX_UPLOADS:
            break
    print(json.dumps({'status':'ok','target_min_per_source':TARGET_MIN,'max_per_source':MAX_PER_SOURCE,'include_shorts':INCLUDE_SHORTS,'candidate_sources':len(candidates),'uploaded_count':total_uploads,'results':results}, indent=2, ensure_ascii=False))
    return 0 if total_uploads or not candidates else 2

if __name__ == '__main__':
    raise SystemExit(main())

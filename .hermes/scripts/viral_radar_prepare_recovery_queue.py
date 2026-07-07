#!/usr/bin/env python3
"""Render and queue missing Viral Radar clips for real creator videos below target.

This does not upload. It prepares real clips from the exact source videos so the
upload workflow can publish them later without substituting placeholders.
"""
from __future__ import annotations
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/opt/data/HeRmEz/projects/viral-clip-radar')
PIPELINE = Path('/opt/data/scripts/viral_radar_daily_upload.py')
TOPUP = Path('/opt/data/scripts/viral_radar_topup_one_clip_sources.py')
TARGET_MIN = max(10, int(os.getenv('VIRAL_RADAR_RECOVERY_TARGET_MIN', '10')))
MAX_SOURCES = int(os.getenv('VIRAL_RADAR_RECOVERY_MAX_SOURCES', '12'))
MAX_RENDERS = int(os.getenv('VIRAL_RADAR_RECOVERY_MAX_RENDERS', '120'))

spec = importlib.util.spec_from_file_location('vr_pipeline', PIPELINE)
vr = importlib.util.module_from_spec(spec); sys.modules['vr_pipeline'] = vr
assert spec and spec.loader; spec.loader.exec_module(vr)

tspec = importlib.util.spec_from_file_location('vr_topup', TOPUP)
topup = importlib.util.module_from_spec(tspec); sys.modules['vr_topup'] = topup
assert tspec and tspec.loader; tspec.loader.exec_module(topup)


def upload_counts() -> dict[str, list[dict]]:
    by = defaultdict(list)
    for log in [ROOT/'UPLOADS/viral_radar_enriched_uploads.jsonl', ROOT/'UPLOADS/youtube_uploads.jsonl']:
        if not log.exists():
            continue
        for line in log.read_text(encoding='utf-8', errors='ignore').splitlines():
            try:
                row = json.loads(line)
            except Exception:
                continue
            src = row.get('source_url')
            if src:
                by[src].append(row)
    return by


def is_real_longform(manifest: dict) -> bool:
    creator = str(manifest.get('creator') or manifest.get('channel') or 'unknown')
    title = str(manifest.get('source_title') or manifest.get('title') or '')
    src = str(manifest.get('source_url') or '')
    blob = f'{creator} {title} {src}'.lower()
    if creator.lower() == 'unknown':
        return False
    if '/shorts/' in src:
        return False
    if any(w in blob for w in ['nasa', 'jpl', 'mars', 'space', 'perseverance']):
        return False
    if vr._is_evergreen_fallback_creator(manifest):
        return False
    return bool(src)


def title_desc_tags(manifest: dict, clip: dict, output: Path) -> tuple[str, str, str]:
    title = str(clip.get('public_title') or clip.get('hook') or output.stem.replace('-', ' ').title())[:95]
    context = str(clip.get('public_subtitle') or clip.get('context') or manifest.get('transcript_summary') or '').strip()
    src = str(manifest.get('source_url') or '').strip()
    creator = manifest.get('creator') or manifest.get('channel') or 'source creator'
    source_title = manifest.get('source_title') or manifest.get('title') or 'source footage'
    hashtags = vr.build_relevant_hashtags(title, context, str(clip.get('hook') or ''), source_title, str(clip.get('transcript_excerpt') or ''), str(manifest.get('transcript_summary') or ''))
    description_parts = [title]
    if context:
        description_parts += ['', context]
    description_parts += ['', 'Source:', f'{creator} — {source_title}']
    if src:
        description_parts += ['', 'Original source:', src]
    description_parts += ['', 'Edited with vertical framing, burned captions, context, and source attribution.', '', ' '.join(f'#{h}' for h in hashtags)]
    return title, '\n'.join(description_parts), vr.build_youtube_tags(hashtags)


def main() -> int:
    counts = upload_counts()
    candidates = []
    for mp in ROOT.glob('CLIP_PLANS/*/clip_manifest.json'):
        try:
            manifest = json.loads(mp.read_text(encoding='utf-8'))
        except Exception:
            continue
        if not is_real_longform(manifest):
            continue
        src = str(manifest.get('source_url') or '')
        have = len(counts.get(src, []))
        if have >= TARGET_MIN:
            continue
        source_path = ROOT / str(manifest.get('source_file') or '')
        source_ready = source_path.exists() and source_path.stat().st_size > 1000
        candidates.append((not source_ready, -mp.stat().st_mtime, have, mp, manifest))
    candidates.sort()

    results = []
    rendered_total = 0
    for _not_ready, _neg_mtime, have, mp, manifest in candidates[:MAX_SOURCES]:
        src = manifest.get('source_url')
        item = {'creator': manifest.get('creator') or manifest.get('channel'), 'source_title': manifest.get('source_title'), 'source_url': src, 'had_uploads': have, 'manifest': str(mp), 'queued': [], 'failures': []}
        try:
            source = vr.ensure_source(manifest)
            topup.expand_clips_if_needed(manifest, source, TARGET_MIN)
            mp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        except Exception as exc:
            item['failures'].append({'stage': 'source_or_expand', 'error': str(exc)[:2000]})
            results.append(item)
            continue
        clips = manifest.get('clips') or []
        local_day = dt.datetime.now(ZoneInfo('America/Chicago')).date().isoformat()
        for idx in range(have, min(TARGET_MIN, len(clips))):
            if rendered_total >= MAX_RENDERS:
                break
            clip = clips[idx]
            try:
                single = vr.write_single_clip_manifest(mp, manifest, clip, local_day)
                render_proc = vr.run([sys.executable, str(vr.RENDER), str(single), '--suffix=-recovery', '--keep-source'])
                if render_proc.returncode != 0:
                    item['failures'].append({'stage': 'render', 'clip_index': idx, 'stderr_tail': render_proc.stderr[-1600:]})
                    continue
                payload = vr.parse_json_output(render_proc.stdout)
                for rendered in payload.get('rendered', []):
                    output = Path(rendered['output'])
                    title, desc, tags = title_desc_tags(manifest, clip, output)
                    fake_proc = subprocess.CompletedProcess(['deferred-upload'], 1, '', 'queued for recovery upload; not attempted in prepare step')
                    queued = vr.queue_failed_upload(output, title=title, description=desc, tags=tags, manifest=manifest, selected_clip=clip, proc=fake_proc)
                    queued['clip_index'] = idx
                    item['queued'].append(queued)
                    rendered_total += 1
            except Exception as exc:
                item['failures'].append({'stage': 'queue', 'clip_index': idx, 'error': str(exc)[:2000]})
        results.append(item)
        if rendered_total >= MAX_RENDERS:
            break
    print(json.dumps({'status': 'ok', 'target_min': TARGET_MIN, 'max_sources': MAX_SOURCES, 'rendered_queued_count': rendered_total, 'results': results}, indent=2, ensure_ascii=False))
    return 0 if rendered_total or results else 2

if __name__ == '__main__':
    raise SystemExit(main())

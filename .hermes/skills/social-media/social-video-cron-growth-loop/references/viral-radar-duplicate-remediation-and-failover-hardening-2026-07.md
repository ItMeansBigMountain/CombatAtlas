# Viral Radar duplicate remediation and failover hardening (2026-07)

Use this when Viral Radar double-uploads, leaves queue uncertainty, or the user wants to add more YouTube failover accounts.

## What went wrong

A TOGI manual run uploaded 10 clips, then a second run uploaded 9 duplicate titles because the duplicate guard compared rendered output stems naively. The prior log stem was like `...-01-captioned-daily`, while the manifest clip stem was `...-01-captioned`, so the guard did not match.

## Remediation applied

- Duplicate TOGI reuploads were made **unlisted**, not deleted.
- The first/canonical 10 TOGI uploads remained public.
- Remediation record path:
  - `/opt/data/HeRmEz/projects/viral-clip-radar/UPLOADS/remediations/togi_duplicate_unlist_2026-07-10.json`

## Current hardening rules

1. Viral Radar daily upload script takes an exclusive lock:
   - `/opt/data/HeRmEz/projects/viral-clip-radar/STATE/viral_radar_upload.lock`
   - If another run is active, the second run exits `blocked_already_running`.
2. Duplicate detection normalizes render suffixes:
   - `-captioned-daily`
   - `-captioned-cron`
   - `-captioned`
   - `-daily`
   - `-cron`
3. Duplicate detection checks both upload logs:
   - `UPLOADS/youtube_uploads.jsonl`
   - `UPLOADS/viral_radar_enriched_uploads.jsonl`
4. Duplicate detection checks:
   - normalized file stem
   - public title
   - `source_url + title`
   - selected clip file/captioned file/hook
5. Queue replay also checks already-public signatures before upload. If a queued MP4 is already public, remove the queue item instead of reuploading it. Do **not** count skipped duplicates toward the upload minimum.
6. Rendered duplicate outputs are deleted and skipped, not queued or uploaded.

## Failover account model

The upload wrapper now loads failover accounts dynamically from:

- `/opt/data/HeRmEz/projects/_ops/google-email-profiles.json`

The active order is:

```json
"viral_radar_failover_order": ["classicalechos", "trapiistan", "fareed320"]
```

To add more failover accounts, create/verify the YouTube OAuth token, add a `youtube_profiles.<profile_key>` entry with `token_path` and `channel_id`, then append that key to `rules.viral_radar_failover_order`. No upload wrapper code change is needed.

Required scopes for upload failovers:

- `youtube.upload`
- `youtube.force-ssl`
- `youtube.readonly`
- `yt-analytics.readonly` preferred for metrics

## Verification commands

Check failovers:

```bash
/opt/hermes/.venv/bin/python3 - <<'PY'
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('up','/opt/data/HeRmEz/projects/viral-clip-radar/scripts/upload_to_youtube.py')
up=importlib.util.module_from_spec(spec); spec.loader.exec_module(up)
print([(x[0], Path(x[1]).is_file(), x[2]) for x in up.all_upload_profiles()])
PY
```

Check that a previously-uploaded plan has no candidates:

```bash
VIRAL_RADAR_PRIORITY_PLANS='/opt/data/HeRmEz/projects/viral-clip-radar/CLIP_PLANS/2026-07-07-togi-togi-on-how-to-be-successful-2Z2UT5aX0cw' \
VIRAL_RADAR_STRICT_DISCOVERED_ONLY=1 \
/opt/hermes/.venv/bin/python3 - <<'PY'
import importlib.util
spec=importlib.util.spec_from_file_location('vr','/opt/data/scripts/viral_radar_daily_upload.py')
vr=importlib.util.module_from_spec(spec); spec.loader.exec_module(vr)
print(vr.iter_candidate_manifest_clips())
PY
```

Expected after successful dedupe: `RuntimeError no reviewed manifest clips available` for that fully-uploaded TOGI plan.

# Viral Radar queue drain, failover, and render fixes (2026-07)

Use this when the user asks to drain Viral Radar queues/backlogs until all possible clips are uploaded.

## Standing operating goal

- If `UPLOAD_QUEUE/` has rendered `.mp4` + `.upload.json` items, drain it first.
- If the rendered upload queue is empty but `CLIP_PLANS/` has backlog, continue source acquisition → render → public upload runs.
- Keep looping in batches until:
  - upload queue is empty,
  - no source-ready manifests remain,
  - and the next run is blocked by real source/auth/quota constraints.
- Do not reserve YouTube upload capacity for faceless/newsletter work while real Viral Radar queue/backlog items remain.

## Standard run command

```bash
FORCE_UPLOAD=1 \
VIRAL_RADAR_UPLOAD_QUEUE_FIRST=1 \
VIRAL_RADAR_MIN_UPLOADS=10 \
VIRAL_RADAR_MAX_SOURCE_ATTEMPTS=50 \
VIRAL_RADAR_DAILY_UPLOAD_CAP=100 \
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

For a pure upload-queue replay, set `VIRAL_RADAR_MIN_UPLOADS` to the current number of `.upload.json` files so the run attempts to drain the queue in one pass.

## Verification after each batch

Run a lightweight queue/backlog check and report only the useful counts:

```bash
python3 - <<'PY'
from pathlib import Path
import json
root=Path('/opt/data/HeRmEz/projects/viral-clip-radar')
q=root/'UPLOAD_QUEUE'
print('upload_queue_metadata', len(list(q.glob('*.upload.json'))))
print('upload_queue_mp4', len(list(q.glob('*.mp4'))))
print('clip_plan_dirs', len([p for p in (root/'CLIP_PLANS').iterdir() if p.is_dir()]))
ready=[]
for m in (root/'CLIP_PLANS').glob('*/clip_manifest.json'):
    try: d=json.loads(m.read_text())
    except Exception: continue
    sf=d.get('source_file')
    if sf and Path(sf).exists(): ready.append(m)
print('source_ready_manifests', len(ready))
PY
```

Also inspect the last `UPLOADS/youtube_uploads.jsonl` rows for public URLs.

## Upload failover quota markers

The uploader should treat all of these stderr markers as upload-quota/rate-limit failover triggers, not generic hard failures:

- `uploadLimitExceeded`
- `exceeded the number of videos`
- `daily upload limit`
- `Quota exceeded for quota metric`
- `Video Uploads per day`
- `rateLimitExceeded`

When any of these appears, queue the failed rendered clip safely and retry via the next configured account/token failover:

1. Classical Echos
2. Trapiistan/Sosai
3. fareed320

The Google API error can appear as `HttpError 429` / `ResumableUploadError` from `googleapiclient`, with text like `Quota exceeded for quota metric 'Video Uploads' and limit 'Video Uploads per day'`.

## Low-res vertical render fix

If ffmpeg fails with `Invalid argument` / `Nothing was written into output file` while rendering a low-res vertical source such as `202x360`, check the renderer filter.

Bad pattern:

```text
scale=-2:1920,crop=1080:1920
```

This scales by height only, leaving width too narrow for a 1080 crop.

Correct scale-to-cover pattern:

```text
scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1
```

This works for low-res vertical and landscape sources and still produces real 1080x1920 Shorts.

## Reporting style

Keep Discord updates terse:

- State whether the queue is drained.
- Give counts: `upload_queue_metadata`, `upload_queue_mp4`, `clip_plan_dirs`, `source_ready_manifests`.
- Include latest uploaded URLs.
- If backlog remains, immediately start the next background drain run and provide its `session_id`.
- Only stop when complete or blocked by a real constraint needing user input.
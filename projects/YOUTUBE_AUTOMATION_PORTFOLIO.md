# YouTube Automation Portfolio

This is the working organization layer for the user's YouTube automation projects under `/opt/data/HeRmEz/projects`.

## Canonical upload method

All projects should use the shared OAuth/upload method documented in:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/YOUTUBE_UPLOAD_METHOD.md
```

Shared upload scripts:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py
```

## Active YouTube projects

### 1. `faceless-youtube-channel`

Path:

```text
/opt/data/HeRmEz/projects/faceless-youtube-channel
```

Role: **AI/tech/self-improvement faceless channel automation.**

Current status:

- Vercel dashboard deployed: `https://faceless-youtube-channel-beta.vercel.app`
- YouTube OAuth upload flow proven.
- Private smoke-test video uploaded successfully.
- One-command trend → script → TTS → kinetic MP4 → private upload pipeline exists at `scripts/run_trend_video.py`.
- First produced private content uploaded: `https://youtu.be/gSghO62fL5M`.

Owns:

- Automated original/faceless videos.
- Discipline/self-improvement angle using current trends.
- Cheap/free production stack: RSS/HN/Reddit/GDELT, TTS, FFmpeg kinetic text.

### 2. `viral-clip-radar`

Path:

```text
/opt/data/HeRmEz/projects/viral-clip-radar
```

Role: **Transformative clipping radar and short-form repurposing.**

Current status:

- Has discovery, clip planning, download/render helpers, review packets, and social upload stubs.
- Uses the canonical shared YouTube upload method when a reviewed clip is ready.
- User approval is **not required** for private uploads. Upload reviewed/generated clips as `private`; the user will decide when to make them public.
- First private review upload produced: `https://youtu.be/lLDXJIZQEqo`.

Owns:

- Finding viral long-form videos.
- Creating timestamped clip plans.
- Rendering vertical captioned clips.
- Keeping attribution/risk notes.

Boundaries:

- Not a lazy reupload farm.
- Human review/transformative context is preferred before public release, but private upload can happen automatically for user review.

### 3. `youtube-high-ticket-leverage`

Path:

```text
/opt/data/HeRmEz/projects/youtube-high-ticket-leverage
```

Role: **Personal-brand/story-driven channel that can lead to a high-ticket offer.**

Current status:

- Strategy, story bank, scripts, offer ladder, and calendar structure exist.
- This is not the same brand as the clipping/faceless channel.
- First private origin-draft upload produced: `https://youtu.be/tohDKZndsvk`.

Owns:

- Original personal story content.
- Transformation log.
- Audience trust and future offer validation.

### 4. Legacy/source material: `tweet_video_generator`

Path:

```text
/opt/data/HeRmEz/projects/tweet_video_generator
```

Role: **Tweet-to-video generator that must be repaired and brought under the shared YouTube upload method.**

Current status:

- Old YouTube token failed due to `deleted_client`.
- Do not use old pickle tokens as the source of truth.
- Repaired upload path: `upload_output_to_youtube.py` routes final `output.mp4` through the shared uploader.
- Twitter/X credentials moved to environment variables in `topTweet.py`; do not hardcode credentials.
- First repaired-lane private upload produced: `https://youtu.be/BEV1F-jo0Hc`.
- Keep as an active repair target, not just an archive.

## Project boundaries

```text
faceless-youtube-channel = original faceless videos generated from trends
viral-clip-radar         = transformative short clips from existing long-form content
youtube-high-ticket-*    = personal story / authority / future offer channel
tweet_video_generator    = tweet-to-video repair lane using shared upload method
```

## Definition of done

The next definition of done is **actual produced content**, not only setup:

- each active content lane has a generated/rendered asset or upload-ready artifact;
- private YouTube uploads are allowed without waiting for approval;
- public release remains a user decision inside YouTube Studio;
- upload metadata and video IDs are logged in each project's `UPLOADS/youtube_uploads.jsonl`.

## Next implementation queue

1. Update `viral-clip-radar` to call shared `_ops/youtube-automation/scripts/upload_youtube.py` instead of its older local upload method.
2. Build `faceless-youtube-channel/scripts/run_trend_video.py`:
   - trend ingest
   - script generation
   - TTS
   - FFmpeg kinetic render
   - dry-run upload
   - private upload
   - append upload record
3. Add upload history logs to each project:

```text
UPLOADS/youtube_uploads.jsonl
```

4. Add one shared dashboard/report that lists:
   - project
   - latest rendered MP4
   - YouTube video ID
   - privacy status
   - upload date
   - next action
5. Keep all uploads private until the user manually approves publishing.

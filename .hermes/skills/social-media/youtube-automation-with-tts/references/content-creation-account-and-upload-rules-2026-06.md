# Content creation account and upload rules — 2026-06

Use this reference for the user's faceless YouTube newsletter pipeline, Viral Clip Radar uploads, and future self-improving content loop.

## Account roles

- **Read newsletter source emails from `fareed320@gmail.com`**.
  - Canonical profile: `personal-secondary`.
  - Legacy alias: `fareed320` may point to `personal-secondary`.
  - Use for Gmail newsletter source reads and post-processing cleanup.

- **Use `trapiistan@gmail.com` for Hermes Workspace/calendar coordination**.
  - Canonical profile: `trapiistan`.
  - Use for Google Calendar events that communicate production schedules and cron/upload timing.

- **Use the correct YouTube channel token for uploads**.
  - `classicalechos` YouTube token owns **Classical Echos**.
  - `trapiistan` YouTube token owns **Sosai Oyama**.
  - Before editing an existing video, verify `channels.list(mine=true)` and `videos.list(..., id=VIDEO_ID)` show the expected channel/video.

## Upload privacy rule

- The user corrected the default: **do not upload YouTube automation outputs as private by default**.
- Approved content automation lanes should upload `public` unless the user explicitly requests private/unlisted review mode.
- The shared uploader should default to `public`.
- If the user asks for a backlog with future releases, prefer cron/calendar scheduling that uploads publicly at the chosen time.
- Only use YouTube `publishAt` when explicitly desired; explain that YouTube's API represents scheduled releases as private until publish time.

## Required YouTube scopes

- `youtube.upload` for uploads.
- `youtube.force-ssl` for existing video status/privacy/metadata edits. `youtube.upload` alone is insufficient to change a previously uploaded video from private to public.
- `youtube.readonly` for verifying channel/video ownership and status.
- `yt-analytics.readonly` for performance loops and self-improving channel analytics.

## Faceless newsletter pipeline

- Canonical account flow: read newsletter/source emails from `fareed320@gmail.com` via Workspace profile `personal-secondary`, then upload the produced newsletter videos to Trapiistan's YouTube account/channel **Sosai Oyama** using the explicit Trapiistan token path (`/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`).
- Do **not** route fareed320 newsletter videos to Classical Echos unless the user explicitly requests that lane. Classical Echos remains a separate channel/token.
- One real newsletter email = one video.
- Use actual newsletter body content, not placeholder topics.
- Visuals should use Pexels stock pictures/videos and Hugging Face visuals for now; Sora is not the default because of cost.
- Use ElevenLabs voiceover.
- After upload returns a verified YouTube `video_id`, delete/trash the source newsletter email and delete local rendered media to save VPS space.
- Keep durable metadata/logs/manifests.

## Viral Clip Radar distinction

- Viral Clip Radar does **not** need stock footage for clipping videos.
- It scouts long-form creator videos, clips them, adds captions/transcription, reframes to portrait 9:16 for smartphone/Shorts/Reels distribution, and uploads.
- Do not conflate this with the faceless newsletter stock-footage workflow.

## Reporting style

- For Discord reports about accounts, videos, and scheduled uploads, avoid Markdown tables.
- Use short bold bullets with concrete IDs/URLs and verification status.

# Social Video Performance Learnings

Last updated: `2026-06-12T14:00:34.680668+00:00`

## Metrics status

- `YOUTUBE_API_KEY` was not available, so this run could not fetch live view/like/comment metrics.
- Upload logs were still parsed so cron jobs can avoid duplicate video IDs/titles.
- To enable the learning loop, add a YouTube Data API v3 key as `YOUTUBE_API_KEY` in `/opt/data/.env`.

## Backlog Processor Status (2026-06-12)

- **New cron job**: `Daily Content Backlog Processor` (job_id: `f02334d43494`)
- **Schedule**: Daily at 09:00 UTC
- **Gmail profile**: `fareed320` (needs OAuth refresh for full Gmail modify scope)
- **Workflow**: Fetch emails → Generate video (Pexels + ElevenLabs) → Upload to YouTube (private, scheduled) → Add Calendar event → Delete email → Clean local files
- **Calendar**: `trapi-3226%40group.calendar.google.com`
- **Status**: Cron created, awaiting first run

## faceless-youtube-channel

- Uploads logged: 16 total; 3 public.
- Live metrics unavailable for public videos in this snapshot; use upload-log dedupe only until API metrics are configured.

## viral-clip-radar

- Uploads logged: 22 total; 4 public.
- Live metrics unavailable for public videos in this snapshot; use upload-log dedupe only until API metrics are configured.

## Operating rule for future cron runs

- Before generating the next video, read this file and avoid repeating low-signal titles/hooks.
- Double down on topics whose public videos beat the channel median views and comments.
- Treat missing metrics as a setup issue, not as proof the content failed.

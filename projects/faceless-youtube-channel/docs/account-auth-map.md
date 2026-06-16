# Faceless newsletter account/auth map

Last verified: 2026-06-15.

## Canonical workflow

- Read newsletter/source emails from `fareed320@gmail.com` using Workspace profile `personal-secondary`.
- Generate one video per real source email from that Gmail account.
- Upload the newsletter videos to Trapiistan's YouTube account/channel using the explicit Trapiistan YouTube token.
- Trash/delete the source newsletter email only after a verified YouTube `video_id` is returned.

## Auth paths

- Gmail source token: `/opt/data/google_profiles/personal-secondary/google_token.json`
  - Verified profile email: `fareed320@gmail.com`.
  - Required role: read/process/trash used newsletter emails.
- YouTube upload token: `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`
  - Verified channel: `Sosai Oyama`.
  - Verified channel ID: `UCsxzQlusqwmMUdjMvKAJDfA`.
  - Required scopes: `youtube.upload`, `youtube.force-ssl`, `youtube.readonly`, `yt-analytics.readonly`.
- Legacy compatibility token: `/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json`
  - Currently verifies to the same `Sosai Oyama` channel, but new scripts/docs should prefer `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json` so account intent is unambiguous.
- Classical Echos token: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`
  - Verified channel: `Classical Echos`.
  - Do not use for fareed320 newsletter videos unless the user explicitly asks for a Classical Echos run.

## Updated scripts

These now default to the explicit Trapiistan YouTube token unless `YOUTUBE_UPLOAD_TOKEN` overrides it:

- `scripts/newsletter_batch_upload.py`
- `scripts/newsletter_video_pipeline.py`
- `scripts/upload_youtube.py`
- `scripts/youtube_oauth.py`
- `scripts/update_bad_youtube_metadata.py`
- `scripts/run_graphic_video.py`

## Operational rule

For this project, “faceless/newsletter videos” means: source = `fareed320` / `personal-secondary`; destination = Trapiistan's YouTube channel `Sosai Oyama`.

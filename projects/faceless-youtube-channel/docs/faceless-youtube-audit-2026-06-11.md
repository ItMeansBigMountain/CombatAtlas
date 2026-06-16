# Faceless YouTube Video System Audit — 2026-06-11

## Current status

The system is partially wired but not production-ready for the user's quality bar.

- YouTube OAuth works for both channels:
  - Newsletter source Gmail: `personal-secondary` / `fareed320@gmail.com`.
  - Faceless/newsletter upload token: `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json` → YouTube channel **Sosai Oyama** / Trapiistan.
  - Legacy compatibility token: `/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json` currently verifies to the same **Sosai Oyama** channel, but new docs/scripts should prefer the explicit `youtube-trapiistan` path.
  - Classical Echos token: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json` → YouTube channel **Classical Echos**; do not use it for fareed320 newsletter videos unless specifically requested.
- Support links are configured and injected into descriptions:
  - Linktree: https://linktr.ee/sosai.oyama
  - Buy Me a Coffee: https://buymeacoffee.com/affanfareev
  - Cash App: https://cash.app/$sosaioyama
  - Venmo: https://venmo.com/u/SosaiOyama
- Bad newsletter upload metadata was cleaned for:
  - `vYIO5ELTtBI`
  - `YHaZ8Jh4AZQ`
- Public upload crons that could keep publishing bad videos are paused.
- Preflight currently blocks production quality:
  - ElevenLabs returns `HTTP Error 401: Unauthorized`.
  - No configured AI video/B-roll provider key is present.
  - Higgsfield CLI exists but is not authenticated.

## How the newsletter video path works

1. Select one source email as `profile:message_id`, usually from `/opt/data/google_profiles/<profile>/google_token.json`.
2. `scripts/newsletter_video_pipeline.py` loads Gmail with `gmail.modify` scope.
3. It fetches the Gmail message in full format.
4. It extracts headers: profile, id, threadId, From, Subject, Date, Snippet.
5. It walks MIME parts and extracts text/plain or HTML text.
6. It stores local source metadata under `videos/<timestamp-slug>/source_email.json`.
7. It builds six scripted scenes from the subject/body.
8. It writes `script.md` in the per-video workspace.
9. It renders scenes with FFmpeg.
10. It uploads through `/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py`.
11. It logs to `UPLOADS/newsletter_youtube_uploads.jsonl`.
12. If YouTube returns `video_id`, it trashes the source Gmail message.

## Intended quality gate

A newsletter video may upload only if:

1. One email becomes exactly one video.
2. Actual newsletter content drives hook/script/captions/B-roll.
3. Voice is realistic ElevenLabs or equivalent quality.
4. B-roll is relevant video/AI video, not static slides.
5. Public metadata hides production method.
6. Support links are present.
7. Source email is deleted only after verified upload.

## Current implementation gaps

- `newsletter_video_pipeline.py` checks for an ElevenLabs key and provider key, but does not actually call ElevenLabs or generate AI B-roll.
- If keys are present, `newsletter_video_pipeline.py` still renders static-ish FFmpeg text scenes with flite audio. This violates the quality bar.
- `run_graphic_video.py` can use ElevenLabs if working, but falls back to flite. It also uses generated FFmpeg graphics, not true AI/video B-roll.
- `run_trend_video.py` now refuses upload unless quality providers are present, but its renderer is still text/FFmpeg/flite-based.
- `newsletter_storyboard_package.py` is safer: it creates script and B-roll prompts only and does not upload.
- The old upload logs include bad/generic uploads. Metadata cleanup was done for two newsletter videos, but older trend videos may still need review.
- Cron job `c9e81ae638fe` is paused and should remain paused until the real pipeline exists.
- Cron job `bce8ebabac36` is also paused after errors.

## Current recommended step-by-step production flow

Until providers are fixed, use storyboard-only mode:

```bash
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
python3 scripts/newsletter_video_preflight.py
python3 scripts/newsletter_storyboard_package.py --message personal-secondary:MESSAGE_ID
```

Do not run public upload unless preflight is green and the renderer actually produces:

- ElevenLabs narration
- AI/generated or relevant B-roll clips
- 9:16 final MP4
- clean metadata with support links

## Next build needed

1. Fix ElevenLabs credentials/account.
2. Authenticate Higgsfield or configure one provider key: Fal, Runway, Luma, Pika, Replicate, or Comfy Cloud.
3. Add a real `generate_broll_clips()` step.
4. Add a real `generate_voiceover()` step that fails closed if voice generation fails.
5. Replace static FFmpeg scenes with B-roll timeline assembly.
6. Add a final `ffprobe` + visual asset audit before upload.
7. Keep source-email deletion gated behind verified YouTube upload.
8. Keep upload crons paused until a sample passes manual review.

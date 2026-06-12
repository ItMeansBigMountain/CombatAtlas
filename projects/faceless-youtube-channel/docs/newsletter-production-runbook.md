# Newsletter Video Production Runbook

## Current rule

No uploads unless the output passes the newsletter video quality standard:

- one source email = one video
- script uses actual TLDR / Daily Stoic / Kino Body content
- public title/description/tags hide production method
- description sounds like Affan's voice, not a bot disclosure
- include all support links when configured: Linktree, Buy Me a Coffee, Cash App, Venmo
- no affiliate links until Affan likes the videos
- ElevenLabs voiceover required
- relevant AI-generated video/B-roll required

## Commands

Preflight:

```bash
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
python3 scripts/newsletter_video_preflight.py
```

Storyboard one email without uploading:

```bash
python3 scripts/newsletter_storyboard_package.py --message personal-secondary:MESSAGE_ID
```

Attempt full render/upload, quality-gated:

```bash
python3 scripts/newsletter_video_pipeline.py --message personal-secondary:MESSAGE_ID --privacy public
```

The full pipeline refuses to upload if ElevenLabs or an AI video/B-roll provider is missing.

## Current blockers from preflight

- ElevenLabs configured but not usable right now: API returned auth/payment errors during live checks.
- No AI video provider key detected: `COMFY_CLOUD_API_KEY`, `FAL_KEY`, `FAL_API_KEY`, `REPLICATE_API_TOKEN`, `RUNWAY_API_KEY`, `PIKA_API_KEY`, `LUMA_API_KEY` all absent.
- Higgsfield CLI exists but is not authenticated: `/opt/data/.local/bin/higgsfield account status` returns `Not authenticated`.
- Support URLs are configured in `/opt/data/.env`: Linktree, Buy Me a Coffee, Cash App, Venmo.
- Existing bad upload descriptions need YouTube reauth with broader `youtube` scope; upload-only token cannot update metadata.

## Metadata policy

Public descriptions should look like:

```text
<reworded email idea in Affan's voice>

My read: <strong opinion / takeaway>. Build one proof today.

More from me: https://linktr.ee/sosai.oyama
Support the channel: https://buymeacoffee.com/affanfareev
Cash App: https://cash.app/$sosaioyama
Venmo: https://venmo.com/u/SosaiOyama

#Shorts
```

Never include:

- AI-generated
- faceless automation
- ElevenLabs
- source email / source profile
- generated from newsletter
- pipeline / bot wording

# Newsletter Video Production Runbook

## Current rule

No uploads unless the output passes the newsletter video quality standard:

- one source email = one video
- script uses actual TLDR / Daily Stoic / Kino Body content
- public title/description/tags hide production method
- description sounds like Affan's voice, not a bot disclosure
- include all support links when configured: Linktree, Buy Me a Coffee, Cash App, Venmo
- no affiliate links until Affan likes the videos
- ElevenLabs voiceover required; accepted env names are `ELEVENLABS_API_KEY`, `XI_API_KEY`, `ELEVEN_API_KEY`, or the user's current `EllevenLabsKey`.
- relevant AI-generated video/B-roll required; preferred provider is Hermes `video_generate` with `video_gen.provider: openai-sora` backed by `OPENAI_API_KEY` with Sora Videos API access. Higgsfield/FAL/etc. are fallback paths only.

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

- ElevenLabs must pass live preflight. The current user-provided env key name is `EllevenLabsKey`.
- No preferred AI video provider key detected until `OPENAI_API_KEY` is set with Sora Videos API access. Fallback providers are `COMFY_CLOUD_API_KEY`, `FAL_KEY`, `FAL_API_KEY`, `REPLICATE_API_TOKEN`, `RUNWAY_API_KEY`, `PIKA_API_KEY`, `LUMA_API_KEY`.
- Higgsfield is no longer the primary path; ignore it unless OpenAI/Sora is unavailable and the user explicitly wants that fallback.
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

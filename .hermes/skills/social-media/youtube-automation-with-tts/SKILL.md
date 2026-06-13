---
name: youtube-automation-with-tts
title: YouTube Automation with ElevenLabs TTS
author: ItMeansBigMountain
description: Automated faceless YouTube video generation with professional voice-overs
version: 1.0
category: social-media
tags: ["youtube", "automation", "tts", "elevenlabs", "faceless-channel"]
---

## Overview
Automated YouTube video creation pipeline with ElevenLabs voice-over integration for faceless channels and viral radar content. Ensures professional-quality narration on all videos.

For newsletter-driven videos (TLDR, Daily Stoic, Kino Body, Robinhood Snacks, similar), follow `references/faceless-newsletter-quality-gate.md`: **one email = one video**, use the actual email content, require realistic ElevenLabs narration plus relevant Pexels stock footage/images or Hugging Face visuals, and upload public by default unless the user explicitly requests private/unlisted review mode.

For the user's Hermes-level email sorting agent, Gmail source labels/folders, the `EllevenLabsKey` env alias, and the dark monochrome particle-video visual direction from the user's screenshots, follow `references/email-sorting-agent-and-particle-video-style.md`.

For the current faceless newsletter pipeline, use Pexels stock footage/images first and Hugging Face visuals as the AI fallback. Sora is no longer the default path because the user called out cost concerns; only revisit `references/openai-sora-video-gen-provider.md` if the user explicitly asks to use Sora or another text-to-video provider.

For YouTube OAuth, channel-token selection, public/default upload behavior, and account-specific content rules, follow `references/youtube-oauth-metadata-cleanup.md` and `references/content-creation-account-and-upload-rules-2026-06.md`.

For the user's current content-creation system, account mapping, upload visibility, calendar/cron contract, and faceless-vs-Viral-Clip-Radar boundaries, follow `references/content-creation-account-and-upload-rules-2026-06.md`: read newsletter emails from fareed320/personal-secondary, upload/manage calendar as trapiistan, keep affan.fareed@gmail.com read-only, use public YouTube uploads by default, and do not add stock footage to clipping videos.

For OpenAI Sora as the preferred AI B-roll/video backend, follow `references/openai-sora-video-gen-provider.md`: ChatGPT UI access is not enough for cron automation; configure a Hermes `video_gen` provider (`openai-sora`) with `OPENAI_API_KEY` Videos/Sora API access, and treat Higgsfield/FAL/etc. as fallbacks.

For auditing/rebuilding the user's faceless/newsletter pipeline after quality issues, follow `references/faceless-youtube-audit-lessons-2026-06.md`: key presence is not readiness; provider checks must be live where possible; renderer must actually generate realistic voice + relevant B-roll; otherwise stop at storyboard-only and keep upload crons paused.

## Triggers
- Manual request: "Generate YouTube video about [topic]"
- Batch processing: "Create 10 videos for my YouTube channel"
- Social media upload: "Upload to YouTube/Instagram/TikTok"

## Configuration Requirements

For the user's newsletter-driven faceless channel, also load `references/faceless-newsletter-quality-gate.md`. That reference captures the current bar: one real video per newsletter email, actual TLDR/Daily Stoic/Kino Body content, realistic voiceover, relevant AI B-roll, motivational pacing, and public metadata that does **not** disclose AI/faceless automation.

### Visual provider priority

For this user's newsletter/faceless pipeline, use **Pexels first** for stock footage/images and **Hugging Face** as the AI visual fallback. Sora/text-to-video is not the default because of cost; only use it if explicitly requested for a special video.

```yaml
visuals:
  primary: pexels
  fallback: huggingface
  avoid_by_default: sora
```

Keep Viral-Clip Radar separate: it clips creator long-form source videos into 9:16 captioned shorts and does **not** need stock footage by default.
```yaml
elevenlabs:
  api_key_env: "EllevenLabsKey"  # also accept ELEVENLABS_API_KEY, XI_API_KEY, ELEVEN_API_KEY
  voice: "Adam"  # Professional male voice
  speed: 1.0
  pitch: 0.0
  emphasis: 0.5
  model: "eleven_monolingual_v1"
```

Always run a live ElevenLabs probe before upload; key presence alone is not readiness. For 401/402/auth/scope/voice issues, follow `references/elevenlabs-auth-and-free-tier-probe.md`: use the exact `xi-api-key` header, prefer `EllevenLabsKey` before legacy env aliases, probe `/v1/user` and `/v1/user/subscription`, and fall back to a verified free-tier voice/model before declaring the key broken.

## Script Templates
```yaml
motivational_script:
  intro_hook: "Montage of {content_type} training..."
  content_bridge: "This is where {various} clips will be..."
  outro_motivator: "Final cinematic shots with {goal}..."

viral_radar_script:
  hook: "Breaking news: {viral_topic}"
  explanation: "What you need to know about {topic}"
  call_to_action: "Subscribe for more viral updates"
```

## Execution Flow
1. **Content Analysis**
   - Parse user request for topic/theme
   - For newsletter/email-driven videos, follow `references/newsletter-email-to-youtube-pipeline.md` and `references/faceless-newsletter-quality-gate.md`: audit source emails, make **one video per email**, use the actual newsletter content, generate relevant B-roll/voiceover, upload only after the quality gate passes, then trash the source email only after YouTube returns a verified `video_id`.
   - For scheduled/cron runs, load `social-video-cron-growth-loop` and run the metrics monitor before choosing the next topic.
   - Identify appropriate B-roll terminology
   - Generate script based on video type

2. **Voice-Over Generation**
   ```python
   def generate_tts(script, voice="Adam", api_key="YOUR_KEY"):
       headers = {"Authorization": f"Bearer {api_key}"}
       response = requests.post(
           "https://api.elevenlabs.io/v1/text-to-speech/{voice}",
           headers=headers,
           json={
               "text": script,
               "model_id": "eleven_monolingual_v1",
               "voice_settings": {
                   "stability": 0.5,
                   "similarity_boost": 0.8
               }
           }
       )
       return response.content
   ```

3. **Video Assembly**
   - Generate B-roll using stock footage libraries
   - Apply voice-over to timeline
   - Add transitions and effects
   - Export final video

4. **Upload Pipeline**
   - YouTube API integration
   - Title/description optimization
   - Thumbnail generation
   - Cross-platform posting
   - If editing existing YouTube metadata, first verify the OAuth token owns the target channel; `youtube.upload` alone is insufficient for metadata updates, and wrong-channel tokens return `403 forbidden`.
   - If Google consent shows `deleted_client`, switch to a current OAuth client secret and regenerate the auth URL instead of retrying the stale URL.

## B-Roll Terminology Mapping
- Motivational: "motivational B-roll", "cinematic stock footage"
- Success: "success montage clips", "inspirational stock video"
- Lifestyle: "lifestyle B-roll footage"
- Training: "athlete training", "gym footage"

## Quality Control
- Script review for emotional impact
- Voice-over validation
- Content licensing compliance
- Platform optimization
- For the user's faceless newsletter channel, run the `faceless-newsletter-quality-gate` reference before upload: no static text-slide placeholders, no generic filler script, one email per video, relevant AI B-roll, realistic voiceover, and no public disclosure of AI/faceless automation in metadata.
- YouTube metadata validation: strip emoji/control-ish Unicode from upload title/description if the API returns `invalidDescription`; keep richer source metadata locally.
- Public metadata should reword the email idea in the user's voice and include the configured support URLs when available (Linktree, Buy Me a Coffee, Cash App, Venmo); affiliate links are added later only after the user approves the video quality.
- For email/newsletter sources, verify upload with a returned YouTube `video_id` before trashing the Gmail message.
- For the user's faceless newsletter channel, load `references/faceless-newsletter-quality-gate.md` before scripting/rendering/uploading. Key corrections: one email = one video; actual TLDR/Daily Stoic/Kino Body content drives the video; public metadata must hide AI/faceless/automation/source-email details; descriptions include the user's support URLs.

## Example Usage
```bash
# Faceless motivational video
hermes --skill youtube-automation-with-tts --topic "fitness motivation"

# Viral radar clip
hermes --skill youtube-automation-with-tts --type viral-radar --topic "latest tech trends"

# Batch generation
hermes --skill youtube-automation-with-tts --batch --count 10
```

## Output Files
- `[topic]_voiceover.mp3` - Generated audio track
- `[topic]_video.mp4` - Final assembled video
- `[topic]_metadata.json` - YouTube optimization data
- `[topic]_thumbnails/` - Thumbnail variations
- `[topic]_assets/` - License documentation
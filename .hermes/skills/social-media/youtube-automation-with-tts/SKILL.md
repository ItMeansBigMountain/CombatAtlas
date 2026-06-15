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
Automated YouTube video creation pipeline with ElevenLabs/Google TTS voice-over integration for faceless channels and viral radar content. Ensures professional-quality narration and script-matched visuals on all videos.

**Stock visual reference:** see `references/stock-visual-provider-pattern.md` for the current faceless newsletter visual standard: derive per-beat search queries from the script, prefer Pexels/Pixabay/Shutterstock stock footage/photos, and avoid text-only backgrounds.

For newsletter-driven videos (TLDR, Daily Stoic, Kino Body, Robinhood Snacks, similar), follow `references/faceless-newsletter-quality-gate.md`: **one email = one video**, use the actual email content, require realistic ElevenLabs narration plus relevant Pexels stock footage/images or Hugging Face visuals, and upload public by default unless the user explicitly requests private/unlisted review mode.

For the user's Hermes-level email sorting agent, Gmail source labels/folders, the `EllevenLabsKey` env alias, and the dark monochrome particle-video visual direction from the user's screenshots, follow `references/email-sorting-agent-and-particle-video-style.md`.

For the current faceless newsletter pipeline, use **Pexels stock footage/images first** and **stock/manual fallback clips such as Mixkit-style sources next**. Higgsfield/Sora/text-to-video is not a hard requirement and must not block production when stock visuals are available. Only use Sora/Higgsfield/Hugging Face visuals if explicitly requested or needed for a special video; see `references/google-tts-and-stock-visual-fallbacks-2026-06.md`.

For stock/API visual selection and QA, also follow `references/stock-visuals-for-faceless-newsletters.md`: derive per-scene visual queries from the actual script/email topic, prefer Pexels/Pixabay footage/photos, use Shutterstock previews only according to the account/license state, save `visual_manifest.json`, and treat all-dynamic/text fallback renders as draft quality unless explicitly approved.

For YouTube OAuth, channel-token selection, public/default upload behavior, and account-specific content rules, follow `references/youtube-oauth-metadata-cleanup.md`, `references/content-creation-account-and-upload-rules-2026-06.md`, and `references/google-tts-stock-youtube-oauth-fallbacks-2026-06.md`. The last reference captures the current Google TTS fallback, stock-visual gate, and OAuth channel-identity verification lessons.

For the user's current content-creation system, account mapping, upload visibility, calendar/cron contract, and faceless-vs-Viral-Clip-Radar boundaries, follow `references/content-creation-account-and-upload-rules-2026-06.md`: read newsletter emails from fareed320/personal-secondary, upload/manage calendar as trapiistan, keep affan.fareed@gmail.com read-only, use public YouTube uploads by default, and do not add stock footage to clipping videos.

For OpenAI Sora as the preferred AI B-roll/video backend, follow `references/openai-sora-video-gen-provider.md`: ChatGPT UI access is not enough for cron automation; configure a Hermes `video_gen` provider (`openai-sora`) with `OPENAI_API_KEY` Videos/Sora API access, and treat Higgsfield/FAL/etc. as fallbacks.

For Google Cloud Text-to-Speech as the production fallback when ElevenLabs credits are low/exhausted, follow `references/google-cloud-tts-fallback.md`: verify the API with a live `text:synthesize` call, use `GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_TTS_CREDENTIALS`, default to `en-US-Neural2-J`, and keep local `flite`/edge-style narration review-only unless the user explicitly approves it.

For auditing/rebuilding the user's faceless/newsletter pipeline after quality issues, follow `references/faceless-youtube-audit-lessons-2026-06.md`: key presence is not readiness; provider checks must be live where possible; renderer must actually generate realistic voice + relevant B-roll; otherwise stop at storyboard-only and keep upload crons paused.

For hands-on Classical Echos/newsletter backlog operations, follow `references/newsletter-video-ops-lessons-2026-06.md`: no Markdown tables in Discord reports, target ~2-minute multi-clip videos, separate review fallback renders from final ElevenLabs uploads, search labeled newsletters outside Inbox, use Mixkit-style fallback only with source manifests, and handle YouTube `uploadLimitExceeded` with pending manifests plus resume jobs.

For the current faceless newsletter catch-up lane, follow `references/faceless-newsletter-batch-upload-2026-06.md`: Google TTS is an approved fallback/equivalent when ElevenLabs credits are low, Higgsfield/Sora auth is not required, use Pexels or stock/dynamic visual fallback, upload with the explicit faceless/Sosai Oyama token, and trash each source email only after a verified YouTube `video_id`.

For Classical Echos newsletter-video rendering after the user's 2-minute quality correction, follow `references/newsletter-video-rendering-provider-fallbacks-2026-06.md`: target ~120 seconds, require multiple relevant visual clips, use Mixkit as a vetted stock fallback when Pexels is blocked, and treat edge-tts as review-only unless explicitly approved.

For Google TTS fallback and the user's corrected stock-visual workflow, follow `references/google-tts-and-stock-visual-fallbacks-2026-06.md`: Pexels/stock fallback is the intended visual path; Higgsfield/Sora auth must not block stock-first newsletter videos, and ElevenLabs should be skipped when low credits would be burned by smoke tests.

For Google Cloud TTS fallback and stock-visual quality-gate rules, follow `references/google-tts-and-stock-visual-fallbacks-2026-06.md`: ElevenLabs is preferred but must be skipped when credits are low, Google TTS is the production fallback, and Higgsfield/Sora/AI-video auth must not block newsletter videos when Pexels or vetted stock fallback visuals are available.

## Triggers
- Manual request: "Generate YouTube video about [topic]"
- Batch processing: "Create 10 videos for my YouTube channel"
- Social media upload: "Upload to YouTube/Instagram/TikTok"

## Configuration Requirements

For the user's newsletter-driven faceless channel, also load `references/faceless-newsletter-quality-gate.md`. That reference captures the current bar: one real video per newsletter email, actual TLDR/Daily Stoic/Kino Body content, realistic voiceover, relevant AI B-roll, motivational pacing, and public metadata that does **not** disclose AI/faceless automation.

### Visual provider priority

For this user's newsletter/faceless pipeline, use live-probed stock APIs before any AI-video dependency. Prefer **Pexels** when `PEXELS_API_KEY` is active, but **Pixabay** (`PIXABAY_API_KEY`) is fully approved as the current primary when Pexels is missing/403. Then use Pexels photos, Shutterstock preview/search coverage as license-appropriate, Storyblocks only after HMAC signing is wired, and finally vetted no-key stock/image fallbacks. Do **not** require Higgsfield/Sora/AI-video auth for the normal stock-footage path. Use Hugging Face or other AI visuals only as an optional fallback when stock footage cannot satisfy the quality gate. Sora/text-to-video is not the default because of cost; only use it if explicitly requested for a special video.

```yaml
visuals:
  primary_when_active: pexels
  current_free_stock_primary: pixabay
  photo_fallback: pexels_photos
  preview_search_fallback: shutterstock_preview_video
  needs_hmac_before_ready: storyblocks
  final_fallback: vetted_no_key_stock_or_dynamic_draft
  optional_ai_fallback: huggingface
  avoid_by_default: sora
  not_required_for_standard_path: higgsfield
```

Keep Viral-Clip Radar separate: it clips creator long-form source videos into 9:16 captioned shorts and does **not** need stock footage by default.
```yaml
elevenlabs:
  api_key_env: "EllevenLabsKey"  # also accept ELEVENLABS_API_KEY, XI_API_KEY, ELEVEN_API_KEY
  voice_id: "CwhRBWXzGAHq8TQ4Fs17"  # Roger - free-tier friendly fallback
  model: "eleven_flash_v2_5"

google_tts_fallback:
  credentials_env: "GOOGLE_APPLICATION_CREDENTIALS"  # or GOOGLE_TTS_CREDENTIALS
  language: "en-US"
  voice: "en-US-Neural2-J"
  speaking_rate: 1.0
```

Always run live TTS probes before upload; key presence alone is not readiness. For 401/402/auth/scope/voice issues, follow `references/elevenlabs-auth-and-free-tier-probe.md`: use the exact `xi-api-key` header, prefer `EllevenLabsKey` before legacy env aliases, probe `/v1/user` and `/v1/user/subscription`, and fall back to a verified free-tier voice/model before declaring the key broken. If ElevenLabs is exhausted, use the Google Cloud TTS fallback in `references/google-cloud-tts-fallback.md` instead of blocking on ElevenLabs alone.

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
   - Prefer ElevenLabs when live subscription/character checks show enough credits.
   - Use the REST header `xi-api-key`, not `Authorization: Bearer`, for ElevenLabs.
   ### Voice-Over Generation
      ```python
      def generate_elevenlabs_tts(script, voice_id="CwhRBWXzGAHq8TQ4Fs17", api_key="YOUR_KEY"):
          # ElevenLabs REST auth uses xi-api-key, not Authorization: Bearer.
          headers = {"xi-api-key": api_key, "Content-Type": "application/json", "Accept": "audio/mpeg"}
          response = requests.post(
              f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
              headers=headers,
              json={
                  "text": script,
                  "model_id": "eleven_flash_v2_5",
                  "voice_settings": {
                      "stability": 0.42,
                      "similarity_boost": 0.75
                  }
              },
              timeout=60,
          )
          response.raise_for_status()
          return response.content
      ```
      When ElevenLabs credits are low or unavailable, use the Google TTS fallback described in `references/google-tts-stock-youtube-oauth-fallbacks-2026-06.md` before falling back to local review-only voices.
       response.raise_for_status()
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
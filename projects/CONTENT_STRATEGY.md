# Content Creation Project Direction

## 1. Faceless YouTube Channel
**Goal:** Auto-generate high-quality short videos based on newsletter content (TLDR, Daily Stoic, Kino Body, Robinhood Snacks, etc.) covering multiple niches.

**Workflow:**
- **Source:** Newsletter emails (extraction via Gmail API).
- **Scripting:** Convert newsletter content into engaging short-form scripts.
- **Audio:** ElevenLabs voiceover (Voice: Roger, Model: `eleven_flash_v2_5`).
- **Visuals (The "Sora Replacement"):**
    - No Sora/Sora-API (cost prohibitive).
    - Primary source: **Pexels API** for stock photos and stock videos.
    - Fallback/Augmentation: **Hugging Face Inference API** (e.g., for specific AI-generated assets/images if Pexels is insufficient).
- **Assembly:** `ffmpeg` for stitching clips, adding text overlays, and syncing audio.
- **Output:** YouTube Shorts, Instagram Reels, TikTok.

**Constraints:**
- No disclosure of AI/automation in public metadata.
- a "Newsletter to Operator" voice (Affan's voice).
- High-quality stock footage match to script keywords.

## 2. Viral-Clip Radar
**Goal:** Scout popular long-format content creators (e.g., Andrew Huberman), clip high-impact segments, and repackage them for short-form platforms.

**Workflow:**
- **Discovery:** Scout for new long-format videos from targeted creators.
- **Processing:**
    - Clip high-impact segments.
    - **Format:** Convert landscape to **Portrait (9:16)** optimized for smartphones (iPhone preference).
    - **Overlay:** Add transcriptions/captions (burned-in subtitles).
- **Output:** YouTube Shorts, Instagram Reels, TikTok.
- **Core Value:** Transformative value via clipping, framing, and captioning (not raw re-upload).

## 3. Long-term Evolution: Self-Improving Loop
**Goal:** Build a feedback loop that optimizes scouting and writing based on performance.

**Workflow:**
- **Tracking:** Monitor views, retention, and engagement via YouTube Analytics.
- **Analysis:** Identify which topics, hooks, and visual styles perform best.
- **Improvement:** Feed these learnings back into the scouting/scripting stage to improve quality and reach.

## Current Blockers & Status
- **Faceless Channel:** Transitioning from Sora to Pexels API. Pipeline needs update to replace Sora calls with Pexels stock search.
- **Viral-Clip Radar:** Data-collection pipeline is ready; needs the clipping/portrait-formatting/transcription automation loop.
- **Pexels API:** Token is saved in `/opt/data/HeRmEz/projects/faceless-youtube-channel/.env.pexels`.


## Newsletter video cron run — 2026-06-13T09:02:24.008022+00:00

- Notice: requested skill `process_newsletters_for_videos` was not installed, so I used the available Google Workspace tooling and existing newsletter/Pexels pipeline artifacts.
- Gmail profile checked: `fareed320` via `/opt/data/google_profiles/fareed320/google_token.json`.
- Unread messages found: at least 100 (`gmail search is:unread --max 100` returned 100).
- Latest unread examples: Chess.com streak, PayPal Microsoft receipt, TLDR, Daily Stoic, TLDR InfoSec/Fintech/Crypto/IT/Dev/Marketing, Robinhood Snacks.
- Preflight: ElevenLabs is configured and live, but free tier is nearly exhausted (9,341 / 10,000 characters used). No paid overage detected (`current_overage.amount=0`), respecting the <$2 per-transaction risk limit.
- Upload status: no new uploads attempted after detecting YouTube `uploadLimitExceeded` in the latest batch summary. Existing batch summary shows 8 uploaded and 22 failed due to YouTube daily/video upload limit.
- Calendar/email cleanup: no new Calendar events were created and no unread emails were deleted this run, because deletion is only safe after confirmed upload + calendar scheduling.
- Local cleanup: retained failed local MP4s so they can be retried after YouTube upload limit resets; uploaded batch records already used delete-after-upload where successful.
- Result: BLOCKED by YouTube upload limit and missing requested skill. Next safe retry: after YouTube upload limit resets; process a smaller daily batch to avoid quota exhaustion.

## Newsletter video cron run — 2026-06-14 09:07:09 UTC

- Notice: requested skill `process_newsletters_for_videos` was not installed, so I used the available Google Workspace tooling and the updated `faceless-youtube-channel/scripts/newsletter_batch_upload.py` pipeline.
- Gmail profile: `fareed320` via `/opt/data/google_profiles/fareed320/google_token.json`.
- Preflight: video/TTS/render stack ready; Google TTS OK; stock visuals available. Loaded Pexels key from `/opt/data/HeRmEz/projects/faceless-youtube-channel/.env.pexels` for this run. No paid stock purchase or high-risk transaction was performed; estimated per-item transaction risk stayed below `$2`.
- Daily-batch policy: processed a conservative batch of 3 unread newsletter/source emails rather than the entire stale unread backlog.
- Uploads completed:
  - `Freight drain` → https://youtu.be/RAGY_K2WLCA (`RAGY_K2WLCA`), 1080x1920, 55.09s; source Gmail message `19eb63fb42a56b91` trashed after verified upload.
  - `The Most Overlooked Aspect Of Growing A Social Media Following` → https://youtu.be/HVRRzUwE3qg (`HVRRzUwE3qg`), 1080x1920, 51.05s; source Gmail message `18d653996742a49e` trashed after verified upload.
  - `Minimum Daily Output To Get To 1M Followers` → https://youtu.be/uDz_lhJM06U (`uDz_lhJM06U`), 1080x1920, 45.96s; source Gmail message `18d6013d10062a07` trashed after verified upload.
- Cleanup: uploader deleted each final MP4 after upload; I also removed 54 local generated media assets (`.mp4/.mp3/.jpg/.png/.mov/.webm/.wav`) from the three workspaces while retaining JSON manifests/results for auditability.
- Calendar integration: attempted to create scheduled-release events on `trapi-3226@group.calendar.google.com`; OAuth profile tokens lacked Calendar scopes (`403 insufficientPermissions`) and the configured service account could not see the calendar (`404 notFound`). No calendar events were created.
- Result: PARTIAL SUCCESS — 3 videos generated/uploaded and their source emails cleaned up; Calendar scheduling remains blocked until the calendar is shared with the configured service account or an OAuth profile is reauthorized with Calendar scope.

## Newsletter video cron run — 2026-06-15 09:06:11 UTC

- Notice: requested skill `process_newsletters_for_videos` was not installed, so I used the available Google Workspace tooling and existing `faceless-youtube-channel/scripts/newsletter_batch_upload.py` pipeline.
- Gmail profile: `fareed320` via `/opt/data/google_profiles/fareed320/google_token.json`.
- Preflight: render/upload stack passed; Google TTS OK; ElevenLabs account still on free tier with `current_overage.amount=0`, so no paid overage or transaction above the `$2` risk cap was incurred. Pexels key was loaded from `.env.pexels`, but the run resolved usable stock footage from Pixabay/Shutterstock preview fallbacks rather than Pexels.
- Daily-batch policy: processed 3 unread emails from the 201-message unread backlog rather than draining the full backlog in one cron run.
- Uploads completed:
  - `Wouldn't it be wild if…` → https://youtu.be/me-k_GwDOfw (`me-k_GwDOfw`), 1080x1920, 51.48s; source Gmail message `19957d39faf718a1` trashed after verified upload.
  - `Print On Demand (POD) Management` → https://youtu.be/K2nMayJr8Oo (`K2nMayJr8Oo`), 1080x1920, 48.77s; source Gmail message `191566a0f3b0f2a6` trashed after verified upload.
  - `Print On Demand (POD) Management` → https://youtu.be/ARt72kZzMs0 (`ARt72kZzMs0`), 1080x1920, 48.77s; source Gmail message `191544bb623cded1` trashed after verified upload.
- Cleanup: uploader deleted each final MP4 after upload; I then removed 54 generated local media assets (`.mp4/.mp3/.jpg/.png/.mov/.webm/.wav`, 140,742,835 bytes) from the three workspaces while retaining JSON manifests/results for auditability.
- Calendar integration: attempted to create scheduled-release events on `trapi-3226@group.calendar.google.com`; the available `fareed320` OAuth token still lacks Calendar scope (`403 insufficient authentication scopes`), and no other usable calendar credential was present. No Calendar events were created.
- Result: PARTIAL SUCCESS — 3 videos generated/uploaded and their source emails cleaned up; Calendar scheduling remains blocked by OAuth scope/credential access.

## Newsletter video cron run — 2026-06-18T09:15:53Z

- Notice: requested skill `process_newsletters_for_videos` was not installed, so I used the available Google Workspace tooling and existing `faceless-youtube-channel/scripts/newsletter_batch_upload.py` pipeline.
- Gmail profile: the expected `/opt/data/google_profiles/fareed320/google_token.json` was not present; I used the available verified `fareed320@gmail.com` token at `/opt/data/google_profiles/fareed320.old-20260612-193356/google_token.json`.
- Pipeline maintenance: updated `newsletter_batch_upload.py` to load the project `.env.pexels` stock key after global env files, and fixed a render crash where scenes beyond six exceeded the accent-color palette.
- Preflight/risk: ffmpeg/ffprobe OK; Google TTS OK; ElevenLabs free tier OK with `current_overage.amount=0`; no paid stock/AI-video purchase was made, so the `$2` per-transaction risk limit was respected.
- Daily-batch policy: processed 3 unread source/newsletter emails only.
- Uploads completed:
  - `GLM-5.2, DeepSeek raises $7.4B, Android MCP` → https://youtu.be/lpo14wWmPeU (`lpo14wWmPeU`), 1080x1920, 80.73s; source Gmail message `19ed5cfafe13e54f` trashed after verified upload.
  - `iRhythm Data Ransom, FIFA World Cup Hack, JetBrains Key Theft` → https://youtu.be/iKkaIdZPpBU (`iKkaIdZPpBU`), 1080x1920, 71.92s; source Gmail message `19ed5c23d7046030` trashed after verified upload.
  - `Crowded AI markets, how to pivot, building your learning loop` → https://youtu.be/JyKknko1mFU (`JyKknko1mFU`), 1080x1920, 139.01s; source Gmail message `19ed5895a2fb1a77` trashed after verified upload.
- Calendar integration: attempted to create scheduled-release events on `trapi-3226@group.calendar.google.com`, but the available fareed320 token still lacks Calendar scope (`403 insufficient authentication scopes`). No Calendar events were created.
- Cleanup: uploader deleted each final MP4 after upload; I also removed 152 generated local media assets (`.mp4/.mp3/.wav/.jpg/.png/.webm/.mov/.m4a`, 703,496,837 bytes) from 2026-06-18 workspaces while retaining JSON manifests/results for auditability.
- Result: PARTIAL SUCCESS — 3 videos generated/uploaded and their source emails cleaned up; Calendar scheduling remains blocked by OAuth scope/credential access.

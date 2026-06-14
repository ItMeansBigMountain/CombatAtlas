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

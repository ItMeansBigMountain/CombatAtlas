# Viral Growth Playbook — Social/Short-Form Operating Rules

Last researched: 2026-06-04

## Core thesis

Virality is not “post whenever.” It is a feedback loop:

```text
high-emotion hook
|
V
watch-time / retention spike
|
V
comments + saves + shares
|
V
platform tests wider audience
|
V
repeat winning pattern faster than competitors
```

The automation projects should optimize for repeatable tests, not one perfect video.

## Default upload windows

Use audience local time. For our current Texas/US audience assumption, schedule in Central Time unless analytics prove otherwise.

### YouTube Shorts

- Primary: **2–4 PM** and **8–10 PM**.
- Test slots: **Tue–Thu 9 AM–12 PM**, especially if posting educational/career content.
- Cadence: **1 Short/day minimum** for growth experiments; **2/day** if the render/upload queue can keep quality high.
- Long-form support: publish the long video **Thu or Fri afternoon/evening**, then clip it for 3–7 days.

### TikTok

- Primary: **7–9 PM weekdays**.
- Test slots: **7–9 AM Tue/Thu/Fri** and **Saturday 3–5 PM**.
- Cadence: **1–3/day** when testing trend formats; never fewer than **5/week** for a growth sprint.
- First 30 minutes matter: post when the user can reply to comments quickly.

### Instagram Reels

- Primary: **11 AM–1 PM** and **7–9 PM**.
- Strong test slots from Buffer-style 2026 data: **Wednesday 12 PM**, **Wednesday 6 PM**, **Thursday 9 AM**.
- Cadence: **3–5 Reels/week** minimum; **1/day** during a sprint.
- Pair with daily Stories when the user has real-life receipts.

## Posting frequency rules

- **30-day sprint:** 1 short/day per active channel, 1 long-form/week if the channel has a long-form lane.
- **Aggressive sprint:** 2 shorts/day, spaced at least 4 hours apart; only if hook quality stays high.
- **Minimum viable consistency:** 3–5 short-form posts/week. Below that, learning is too slow.
- **Do not batch-upload 5 videos at once.** Schedule them into peak windows.

## Hook formulas for our niches

### Faceless discipline/self-improvement

- “You are not lazy. Your day has no rules.”
- “AI did not make you productive. It exposed your discipline.”
- “If you are fatherless, motivation is not enough — you need systems.”
- “The problem is not weed/food/scrolling. The problem is no standard after stress.”

### No-college tech / Cloud Engineer authority

- “If I had to become a Cloud Engineer again with no degree, I would do this.”
- “Most beginners study cloud wrong. They avoid receipts.”
- “This is the skill stack I would build before applying.”

### Viral clipping / transformative commentary

- “This 17-second moment explains why people keep failing dopamine resets.”
- “He said the quiet part out loud — here is the actual lesson.”
- “Do not copy the clip. Add the frame the original left out.”

## Visual rules for faceless YouTube

Use cheap/free graphics that look intentional instead of generic AI slop:

1. **Kinetic typography:** large 2–5 word phrases, animated progress bars, sharp color contrast.
2. **Diagram scenes:** ladders, meters, split screens, funnels, checklists, timelines, identity conflict maps.
3. **Receipt overlays:** calendar blocks, fake terminal/build logs, habit scorecards, food/weed/dopamine counters, job-search boards.
4. **Minimal mascot/silhouette:** faceless hooded figure, desk setup, phone addiction loop, prayer/gym/work triangle — no uncanny faces.
5. **Color system:** dark navy/black base, white text, cyan for discipline/system, orange/red for temptation/friction, green for receipts/proof.
6. **Pattern interrupts every 2–4 seconds:** zoom, meter fill, text swap, red strike-through, diagram node pulse.
7. **Always burn captions** for Shorts/Reels/TikTok. Silent autoplay must still work.

## Free / API-friendly Opus-like stack

Preferred production path:

```text
local ffmpeg + transcript/Whisper + LLM segment scoring
-> render vertical clips with captions
-> upload through native APIs/private-draft modes
```

Candidates to evaluate before paying for Opus:

- **Self-host/open-source:** SupoClip, Vinci Clips, AutoCut/AI video-editor style repos. Use only after checking license, install health, and API endpoints.
- **Developer video APIs:** Shotstack free sandbox for templated renders/captions; use if local FFmpeg becomes too slow or the dashboard needs cloud rendering.
- **Native platform APIs:** YouTube Data API for private uploads; TikTok Content Posting API for `SELF_ONLY`/draft upload; Meta Graph API for Instagram Reels when a public `video_url` is available.
- **Broker fallback only:** Upload-Post/Postproxy/Ayrshare-style APIs if native setup is too slow. Do not make brokers the core unless they prove reliable with returned post IDs/status polling.

## Automation requirements

Every content automation project should implement:

- `publish_window` metadata: platform, intended local timezone, scheduled slot, test cohort.
- Private/draft/self-only upload first, unless manually approved public.
- Upload log with video ID/URL, privacy, title, description, tags, source, and local artifact path.
- Cleanup after confirmed upload: delete local rendered MP4 and disposable workspace assets under known cache folders only.
- Human review gate for transformed third-party clips.
- Weekly analytics loop: keep hooks that beat median retention/share/save rate; kill formats after 3–5 poor tests.

## Cleanup rule

After a successful upload returns a platform ID/URL:

1. Log the upload result first.
2. Delete only allowlisted generated assets: `videos/<job>`, `EXPORTS/`, `TMP/`, `SOURCES/`, `DOWNLOADS/`, `RAW_VIDEO/`, scratch frames/audio.
3. Preserve source metadata, scripts, clip manifests, subtitles, upload logs, and review notes.
4. Provide `--keep-workspace`, `--keep-source`, or `--no-cleanup` for debugging.

## Sources checked

- Buffer 2026 search results: 52M-post study snippets for Instagram/TikTok timing.
- Socialync/FlowShorts search results: cross-platform timing windows for TikTok, Reels, Shorts.
- NewZenler/ImageWorks/HeyOrca search results: 3–5 posts/week minimum consistency guidance.
- GitHub/search results: SupoClip and Vinci Clips as open-source Opus-style candidates; Shotstack as API video rendering candidate.

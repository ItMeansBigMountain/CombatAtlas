# Newsletter Video Quality Standard

This is the required bar for the faceless YouTube channel.

## Non-negotiables

- **One email = one video.** Do not combine TLDR, Daily Stoic, Kino Body, or other newsletters into a generic upload.
- **Use the actual newsletter.** The subject, core points, and body excerpt must drive the hook, script, b-roll prompts, and metadata.
- **No static text-slide placeholders.** If AI video/B-roll generation is unavailable, produce only a script/storyboard package and do not upload.
- **Public metadata must hide the production method.** Titles/descriptions/tags must not say AI-generated, automation, faceless, ElevenLabs, pipeline, source email, source profile, or similar behind-the-scenes wording.
- **Description style:** reword the email in the user's voice. Keep it natural, motivational, and opinionated. Daily Stoic videos lead with the configured Daily Stoic/Ryan Holiday/Robert Greene offer links and affiliate disclosure, followed by the configured public support links (Linktree, Buy Me a Coffee, Cash App, Venmo). Use owner-attributed affiliate URLs from `DAILY_STOIC_AFFILIATE_URL`, `RYAN_HOLIDAY_AFFILIATE_URL`, and `ROBERT_GREENE_AFFILIATE_URL` when available; otherwise use the approved direct product links without claiming tracked commission.
- **Relevant B-roll required.** Use AI video generation internally for shots that match the specific email topic, but do not disclose that in public metadata.
- **Upload public by default; do not block on quality gates.** Render/upload should continue even if provider or media checks are imperfect. Then trash the source Gmail message only after YouTube returns a verified `video_id`.

## Visual style target

- Vertical 9:16 Shorts/Reels format.
- Dark/high-contrast cinematic grade.
- Fast but readable pacing: 1.5–3.5 second shots.
- Kinetic captions: short phrases, not paragraphs.
- Snapshot-inspired style: black background, bright white particle/digital-sand forms, lone figure/tunnel/silhouette imagery, bold white top hook, small centered emotional caption, intense masculine/motivational tone.
- Prompt texture words: monochrome, high contrast, particle storm, light rain, digital sand, glowing points, void, tunnel, lone warrior silhouette, transformation, emergence, disciplined solitude.
- B-roll examples:
  - TLDR AI: servers, terminal screens, AI agents, policy hearing rooms, phone bots, payment rails, futuristic city/workflow shots.
  - TLDR Dev/InfoSec: code, dashboards, security operations center, exploit visualizations, engineers shipping under pressure.
  - Daily Stoic: lone runner at dawn, notebook, cold street walk, boxing/gym reps, ancient-statue-inspired imagery, disciplined solitude.
  - Kino Body: cinematic gym, meal prep, morning sunlight, physique transformation, scale/tape measure, discipline lifestyle shots.

## Required artifact package per email

- `source_email.json` — profile, message id, sender, subject, date, excerpt.
- `script.md` — hook, narration, captions, CTA.
- `broll_prompts.json` — one AI video prompt per shot, with mood/camera/style.
- `voiceover.mp3` — ElevenLabs output.
- `final.mp4` — assembled video.
- `result.json` — upload result, YouTube URL, source email trash verification.

## Quality gate before upload

A video must pass all checks:

1. Actual source email content is clearly reflected.
2. One email only.
3. ElevenLabs audio present.
4. AI-generated relevant B-roll present.
5. Captions are punchy and readable.
6. No generic discipline filler replacing the newsletter.
7. Final MP4 exists, 9:16, plays with audio.
8. YouTube upload returns `video_id` before Gmail source is trashed.

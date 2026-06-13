# Email Sorting Agent Operating Model

## Purpose

Keep the user's primary inbox clean while preserving high-signal newsletter/source emails for the morning agent and video pipeline.

This is Hermes-level behavior, not project-specific email handling. Project-specific apps that use email own their own rules.

## Ownership loop

1. **Discovery** — read-only scan across all five Google profiles, classify senders, and detect new recurring newsletter/source senders.
2. **Harnessing** — apply stable labels/folders, keep source emails available for content generation, and keep the visible Inbox focused on important human/account/security mail.
3. **Ownership** — morning cron uses the sorted source folders, produces reports/videos, and only trashes newsletter source emails after verified YouTube upload.

## Profile scope

Known Google profiles:

- `personal-main` — primary personal.
- `personal-secondary` — backup/restricted; preferred TLDR source.
- `hermes-agent` — Hermes automation/account-linked communications.
- `burner` — temporary/disposable sending.
- `classicalechos` — archive/curated content sending.

## Labels / folders

Create or reuse these Gmail labels:

- `Hermes/Source/TLDR`
- `Hermes/Source/Daily Stoic`
- `Hermes/Source/Kino Body`
- `Hermes/Source/Newsletter Queue`
- `Hermes/Review/Important`
- `Hermes/Review/Needs Human`
- `Hermes/Junk/Known`

Newsletter source rule: apply the source label and remove `INBOX` only after the sender is confidently matched. Do not trash source newsletters until the content pipeline returns a verified YouTube `video_id`.

## Sender intent

- **TLDR** — bleeding-edge tech/AI/dev/security/news signals. Turn each email into one operator-style video, plus possible project ideas and morning-report intelligence.
- **Daily Stoic** — one lesson per email. Turn into a Stoic reflection script with disciplined, motivational narration.
- **Kino Body** — testosterone, men's health, warrior fitness, getting shredded while living better. Turn into fitness/self-mastery shorts.
- **Known junk/spam** — the user allows cleanup without per-item review when the sender/category is already known junk.
- **Important flow** — billing, security, bank/card, cloud/API, official notices, tickets, and human mail should stay visible or be labeled for review.

## Morning cron behavior

The morning operator/email manager should:

1. Run a read-only scan first.
2. Count actual Inbox with `labelIds=["INBOX"]`.
3. Sort source newsletters into labels/folders.
4. Report important/new items concisely.
5. Feed newsletter folders into the video queue.
6. Never delete source newsletters until verified upload.
7. Keep Discord reports short, no tables.

## Video style target from user snapshots

- Vertical 9:16.
- Black background, bright white graphic forms, heavy contrast.
- Particle/digital-sand subjects: lone figure, tunnel, rain-like human silhouette, emergence/transformation.
- Fast scene changes: about 1.5–3 seconds per shot.
- Large top hook text in bold white sans-serif.
- Short centered caption over the visual, not paragraphs.
- Mood: dark, cinematic, masculine, intense, motivational.
- B-roll prompts should favor abstract high-contrast AI visuals rather than literal stock footage: particle tunnel, lone warrior silhouette, kinetic light rain, chrome/white points forming a body, dawn training shadows, code/data storm, ancient statue fragments, gym chalk/sweat, city at night.

## Production rules

- One email equals one video.
- Actual email content drives hook, narration, captions, B-roll prompts, and metadata.
- ElevenLabs voice is required. Current accepted env names include `ELEVENLABS_API_KEY`, `XI_API_KEY`, `ELEVEN_API_KEY`, and `EllevenLabsKey`.
- Relevant AI-generated B-roll is required; no static text-slide placeholder uploads.
- Public metadata must not disclose AI, automation, source email, ElevenLabs, or pipeline details.
- Preserve source metadata locally for traceability.

---
name: social-video-cron-growth-loop
description: Run scheduled social-video jobs as full research-to-publish loops with metrics feedback, fresh topics/assets, upload timing, cleanup, and performance learning.
version: 1.0.0
created_by: agent
---

# Social Video Cron Growth Loop

Use this skill when a cron job must create and publish a new social video every run, especially for the user's faceless YouTube and Viral Radar lanes.

## Required loop per cron run

Before expensive generation/render/upload work, apply the blocked-status preflight pattern in `references/content-cron-blocked-status-preflight.md`: verify required Workspace/YouTube tokens, channel identity, provider readiness, and source availability; report `blocked_auth`, `blocked_source`, `blocked_provider`, `blocked_quality`, or `ok_uploaded` rather than treating scheduler exit status as product success.

0. **Apply viral packaging rules**
   - For the faceless newsletter lane, read `/opt/data/HeRmEz/projects/faceless-youtube-channel/VIRAL_YOUTUBE_SYSTEM.md` before scripting or rendering; the portable skill-library version is `references/viral-youtube-system-2026.md`.
   - First 1-3 seconds must contain a high-contrast curiosity hook; no intro/welcome/source disclosure.
   - Build scripts around hook → context → receipts → implication → identity/action close.
   - Keep on-screen captions short, change visual state every 2-4 seconds, and match title/on-screen text/description semantically.
   - Use timing cohorts from that doc until YouTube Studio metrics override them.

1. **Read performance memory first**
   - Run `/opt/data/scripts/youtube_metrics_monitor.py --json` if available.
   - Read `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md`.
   - Prefer topics/hooks related to previous winners; avoid duplicate recent titles.

2. **Research the current opportunity**
   - Faceless lane: research current self-improvement, AI, dopamine, discipline, no-degree/cloud-career, fatherless-men, first-gen-men angles.
   - Viral Radar lane: research current viral discourse and/or use the project watchlist/clip manifests.
   - Creator examples currently useful to the user: Andrew Huberman for science-backed protocols; Chris Williamson for Modern Wisdom/self-development interviews; Greg O'Gallagher/Kinobody for physique/fitness; Andrew Tate/TateSpeech/Cobratate for mindset/business/masculinity clips; Zerkaa/ZerkaaPlays for Sidemen/gaming/creator-culture moments; GG33 for numerology/astrology/spiritual framing; Luke Belmar/Capital Club and Nate Belmar/Mr Belmar for wealth/health/biohacking; Alex Hormozi for business/sales/wealth; Hamza/Hamza Unfiltered for raw self-improvement/discipline/social-confidence language. Treat all creator sources as inspiration/source material for transformative clips, not raw-reupload material.
   - Write the research brief into the project `STATE/`, `OUTPUTS/`, or equivalent durable folder.

3. **Generate or accumulate assets**
   - Faceless lane: use the project renderer (`scripts/run_graphic_video.py` or the newsletter pipeline) to generate fresh graphic/stock scenes, realistic TTS, captions/burned-in text, and a vertical MP4.
   - For newsletter videos, every email becomes one natural spoken story around one topic. Do not make the narration sound like a rigid outline; use actual newsletter facts as receipts inside a charismatic monologue. Captions are display-only and must never be sent to TTS as spoken text. Pick an internal actor-style narrator archetype from the email tone/topic for writing energy only; do not clone or publicly claim celebrities.
   - Match backgrounds to the current beat: multiple distinct videos/images, semantic per-scene queries, and preserved `visual_manifest.json`. Keep stock queries short and keyword-driven; if every approved stock/API visual provider fails for a scene, block for review instead of rendering generic filler.
   - Viral Radar lane: select one fresh clip from a reviewed manifest, download/restore source media from rights-safe fallback/archive source, render vertical with captions/context, and preserve source attribution.
   - Do not raw-reupload third-party clips. Viral Radar must add captions, hook/context framing, attribution, and commentary/transformative value.

4. **Upload at a tested viral window**
   - Use Central Time for the user's Texas/US audience until analytics prove otherwise.
   - YouTube Shorts default test windows: **2–4 PM CT** and **8–10 PM CT**.
   - TikTok/Reels references if cross-posting later: TikTok **7–9 PM weekdays**; Reels **11 AM–1 PM** or **7–9 PM**.
   - Log returned platform IDs/URLs before cleanup.

5. **Clean up safely**
   - Delete only generated/allowlisted media folders after confirmed upload.
   - Preserve upload logs, manifests, subtitles, source metadata, analytics snapshots, and performance notes.

6. **Report concise result**
   - Include created topic/hook, generated asset path or cleanup note, upload URL/ID, metrics-monitor status, and any blocker.

## Current local commands

---
**User style preferences (embedded from session)**
- Use concise bullet lists, no tables, short sentences.
- Keep responses terse and informal.
- Remember to embed these preferences in all future cron‑job communications.
---

## Current local commands

Faceless fresh-topic upload (Hacker News trend-based):

```bash
FACELESS_TOPIC='<researched topic/hook>' \\
FACELESS_RESEARCH_JSON='<compact JSON research brief>' \\
python3 /opt/data/scripts/faceless_daily_upload.py
```

Faceless YouTube channel (newsletter-based) - project specific:

- Project path: `/opt/data/HeRmEz/projects/faceless-youtube-channel`
- Core script: `/opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/run_trend_video.py`
- Cron wrapper: `~/.hermes/scripts/run_faceless_video.sh` (changes to project directory before execution)
- Example manual run (dry-run): `python3 /opt/data/HeRmEz/projects/faceless-youtube-channel/scripts/run_trend_video.py --dry-run-upload`
- Can be adapted to process newsletter emails via Google Workspace Gmail API.

Viral Radar one-fresh-clip public upload:

```bash
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

Metrics learning loop:

```bash
python3 /opt/data/scripts/youtube_metrics_monitor.py --json
```

## Monitoring notes

- Live metrics should use the OAuth token/account that uploaded the video, not a generic cross-account API key. The metrics monitor should still parse upload logs and write setup notes if token access fails.
- The learning source of truth is `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md`.
- Future automation should add retention/watch-time if YouTube Analytics OAuth scopes are configured; Data API statistics alone cover views/likes/comments, not retention.
- For the concrete cron conversion pattern, timing defaults, duplicate guard, and verification rules, see `references/cron-full-pipeline-and-metrics-loop.md`.
- For the viral YouTube script/visual/timing rules and the safe pipeline quality-gate pattern from the 2026-06 hardening pass, see `references/viral-youtube-system-and-pipeline-gates-2026-06.md`.
- For the current creator-source expansion, see `references/creator-source-expansion-huberman-hamza-2026-06.md`: Huberman and Hamza are both useful source examples, but clips must be transformed with hook/context/captions/analysis and attribution. The active project workflow is `/opt/data/HeRmEz/projects/viral-clip-radar/WORKFLOWS/daily_creator_clip_release_google_api_fallbacks.md`: each daily job refreshes latest long-form candidates via Google/YouTube APIs, downloads/restores the selected source, renders a transformative Short, uploads through the correct YouTube OAuth token, and reports exact blockers for YouTube download or Opus Clips fallback failures. See `references/viral-radar-google-api-and-source-fallbacks-2026-06.md` for the durable fallback ladder and Classical Echos token rule.
- For the expanded Viral Radar long-form creator release lane, daily 12:15 PM Central schedule, YouTube Data API seeding pattern, and creator pool, see `references/viral-radar-creator-longform-release-lane-2026-06.md`.
- For manual Viral Radar batch requests where the user pastes multiple creator URLs/plan paths, see `references/viral-radar-manual-batch-clip-up-2026-06.md`: prepare `clip_manifest.json`/edit notes first, then use the source acquisition ladder, and report exact source/provider blockers without claiming renders.
- For the script path fix used in the daily faceless YouTube cron job, see `references/script-path-fix.md`.

## Pitfalls

- Do not let cron publish the same fixed title/video every day.
- Do not use the old fixed NASA-only Viral Radar lane as the default unless no reviewed fresh clips are available.
- Do not treat missing metrics credentials as content performance data.
- Keep cron prompts self-contained because scheduled runs do not inherit chat context.
- Do not leave creative content jobs as `no_agent=true` script-only jobs when the user expects fresh research and decision-making each run; use deterministic scripts only as substeps inside an agent-driven cron.

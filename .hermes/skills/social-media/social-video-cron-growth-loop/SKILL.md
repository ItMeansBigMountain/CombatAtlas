---
name: social-video-cron-growth-loop
description: Run scheduled social-video jobs as full research-to-publish loops with metrics feedback, fresh topics/assets, upload timing, cleanup, and performance learning.
version: 1.0.0
created_by: agent
---

# Social Video Cron Growth Loop

Use this skill when a cron job must create and publish a new social video every run, especially for the user's faceless YouTube and Viral Radar lanes.

## Required loop per cron run

1. **Read performance memory first**
   - Run `/opt/data/scripts/youtube_metrics_monitor.py --json` if available.
   - Read `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md`.
   - Prefer topics/hooks related to previous winners; avoid duplicate recent titles.

2. **Research the current opportunity**
   - Faceless lane: research current self-improvement, AI, dopamine, discipline, no-degree/cloud-career, fatherless-men, first-gen-men angles.
   - Viral Radar lane: research current viral discourse and/or use the project watchlist/clip manifests.
   - Write the research brief into the project `STATE/`, `OUTPUTS/`, or equivalent durable folder.

3. **Generate or accumulate assets**
   - Faceless lane: use the project renderer (`scripts/run_graphic_video.py`) to generate fresh graphic scenes, TTS, captions/burned-in text, and a vertical MP4.
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

Faceless fresh-topic upload:

```bash
FACELESS_TOPIC='<researched topic/hook>' \
FACELESS_RESEARCH_JSON='<compact JSON research brief>' \
python3 /opt/data/scripts/faceless_daily_upload.py
```

Viral Radar one-fresh-clip public upload:

```bash
python3 /opt/data/scripts/viral_radar_daily_upload.py
```

Metrics learning loop:

```bash
python3 /opt/data/scripts/youtube_metrics_monitor.py --json
```

## Monitoring notes

- Live metrics require `YOUTUBE_API_KEY` in `/opt/data/.env`; without it, the monitor still parses upload logs and writes a setup note.
- The learning source of truth is `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md`.
- Future automation should add retention/watch-time if YouTube Analytics OAuth scopes are configured; Data API statistics alone cover views/likes/comments, not retention.
- For the concrete cron conversion pattern, timing defaults, duplicate guard, and verification rules, see `references/cron-full-pipeline-and-metrics-loop.md`.

## Pitfalls

- Do not let cron publish the same fixed title/video every day.
- Do not use the old fixed NASA-only Viral Radar lane as the default unless no reviewed fresh clips are available.
- Do not treat missing metrics credentials as content performance data.
- Keep cron prompts self-contained because scheduled runs do not inherit chat context.
- Do not leave creative content jobs as `no_agent=true` script-only jobs when the user expects fresh research and decision-making each run; use deterministic scripts only as substeps inside an agent-driven cron.

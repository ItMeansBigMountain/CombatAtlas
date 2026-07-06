---
name: social-video-cron-growth-loop
description: Run scheduled social-video jobs as full research-to-publish loops with metrics feedback, fresh topics/assets, upload timing, cleanup, and performance learning.
version: 1.0.0
created_by: agent
---

# Social Video Cron Growth Loop

Use this skill when a cron job must create and publish a new social video every run, especially for the user's faceless YouTube and Viral Radar lanes.

## Required loop per cron run

Before expensive generation/render/upload work, apply the blocked-status preflight pattern in `references/content-cron-blocked-status-preflight.md`: verify required Workspace/YouTube tokens, channel identity, provider readiness, and source availability; report `blocked_auth`, `blocked_source`, `blocked_provider`, or `ok_uploaded` rather than treating scheduler exit status as product success. For the user's faceless/newsletter lane, do **not** block public upload on quality/review/provider gates; see `references/faceless-public-upload-no-quality-gate-2026-06.md`.

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
   - Creator examples currently useful to the user: Andrew Huberman for science-backed protocols; Chris Williamson for Modern Wisdom/self-development interviews; Greg O'Gallagher/Kinobody for physique/fitness; Andrew Tate/TateSpeech/Cobratate for mindset/business/masculinity clips; GG33 for numerology/astrology/spiritual framing; Luke Belmar/Capital Club and Nate Belmar/Mr Belmar for wealth/health/biohacking; Alex Hormozi for business/sales/wealth; Hamza/Hamza Unfiltered for raw self-improvement/discipline/social-confidence language. Do **not** use Zerkaa/ZerkaaPlays unless the user explicitly re-adds the correct channel; the user said the existing Zerkaa source was wrong. Treat all creator sources as inspiration/source material for transformative clips, not raw-reupload material.
   - Write the research brief into the project `STATE/`, `OUTPUTS/`, or equivalent durable folder.

3. **Generate or accumulate assets**
   - Faceless lane: use the project renderer (`scripts/run_graphic_video.py` or the newsletter pipeline) to generate fresh graphic/stock scenes, realistic TTS, captions/burned-in text, and a vertical MP4.
   - For newsletter videos, every email becomes one natural spoken story around one topic. Do not make the narration sound like a rigid outline; use actual newsletter facts as receipts inside a charismatic monologue. Captions are display-only and must never be sent to TTS as spoken text. Pick an internal actor-style narrator archetype from the email tone/topic for writing energy only; do not clone or publicly claim celebrities.
   - Match backgrounds to the current beat: multiple distinct videos/images, semantic per-scene queries, and preserved `visual_manifest.json`. Keep stock queries short and keyword-driven. For the user's faceless/newsletter lane, provider/media quality problems are warnings, not public-upload blockers; see `references/faceless-public-upload-no-quality-gate-2026-06.md`.
   - Viral Radar lane: clip all newly discovered influencer content, not just the first successful item. The cron pipeline must upload at least 3 public Shorts per run when source material is available; 3 is a floor, not a ceiling. For long-form creator videos, seed at least 3 candidate clips per video and use best judgment from duration, transcript quality, and clip opportunities to produce more. Enrich clip/title/description planning with YouTube transcript text when available, render vertical with captions/context, and preserve source attribution. Viral Radar uploads must use the Classical Echos YouTube account/token; faceless/newsletter videos use Trapiistan/Sosai. Keep hashtags out of YouTube titles; put them in description/tags.
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
- When the user asks to "look back" at recent social-video errors, actively combine session-history discovery with live probes: search recent sessions for `blocked_auth`, `invalid_grant`, `needs_provider_credentials`, bot-check/source-download failures, and tracebacks; rerun the relevant harmless preflight/monitor commands; inspect cron status; then repair what can be repaired immediately.
- If a recurring social-video cron is repeatedly hitting the same unrepaired auth/provider/source blocker, pause only that noisy job after confirming the live blocker, generate the exact reauth/setup next step, and plan to resume/replay it after verification. Do not leave a known-broken upload cron running just because scheduler status says `ok`.
- The learning source of truth is `/opt/data/HeRmEz/projects/_ops/social-growth/PERFORMANCE_LEARNINGS.md`.
- Future automation should add retention/watch-time if YouTube Analytics OAuth scopes are configured; Data API statistics alone cover views/likes/comments, not retention.
- For the concrete cron conversion pattern, timing defaults, duplicate guard, and verification rules, see `references/cron-full-pipeline-and-metrics-loop.md`.
- For replaying historical failed social-video cron runs after OAuth/provider fixes, see `references/replay-failed-social-video-crons.md`: classify past failures, run deterministic preflights, rerun lanes one by one, and report product-level statuses like `ok_uploaded`, `ok_rendered_review`, `blocked_auth`, `blocked_source`, or `blocked_provider`. For faceless/newsletter videos specifically, quality/review/provider gates must not block public upload; see `references/faceless-public-upload-no-quality-gate-2026-06.md`.
- For YouTube source-acquisition auth failures that require a logged-in account/device code, follow `references/youtube-device-login-reauth-workflow.md`: use the Classical Echos account for pytubefix device login, save the cached token at `/opt/data/secrets/pytubefix-classical-echos/tokens.json`, and run Viral Radar downloads with `--no-ytdlp --try-pytubefix --oauth --pytubefix-client WEB`.
- Viral Radar cron jobs must be full clip→render→public-upload jobs, not discovery-only jobs. For creator watchlist/discovery-triggered crons, see `references/viral-radar-discovery-triggered-autopublish.md`: extract the exact discovered plan paths, pass them as `VIRAL_RADAR_PRIORITY_PLANS`, auto-create minimal manifests from `source_metadata.json` when needed, then attempt source→render→public upload before falling back. If a fresh YouTube source is blocked by cloud-IP bot checks, the pipeline should continue to another reviewed/source-ready manifest with local/direct/archive source media and upload that instead. Only report a blocker after exhausting source-ready fallbacks; do not return exit code 0 for discovery-only `blocked_source` results.
- For the viral YouTube script/visual/timing rules and the safe pipeline quality-gate pattern from the 2026-06 hardening pass, see `references/viral-youtube-system-and-pipeline-gates-2026-06.md`.
- For the current creator-source expansion, see `references/creator-source-expansion-huberman-hamza-2026-06.md`: Huberman and Hamza are both useful source examples, but clips must be transformed with hook/context/captions/analysis and attribution. The active project workflow is `/opt/data/HeRmEz/projects/viral-clip-radar/WORKFLOWS/daily_creator_clip_release_google_api_fallbacks.md`: each daily job refreshes latest long-form candidates via Google/YouTube APIs, downloads/restores the selected source, renders a transformative Short, uploads through the correct YouTube OAuth token, and reports exact blockers for YouTube download or Opus Clips fallback failures. See `references/viral-radar-google-api-and-source-fallbacks-2026-06.md` for the durable fallback ladder and Classical Echos token rule.
- For the expanded Viral Radar long-form creator release lane, daily 12:15 PM Central schedule, YouTube Data API seeding pattern, and creator pool, see `references/viral-radar-creator-longform-release-lane-2026-06.md`. Also follow `youtube-automation-with-tts/references/social-video-recovery-and-source-policy-2026-06.md` when replaying failed runs: Opus Clips is out of scope/disabled for this user; external-provider fallback should not produce OPUS missing-key warnings. Source acquisition must use cookies/proxy/local/official direct source, pytubefix/yt-dlp/plain-pytube fallback, or a non-Opus provider only if configured. For the current no-Opus fallback ladder, official Facebook/creator repost search pattern, pytube fallback, and credible-source strategy, see `references/youtube-source-acquisition-fallback-ladder-2026-07.md`. When the user explicitly does not want yt-dlp, use the `pytubefix` OAuth device-login path documented in `references/pytubefix-oauth-youtube-source-acquisition-2026-07.md`; Classical Echos is approved for that downloader account. For the no-vendor workaround that succeeded, see `references/viral-radar-no-vendor-influencer-source-acquisition-2026-06.md`: search official Facebook/creator reposts, download with yt-dlp, seed source-ready manifests, render, upload public, and avoid Huberman/NASA filler when the user asked for all influencers.
- For Viral Radar cases where OAuth reauth verifies successfully but cron replay still shows `invalid_grant`, check token defaults/env propagation in scripts and distinguish upload-auth success from source/provider blockers; see `references/viral-radar-token-default-and-source-blockers-2026-06.md`.
- If Viral Radar upload replay fails with `ModuleNotFoundError: No module named 'google'` from the shared uploader, the cron/shell resolved `python3` to an interpreter without Google API deps. Make `scripts/upload_to_youtube.py` invoke `/opt/hermes/.venv/bin/python3` for `/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py`, or otherwise use the same Hermes venv that has `google-auth` and `googleapiclient`; then verify with a `--dry-run` upload before rerunning public uploads.
- For recurring YouTube auth/token/channel issues, use `/opt/data/scripts/youtube_auth_healthcheck.py --verbose`. It verifies Trapiistan and Classical Echos OAuth tokens, expected channel IDs, upload guard snippets, Python Google API deps, and the metrics monitor. A silent no-agent cron named `YouTube auth/channel guard watchdog` runs this every 6h and only emits JSON when something breaks.
- For manual Viral Radar batch requests where the user pastes multiple creator URLs/plan paths, see `references/viral-radar-manual-batch-clip-up-2026-06.md`: prepare `clip_manifest.json`/edit notes first, then use the source acquisition ladder, and report exact source/provider blockers without claiming renders.
- For the script path fix used in the daily faceless YouTube cron job, see `references/script-path-fix.md`.

## Pitfalls

- Do not let cron publish the same fixed title/video every day.
- Do not use the old fixed NASA-only Viral Radar lane as the default unless no reviewed fresh clips are available.
- Do not treat missing metrics credentials as content performance data.
- Keep cron prompts self-contained because scheduled runs do not inherit chat context.
- Do not leave creative content jobs as `no_agent=true` script-only jobs when the user expects fresh research and decision-making each run; use deterministic scripts only as substeps inside an agent-driven cron.

# Social video cron replay after auth/provider repair

Use this when the user asks to replay failed faceless YouTube, Viral Radar, backlog, metrics, or creator-discovery cron runs after an OAuth or setup repair.

## Replay order

1. **Classify historical failures first**
   - Search session history for job IDs/names, script names, and blockers such as `invalid_grant`, `uploadLimitExceeded`, `needs_provider_credentials`, `Sign in to confirm you're not a bot`, `HTTP Error 401`, and missing script wrappers.
   - Produce a compact affected-attempt list before reruns.

2. **Run deterministic preflights before expensive rendering**
   - Metrics monitor: `python3 /opt/data/scripts/youtube_metrics_monitor.py --json`.
   - Google context or Gmail source probe if newsletter jobs previously failed on Workspace OAuth.
   - YouTube token/channel probe after upload-token reauth.

3. **Rerun lanes one by one**
   - Email/source sorting first if newsletter discovery depends on Gmail labels.
   - Metrics next; it informs topic selection but should not block rendering if unavailable.
   - Faceless trend wrapper / newsletter backlog processor.
   - Viral Radar daily upload and creator-watchlist feeder.

4. **Report product status, not just process exit**
   - `ok_uploaded`: video uploaded and ID/URL logged.
   - `ok_rendered_review`: video rendered but not uploaded due to review fallback or upload disabled.
   - `ok_noop`: no eligible source items.
   - `blocked_auth`: OAuth/token/channel identity issue.
   - `blocked_source`: YouTube source acquisition, bot check, missing local/Drive source, etc.
   - `blocked_provider`: missing Opus/Choppity/Vizard/Klap/MuAPI or visual/TTS provider credentials.
   - `blocked_quality`: quality gate failed; do not upload.

## Durable fixes from rerun sessions

- If a cron references a deterministic wrapper path that no longer exists but the underlying project script exists, recreate a tiny wrapper that `cd`s into the project and executes the intended script. Verify by running the wrapper directly.
- If a multi-profile Google collector has partial token failures, continue with healthy profiles and emit structured blocked-profile lines.
- If ElevenLabs returns 401/402 and a review fallback is allowed, render `--no-upload` / review output only; do not public-upload edge/local TTS unless the user explicitly approves it as production quality.
- For Viral Radar source acquisition, after current downloader attempts fail with YouTube bot verification, stop and request one of: cookies file, residential proxy, local/Drive MP4 source, or a configured clipping provider key. Do not claim a clip/upload succeeded.

## Pitfalls

- A cron `last_status=ok` can still mean product-level failure if the script reported a structured blocker.
- Do not trash newsletter source emails unless upload returned a verified YouTube video ID.
- Do not raw-reupload creator clips; Viral Radar still requires transformative hook/context/captions/attribution.

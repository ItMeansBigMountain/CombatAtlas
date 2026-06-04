# HeRmEz Shared YouTube Upload Method (2026-06)

Session learning: the user wants this OAuth pattern treated as the canonical way Hermes uploads to YouTube across multiple automation projects.

## Canonical pattern

Use **user OAuth**, not service accounts, for YouTube channel uploads.

Shared project-level docs/scripts created in the HeRmEz workspace:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/YOUTUBE_UPLOAD_METHOD.md
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/youtube_oauth.py
/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py
```

Canonical secrets path:

```text
/opt/data/secrets/youtube-main/youtube_client_secret.json
/opt/data/secrets/youtube-main/youtube_upload_token.json
/opt/data/secrets/youtube-main/youtube_oauth_pending.json
```

## OAuth setup checklist

1. Google Cloud Console → OAuth Client ID → **Web application**.
2. Enable **YouTube Data API v3**.
3. Add redirect URI:

```text
http://localhost:5000/
```

4. Generate auth URL from the helper.
5. User opens it and pastes the full returned `http://localhost:5000/?code=...` URL.
6. Exchange with localhost HTTP allowed only for that process:

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 python3 youtube_oauth.py exchange 'FULL_LOCALHOST_URL'
```

7. Verify with `youtube_oauth.py check`.
8. Upload private-first with `upload_youtube.py`.

## Headless PKCE pitfall

For web OAuth clients, `google-auth-oauthlib` can generate a PKCE `code_verifier` during auth URL creation. In headless VPS workflows, auth URL generation and token exchange often happen in different CLI processes. Persist the pending OAuth state including:

- `state`
- `redirect_uri`
- client secret path
- token path
- `code_verifier`

Restore `flow.code_verifier` before `fetch_token()`. If the exchange fails with `InvalidGrantError: Missing code verifier`, regenerate a new auth URL after adding this persistence; old auth codes cannot be reused.

## Private-first upload rule

For the user's YouTube automation projects, upload as `private` by default unless they explicitly approve `unlisted` or `public`.

Important user preference: **do not wait for per-upload approval when the target privacy is `private`**. Produce the artifact, upload it privately, log the result, and report the video ID/URL. The user will review in YouTube Studio and manually switch winners to public.

## Shorts classification checklist

For YouTube Shorts lanes, do not just upload a small/vertical-looking video. Verify the rendered MP4 before upload:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,sample_aspect_ratio,display_aspect_ratio,pix_fmt,r_frame_rate \
  -of json EXPORT.mp4
```

Required: `1080x1920`, `display_aspect_ratio=9:16`, `sample_aspect_ratio=1:1`, `pix_fmt=yuv420p`, normal frame rate such as 30fps, and duration under YouTube's Shorts limit. The render filter should force square pixels, e.g. `scale=-2:1920,crop=1080:1920,setsar=1`, and encode with `-pix_fmt yuv420p`.

When uploading Shorts, include `#Shorts` in the title or description and a `shorts` tag. Avoid angle brackets like `<60` or `<=60` in YouTube descriptions; the API can reject them as `invalidDescription`.

## Production-over-setup rule

For this user's YouTube automation lanes, setup is not considered done until at least one real/private pilot artifact has been rendered and uploaded. After OAuth and scripts are working, keep iterating toward actual content output rather than stopping at docs, stubs, or plans.

Minimum proof for a lane:

- exported MP4 exists,
- private YouTube upload succeeded,
- returned video ID/URL is reported,
- metadata is appended to the lane's `UPLOADS/youtube_uploads.jsonl`.

## Project lanes recorded in HeRmEz

The workspace portfolio doc is:

```text
/opt/data/HeRmEz/projects/YOUTUBE_AUTOMATION_PORTFOLIO.md
```

Current lanes:

- `faceless-youtube-channel`: original faceless trend → script → flite TTS → FFmpeg kinetic video → private upload; script lives at `scripts/run_trend_video.py`.
- `viral-clip-radar`: transformative clipping/radar lane; private-first pilot uploads are allowed without waiting for user approval, but real clips still need added commentary/context/captions/analysis rather than raw reuploads. Viral Radar defaults to YouTube Shorts: render/verify full-frame 1080x1920 9:16 square-pixel MP4s and add Shorts metadata; use an explicit longform opt-out only when requested. User specifically wants Andrew Huberman / Huberman Lab watched for new clip candidates because the content is personally useful.
- `youtube-high-ticket-leverage`: personal story/authority/future offer channel; can use shared headless text-video renderer for private origin drafts.
- `tweet_video_generator`: active repair lane, not just archive. Route final `output.mp4` through the canonical shared private uploader; remove hardcoded Twitter/X credentials in favor of environment variables.

## Canonical pilot upload evidence from the setup session

Known-good private upload IDs from the initial consolidation session:

- Faceless YouTube Channel: `gSghO62fL5M`
- Viral Clip Radar: `lLDXJIZQEqo`
- YouTube High-Ticket Leverage: `tohDKZndsvk`
- tweet_video_generator: `BEV1F-jo0Hc`

Treat these as verification that the shared OAuth token and uploader worked at least once; for future sessions, still run a fresh smoke test or inspect the latest upload log before assuming current readiness.

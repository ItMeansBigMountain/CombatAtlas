# Faceless YouTube Channel

Project workspace for building a faceless YouTube channel using Hermes as the AI operating partner instead of Claude.

## Goal

Create a repeatable system for ideating, scripting, producing, publishing, and improving faceless YouTube videos under the same YouTube/Google account.

## Live MVP

- Public URL: https://faceless-youtube-channel-beta.vercel.app
- Purpose: lightweight landing/dashboard for the cheap/free trend-to-video automation pipeline.
- Vercel project: `faceless-youtube-channel`

## Review/deploy/smoke evidence

- Classification: live Vite + React frontend/dashboard with supporting Python YouTube automation scripts. No `PRODUCT_DIRECTION.md` is present; README/docs are the current product direction source.
- Local validation: `npm ls --depth=0` clean; `npm run build` passes (`vite v8.0.16`, production assets built under `dist/`). No `test` or `lint` script is defined in `package.json`.
- Deployment: production Vercel project `faceless-youtube-channel` is Ready. Public alias `https://faceless-youtube-channel-beta.vercel.app` returns anonymous HTTP 200; the unique deployment URL may be Vercel-protected and return 401.
- Smoke test: anonymous page load and in-page CTA navigation were browser-tested with no JS console errors observed. Invalid route returns 404 as expected.
- Follow-up PBI: `t_f8df6c43` tracks a low-severity direct hash deep-link scroll issue reported by the dogfood pass; current root PBI should stay open until that child is resolved or explicitly waived.

## Starting Assumption

The user has an existing YouTube account and wants to add a faceless channel/project to it. If a specific guide is provided later, paste or upload it here and Hermes will adapt this workspace to match it step-by-step.

## Workspace Structure

- `docs/channel-strategy.md` — niche, positioning, voice, and content pillars.
- `docs/hermes-youtube-workflow.md` — how Hermes replaces the Claude steps in the guide.
- `docs/production-sop.md` — repeatable video creation workflow.
- `docs/content-pipeline.md` — idea backlog and status workflow.
- `docs/viral-production-system.md` — viral posting cadence, faceless graphic system, and cleanup rules.
- `assets/` — brand visuals, generated images, thumbnails, audio, exports.
- `scripts/` — future automation scripts.
- `videos/` — per-video workspaces.

## Canonical YouTube Upload Method

This project now uses the shared HeRmEz YouTube upload method:

```text
/opt/data/HeRmEz/projects/_ops/youtube-automation/YOUTUBE_UPLOAD_METHOD.md
```

Current upload status:

- OAuth token verified with `youtube.upload` scope.
- Private API smoke-test upload succeeded.
- All generated videos should be uploaded as `private` first unless explicitly approved otherwise.
- Successful uploads delete generated local video/workspace assets by default; pass `--keep-workspace` only for debugging.

## First Milestone

Build the first one-command pilot:

1. Trend idea.
2. Script.
3. TTS voiceover.
4. Kinetic FFmpeg render.
5. Dry-run upload.
6. Private YouTube upload.
7. Upload record in `UPLOADS/youtube_uploads.jsonl`.

## Viral cadence default

Run a 30-day Shorts sprint: **1 private-reviewed Short/day**, scheduled for **2–4 PM** or **8–10 PM Central**. Reuse the same render for TikTok at **7–9 PM** and Instagram Reels at **11 AM–1 PM** or **7–9 PM** once those tokens are connected.

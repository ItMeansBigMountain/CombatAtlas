# Faceless YouTube Channel

Project workspace for building a faceless YouTube channel using Hermes as the AI operating partner instead of Claude.

## Goal

Create a repeatable system for ideating, scripting, producing, publishing, and improving faceless YouTube videos under the same YouTube/Google account.

## Live MVP

- Public URL: https://faceless-youtube-channel-beta.vercel.app
- Purpose: lightweight landing/dashboard for the cheap/free trend-to-video automation pipeline.
- Vercel project: `faceless-youtube-channel`

## Starting Assumption

The user has an existing YouTube account and wants to add a faceless channel/project to it. If a specific guide is provided later, paste or upload it here and Hermes will adapt this workspace to match it step-by-step.

## Workspace Structure

- `docs/channel-strategy.md` — niche, positioning, voice, and content pillars.
- `docs/hermes-youtube-workflow.md` — how Hermes replaces the Claude steps in the guide.
- `docs/production-sop.md` — repeatable video creation workflow.
- `docs/content-pipeline.md` — idea backlog and status workflow.
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

## First Milestone

Build the first one-command pilot:

1. Trend idea.
2. Script.
3. TTS voiceover.
4. Kinetic FFmpeg render.
5. Dry-run upload.
6. Private YouTube upload.
7. Upload record in `UPLOADS/youtube_uploads.jsonl`.

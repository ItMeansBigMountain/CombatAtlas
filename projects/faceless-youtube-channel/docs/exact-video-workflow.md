# Exact Faceless Timestamp-to-Image Workflow

This is the Hermes version of the referenced video workflow: use Hermes + Higgsfield instead of Claude Code + Higgsfield.

## Matched Workflow

1. Record a human voiceover.
2. Transcribe it with timestamps.
3. Feed the timestamped transcript to Hermes.
4. Generate one simple MS-Paint-style image for every timestamp.
5. Download each image locally and rename it to its timestamp, like `0.07.png`.
6. Drag the images into an editor and stretch each image until the next timestamp.

## Installed Here

- Higgsfield CLI: `/opt/data/.local/bin/higgsfield`
- Higgsfield project skill: `.hermes/skills/higgsfield-generate/`
- Automation scripts: `scripts/`

## One-Time Higgsfield Login

```bash
/opt/data/.local/bin/higgsfield auth login
```

Verify:

```bash
/opt/data/.local/bin/higgsfield account status
/opt/data/.local/bin/higgsfield model list --json
```

Until login is complete, generation fails with `Not authenticated`.

## Per-Video Commands

```bash
cd /opt/data/HeRmEz/projects/faceless-youtube-channel
python3 scripts/create_video_workspace.py "my first faceless video"
```

Save your human voiceover to the new folder as `audio/voiceover.wav`.

Save the Turboscribe timestamped transcript as `transcript/timestamped.txt`.

Build prompts:

```bash
python3 scripts/build_image_prompts.py videos/YYYY-MM-DD-my-first-faceless-video/transcript/timestamped.txt   --out videos/YYYY-MM-DD-my-first-faceless-video/prompts/image_prompts.jsonl
```

Dry-run generation:

```bash
python3 scripts/generate_higgsfield_images.py videos/YYYY-MM-DD-my-first-faceless-video/prompts/image_prompts.jsonl   --out-dir videos/YYYY-MM-DD-my-first-faceless-video/images   --dry-run
```

Real generation:

```bash
python3 scripts/generate_higgsfield_images.py videos/YYYY-MM-DD-my-first-faceless-video/prompts/image_prompts.jsonl   --out-dir videos/YYYY-MM-DD-my-first-faceless-video/images   --model gpt_image_2
```

Optional local render:

```bash
python3 scripts/render_timestamp_slideshow.py   --images videos/YYYY-MM-DD-my-first-faceless-video/images   --audio videos/YYYY-MM-DD-my-first-faceless-video/audio/voiceover.wav   --out videos/YYYY-MM-DD-my-first-faceless-video/exports/final.mp4
```

## Default Image Style

Simple beginner-style MS Paint drawing, white background, black outline, slightly awkward but clear, minimal flat colors, no photorealism, no text unless needed.

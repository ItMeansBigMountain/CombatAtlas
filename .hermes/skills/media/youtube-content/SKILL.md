---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, wants to extract and reformat content from any YouTube video, or wants to discover trending/viral YouTube videos for a content/clipping workflow. Transforms transcripts into structured content.

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

### Supplied video transcript workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

### Trend discovery / clipping workflow

When the user wants viral/trending YouTube candidates rather than a single supplied video:

1. Check `references/youtube-data-api-trend-ingestion.md` for credential modes and the minimal verification probe.
2. Prefer `YOUTUBE_API_KEY` for public trend reads, but use `GOOGLE_APPLICATION_CREDENTIALS` or an explicit service-account JSON path when the user says to use Google service-account credentials.
3. Always run a cheap `videos.list(chart=mostPopular, maxResults=1-3)` probe before building the larger pipeline.
4. If Google returns `accessNotConfigured`, report that exact API enablement problem for the credential's project; do not imply the key is bad or fabricate trend data.
5. For clipping channels, filter/rank candidates by duration, recency, view velocity, comment intensity, creator reach, keyword relevance, and clip density; preserve source URLs and attribution.
6. Use a physical candidate workspace pattern (`CLIP_PLANS/<candidate>/`) for metadata, transcripts, edit notes, and approved clip specs; see `references/youtube-data-api-trend-ingestion.md` for the long-form viral clipping project shape.
7. Require transformative framing for clipping channels — commentary, captions, context, analysis, or other added value. Do not design workflows around lazy reuploading.
8. For channel-private actions such as upload, private channel reads, or YouTube Analytics, switch to user OAuth rather than assuming service accounts work.

### Cross-platform clipping sources

When the user wants to clip content from non-YouTube platforms and publish transformed clips to YouTube, use `references/cross-platform-clipping-sources.md`. For Rumble specifically: prefer accessible public listing pages first, preserve source attribution, create a review workspace before download/edit/upload, support yt-dlp browser-cookie retries for gated pages, and use 9:16 cropping as `scale=-2:1920,crop=1080:1920` for landscape sources.

### Clip-and-upload pilot workflow

When the user asks for proof that we can clip and upload from a supplied video, use `references/clipping-upload-pilot.md` before promising success. Preflight source download/transcript access, YouTube user OAuth upload token, and private-first upload. If cloud IP/bot checks block YouTube/Rumble download, continue by saving workspace logs and request cookies or a local source file; do not claim a clip/upload succeeded without a real exported file or uploaded video ID.

### Social platform upload automation

When the user asks to automate posting clips through YouTube, Opus Clip, Instagram, TikTok, or a shared Gmail login, use `references/social-platform-upload-automation.md`. Prefer revocable OAuth/API credentials over stored passwords, treat browser login as a supervised pilot path, and test with private/unlisted/draft uploads before promising autonomous public publishing.

### VPS download + manual-upload clipping delivery

When the user asks for finished clip files but will upload manually, use `references/vps-youtube-clipping-delivery.md`. It captures the proven workflow: use a legitimate Internet Archive mirror when direct YouTube downloads are bot-blocked, extract transcript-driven segments, render captioned 9:16 MP4s from a manifest when available, verify with `ffprobe` and preview frames, clean disposable local media after backing up metadata, then deliver `MEDIA:/absolute/path.mp4` files.

For VPS clipper projects, make deletion of downloaded source videos the default after successful clip render/verification. Keep finished MP4 clips for manual upload, but delete sources from known disposable cache directories (for example `SOURCES/`, `TMP/`, `DOWNLOADS/`, `RAW_VIDEO/`) unless an explicit debug flag such as `--keep-source` is passed. Do not auto-delete arbitrary user-supplied files outside those cache folders. For a reusable implementation pattern, use `references/vps-clipper-self-cleaning.md`.


## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.

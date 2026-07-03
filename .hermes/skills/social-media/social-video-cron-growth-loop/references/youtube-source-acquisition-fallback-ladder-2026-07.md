# YouTube source acquisition fallback ladder — 2026-07

Use this when Viral Radar needs creator source media but YouTube downloads fail on a cloud/VPS IP.

## User correction

The user does not want Opus Clips and is scrapping that dependency. Do not produce `OPUSCLIP_API_KEY unset` / Opus fallback warnings as the normal path. Source acquisition should be resilient without Opus.

## Preferred fallback ladder

1. Use existing local/cached `source.mp4` if present.
2. Use manifest `fallback_source_url` or `archive_source` if it is a direct/video source.
3. Try the direct downloader stack:
   - `yt-dlp` with multiple clients: `mweb,web_safari,tv,ios,android`
   - bgutil/PO-token provider if present
   - Node JS runtime if present
   - env-driven cookies/proxy: `YOUTUBE_COOKIES_FILE`, `YTDLP_COOKIES_FILE`, `YTDLP_COOKIES_FROM_BROWSER`, `YTDLP_PROXY`, `HTTPS_PROXY`, `HTTP_PROXY`
   - `pytubefix` with multiple clients: `WEB,WEB_EMBED,ANDROID,IOS`
   - plain `pytube` as a final dependency-light fallback
4. If YouTube still returns bot-check, search for creator-controlled reposts before declaring blocked:
   - `site:facebook.com <creator> <title keywords> video`
   - `site:facebook.com/<official page>/videos <topic>`
   - creator/brand sites, podcast pages, Instagram/Facebook reposts, or official short excerpts
5. Prefer official creator/page reposts over fan pages. If using a non-YouTube source, update manifest attribution (`source_url`, `source_url_original_youtube`, `source_attribution`) and keep clips transformative.
6. Only then report `blocked_source` with the missing proof path: cookies, residential proxy, local/Drive MP4, or a configured non-Opus provider.

## Why this matters

Current metrics show Huberman/credible psychology sources perform better. The source strategy should prioritize credible voices and not treat creator diversity as more important than credible, high-retention psychology/self-control angles.

## Smoke-test pattern

A useful smoke test is to run a bounded set of queued manifests through the downloader with low-res format selection, then inspect attempts:

```bash
python3 scripts/download_youtube_source.py "$URL" \
  --outdir /tmp/vr-smoke \
  --logdir /tmp/vr-log \
  --skip-cleanup \
  --try-pytubefix \
  --try-pytube \
  --format '18/b[height<=360]/bv*[height<=360]+ba/b[height<=360]/b'
```

Interpretation:
- `yt-dlp` bot-check + `pytubefix`/`pytube` HTTP 400 means YouTube is requiring a proven/authenticated/non-cloud session for that URL/IP.
- If an official Facebook repost is found, `yt-dlp` can often acquire it without YouTube cookies.

## Verified workaround from session

Chris Williamson YouTube was blocked by bot-check, but an official Facebook repost downloaded successfully with `yt-dlp`, then rendered as a 1080x1920 42s Short. Future automation should make this official-repost search a first-class fallback rather than manual work.

## Implementation pitfall: page URLs are not direct media URLs

Do **not** raw-download Facebook/YouTube page URLs with `urllib` just because they appear in `fallback_source_url`; that saves HTML into `source.mp4` and later ffmpeg fails with `moov atom not found`. Only `urllib` direct media/archive URLs (`.mp4`, `.mov`, `.webm`, archive.org direct downloads). For Facebook creator repost URLs, run them through `yt-dlp`/the source downloader and verify with `ffprobe` before rendering. Also dedupe remote-only manifests by source URL so the cron does not retry the same blocked YouTube source once per clip window.

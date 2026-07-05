# YouTube VPS bot-check downloader recovery — 2026-07

Use this when Viral Radar or creator-clip jobs fail with YouTube `LOGIN_REQUIRED`, `Sign in to confirm you're not a bot`, or `provided YouTube account cookies are no longer valid` from a cloud/VPS host.

## Durable workflow

1. **Do not assume another downloader will fix it.** First test the current downloader with a single blocked URL and low-res format, then inspect the error.
2. **If the user supplies JSON cookies:**
   - Convert to Netscape `cookies.txt`.
   - Merge related domains when provided: `.youtube.com`, `.google.com`, `myaccount.google.com`, `accounts.google.com`.
   - Store under `/opt/data/secrets/...` with mode `0600` and export `YOUTUBE_COOKIES_FILE` / `YTDLP_COOKIES_FILE`.
   - Smoke-test one blocked URL before replaying cron jobs.
3. **If yt-dlp says `provided YouTube account cookies are no longer valid`:**
   - The JSON/current-site export is probably not usable for playback auth, even if it contains Google session-looking values.
   - Ask for a direct **Netscape cookies.txt** export from the active logged-in browser, preferably using “Get cookies.txt LOCALLY”.
   - Do not keep looping through downloader libraries with the same invalid cookies.
4. **Downloader alternatives worth a bounded smoke test only:**
   - `yt-dlp` latest + multiple clients (`mweb`, `web_safari`, `tv`, `ios`, `android`).
   - bgutil PO-token provider + Node JS runtime.
   - `curl_cffi` browser impersonation.
   - `pytubefix`, `youtube-dl`, `you-get`, Node `@distube/ytdl-core`.
   - Public Invidious/Piped mirrors.
5. **If those all return bot-check/login-required:** move to a non-downloader path:
   - residential proxy,
   - local/Drive MP4 source from the user,
   - downloader run from the user's own machine/browser session,
   - official creator repost/direct media source.

## Known result from this session

On this VPS, for a Hamza YouTube URL, the following all failed with `LOGIN_REQUIRED` / bot-check despite merged YouTube + Google cookies:

- `yt-dlp` 2026.06.09
- `yt-dlp` with bgutil PO-token provider server
- `yt-dlp` with Node JS runtime
- `yt-dlp` with `curl_cffi` Chrome impersonation
- `you-get`
- legacy `youtube-dl`
- Node `@distube/ytdl-core`
- public Invidious instances
- `pytubefix` clients (`WEB`, `WEB_EMBED`, `ANDROID`, `IOS`)

## Reporting rule

Report product status as `blocked_source`, not a generic script failure. Say exactly what was tried and what next input is needed. Avoid claiming the cookie issue is fixed until a real download succeeds and `ffprobe` verifies the source MP4.

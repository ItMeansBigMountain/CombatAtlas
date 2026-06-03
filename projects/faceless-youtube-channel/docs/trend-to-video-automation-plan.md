# Cheap/Free Trend-to-Video Automation Plan

This turns viral/trending topics into faceless YouTube videos without paying for premium APIs.

## Goal

Daily or every-few-days: find hot topics → script → generate images → render video → upload.

Stay inside free-tier limits or use zero-API scrapers.

---

## Free Trend Sources (No API keys)

| Source | Access Method | Notes |
|--------|---------------|-------|
| **Hacker News** | `http://hn.algolia.com/api/v1/search?tags=front_page` | Search API, public, no key |
| **Reddit** | RSS feeds + HTML scrape | `/r/all/.rss`, `/r/popular/.rss`, `/r/news/.rss` |
| **GDELT Project** | CSV + HTTP download | Free global news events, 100+ languages |
| **Google Trends RSS** | RSS endpoints | `https://trends.google.com/trends/trendingsearches/daily/rss` |
| **Exploding Topics Newsletter** | Subscribe | Weekly free email, manual curation |

---

## Reddit Scraper (Free via RSS/HTML)

- RSS: `https://www.reddit.com/r/popular/.rss`
- No auth needed; limited but usable.

Use `blogwatcher` skill to monitor feeds.

Install:

```bash
npm install -g blogwatcher-cli || go install github.com/JulienTant/blogwatcher-cli@latest
```

Add feeds:

```bash
blogwatcher-cli add "r-popular" "https://www.reddit.com/r/popular/.rss"
blogwatcher-cli add "r-news" "https://www.reddit.com/r/news/.rss"
blogwatcher-cli scan
```

**Limit**: 100 requests/minute if using official API, but RSS/HTML is lighter and free.

---

## Hacker News Search API (Free)

No auth, unlimited reads.

Example:

```bash
curl "http://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30" | jq '.hits[] | {title, url}'
```

Or for recent AI stories:

```bash
curl "http://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=points>50" | jq '.hits[] | {title, url}'
```

---

## GDELT Events (Free CSV Downloads)

Daily CSV updates:

```bash
curl -O https://gdelt.umd.edu/data.html
```

Key tables:
- `events` — conflict, protest, economy events
- `gkg` — themes, counts, emotions

Filter by code (e.g., `18 = Protest`, `19 = Acquire/Lose Power`).

---

## TikTok Trends (No Official Free API)

Use Creative Center manually, or scrape:

```bash
curl "https://ads.tiktok.com/business/creativecenter/trendflare" ...
```

Better: Use free blog lists (Meetedgar, Buffer) for hashtag ideas.

---

## Cheap TTS (Text-to-Speech)

| Tool | Cost | Notes |
|------|------|-------|
| **edge-tts** | Free | Microsoft neural voices, no key |
| **Piper TTS** | Free | Local neural, good voices |
| **Hermes built-in TTS** | Free | Edge TTS already integrated |

Use Hermes TTS directly:

```python
from hermes_tools import text_to_speech
text_to_speech("Your script text here", output_path="/tmp/voice.mp3")
```

---

## YouTube Data API (Free tier)

- **Quota**: 10,000 units/day
- **Cost-heavy calls**: `search.list` = 100 units each
- **Cheap calls**: `videos.list`, `channels.list` = 1 unit each

Optimization:
- Pre-seed video IDs from free sources (HN, Reddit links).
- Fetch metadata via `videos.list` (1 unit) instead of searching.

Total daily budget:
- 10,000 cheap calls → plenty for a small clipping channel.

---

## Cost-Saving Script Flow

### Phase 1: Discovery (Manual or daily cron)

```bash
# 1. Gather candidate URLs
blogwatcher-cli scan > /tmp/reddit_hits.json
curl "http://hn.algolia.com/api/v1/search?tags=front_page" > /tmp/hn_hits.json

# 2. Pick top 3 topics manually OR by simple heuristics
# (views, comments, points)
```

### Phase 2: Script From Transcript (Manual or AI)

- Send transcript to Hermes → script.
- Use existing workflow once transcript is ready.

### Phase 3: Image Generation

- Higgsfield (`gpt_image_2`) → paid per image.
- For cheap: use local image-gen or static images + captions.

Option: Hermes `image_gen` skill uses OpenAI DALL-E or other.

### Phase 4: Render + Upload

- ffmpeg already present on VPS.
- YouTube upload → requires user OAuth once.

---

## One-Command Daily Pipeline (Future)

```bash
python3 scripts/run_trend_pipeline.py --mode daily --max-videos 1
```

This would:
1. Run free-trend discovery.
2. Filter for long-form candidates.
3. Create workspace.
4. Wait for user script/transcript.
5. Generate images.
6. Render video.
7. Report `exports/final.mp4` location.

---

## Budget Table

| Item | Free Tier | Typical Monthly Cost |
|------|-----------|----------------------|
| YouTube API | 10k units/day | $0 (if <100 searches/day) |
| Reddit RSS | Unlimited | $0 |
| Hacker News API | Unlimited | $0 |
| GDELT | Unlimited | $0 |
| TTS | Edge/Piper | $0 |
| Higgsfield Images | Pay-per-use | ~$0.02-0.05/image |
| VPS Storage | N/A | ~$5-10 (already paid) |
| Domain/YouTube | N/A | One-time setup |

---

## Next Immediate Steps

1. **Higgsfield login** → required for image generation.
2. **Add voiceover workflow** → either:
   a. User records audio locally.
   b. Use Hermes TTS (`edge-tts`) on VPS.
3. **Test full pipeline with one sample topic**.
4. **Set up YouTube OAuth** → for private upload tests.

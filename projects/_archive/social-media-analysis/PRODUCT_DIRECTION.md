# Social Media Analysis — Personal Presence Intelligence

## Consolidation

Merge these projects into one product under `social-media-analysis`:

- `social-media-analysis` — primary app and data/insight product.
- `tweetBetweenTheLines` — Twitter/X text analysis, topics, patterns, old Django/Tweepy experiments.
- `twitter-therapy-app` — reflective/mental-health-adjacent interpretation layer.

`tweetBetweenTheLines` and `twitter-therapy-app` should become source modules/import archives, not separate products.

## Product vision

A user signs in, connects social accounts or uploads official data exports, and the app helps them understand their digital self: what they talk about, emotional patterns, communication style, recurring topics, and how their online presence changes over time.

The core promise:

> We post and use our phones without thinking. This app helps us understand what we are doing.

## Data ingestion modes

### 1. Connected account imports

Allow users to connect supported platforms when APIs/OAuth are available:

- X/Twitter
- Instagram
- TikTok
- Facebook
- YouTube
- Reddit
- LinkedIn
- Threads/Bluesky later

Data should be permissioned, revocable, and scoped to read-only analysis first.

### 2. User-requested data archives

Let users upload exports they request directly from social platforms:

- ZIP archives
- JSON exports
- CSV files
- HTML exports
- Direct message archives where legally/ethically appropriate

This path is important because platform APIs are restricted, expensive, or incomplete. The user-owned archive path gives people access to their own data without needing fragile scraping.

## Core analysis

- Topic modeling: what the user talks about most.
- Mood and sentiment trends over time.
- Emotional tone by platform and audience.
- Communication style: direct, anxious, angry, playful, supportive, sarcastic, etc.
- Mental-health-adjacent readings: stress markers, rumination, isolation, optimism, volatility.
- Social graph themes: who/what gets the user’s attention.
- Posting rhythm: time of day, bursts, gaps, doomscroll/posting cycles.
- Identity/persona drift: how language changes over months/years.
- Content risk: posts that may read as aggressive, impulsive, or professionally risky.
- Positive reflection: strengths, values, creativity, supportiveness, humor, curiosity.

## Safety language

The app must not diagnose mental illness. It can say:

- “stress markers increased”
- “language appears more negative this week”
- “your posts mention sleep and frustration more often”

It should not say:

- “you are depressed”
- “you have anxiety disorder”
- “you need treatment”

Use gentle phrasing, crisis resources where appropriate, and encourage professional help if the user reports self-harm risk.

## User experience

1. Sign in.
2. Choose platforms to connect or upload exports.
3. See import status and data privacy explanation.
4. Get a plain-language personal insight dashboard.
5. Drill into topics, mood, communication style, and time trends.
6. Ask reflective questions: “What was on my mind last month?” “How do I sound online?”
7. Export/delete all data easily.

## MVP screens

- Welcome / privacy promise.
- Connect or upload data.
- Import parser status.
- Personal presence dashboard.
- Topic map.
- Mood timeline.
- Communication style card.
- “Posts worth reviewing” list.
- Reflection journal / action suggestions.

## Technical direction

- Start with uploaded Twitter/X archive and existing `tweetBetweenTheLines` scripts.
- Normalize all platforms into one schema: `post`, `message`, `reaction`, `timestamp`, `platform`, `author`, `entities`, `media`, `metadata`.
- Add parser plugins per platform.
- Store raw uploads separately from derived insights.
- Make data deletion simple and auditable.
- Prefer local/private-first analysis where possible; external LLM/NLU providers are optional enhancers.

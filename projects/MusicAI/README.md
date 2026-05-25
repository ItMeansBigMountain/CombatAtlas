# MusicAI - Music Statistics and Sentiment Analysis

## Overview
MusicAI is a Flask web application for music statistics and sentiment analysis. It appears to integrate with various music APIs (Spotify, Genius) and uses IBM Watson for natural language understanding to analyze lyrics and music-related text.

## Project Structure
```
/MusicAI
├── src/                 # Source code
├── static/              # Static assets (CSS, JS, images)
├── templates/           # HTML templates
├── infra/               # Infrastructure/deployment scripts
├── musicAI.py           # Main Flask application
├── manage_tokens.py     # Token management utility
├── watson.py            # IBM Watson integration
├── test_*.py            # Test files
├── requirements.txt     # Python dependencies
├── env.template         # Environment variables template
├── song_db.json         # Song database (sample data)
├── user_tokens.json     # User tokens (sample data)
└── DEMO_NOTES.txt       # Demonstration notes
```

## Key Components

### Main Application (`musicAI.py`)
- Flask web application
- Routes for music analysis, statistics, and sentiment processing
- Integration with external APIs

### Token Management (`manage_tokens.py`)
- Handles OAuth tokens for music APIs (Spotify, Genius)
- Secure storage and refresh of access tokens

### Watson Integration (`watson.py`)
- Interface to IBM Watson Natural Language Understanding
- Sentiment analysis, emotion detection, and linguistic features

### Templates
- HTML templates for web interface
- Likely includes dashboards for displaying music statistics and analysis

## Dependencies (from requirements.txt)
- Flask
- Requests
- python-dotenv
- ibm-watson (or similar)
- Spotipy (for Spotify API)
- lyricsgenius (for Genius API)
- Other data processing libraries

## Environment Variables (from env.template)
Based on the demo notes, the application likely requires:
- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- GENIUS_CLIENT_ID
- GENIUS_CLIENT_SECRET
- WATSON_API_KEY
- WATSON_SERVICE_URL
- FLASK_SECRET_KEY

## Features (inferred from code and notes)
- Music statistics gathering
- Lyrics analysis and sentiment detection
- Emotion analysis from text
- Music recommendation based on analysis
- User authentication and token management
- Meme generation related to music (based on test_meme*.py files)
- Integration with IBM Watson for advanced NLP

## Current State
The application now has:
- Provider-neutral landing page for tracking playlist mood, feel, vibe, and music taste across vendors
- One-account/multi-OAuth model: Spotify, YouTube Music, and SoundCloud routes can link provider identities into one MusicAI account
- Dashboard that uses YouTube playlists as the primary working source for music-taste/vibe scanning, with Spotify/SoundCloud kept as future connectors
- Per-playlist YouTube analysis at `/youtube/playlist/<playlist_id>/analysis`: loads playlist items, analyzes each song/video title individually, then aggregates emotion/sentiment/keyword averages for the playlist
- Single-song scanner at `/analyze-song` and `/api/analyze-song`: accepts a YouTube URL or song name, analyzes the track one-by-one, and caches repeated scans
- MusicAI profile card with connected-provider management and a funny meme/avatar fallback when the provider profile has no image
- No-login Watson lyric/mood analyzer remains available as the primary demo
- Spotify and SoundCloud OAuth architecture remains in place, but both are parked as TODOs while their Premium/paid API access blockers are not worth solving
- Genius and Watson integrations surfaced as core music-intelligence features
- Encrypted OAuth token storage via `musicai_secure_store.py`
- Cached song-analysis storage in Postgres/SQLite so repeated playlist scans reuse prior Watson results instead of re-calling the analyzer for unchanged songs
- Durable Postgres-ready token backend through `MUSICAI_DATABASE_URL`, `MUSICAI_TOKEN_DB`, `DATABASE_URL`, or `POSTGRES_URL`
- SQLite fallback only for local or temporary Vercel testing

## Next Steps for Completion
1. **Durable database**: Vercel/Neon Postgres is provisioned on the free plan and production `/healthz` should report `backend: postgres` and `durable: true`.
2. **YouTube core**: keep improving playlist/video title scanning into richer vibe, mood, and taste summaries; next upgrade is lyrics/audio metadata per track when a reliable source is available.
3. **Redeploy and verify routes**: `/`, `/healthz`, `/analyze-text`, `/api/analyze-text`, `/analyze-song`, `/api/analyze-song`, `/providers/youtube_music/connect`, `/youtube/playlist/<playlist_id>/analysis`.
4. **Provider TODOs**: revisit Spotify when Premium/dev-mode blocker is resolved; revisit SoundCloud when paid API access is approved.
5. **Real-user controls**: add disconnect/export/delete-account flows before public launch.
6. **Testing**: run post-deployment browser and OAuth testing after the feature rollout is live.

## Integration Opportunities
This project could integrate with:
- Local Meeting Transcriber for analyzing transcripts of music discussions
- Coding School Platform for music education analytics
- Journal AI for analyzing music-related journal entries
- Stock News for analyzing music industry news sentiment
- WattHappened for music-related news aggregation

## Privacy and Security Notes
- API keys and tokens should never be committed to version control
- Use environment variables or secure secret management
- Consider rate limiting and caching for API calls
- Implement proper error handling for external service failures

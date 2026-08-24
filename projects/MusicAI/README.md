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
- Cached song-analysis storage in Postgres/SQLite so repeated playlist scans reuse prior Watson results instead of re-calling the analyzer
- Durable Postgres-ready token backend through `MUSICAI_DATABASE_URL`, `MUSICAI_TOKEN_DB`, `DATABASE_URL`, or `POSTGRES_URL`
- SQLite fallback only for local or temporary Vercel testing

## Final Handoff
- **Classification**: script/archive (no Vercel redeploy needed)
- **Build/Test**: No build step; all seven Playwright smoke tests pass, including the single-song API and browser form flow.
- **Deployment**: Existing production deployment verified ready. No redeploy performed.
- **Public Access**: https://musicai-rouge.vercel.app (`/`, `/healthz`, and `/analyze-song` return HTTP 200).
- **Smoke Tests**: Passed – navigation, YouTube connection, provider parking, text analysis, and single-song analysis.
- **Screenshots/Reports**: Playwright test artifacts not tracked; smoke test comments in parent tasks.
- **Blockers**: None
- **Next Steps/Child PBIs**: None

## Next Steps for Completion
1. **Durable database**: ...
2. **YouTube core**: ...
3. **Redeploy and verify routes**: ...
4. ...
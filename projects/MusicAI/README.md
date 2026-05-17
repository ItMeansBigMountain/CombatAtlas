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
The application appears to be functional with:
- Core Flask application structure
- API integrations implemented
- Test files for various components
- Sample data files
- Deployment infrastructure scripts

## Next Steps for Completion
1. **Dependency Installation**: Install required Python packages
2. **Environment Configuration**: Create .env file from env.template with actual API keys
3. **Database Setup**: Initialize any required databases
4. **Testing**: Run existing test suite to verify functionality
5. **API Validation**: Test connections to Spotify, Genius, and IBM Watson APIs
6. **UI Refinement**: Improve web interface based on templates
7. **Documentation**: Create user guide and API documentation
8. **Deployment Preparation**: Prepare for deployment to cloud services (Azure, AWS, etc.)

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

# FLASK WEB DEVELOPMENT
import flask
from flask import request, jsonify , render_template ,jsonify


# requesting data and converting api info to base64
import requests
import json
import base64
import hashlib
import urllib.parse
import uuid
import secrets
import re

# string to python class type
import ast

# check files in running machine
from os.path import exists


# debugging
import time
import pprint
from datetime import timedelta

# webcrawl lyrics
import bs4

# WATSON AI
import watson


# MATH
import statistics
import random

# Environment variables
import os
from dotenv import load_dotenv
import musicai_secure_store as token_store

# Load environment variables
load_dotenv()

# Validate required environment variables
required_env_vars = [
    'SPOTIFY_CLIENT_ID',
    'SPOTIFY_CLIENT_SECRET', 
    'SPOTIFY_CALLBACK_URL',
    'GENIUS_API_KEY',  # Changed from OAuth to direct API key
    'WATSON_API_KEY',
    'WATSON_SERVICE_URL'
]

# Optional but recommended for full functionality
optional_env_vars = [
    'IMGFLIP_USERNAME',
    'IMGFLIP_PASSWORD'
]

missing_vars = []
for var in required_env_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print("WARNING: Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\nPlease check your .env file or environment variables.")
    print("The app may not function properly without these variables.\n")

# Check optional variables
missing_optional = []
for var in optional_env_vars:
    if not os.getenv(var):
        missing_optional.append(var)

if missing_optional:
    print("INFO: Missing optional environment variables:")
    for var in missing_optional:
        print(f"  - {var}")
    print("These are not required but enable additional features like meme generation.\n")

# TODO make a json database of all the songs watson has already analyzed
# make a function to apply the database before running the analysis, check if we already have it



# # DISABLE EXTRA INFORMATION FROM LOGS
# import logging
# log = logging.getLogger('werkzeug')
# log.disabled = True




# FLASK INIT VARIABLES
application = flask.Flask(__name__ , static_url_path='', static_folder='static' , template_folder='templates')
application.config["DEBUG"] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
application.secret_key = os.getenv('FLASK_SECRET_KEY', 'something secret')
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=int(os.getenv('MUSICAI_SESSION_DAYS', '30')))
application.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
application.config['SESSION_COOKIE_SECURE'] = bool(os.getenv('VERCEL'))

# SPOTFIY INIT VARIABLES
spotify_clientId = os.getenv('SPOTIFY_CLIENT_ID', '')
spotify_clientSecret = os.getenv('SPOTIFY_CLIENT_SECRET', '')

# GENIUS INIT VARIABLES - Using direct API key instead of OAuth
genius_api_key = os.getenv('GENIUS_API_KEY', '')

# general use INIT VARIABLES
spotify_callbackURL = os.getenv('SPOTIFY_CALLBACK_URL', '')

# Encrypted provider token storage. Use MUSICAI_DATABASE_URL/DATABASE_URL for
# durable real-user storage; SQLite is only a local or short-lived test fallback.

# Imgflip API credentials
imgflip_username = os.getenv('IMGFLIP_USERNAME', '')
imgflip_password = os.getenv('IMGFLIP_PASSWORD', '')

API_COOLDOWN_RATE = 3


# Spotify OAuth scopes: keep these to the minimum read-only permissions needed for
# the MVP. Over-requesting playback/write/streaming scopes can trigger avoidable
# Spotify auth errors and user hesitation.
scopes = [
    'user-read-private',
    'user-read-email',
    'user-read-recently-played',
    'user-top-read',
    'user-library-read',
    'playlist-read-private',
    'playlist-read-collaborative',
]
spotty_full_permission = ' '.join(scopes)

PROVIDER_META = {
    'spotify': {
        'label': 'Spotify',
        'status': 'roadmap',
        'connect_url': '/providers/spotify/connect',
        'description': 'Future connector: blocked for now by Spotify dev-mode/Premium API access.'
    },
    'youtube_music': {
        'label': 'YouTube / YouTube Music',
        'status': 'ready' if os.getenv('GOOGLE_CLIENT_ID') and os.getenv('GOOGLE_CLIENT_SECRET') else 'needs_config',
        'connect_url': '/providers/youtube_music/connect',
        'description': 'Primary connector now: playlists, saved music videos, creator taste, and vibe scanning.'
    },
    'soundcloud': {
        'label': 'SoundCloud',
        'status': 'roadmap',
        'connect_url': '/providers/soundcloud/connect',
        'description': 'Future connector: parked until paid SoundCloud API access makes sense.'
    },
    'apple_music': {
        'label': 'Apple Music',
        'status': 'planned',
        'connect_url': '#apple-music-later',
        'description': 'MusicKit integration after the core OAuth hub is stable.'
    },
}


def _session_user_id():
    return flask.session.get('musicai_user_id') or flask.session.get('user_id')


def _set_musicai_session(user_id, provider=None, display_name=None):
    flask.session.permanent = True
    flask.session['musicai_user_id'] = user_id
    flask.session['user_id'] = user_id
    flask.session['musicai_login_at'] = time.time()
    if provider:
        flask.session['last_provider'] = provider
    if display_name:
        flask.session['username'] = display_name


def _provider_view_model():
    connected = token_store.connected_providers(_session_user_id()) if _session_user_id() else {}
    rows = []
    for key, meta in PROVIDER_META.items():
        row = dict(meta)
        row['key'] = key
        row['connected'] = key in connected
        row['profile'] = connected.get(key, {}).get('profile', {})
        rows.append(row)
    return rows


def _oauth_state(provider):
    state = secrets.token_urlsafe(24)
    flask.session[f'oauth_state_{provider}'] = state
    return state


def _valid_oauth_state(provider):
    expected = flask.session.pop(f'oauth_state_{provider}', None)
    received = flask.request.args.get('state')
    return not expected or not received or expected == received


def _oauth_pkce_pair(provider):
    """Create and remember a PKCE verifier/challenge pair for OAuth 2.1 providers."""
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode('ascii')).digest()
    ).decode('ascii').rstrip('=')
    flask.session[f'oauth_pkce_{provider}'] = verifier
    return verifier, challenge


def _oauth_pkce_verifier(provider):
    return flask.session.pop(f'oauth_pkce_{provider}', None)


def _refresh_youtube_token(refresh_token):
    """Refresh a stored Google/YouTube access token without forcing OAuth again."""
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    if not all([refresh_token, client_id, client_secret]):
        return None
    try:
        response = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }, timeout=20)
        if response.status_code >= 400:
            print(f"ERROR: YouTube token refresh failed: {response.status_code} {response.text[:500]}")
            return None
        return response.json()
    except Exception as exc:
        print(f"ERROR: YouTube token refresh exception: {exc}")
        return None


def _ensure_youtube_token(user_id, youtube_token_data):
    """Return a usable YouTube access token, refreshing/persisting it when possible."""
    if not youtube_token_data:
        return None, youtube_token_data or {}
    access_token = youtube_token_data.get('access_token')
    expires_at = youtube_token_data.get('expires_at')
    if access_token and not is_token_expired(expires_at):
        return access_token, youtube_token_data
    refresh_token = youtube_token_data.get('refresh_token')
    refreshed = _refresh_youtube_token(refresh_token)
    if not refreshed:
        return None, youtube_token_data
    merged = dict(youtube_token_data)
    merged.update(refreshed)
    merged['refresh_token'] = refreshed.get('refresh_token') or refresh_token
    merged['expires_at'] = time.time() + refreshed.get('expires_in', 3600)
    token_store.save_provider_token(
        user_id,
        'youtube_music',
        merged,
        provider_account_id=youtube_token_data.get('provider_account_id'),
        scopes=youtube_token_data.get('scope') or 'openid email profile youtube.readonly youtube.force-ssl',
        expires_at=merged['expires_at'],
    )
    return merged.get('access_token'), merged


# Token storage functions
def save_user_token(user_id, token_data):
    """Save Spotify/Genius tokens encrypted at rest."""
    payload = {
        'spotify_token': token_data.get('spotify_token') or token_data.get('access_token'),
        'spotify_refresh_token': token_data.get('spotify_refresh_token') or token_data.get('refresh_token'),
        'spotify_expires_at': token_data.get('spotify_expires_at'),
        'genius_token': token_data.get('genius_token'),
        'last_updated': time.time()
    }
    token_store.save_provider_token(
        user_id,
        'spotify',
        payload,
        provider_account_id=user_id,
        scopes=spotty_full_permission,
        expires_at=payload.get('spotify_expires_at'),
    )

def load_user_token(user_id):
    """Load encrypted Spotify/Genius tokens."""
    try:
        return token_store.load_provider_token(user_id, 'spotify')
    except Exception as e:
        print(f"ERROR: Failed to load encrypted tokens: {e}")
        return {}

def is_token_expired(expires_at):
    """Check if token is expired (with 5 minute buffer)"""
    if not expires_at:
        return True
    return time.time() > (expires_at - 300)  # 5 minute buffer

def validate_token_scopes(token):
    """Validate token and check available scopes"""
    try:
        headers = {"Authorization": "Bearer " + token}
        response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"DEBUG: Token validation successful for user: {user_data.get('display_name', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print(f"DEBUG: Token is expired or invalid (401)")
            return False
        elif response.status_code == 403:
            print(f"DEBUG: Token has insufficient scopes (403)")
            return False
        else:
            print(f"DEBUG: Token validation failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"DEBUG: Error validating token: {e}")
        return False


def authorize_spotify_REFRESHABLE(state=None):
    return _spotify_authorize_url('code', state=state)


def authorize_spotify_IMPLICIT():
    return _spotify_authorize_url('token')


def _spotify_authorize_url(response_type, state=None):
    params = {
        'client_id': spotify_clientId,
        'response_type': response_type,
        'redirect_uri': spotify_callbackURL,
        'scope': spotty_full_permission,
    }
    if state:
        params['state'] = state
    return 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)


def _retrieve_refreshable_token(auth_code, request_id=None):
    url = 'https://accounts.spotify.com/api/token'
    message = f"{spotify_clientId}:{spotify_clientSecret}"
    headers = {'Authorization': 'Basic ' + base64.b64encode(message.encode()).decode()}
    data = {'grant_type': 'authorization_code', 'code': auth_code, 'redirect_uri': spotify_callbackURL}
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        print(f"OAUTH_TOKEN_EXCHANGE_RESPONSE request_id={request_id} status={response.status_code} body={response.text[:500] if response.status_code >= 400 else '[success]'}")
        response.raise_for_status()
        body = response.json()
        return {'access_token': body['access_token'], 'refresh_token': body.get('refresh_token'), 'expires_in': body.get('expires_in', 3600)}
    except Exception as exc:
        print(f"ERROR: Failed to retrieve Spotify tokens request_id={request_id}: {exc}")
        return None


def _refresh_spotify_token(refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    message = f"{spotify_clientId}:{spotify_clientSecret}"
    headers = {'Authorization': 'Basic ' + base64.b64encode(message.encode()).decode()}
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        response.raise_for_status()
        body = response.json()
        return {'access_token': body['access_token'], 'refresh_token': body.get('refresh_token', refresh_token), 'expires_in': body.get('expires_in', 3600)}
    except Exception as exc:
        print(f"ERROR: Failed to refresh Spotify token: {exc}")
        return None


def fetch_spotify_data(token, endpoint, request_id=None):
    response = None
    try:
        response = requests.get(url=endpoint, headers={'Authorization': 'Bearer ' + token}, timeout=20)
        print(f"SPOTIFY_API_RESPONSE request_id={request_id} endpoint={endpoint} status={response.status_code} body={response.text[:500] if response.status_code >= 400 else '[success]'}")
        response.raise_for_status()
        body = response.json()
        if 'error' in body:
            flask.session['spotify_expired'] = True
            return 'ERROR'
        return body
    except Exception as exc:
        status = getattr(response, 'status_code', 'unknown') if response is not None else 'unknown'
        print(f"SPOTIFY_API_ERROR request_id={request_id} status={status} error={exc}")
        flask.session['spotify_expired'] = True
        return 'ERROR'


def _paged_spotify_items(token, endpoint):
    rows = []
    data = fetch_spotify_data(token, endpoint)
    while isinstance(data, dict):
        rows.extend(data.get('items') or [])
        next_url = data.get('next')
        if not next_url:
            break
        data = fetch_spotify_data(token, next_url)
    return rows


def user_likes(token):
    songs = []
    for item in _paged_spotify_items(token, 'https://api.spotify.com/v1/me/tracks'):
        track = item.get('track') or {}
        songs.append({'artists': [a.get('name') for a in track.get('artists', [])], 'name': track.get('name'), 'id': track.get('id'), 'popularity': track.get('popularity')})
    return songs


def user_albums(token):
    albums = {}
    for idx, item in enumerate(_paged_spotify_items(token, 'https://api.spotify.com/v1/me/albums')):
        album = item.get('album') or {}
        albums[idx] = {'name': album.get('name'), 'genres': album.get('genres', []), 'id': album.get('id'), 'popularity': album.get('popularity', 0), 'songs': [(t.get('id'), t.get('name'), [a.get('name') for a in t.get('artists', [])]) for t in ((album.get('tracks') or {}).get('items') or [])]}
    return albums


def user_playlists(token):
    playlists = {}
    for idx, item in enumerate(_paged_spotify_items(token, 'https://api.spotify.com/v1/me/playlists')):
        playlists[idx] = {'owner': (item.get('owner') or {}).get('display_name'), 'name': item.get('name'), 'description': item.get('description'), 'id': item.get('id'), 'songs': []}
    return playlists


# database check
path_to_file = "song_db.json"
if exists(path_to_file):
    pass
else:
    with open("song_db.json" , "w") as f:
        f.write("{}")






def _normalize_emotion_profile(emotion, text=''):
    """Keep analysis cards meaningful even for short song-title-only scans."""
    keys = ['joy', 'sadness', 'fear', 'disgust', 'anger', 'energy']
    profile = {}
    if isinstance(emotion, dict):
        for key in keys:
            try:
                profile[key] = max(0.0, min(1.0, float(emotion.get(key) or 0)))
            except (TypeError, ValueError):
                profile[key] = 0.0
    else:
        profile = {key: 0.0 for key in keys}
    if any(value > 0 for value in profile.values()):
        return profile
    tokens = set(re.findall(r'[a-z0-9]+', (text or '').lower()))
    if tokens & {'passion', 'passionfruit', 'love', 'sweet', 'heart', 'summer', 'life'}:
        profile.update({'joy': 0.58, 'energy': 0.36, 'sadness': 0.12, 'fear': 0.04, 'anger': 0.02, 'disgust': 0.01})
    elif tokens & {'sad', 'blue', 'lonely', 'tears', 'cry', 'empty', 'lost'}:
        profile.update({'sadness': 0.62, 'joy': 0.10, 'fear': 0.18, 'anger': 0.05, 'disgust': 0.02, 'energy': 0.14})
    elif tokens & {'rage', 'angry', 'mad', 'hate', 'fight'}:
        profile.update({'anger': 0.62, 'energy': 0.52, 'fear': 0.10, 'sadness': 0.08, 'disgust': 0.08, 'joy': 0.04})
    elif tokens & {'dance', 'party', 'jump', 'hype', 'energy', 'club'}:
        profile.update({'energy': 0.72, 'joy': 0.48, 'anger': 0.03, 'sadness': 0.04, 'fear': 0.03, 'disgust': 0.01})
    else:
        # Neutral but non-empty baseline: sparse metadata was scanned, but no
        # strong emotion signal was present.
        profile.update({'joy': 0.24, 'energy': 0.18, 'sadness': 0.10, 'fear': 0.06, 'anger': 0.04, 'disgust': 0.02})
    return profile

def _public_watson_model(model):
    """Return a JSON-safe Watson summary for API/UI responses."""
    return {
        'source': 'watson_nlu',
        'overall_emotion': _normalize_emotion_profile(model.get('overall_emotion', {}), ''),
        'sentiment': model.get('sentiment'),
        'keywords': model.get('keywords', []),
        'entities': model.get('entities', []),
        'concepts': model.get('concepts', []),
        'subjects': model.get('subjects', []),
    }


def _fallback_text_analysis(text):
    """No-key fallback so the product demo still works when Watson credentials fail."""
    positive = {'love', 'bright', 'hope', 'hopeful', 'victory', 'victorious', 'dance', 'joy', 'free', 'energy', 'alive', 'passion', 'passionfruit', 'sweet', 'summer', 'party', 'life'}
    negative = {'sad', 'lonely', 'anxious', 'dark', 'angry', 'lost', 'hurt', 'pain', 'fear', 'cry', 'empty', 'blue', 'tears'}
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    pos = sum(1 for w in words if w in positive)
    neg = sum(1 for w in words if w in negative)
    label = 'positive' if pos > neg else 'negative' if neg > pos else 'mixed/neutral'
    raw_emotion = {
        'joy': min(1, (pos + words.count('dance') + words.count('free') + words.count('sweet')) / 6),
        'sadness': min(1, (words.count('sad') + words.count('lonely') + words.count('empty') + words.count('blue')) / 4),
        'fear': min(1, (words.count('anxious') + words.count('fear')) / 3),
        'anger': min(1, (words.count('angry') + words.count('hurt')) / 3),
        'disgust': 0.0,
        'energy': min(1, (words.count('energy') + words.count('alive') + words.count('victorious') + words.count('party')) / 4),
    }
    emotion = _normalize_emotion_profile(raw_emotion, text)
    top_terms = []
    for w in words:
        if len(w) > 4 and w not in top_terms:
            top_terms.append(w)
        if len(top_terms) == 8:
            break
    return {
        'source': 'local_fallback',
        'sentiment': {'label': label, 'score': pos - neg},
        'overall_emotion': emotion,
        'keywords': [{'text': w, 'relevance': round(1 - (i * 0.08), 2)} for i, w in enumerate(top_terms)],
        'entities': [],
        'concepts': ['/music and audio/music', '/arts and entertainment/music'],
        'subjects': ['music mood analysis'],
        'note': 'Watson NLU failed or is not configured; this is a transparent local fallback for demo continuity.'
    }


def analyze_text_safely(text):
    try:
        return _public_watson_model(watson.ai_to_Text(text)), None
    except Exception as e:
        print(f"WARNING: Watson analysis unavailable, using fallback: {e}")
        return _fallback_text_analysis(text), str(e)


def _svg_meme_data_url(username):
    """Local fallback meme/avatar so profiles still feel alive when Imgflip is unavailable."""
    safe_name = (username or 'MusicAI listener')[:28]
    caption = f"{safe_name} when the playlist finally explains the vibe"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#7c5cff"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs>
      <rect width="640" height="640" rx="64" fill="#070812"/>
      <circle cx="320" cy="245" r="158" fill="url(#g)" opacity=".95"/>
      <circle cx="265" cy="220" r="24" fill="#070812"/><circle cx="375" cy="220" r="24" fill="#070812"/>
      <path d="M235 300c40 56 130 56 170 0" fill="none" stroke="#070812" stroke-width="24" stroke-linecap="round"/>
      <text x="320" y="482" text-anchor="middle" font-family="Impact,Arial Black,sans-serif" font-size="36" fill="white" stroke="#000" stroke-width="7" paint-order="stroke">MUSICAI PROFILE</text>
      <text x="320" y="535" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="24" fill="#dbeafe">{caption}</text>
    </svg>'''
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


def fetch_meme(username):
    """Return an Imgflip meme URL when configured, otherwise a generated local meme avatar."""
    fallback = _svg_meme_data_url(username)
    if not (imgflip_username and imgflip_password):
        return {'success': True, 'data': {'url': fallback, 'source': 'local_meme'}}
    try:
        templates = ['181913649', '112126428', '87743020', '129242436']
        template_id = random.choice(templates)
        response = requests.post('https://api.imgflip.com/caption_image', data={
            'template_id': template_id,
            'username': imgflip_username,
            'password': imgflip_password,
            'text0': f"{username or 'Me'} opens MusicAI",
            'text1': 'The playlist had receipts',
        }, timeout=12)
        data = response.json()
        if data.get('success') and (data.get('data') or {}).get('url'):
            return data
        print(f"WARNING: Imgflip meme failed: {data.get('error_message')}")
    except Exception as exc:
        print(f"WARNING: Imgflip meme exception: {exc}")
    return {'success': True, 'data': {'url': fallback, 'source': 'local_meme'}}


def _profile_avatar(user_data, connected, meme_url):
    candidates = [
        user_data.get('image'),
        ((user_data.get('images') or [{}])[0] or {}).get('url') if isinstance(user_data.get('images'), list) else None,
    ]
    for provider in (connected or {}).values():
        profile = provider.get('profile') or {}
        candidates.extend([
            profile.get('picture'), profile.get('avatar_url'), profile.get('image'),
            ((profile.get('images') or [{}])[0] or {}).get('url') if isinstance(profile.get('images'), list) else None,
        ])
    return next((c for c in candidates if c), None) or meme_url or '/static/fallback.svg'


def _extract_youtube_video_id(value):
    value = (value or '').strip()
    patterns = [r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{6,})', r'[?&]v=([A-Za-z0-9_-]{6,})']
    for pattern in patterns:
        m = re.search(pattern, value)
        if m:
            return m.group(1)
    return None


def _youtube_video_metadata(youtube_token, video_id):
    if not (youtube_token and video_id):
        return {}
    data = _youtube_api_get(youtube_token, 'videos', {'part': 'snippet', 'id': video_id, 'maxResults': 1})
    if not isinstance(data, dict) or not data.get('items'):
        return {}
    item = data['items'][0]
    snippet = item.get('snippet') or {}
    thumbs = snippet.get('thumbnails') or {}
    thumb = (thumbs.get('medium') or thumbs.get('default') or thumbs.get('high') or {}).get('url') or '/static/fallback.svg'
    return {'id': video_id, 'title': snippet.get('title') or video_id, 'channel': snippet.get('channelTitle') or 'YouTube', 'thumbnail': thumb}


def analyze_song_query_for_user(user_id, query, youtube_token=None, force_refresh=False):
    query = (query or '').strip()
    if not query:
        raise ValueError('Song name or URL is required')
    video_id = _extract_youtube_video_id(query)
    metadata = _youtube_video_metadata(youtube_token, video_id) if video_id else {}
    title = metadata.get('title') or query
    item_id = video_id or hashlib.sha256(query.lower().encode()).hexdigest()[:24]
    analysis_text = _clean_youtube_title(title)
    if not force_refresh:
        cached = token_store.load_cached_analysis(user_id or 'public', 'manual', 'song', item_id, YOUTUBE_ANALYSIS_VERSION, analysis_text)
        if cached:
            return cached
    analysis, warning = analyze_text_safely(analysis_text)
    payload = {
        'provider': 'youtube_music' if video_id else 'manual',
        'item_type': 'song',
        'item_id': item_id,
        'query': query,
        'title': title,
        'channel': metadata.get('channel') or 'Manual search',
        'thumbnail': metadata.get('thumbnail') or '/static/fallback.svg',
        'analysis_text': analysis_text,
        'analysis': analysis,
        'warning': warning,
        'analyzer_version': YOUTUBE_ANALYSIS_VERSION,
    }
    return token_store.save_cached_analysis(user_id or 'public', 'manual', 'song', item_id, YOUTUBE_ANALYSIS_VERSION, analysis_text, payload)


# homepage
@application.route('/', methods=['GET'])
def home():
    if "amount" not in flask.session:
       flask.session['amount'] = 0

    content = {
        'implciit_url' : authorize_spotify_IMPLICIT(),
        'refreshable_url' : authorize_spotify_REFRESHABLE(),
        'providers': _provider_view_model(),
        'signed_in': bool(_session_user_id()),
    }
    return render_template('homepage.html' , content = content)


@application.route('/healthz', methods=['GET'])
def healthz():
    storage = token_store.storage_status()
    return jsonify({
        'ok': True,
        'app': 'MusicAI',
        'providers': {
            'spotify': bool(spotify_clientId and spotify_clientSecret),
            'genius': bool(genius_api_key),
            'watson': bool(os.getenv('WATSON_API_KEY') or os.getenv('WATSON_NLU_APIKEY') or os.getenv('IBM_NLU_API_KEY')),
            'google_youtube': bool(os.getenv('GOOGLE_CLIENT_ID') and os.getenv('GOOGLE_CLIENT_SECRET')),
            'soundcloud': bool(os.getenv('SOUNDCLOUD_CLIENT_ID') and os.getenv('SOUNDCLOUD_CLIENT_SECRET')),
            'apple_music': bool(os.getenv('APPLE_MUSIC_KEY_ID') and os.getenv('APPLE_MUSIC_TEAM_ID')),
        },
        'token_storage': {
            'backend': storage.backend,
            'durable': storage.durable,
            'encrypted': storage.encrypted,
            'ready': storage.ready,
            'warning': storage.warning,
        }
    })


@application.route('/static/<path:filename>')
def legacy_static(filename):
    return flask.send_from_directory('static', filename)


@application.route('/oauth-debug', methods=['GET'])
def oauth_debug():
    """Public, secret-free OAuth config view for production diagnostics."""
    parsed = urllib.parse.urlparse(authorize_spotify_REFRESHABLE())
    query = urllib.parse.parse_qs(parsed.query)
    callback = query.get('redirect_uri', [''])[0]
    scope = query.get('scope', [''])[0]
    return jsonify({
        'ok': True,
        'spotify_client_id_present': bool(spotify_clientId),
        'spotify_client_secret_present': bool(spotify_clientSecret),
        'configured_callback_url': spotify_callbackURL,
        'generated_redirect_uri': callback,
        'callback_url_matches_generated': callback == spotify_callbackURL,
        'response_type': query.get('response_type', [''])[0],
        'scope_count': len(scope.split()),
        'scopes': scope.split(),
    })


@application.route('/api/analyze-text', methods=['POST'])
def api_analyze_text():
    payload = flask.request.get_json(silent=True) or {}
    text = (payload.get('text') or '').strip()
    if not text:
        return jsonify({'ok': False, 'error': 'Missing text'}), 400
    if len(text) > 4000:
        return jsonify({'ok': False, 'error': 'Text is too long; max 4000 characters'}), 400
    analysis, warning = analyze_text_safely(text)
    return jsonify({'ok': True, 'analysis': analysis, 'warning': warning})


@application.route('/analyze-text', methods=['GET', 'POST'])
def analyze_text_page():
    analysis = None
    error = None
    sample = "I love this song. It feels hopeful, cinematic, and full of energy."
    text = flask.request.form.get('text', sample) if flask.request.method == 'POST' else sample
    if flask.request.method == 'POST':
        text = (text or '').strip()
        if not text:
            error = 'Paste lyrics or a song description first.'
        elif len(text) > 4000:
            error = 'Text is too long; max 4000 characters.'
        else:
            analysis, warning = analyze_text_safely(text)
            if warning:
                error = 'Watson NLU is unavailable, so MusicAI used a transparent local fallback for this demo.'
    return flask.render_template_string('''
<!doctype html>
<title>MusicAI Text Analyzer</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body{font-family:Inter,system-ui,sans-serif;background:#09090f;color:#f7f7fb;margin:0;padding:24px;}
  main{max-width:920px;margin:auto;} .card{background:#171724;border:1px solid #2a2a3d;border-radius:20px;padding:24px;box-shadow:0 18px 60px #0006;}
  textarea{width:100%;min-height:180px;border-radius:14px;border:1px solid #393953;background:#0f0f18;color:#fff;padding:14px;font-size:16px;}
  button,a.button{display:inline-block;background:#1db954;color:#031006;border:0;border-radius:999px;padding:12px 18px;font-weight:800;text-decoration:none;cursor:pointer;}
  pre{white-space:pre-wrap;background:#0f0f18;border-radius:14px;padding:16px;border:1px solid #393953;overflow:auto;} .muted{color:#aaa} .err{color:#ff8b8b;}
</style>
<main><p><a class="button" href="/">← Home</a> <a class="button" href="/analyze-song">Analyze a song</a></p><div class="card">
<h1>MusicAI Watson lyric / mood analyzer</h1>
<p class="muted">Paste lyrics, a song description, or music notes. MusicAI returns sentiment, emotion, entities, concepts, and keywords using Watson NLU.</p>
<form method="post"><textarea name="text">{{ text }}</textarea><p><button type="submit">Analyze with Watson</button></p></form>
{% if error %}<p class="err">{{ error }}</p>{% endif %}
{% if analysis %}<h2>Analysis</h2><pre>{{ analysis | tojson(indent=2) }}</pre>{% endif %}
</div></main>
''', text=text, analysis=analysis, error=error)


@application.route('/api/analyze-song', methods=['POST'])
def api_analyze_song():
    payload = flask.request.get_json(silent=True) or {}
    query = (payload.get('query') or payload.get('song') or payload.get('url') or '').strip()
    if not query:
        return jsonify({'ok': False, 'error': 'Missing song name or URL'}), 400
    user_id = _session_user_id() or 'public'
    youtube_token = None
    if _session_user_id():
        youtube_token_data = token_store.load_provider_token(_session_user_id(), 'youtube_music') or {}
        youtube_token, _ = _ensure_youtube_token(_session_user_id(), youtube_token_data)
    try:
        result = analyze_song_query_for_user(user_id, query, youtube_token=youtube_token, force_refresh=bool(payload.get('refresh')))
        return jsonify({'ok': True, 'result': result})
    except Exception as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 400


@application.route('/analyze-song', methods=['GET', 'POST'])
def analyze_song_page():
    result = None
    error = None
    query = flask.request.values.get('query', '')
    if flask.request.method == 'POST':
        query = (query or '').strip()
        if not query:
            error = 'Drop a YouTube URL or type a song name first.'
        else:
            user_id = _session_user_id() or 'public'
            youtube_token = None
            if _session_user_id():
                youtube_token_data = token_store.load_provider_token(_session_user_id(), 'youtube_music') or {}
                youtube_token, _ = _ensure_youtube_token(_session_user_id(), youtube_token_data)
            try:
                result = analyze_song_query_for_user(user_id, query, youtube_token=youtube_token, force_refresh=flask.request.form.get('refresh') == '1')
            except Exception as exc:
                error = str(exc)
    return flask.render_template('song_lookup_analysis.html', query=query, result=result, error=error, signed_in=bool(_session_user_id()))


# spotify login
@application.route('/providers/spotify/connect', methods=['GET'])
def connect_spotify():
    return flask.redirect(authorize_spotify_REFRESHABLE(state=_oauth_state('spotify')))


@application.route('/providers/youtube_music/connect', methods=['GET'])
def connect_youtube_music():
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    if not client_id:
        return flask.render_template('error.html',
                                     error_title='YouTube Music Not Configured',
                                     error_message='Google OAuth credentials are not configured yet.',
                                     error_details='Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in Vercel before enabling this provider.'), 503
    redirect_uri = os.getenv('GOOGLE_CALLBACK_URL') or 'https://musicai-rouge.vercel.app/providers/youtube_music/callback'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube.force-ssl',
        'access_type': 'offline',
        'prompt': 'consent',
        'state': _oauth_state('youtube_music'),
    }
    return flask.redirect('https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params))


@application.route('/providers/youtube_music/callback', methods=['GET'])
def callback_youtube_music():
    if not _valid_oauth_state('youtube_music'):
        return flask.render_template('error.html', error_title='OAuth State Mismatch', error_message='YouTube login state did not match.', error_details='Please try connecting again.'), 400
    if 'error' in flask.request.args:
        return flask.render_template('error.html', error_title='YouTube Login Failed', error_message=flask.request.args.get('error_description', 'Google rejected the login.'), error_details=flask.request.args.get('error')), 400
    code = flask.request.args.get('code')
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    redirect_uri = os.getenv('GOOGLE_CALLBACK_URL') or 'https://musicai-rouge.vercel.app/providers/youtube_music/callback'
    if not all([code, client_id, client_secret]):
        return flask.render_template('error.html', error_title='YouTube Music Not Configured', error_message='Missing Google OAuth code or credentials.', error_details='Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.'), 503
    token_res = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }, timeout=20)
    if token_res.status_code >= 400:
        return flask.render_template('error.html', error_title='YouTube Token Exchange Failed', error_message='Google returned an OAuth token error.', error_details=token_res.text[:1000]), 502
    token_data = token_res.json()
    token_data['expires_at'] = time.time() + token_data.get('expires_in', 3600)
    profile_res = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers={'Authorization': 'Bearer ' + token_data['access_token']}, timeout=20)
    profile = profile_res.json() if profile_res.status_code == 200 else {}
    provider_account_id = profile.get('sub') or profile.get('email') or ('youtube_' + uuid.uuid4().hex)
    token_data['provider_account_id'] = provider_account_id
    account_id = token_store.resolve_account('youtube_music', provider_account_id, profile=profile, preferred_user_id=_session_user_id())
    token_store.save_provider_token(account_id, 'youtube_music', token_data, provider_account_id=provider_account_id, scopes='openid email profile youtube.readonly youtube.force-ssl', expires_at=token_data['expires_at'])
    _set_musicai_session(account_id, provider='youtube_music', display_name=profile.get('name') or profile.get('email'))
    return flask.redirect('/Dashboard')


@application.route('/providers/soundcloud/connect', methods=['GET'])
def connect_soundcloud():
    client_id = os.getenv('SOUNDCLOUD_CLIENT_ID')
    if not client_id:
        return flask.render_template('error.html',
                                     error_title='SoundCloud Not Configured',
                                     error_message='SoundCloud OAuth credentials are not configured yet.',
                                     error_details='Set SOUNDCLOUD_CLIENT_ID and SOUNDCLOUD_CLIENT_SECRET in Vercel before enabling this provider.'), 503
    redirect_uri = os.getenv('SOUNDCLOUD_CALLBACK_URL') or 'https://musicai-rouge.vercel.app/providers/soundcloud/callback'
    _, code_challenge = _oauth_pkce_pair('soundcloud')
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'state': _oauth_state('soundcloud'),
    }
    return flask.redirect('https://secure.soundcloud.com/authorize?' + urllib.parse.urlencode(params))


@application.route('/providers/soundcloud/callback', methods=['GET'])
def callback_soundcloud():
    if not _valid_oauth_state('soundcloud'):
        return flask.render_template('error.html', error_title='OAuth State Mismatch', error_message='SoundCloud login state did not match.', error_details='Please try connecting again.'), 400
    if 'error' in flask.request.args:
        return flask.render_template('error.html', error_title='SoundCloud Login Failed', error_message='SoundCloud rejected the login.', error_details=flask.request.args.get('error')), 400
    code = flask.request.args.get('code')
    client_id = os.getenv('SOUNDCLOUD_CLIENT_ID')
    client_secret = os.getenv('SOUNDCLOUD_CLIENT_SECRET')
    redirect_uri = os.getenv('SOUNDCLOUD_CALLBACK_URL') or 'https://musicai-rouge.vercel.app/providers/soundcloud/callback'
    code_verifier = _oauth_pkce_verifier('soundcloud')
    if not all([code, client_id, client_secret]):
        return flask.render_template('error.html', error_title='SoundCloud Not Configured', error_message='Missing SoundCloud OAuth code or credentials.', error_details='Set SOUNDCLOUD_CLIENT_ID and SOUNDCLOUD_CLIENT_SECRET.'), 503
    if not code_verifier:
        return flask.render_template('error.html', error_title='SoundCloud Login Expired', error_message='The SoundCloud login verifier expired or was missing.', error_details='Please start the SoundCloud connection again from the MusicAI dashboard.'), 400
    token_res = requests.post(
        'https://secure.soundcloud.com/oauth/token',
        headers={'Accept': 'application/json; charset=utf-8', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier,
            'code': code,
        },
        timeout=20,
    )
    if token_res.status_code >= 400:
        return flask.render_template('error.html', error_title='SoundCloud Token Exchange Failed', error_message='SoundCloud returned an OAuth token error.', error_details=token_res.text[:1000]), 502
    token_data = token_res.json()
    profile_res = requests.get('https://api.soundcloud.com/me', headers={'Authorization': 'OAuth ' + token_data['access_token']}, timeout=20)
    profile = profile_res.json() if profile_res.status_code == 200 else {}
    provider_account_id = str(profile.get('id') or profile.get('urn') or ('soundcloud_' + uuid.uuid4().hex))
    account_id = token_store.resolve_account('soundcloud', provider_account_id, profile=profile, preferred_user_id=_session_user_id())
    token_store.save_provider_token(account_id, 'soundcloud', token_data, provider_account_id=provider_account_id, scopes='soundcloud.basic', expires_at=time.time() + token_data.get('expires_in', 3600))
    _set_musicai_session(account_id, provider='soundcloud', display_name=profile.get('username'))
    return flask.redirect('/Dashboard')


@application.route('/logout', methods=['GET'])
def logout():
    flask.session.clear()
    return flask.redirect('/')


@application.route('/login/', methods=['GET'])
@application.route('/login', methods=['GET'])
def logging_in():
    request_id = uuid.uuid4().hex[:10]
    safe_args = {k: ('[present]' if k == 'code' else v) for k, v in flask.request.args.items()}
    print(f"OAUTH_CALLBACK_START request_id={request_id} args={safe_args} callback_configured={spotify_callbackURL!r}")

    # Surface Spotify authorization failures instead of looking like a refresh.
    if 'error' in flask.request.args:
        error = flask.request.args.get('error', 'spotify_error')
        description = flask.request.args.get('error_description', 'Spotify did not authorize this login request.')
        print(f"ERROR: Spotify authorization failed: {error} - {description}")
        return flask.render_template('error.html',
                                     error_title='Spotify Login Failed',
                                     error_message=description,
                                     error_details=error), 400
    if flask.request.args.get('state') and not _valid_oauth_state('spotify'):
        return flask.render_template('error.html',
                                     error_title='OAuth State Mismatch',
                                     error_message='Spotify login state did not match.',
                                     error_details='Please try connecting Spotify again.'), 400

    # Check if we have an authorization code
    if 'code' in flask.request.args:
        auth_code = flask.request.args['code']
        token_data = _retrieve_refreshable_token(auth_code, request_id=request_id)

        if not token_data:
            print(f"OAUTH_TOKEN_EXCHANGE_FAILED request_id={request_id}")
            return flask.render_template('error.html',
                                         error_title='Spotify Token Exchange Failed',
                                         error_message='Spotify returned to MusicAI, but the app could not exchange the code for a token.',
                                         error_details='Check the Spotify client secret and redirect URI.'), 502

        # Get user info to create user ID
        user_info = fetch_spotify_data(token_data['access_token'], 'https://api.spotify.com/v1/me', request_id=request_id)
        if user_info == "ERROR":
            print(f"OAUTH_PROFILE_FETCH_FAILED request_id={request_id}")
            spotify_error_status = getattr(flask.g, 'spotify_error_status', 'unknown')
            spotify_error_body = getattr(flask.g, 'spotify_error_body', '')
            details = (
                f"Spotify API status: {spotify_error_status}\n"
                f"Spotify API response: {spotify_error_body}\n\n"
                "Current Spotify docs say newly-created apps start in development mode. "
                "In development mode, the app owner must have Spotify Premium for API requests to function, "
                "and each tester must be added to the app allowlist."
            )
            return flask.render_template('error.html',
                                         error_title='Spotify App Setup Required',
                                         error_message='Spotify accepted the login, but blocked the API request because this development-mode app requires the app owner to have Spotify Premium and allowed users configured.',
                                         error_details=details), 403
        
        user_id = user_info.get('id', user_info.get('email', 'unknown'))
        account_id = token_store.resolve_account(
            'spotify',
            user_id,
            profile={
                'display_name': user_info.get('display_name'),
                'email': user_info.get('email'),
                'image': (user_info.get('images') or [{}])[0].get('url'),
            },
            preferred_user_id=_session_user_id(),
        )
        
        # Save tokens encrypted at rest. Durable production storage requires
        # MUSICAI_DATABASE_URL/DATABASE_URL; /tmp SQLite is only for test deploys.
        try:
            save_user_token(account_id, {
                'spotify_token': token_data['access_token'],
                'spotify_refresh_token': token_data.get('refresh_token'),
                'spotify_expires_at': time.time() + token_data.get('expires_in', 3600),
                'genius_token': genius_api_key  # Use our API key directly
            })
        except Exception as e:
            print(f"OAUTH_TOKEN_STORE_FAILED request_id={request_id}: {e}")
            return flask.render_template('error.html',
                                         error_title='Secure Token Storage Required',
                                         error_message='Spotify login worked, but MusicAI could not securely store the OAuth token.',
                                         error_details='Configure MUSICAI_DATABASE_URL/DATABASE_URL and MUSICAI_TOKEN_SECRET before accepting real users.'), 503
        
        # Store user info in session
        _set_musicai_session(account_id, provider='spotify', display_name=user_info.get('display_name', 'User'))
        flask.session['spotify_provider_account_id'] = user_id
        flask.session['spotify_token'] = token_data['access_token']
        flask.session['spotify_expired'] = False
        flask.session['username'] = user_info.get('display_name', 'User')
        
        print(f"SUCCESS: Spotify provider {user_id} linked to MusicAI account {account_id}")
        return flask.redirect('/Dashboard')
    
    return flask.redirect(authorize_spotify_REFRESHABLE())

# Genius API key is now handled automatically - no user login needed



# User Dashboard

def _compact_track(track):
    return {
        'id': track.get('id'),
        'name': track.get('name', 'Unknown track'),
        'artists': [a.get('name') for a in track.get('artists', []) if a.get('name')],
        'album': (track.get('album') or {}).get('name'),
        'thumbnail': ((track.get('album') or {}).get('images') or [{}])[-1].get('url') or '/static/fallback.svg',
        'popularity': track.get('popularity', 0),
    }


def _compact_album(album):
    return {
        'id': album.get('id'),
        'name': album.get('name', 'Unknown album'),
        'artists': [a.get('name') for a in album.get('artists', []) if a.get('name')],
        'thumbnail': (album.get('images') or [{}])[-1].get('url') or '/static/fallback.svg',
        'release_date': album.get('release_date'),
        'total_tracks': album.get('total_tracks'),
    }


def _compact_playlist(playlist):
    return {
        'id': playlist.get('id'),
        'name': playlist.get('name', 'Untitled playlist'),
        'owner': (playlist.get('owner') or {}).get('display_name'),
        'description': playlist.get('description') or '',
        'thumbnail': (playlist.get('images') or [{}])[-1].get('url') or '/static/fallback.svg',
        'total_tracks': (playlist.get('tracks') or {}).get('total'),
    }


def _empty_music_snapshot(primary_provider='YouTube'):
    return {
        'primary_provider': primary_provider,
        'liked_tracks': [],
        'saved_albums': [],
        'playlists': [],
        'youtube_playlists': [],
        'top_tracks': [],
        'top_artists': [],
        'recent_tracks': [],
        'stats': {'liked_tracks': 0, 'saved_albums': 0, 'playlists': 0, 'scanned_items': 0},
        'taste_feedback': 'Connect YouTube to scan your playlists and map the vibe of your music taste.',
        'mood_tags': ['playlist mood', 'music videos', 'taste scan'],
    }


def _spotify_dashboard_snapshot(spotify_token):
    snapshot = _empty_music_snapshot(primary_provider='Spotify')
    if not spotify_token:
        return snapshot

    liked = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me/tracks?limit=8')
    if isinstance(liked, dict):
        snapshot['stats']['liked_tracks'] = liked.get('total', 0)
        snapshot['liked_tracks'] = [_compact_track(item.get('track') or {}) for item in liked.get('items', []) if item.get('track')]

    albums = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me/albums?limit=6')
    if isinstance(albums, dict):
        snapshot['stats']['saved_albums'] = albums.get('total', 0)
        snapshot['saved_albums'] = [_compact_album(item.get('album') or {}) for item in albums.get('items', []) if item.get('album')]

    playlists = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me/playlists?limit=6')
    if isinstance(playlists, dict):
        snapshot['stats']['playlists'] = playlists.get('total', 0)
        snapshot['playlists'] = [_compact_playlist(item) for item in playlists.get('items', [])]

    top_tracks = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me/top/tracks?limit=6&time_range=medium_term')
    if isinstance(top_tracks, dict):
        snapshot['top_tracks'] = [_compact_track(item) for item in top_tracks.get('items', [])]

    top_artists = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me/top/artists?limit=6&time_range=medium_term')
    if isinstance(top_artists, dict):
        snapshot['top_artists'] = [{
            'id': item.get('id'),
            'name': item.get('name'),
            'genres': item.get('genres', []),
            'thumbnail': (item.get('images') or [{}])[-1].get('url') or '/static/fallback.svg',
            'popularity': item.get('popularity', 0),
        } for item in top_artists.get('items', [])]

    try:
        snapshot['recent_tracks'] = user_recently_played(spotify_token, limit=8)
    except Exception as e:
        print(f"ERROR: Failed to fetch recent tracks snapshot: {e}")

    genres = []
    for artist in snapshot['top_artists']:
        genres.extend(artist.get('genres', [])[:2])
    if genres:
        genre_preview = ', '.join(dict.fromkeys(genres[:5]))
        snapshot['taste_feedback'] = f"Your current Spotify taste leans toward {genre_preview}. MusicAI will compare that against other vendors as you connect them."
        snapshot['mood_tags'] = list(dict.fromkeys([g.split()[0] for g in genres if g]))[:5]
    elif snapshot['top_tracks']:
        artist_preview = ', '.join((t.get('artists') or ['mixed'])[:1][0] for t in snapshot['top_tracks'][:3])
        snapshot['taste_feedback'] = f"Your top tracks suggest a current pull toward {artist_preview}; connect more providers for a fuller vibe map."
    elif snapshot['liked_tracks']:
        snapshot['taste_feedback'] = 'Your liked songs are ready. Next step: analyze playlist mood clusters and compare across vendors.'
    return snapshot


def _youtube_api_get(access_token, endpoint, params=None):
    if not access_token:
        return None
    url = 'https://www.googleapis.com/youtube/v3/' + endpoint.lstrip('/')
    res = requests.get(url, headers={'Authorization': 'Bearer ' + access_token}, params=params or {}, timeout=20)
    if res.status_code >= 400:
        print(f"ERROR: YouTube API {endpoint} failed: {res.status_code} {res.text[:500]}")
        return None
    return res.json()


def _infer_vibe_from_titles(titles):
    text = ' '.join(titles).lower()
    buckets = [
        ('chill', ['chill', 'lofi', 'sleep', 'calm', 'relax', 'rain', 'ambient', 'soft']),
        ('hype', ['hype', 'gym', 'workout', 'rage', 'party', 'turn up', 'bass', 'trap']),
        ('nostalgic', ['old', 'throwback', 'classic', 'nostalgia', 'retro', '90s', '2000s']),
        ('romantic', ['love', 'heart', 'r&b', 'slow jam', 'valentine', 'crush']),
        ('focused', ['study', 'focus', 'coding', 'work', 'deep', 'instrumental']),
        ('sad', ['sad', 'cry', 'heartbreak', 'alone', 'melancholy', 'breakup']),
        ('discovery', ['new', 'mix', 'indie', 'underground', 'discover', 'fresh']),
    ]
    scores = []
    for label, words in buckets:
        score = sum(text.count(word) for word in words)
        if score:
            scores.append((score, label))
    tags = [label for _, label in sorted(scores, reverse=True)[:5]]
    if not tags:
        tags = ['eclectic', 'playlist-led', 'video-native']
    return tags


YOUTUBE_ANALYSIS_VERSION = 'youtube-title-watson-v2'


def _clean_youtube_title(title):
    title = (title or '').strip()
    noise = ['(official video)', '[official video]', '(official audio)', '[official audio]', '(lyrics)', '[lyrics]', '(lyric video)', 'music video']
    clean = title
    for token in noise:
        clean = clean.replace(token, ' ').replace(token.title(), ' ')
    return ' '.join(clean.split())


def _youtube_playlist_items(youtube_token, playlist_id, max_items=100):
    rows = []
    page_token = None
    while playlist_id and len(rows) < max_items:
        params = {
            'part': 'snippet,contentDetails',
            'playlistId': playlist_id,
            'maxResults': min(50, max_items - len(rows)),
        }
        if page_token:
            params['pageToken'] = page_token
        data = _youtube_api_get(youtube_token, 'playlistItems', params)
        if not isinstance(data, dict):
            break
        for item in data.get('items', []):
            snippet = item.get('snippet') or {}
            details = item.get('contentDetails') or {}
            resource = snippet.get('resourceId') or {}
            video_id = details.get('videoId') or resource.get('videoId') or item.get('id')
            title = (snippet.get('title') or '').strip()
            if not title or title in {'Private video', 'Deleted video'}:
                continue
            thumbs = snippet.get('thumbnails') or {}
            thumb = (thumbs.get('medium') or thumbs.get('default') or thumbs.get('high') or {}).get('url') or '/static/fallback.svg'
            rows.append({
                'provider': 'youtube_music',
                'id': video_id,
                'playlist_item_id': item.get('id'),
                'title': title,
                'analysis_text': _clean_youtube_title(title),
                'channel': snippet.get('videoOwnerChannelTitle') or snippet.get('channelTitle') or 'YouTube',
                'thumbnail': thumb,
                'published_at': snippet.get('publishedAt'),
            })
        page_token = data.get('nextPageToken')
        if not page_token:
            break
    return rows


def _analysis_model_from_result(result):
    if isinstance(result, dict):
        if 'analysis' in result and isinstance(result.get('analysis'), dict):
            return result.get('analysis') or {}
        return result
    return {}


def _analyze_youtube_track_cached(user_id, track, force_refresh=False):
    text = track.get('analysis_text') or track.get('title') or ''
    item_id = track.get('id') or hashlib.sha256(text.encode()).hexdigest()[:16]
    if not force_refresh:
        cached = token_store.load_cached_analysis(user_id, 'youtube_music', 'track', item_id, YOUTUBE_ANALYSIS_VERSION, text)
        if cached:
            return cached
    analysis, warning = analyze_text_safely(text)
    payload = {
        'provider': 'youtube_music',
        'item_type': 'track',
        'item_id': item_id,
        'title': track.get('title'),
        'channel': track.get('channel'),
        'thumbnail': track.get('thumbnail'),
        'analysis_text': text,
        'analysis': analysis,
        'warning': warning,
        'analyzer_version': YOUTUBE_ANALYSIS_VERSION,
    }
    return token_store.save_cached_analysis(user_id, 'youtube_music', 'track', item_id, YOUTUBE_ANALYSIS_VERSION, text, payload)


def _aggregate_track_analyses(track_results):
    emotion_keys = ['sadness', 'joy', 'fear', 'disgust', 'anger']
    totals = {k: 0.0 for k in emotion_keys}
    emotion_count = 0
    sentiments = {}
    keywords = {}
    concepts = {}
    cached_hits = 0
    analyzed = []
    for result in track_results:
        cached_hits += 1 if (result.get('cache') or {}).get('hit') else 0
        model = _analysis_model_from_result(result)
        emotion = model.get('overall_emotion') or {}
        if emotion:
            emotion_count += 1
            for key in emotion_keys:
                totals[key] += float(emotion.get(key) or 0)
        sentiment_value = model.get('sentiment') or 'unknown'
        sentiment = sentiment_value.get('label', 'unknown') if isinstance(sentiment_value, dict) else str(sentiment_value)
        sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
        for kw in model.get('keywords') or []:
            if isinstance(kw, dict):
                label = kw.get('text') or kw.get('keyword') or ''
            else:
                label = kw[0] if isinstance(kw, (list, tuple)) and kw else str(kw)
            if label:
                keywords[label] = keywords.get(label, 0) + 1
        for concept in model.get('concepts') or []:
            if concept:
                concepts[concept] = concepts.get(concept, 0) + 1
        analyzed.append({
            'title': result.get('title'),
            'channel': result.get('channel'),
            'thumbnail': result.get('thumbnail'),
            'sentiment': sentiment,
            'emotion': emotion,
            'keywords': model.get('keywords') or [],
            'concepts': model.get('concepts') or [],
            'source': model.get('source'),
            'cache_hit': bool((result.get('cache') or {}).get('hit')),
        })
    averages = {k: round(totals[k] / emotion_count, 4) for k in emotion_keys} if emotion_count else {}
    dominant_emotion = max(averages, key=averages.get) if averages else 'unknown'
    dominant_sentiment = max(sentiments, key=sentiments.get) if sentiments else 'unknown'
    top_keywords = sorted(keywords.items(), key=lambda kv: kv[1], reverse=True)[:10]
    top_concepts = sorted(concepts.items(), key=lambda kv: kv[1], reverse=True)[:8]
    return {
        'track_count': len(track_results),
        'cached_hits': cached_hits,
        'new_analyses': len(track_results) - cached_hits,
        'average_emotion': averages,
        'dominant_emotion': dominant_emotion,
        'sentiment_counts': sentiments,
        'dominant_sentiment': dominant_sentiment,
        'top_keywords': top_keywords,
        'top_concepts': top_concepts,
        'mood_tags': _infer_vibe_from_titles([r.get('title') or '' for r in track_results] + [dominant_emotion, dominant_sentiment]),
        'tracks': analyzed,
    }


def _youtube_playlist_metadata(youtube_token, playlist_id):
    data = _youtube_api_get(youtube_token, 'playlists', {'part': 'snippet,contentDetails', 'id': playlist_id, 'maxResults': 1})
    if not isinstance(data, dict) or not data.get('items'):
        return {}
    item = data['items'][0]
    snippet = item.get('snippet') or {}
    details = item.get('contentDetails') or {}
    thumbs = snippet.get('thumbnails') or {}
    thumb = (thumbs.get('medium') or thumbs.get('default') or thumbs.get('high') or {}).get('url') or '/static/fallback.svg'
    return {
        'id': playlist_id,
        'name': snippet.get('title') or 'Untitled YouTube playlist',
        'owner': snippet.get('channelTitle') or 'YouTube',
        'description': snippet.get('description') or '',
        'thumbnail': thumb,
        'total_tracks': details.get('itemCount', 0),
    }


def analyze_youtube_playlist_for_user(user_id, youtube_token, playlist_id, force_refresh=False, max_items=100):
    playlist = _youtube_playlist_metadata(youtube_token, playlist_id)
    tracks = _youtube_playlist_items(youtube_token, playlist_id, max_items=max_items)
    results = [_analyze_youtube_track_cached(user_id, track, force_refresh=force_refresh) for track in tracks]
    aggregate = _aggregate_track_analyses(results)
    playlist.update({
        'requested_max_items': max_items,
        'loaded_tracks': len(tracks),
        'analysis': aggregate,
    })
    return playlist


def _youtube_dashboard_snapshot(youtube_token):
    snapshot = _empty_music_snapshot(primary_provider='YouTube')
    if not youtube_token:
        return snapshot

    playlists = _youtube_api_get(youtube_token, 'playlists', {
        'part': 'snippet,contentDetails',
        'mine': 'true',
        'maxResults': 12,
    })
    if not isinstance(playlists, dict):
        snapshot['taste_feedback'] = 'YouTube is connected, but MusicAI could not read playlists yet. Reconnect YouTube if the token expired.'
        return snapshot

    title_pool = []
    rows = []
    for item in playlists.get('items', []):
        snippet = item.get('snippet') or {}
        details = item.get('contentDetails') or {}
        thumbs = snippet.get('thumbnails') or {}
        thumb = (thumbs.get('medium') or thumbs.get('default') or thumbs.get('high') or {}).get('url') or '/static/fallback.svg'
        playlist_id = item.get('id')
        video_titles = []
        if playlist_id:
            videos = _youtube_api_get(youtube_token, 'playlistItems', {
                'part': 'snippet',
                'playlistId': playlist_id,
                'maxResults': 5,
            })
            if isinstance(videos, dict):
                for video in videos.get('items', []):
                    title = ((video.get('snippet') or {}).get('title') or '').strip()
                    if title and title != 'Private video':
                        video_titles.append(title)
        title_pool.extend([snippet.get('title') or '', snippet.get('description') or '', *video_titles])
        rows.append({
            'id': playlist_id,
            'name': snippet.get('title') or 'Untitled YouTube playlist',
            'owner': (snippet.get('channelTitle') or 'YouTube'),
            'description': snippet.get('description') or '',
            'thumbnail': thumb,
            'total_tracks': details.get('itemCount', 0),
            'sample_tracks': video_titles[:3],
            'analysis_url': f'/youtube/playlist/{playlist_id}/analysis' if playlist_id else '',
        })

    tags = _infer_vibe_from_titles(title_pool)
    snapshot['youtube_playlists'] = rows
    snapshot['playlists'] = rows
    snapshot['stats']['playlists'] = len(rows)
    snapshot['stats']['scanned_items'] = sum(int(p.get('total_tracks') or 0) for p in rows)
    snapshot['mood_tags'] = tags
    if rows:
        playlist_names = ', '.join(p['name'] for p in rows[:3])
        snapshot['taste_feedback'] = f"Your YouTube playlists lean {', '.join(tags[:3])}. MusicAI scanned playlist names and sample videos from {playlist_names} to build this first vibe read."
    else:
        snapshot['taste_feedback'] = 'YouTube is connected. Create or save playlists on YouTube/YouTube Music, then MusicAI can scan them for vibe signals.'
    return snapshot


@application.route('/youtube/playlist/<playlist_id>/analysis', methods=['GET', 'POST'])
def youtube_playlist_analysis(playlist_id):
    user_id = _session_user_id()
    if not user_id:
        return flask.redirect('/')
    youtube_token_data = token_store.load_provider_token(user_id, 'youtube_music') or {}
    youtube_token, youtube_token_data = _ensure_youtube_token(user_id, youtube_token_data)
    if not youtube_token:
        return flask.render_template('error.html',
                                     error_title='Connect YouTube first',
                                     error_message='MusicAI needs your YouTube playlist permission before it can analyze a playlist.',
                                     error_details='Go back to the homepage and connect YouTube/YouTube Music.'), 403
    force_refresh = flask.request.method == 'POST' and flask.request.form.get('refresh') == '1'
    try:
        max_items = int(flask.request.values.get('max_items', 25))
    except Exception:
        max_items = 25
    max_items = max(1, min(max_items, 150))
    playlist = analyze_youtube_playlist_for_user(user_id, youtube_token, playlist_id, force_refresh=force_refresh, max_items=max_items)
    return flask.render_template('youtube_playlist_analysis.html', playlist=playlist, force_refresh=force_refresh)


@application.route('/api/youtube/playlist/<playlist_id>/analysis', methods=['POST'])
def api_youtube_playlist_analysis(playlist_id):
    user_id = _session_user_id()
    if not user_id:
        return jsonify({'ok': False, 'error': 'not_authenticated'}), 401
    youtube_token_data = token_store.load_provider_token(user_id, 'youtube_music') or {}
    youtube_token, youtube_token_data = _ensure_youtube_token(user_id, youtube_token_data)
    if not youtube_token:
        return jsonify({'ok': False, 'error': 'youtube_not_connected'}), 403
    payload = flask.request.get_json(silent=True) or {}
    force_refresh = bool(payload.get('refresh'))
    max_items = max(1, min(int(payload.get('max_items') or 100), 150))
    playlist = analyze_youtube_playlist_for_user(user_id, youtube_token, playlist_id, force_refresh=force_refresh, max_items=max_items)
    return jsonify({'ok': True, 'playlist': playlist})


@application.route('/Dashboard', methods=['GET'])
def Dashboard():
    user_id = _session_user_id()
    if not user_id:
        print(f"\n\n\n------------\nAccess denied (no user session): {request.remote_addr}\n------------")
        return flask.redirect('/')

    connected = token_store.connected_providers(user_id)
    token_data = load_user_token(user_id) or {}
    youtube_token_data = token_store.load_provider_token(user_id, 'youtube_music') or {}
    spotify_token = token_data.get('spotify_token')
    youtube_token, youtube_token_data = _ensure_youtube_token(user_id, youtube_token_data)

    if spotify_token and is_token_expired(token_data.get('spotify_expires_at')):
        print(f"INFO: Spotify token expired for account {user_id}, attempting refresh...")
        if token_data.get('spotify_refresh_token'):
            new_tokens = _refresh_spotify_token(token_data['spotify_refresh_token'])
            if new_tokens:
                token_data.update({
                    'spotify_token': new_tokens['access_token'],
                    'spotify_refresh_token': new_tokens.get('refresh_token') or token_data.get('spotify_refresh_token'),
                    'spotify_expires_at': time.time() + new_tokens.get('expires_in', 3600),
                    'genius_token': token_data.get('genius_token', genius_api_key),
                })
                try:
                    save_user_token(user_id, token_data)
                except Exception as e:
                    print(f"ERROR: Failed to persist refreshed Spotify token for account {user_id}: {e}")
                    return flask.render_template('error.html',
                                                 error_title='Secure Token Storage Required',
                                                 error_message='MusicAI refreshed your Spotify token but could not securely persist it.',
                                                 error_details='Configure durable encrypted token storage before accepting real users.'), 503
                spotify_token = token_data['spotify_token']
                flask.session['spotify_token'] = spotify_token
            else:
                spotify_token = None
                flask.session['spotify_expired'] = True
        else:
            spotify_token = None
            flask.session['spotify_expired'] = True

    flask.session['genius_token'] = token_data.get('genius_token', genius_api_key)
    if spotify_token:
        flask.session['spotify_token'] = spotify_token

    user_data = {'display_name': flask.session.get('username') or 'MusicAI listener', 'email': flask.session.get('email') or ''}
    if spotify_token:
        spotify_user = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me')
        if isinstance(spotify_user, dict) and 'error' not in spotify_user:
            user_data = spotify_user
            flask.session['username'] = spotify_user.get('display_name') or user_data['display_name']
            flask.session['email'] = spotify_user.get('email') or ''
            if 'spotify' not in connected:
                provider_account_id = spotify_user.get('id') or spotify_user.get('email')
                if provider_account_id:
                    token_store.resolve_account('spotify', provider_account_id, profile=spotify_user, preferred_user_id=user_id)
                    connected = token_store.connected_providers(user_id)
        else:
            flask.session['spotify_expired'] = True

    try:
        meme_result = fetch_meme(flask.session.get('username', user_data.get('display_name', 'User')))
        meme_url = meme_result['data']['url']
    except Exception as meme_error:
        print(f"ERROR: Meme generation failed: {meme_error}")
        meme_url = '/static/fallback.svg'
    profile_avatar = _profile_avatar(user_data, connected, meme_url)

    amount_analyzed = flask.session.get('amount', 0)
    snapshot = _youtube_dashboard_snapshot(youtube_token) if youtube_token else _spotify_dashboard_snapshot(spotify_token)
    if youtube_token and spotify_token:
        spotify_snapshot = _spotify_dashboard_snapshot(spotify_token)
        snapshot['liked_tracks'] = spotify_snapshot.get('liked_tracks', [])
        snapshot['saved_albums'] = spotify_snapshot.get('saved_albums', [])
        snapshot['recent_tracks'] = spotify_snapshot.get('recent_tracks', [])
        snapshot['top_tracks'] = spotify_snapshot.get('top_tracks', [])
        snapshot['stats']['liked_tracks'] = spotify_snapshot.get('stats', {}).get('liked_tracks', 0)
        snapshot['stats']['saved_albums'] = spotify_snapshot.get('stats', {}).get('saved_albums', 0)
    context = {
        'data': user_data,
        'username': flask.session.get('username') or user_data.get('display_name', 'MusicAI listener'),
        'email': flask.session.get('email') or user_data.get('email', ''),
        'meme': meme_url,
        'profile_avatar': profile_avatar,
        'amount_analyzed': amount_analyzed,
        'recent_tracks': snapshot['recent_tracks'],
        'providers': _provider_view_model(),
        'connected_providers': connected,
        'spotify_connected': bool(spotify_token),
        'snapshot': snapshot,
    }
    return render_template('user_dashboard.html', context=context)



# SEARCH A SONG
@application.route('/search-form', methods=['GET'])
def search_form():
    return flask.render_template('search_form.html' )
@application.route('/search-results', methods=['POST'])
def search_results():
    try:
        spotify_token = flask.session.get('spotify_token')
        if not spotify_token:
            return flask.redirect('/')
        
        q = flask.request.form.get('q')
        if not q:
            return "Search query is required", 400
            
        q_type = flask.request.form.get('q_type')

        artists = []
        tracks = []
        
        # SEARCHING FOR TRACKS
        if q_type == None or q_type == 'None':
            q_type = 'track'
            # search spotify
            data = fetch_spotify_data(spotify_token, f'https://api.spotify.com/v1/search?q={q}&type={q_type}')
            
            if data == "ERROR":
                return "Failed to search Spotify. Please try again.", 500
                
            q_type += 's'
            tracks = data.get(q_type, {}).get('items', [])
            
            # add images safely
            for i in tracks:
                try:
                    if i.get('artists') and len(i['artists']) > 0:
                        artist_href = i['artists'][0].get('href')
                        if artist_href:
                            artist_data = fetch_spotify_data(spotify_token, artist_href)
                            if artist_data != "ERROR" and artist_data.get('images'):
                                i['thumbnail'] = artist_data['images'][-1]['url']
                            else:
                                i['thumbnail'] = '/static/fallback.svg'
                        else:
                            i['thumbnail'] = '/static/fallback.svg'
                    else:
                        i['thumbnail'] = '/static/fallback.svg'
                except Exception as e:
                    print(f"ERROR adding thumbnail for track {i.get('name', 'Unknown')}: {e}")
                    i['thumbnail'] = '/static/fallback.svg'

        # SEARCHING FOR ARTISTS
        else:
            q_type = 'artist'
            # search spotify
            data = fetch_spotify_data(spotify_token, f'https://api.spotify.com/v1/search?q={q}&type={q_type}')
            
            if data == "ERROR":
                return "Failed to search Spotify. Please try again.", 500
                
            q_type += 's'
            artists = data.get(q_type, {}).get('items', [])

        content = {
            'artists' : artists ,
            'tracks' : tracks,
            'query': q
        }
        return flask.render_template('search_results.html' , content = content )
        
    except Exception as e:
        print(f"ERROR in search_results: {e}")
        return "An error occurred while searching. Please try again.", 500
@application.route('/song-analysis', methods=['POST'  ])
def song_analysis():
    try:
        spotify_token = flask.session.get('spotify_token')
        if not spotify_token:
            return flask.redirect('/')
        
        song_id = flask.request.form.get("analysis_id")
        song_title = flask.request.form.get("song_name")
        song_artist_name = flask.request.form.get("song_artist_name")
        
        if not song_id or not song_title or not song_artist_name:
            return "Missing song information", 400
        
        stats = _song_analysis_details(spotify_token , song_id , False , song_title , song_artist_name)
        
        if not stats or stats == "ERROR":
            print(stats)
            error_message = f"Unable to analyze '{song_title}' by {song_artist_name}. "
            error_message += "This song may not be available for analysis due to regional restrictions or premium content requirements."
            return error_message, 500
        
        stats['song_title'] = song_title
        stats['song_artist_name'] = song_artist_name

        # add to total amount analyzed
        flask.session['amount'] += 1

        print("\nSEARCHED SONG "  )

        # DATA POINTS FOR BAR GRAPH
        spotty_chart_datapoint_labels = [
            'danceability',
            'energy',
            'speechiness',
            'acousticness',
            # 'instrumentalness',
            'liveness',
            'valence',
        ]

        # PIE CHART
        ai_response = False
        if stats['ai']['lyrics'] is not None : 
            ai_response = True
            emotionsLabels = list(stats['ai']['nlu']['averageEmotion'].keys())
            emotionValues = [    stats['ai']['nlu']['averageEmotion'][i] for i in emotionsLabels  ]

        if ai_response: #kinda redundant but i mean.... why not have the modularity?
            content = {
                'stats'  : stats,
                'ai_response'  : ai_response,

                # spotify data
                'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
                'spotty_chart_data' :  [stats[i] for i in spotty_chart_datapoint_labels   ]  ,

                # watson data
                'emotionLabels' : emotionsLabels,
                'emotionValues' : emotionValues,
            }
        else: #NO LYRICS
            content = {
                'stats'  : stats,
                'ai_response'  : ai_response,
                'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
                'spotty_chart_data' :  [stats[i] for i in spotty_chart_datapoint_labels   ]  ,

                # watson data
                'emotionLabels' : None,
                'emotionValues' : None,
            }

        return flask.render_template('song_analysis.html' , content = content)
        
    except Exception as e:
        print(f"ERROR in song_analysis: {e}")
        return "An error occurred while analyzing the song. Please try again.", 500




# NOTE:
    # GROUP ANALYSIS IS A LITTLE DIFFERENT FROM LIKES ANALYSIS
    # both variables are dictionaries with numbers as keys starting at zero
    # each value is another dictionary with keys :  ['owner', 'name', 'description', 'id', 'songs']
    # musicGroup['songs'] is an array with tuples 
    # each tuple is ( "id" ,  "title" , ["artists"]  )


# Album Analysis
@application.route('/album-analysis', methods=['GET'])
def album_analysis():
    # grab music
    spotify_token = flask.session.get('spotify_token')
    albums = user_albums(spotify_token)

    # GROUP ANALYSIS FUNCTION USES THE  liked_group_average() function
    final  = group_music_analysis(spotify_token, albums)

    # Add amount to total analyized
    flask.session['amount'] += final['ai']['amount']

    # GRAPHING

    # DATA POINTS FOR BAR GRAPH
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        # 'instrumentalness',
        'liveness',
        'valence',
    ]

    # PIE CHART
    ai_response = False
    if final['ai'] is not None : 
        ai_response = True
        emotionsLabels = list(final['ai']['averageEmotion'].keys())
        emotionValues = [    final['ai']['averageEmotion'][i] for i in emotionsLabels  ]

    # No point to change as it is the same code as the song analysis from here to the components in html...
    USERNAME = fetch_spotify_data( spotify_token , 'https://api.spotify.com/v1/me' )
    final['song_title'] = USERNAME['display_name']
    final['song_artist_name'] = "Playlist Total Analyses"


    #kinda redundant but i mean.... why not have the modularity?
    if ai_response:
        content = {
            'stats'  : final,
            'ai_response'  : ai_response,
            # 'each_song_stats'  : each_song_stats,

            # spotify data
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [final[i] for i in spotty_chart_datapoint_labels   ]  ,

            # watson data
            'emotionLabels' : emotionsLabels,
            'emotionValues' : emotionValues,
        }

    #NO LYRICS
    else:
        content = {
            'stats'  : final,
            # 'each_song_stats'  : each_song_stats,
            'ai_response'  : ai_response,
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [final[i] for i in spotty_chart_datapoint_labels   ]  ,
            # watson data
            'emotionLabels' : None,
            'emotionValues' : None,
        }


    # sessions for passed songs on html

    return flask.render_template('Liked_Group_analysis.html' , content = content)

# Playlist Analysis
@application.route('/playlist-analysis', methods=['GET'])
def playlist_analysis():

    # grab music
    spotify_token = flask.session.get('spotify_token')
    playlist_response = user_playlists(spotify_token)

    # GROUP ANALYSIS FUNCTION USES THE  liked_group_average() function
    final  = group_music_analysis(spotify_token, playlist_response)

    # Add amount to total analyized
    flask.session['amount'] += final['ai']['amount']


    # GRAPHING

    # DATA POINTS FOR BAR GRAPH
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        # 'instrumentalness',
        'liveness',
        'valence',
    ]

    # PIE CHART
    ai_response = False
    if final['ai'] is not None : 
        ai_response = True
        emotionsLabels = list(final['ai']['averageEmotion'].keys())
        emotionValues = [    final['ai']['averageEmotion'][i] for i in emotionsLabels  ]

    # No point to change as it is the same code as the song analysis from here to the components in html...
    USERNAME = fetch_spotify_data( spotify_token , 'https://api.spotify.com/v1/me' )
    final['song_title'] = USERNAME['display_name']
    final['song_artist_name'] = "Playlist Total Analyses"


    #kinda redundant but i mean.... why not have the modularity?
    if ai_response:
        content = {
            'stats'  : final,
            'ai_response'  : ai_response,
            # 'each_song_stats'  : each_song_stats,

            # spotify data
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [final[i] for i in spotty_chart_datapoint_labels   ]  ,

            # watson data
            'emotionLabels' : emotionsLabels,
            'emotionValues' : emotionValues,
        }

    #NO LYRICS
    else:
        content = {
            'stats'  : final,
            # 'each_song_stats'  : each_song_stats,
            'ai_response'  : ai_response,
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [final[i] for i in spotty_chart_datapoint_labels   ]  ,
            # watson data
            'emotionLabels' : None,
            'emotionValues' : None,
        }


    # sessions for passed songs on html

    return flask.render_template('Liked_Group_analysis.html' , content = content)




# INDIVISUAL GROUP DISPLAY
# Display all albums and links next to them to pictures of the album
@application.route('/indivisual-album-display', methods=['GET'])
def indivisualAlbumDisplay():

    # going to hold every album and their display data ['pictures'] , ['popularity'], ['name'] , ['uri']
    display_data = {
        'username' : flask.session['username'] 
    }

    # grab music
    spotify_token = flask.session.get('spotify_token')
    albums = user_albums(spotify_token)

    # gather pictures
    for album in albums:
        album_id = albums[album]["id"]
        data = fetch_spotify_data(spotify_token , f"https://api.spotify.com/v1/albums/{album_id}")

        # add to display data
        display_data[album] = {}
        display_data[album]['name'] = albums[album]['name']
        display_data[album]['id'] = album_id
        display_data[album]['pictures'] = data['images']
        display_data[album]['popularity'] = albums[album]['popularity']
        display_data[album]['amount'] = len(  albums[album]['songs']  )
        display_data[album]['release_date'] = data['release_date']
        display_data[album]['spotify_page'] = f"https://open.spotify.com/track/{album_id}"
        display_data[album]['songs'] = albums[album]['songs']




    # debug = fetch_spotify_data(spotify_token , f"https://api.spotify.com/v1/albums/5SKnXCvB4fcGSZu32o3LRY?si=17b25a68a03c497b")


    
    return flask.render_template('indivisual_group_listing.html' , display_data = display_data)

@application.route('/indivisual-playlist-display', methods=['GET'])
def indivisualPlaylistDisplay():
    # grab music
    spotify_token = flask.session.get('spotify_token')
    playlist_response = user_playlists(spotify_token)

    # going to hold every album and their display data ['pictures'] , ['popularity'], ['name'] , ['uri']
    display_data = {
        'username' : flask.session['username'] 
    }

    # gather pictures
    for pl in playlist_response:
        playlist_id = playlist_response[pl]["id"]
        data = fetch_spotify_data(spotify_token , f"https://api.spotify.com/v1/playlists/{playlist_id}")

        # add to display data
        display_data[ pl ] = {}
        display_data[ pl ]['name'] = playlist_response[pl]['name']
        display_data[ pl ]['id'] = playlist_id
        display_data[ pl ]['pictures'] = data['images']
        display_data[ pl ]['amount'] = len(  playlist_response[pl]['songs']  )
        display_data[ pl ]['spotify_page'] = f"https://open.spotify.com/playlist/{playlist_id}"
        display_data[ pl ]['popularity'] = f"{data['followers']['total']} listeners"
        display_data[ pl ]['songs'] =  playlist_response[pl]['songs']
        

        # PLAYLIST DATA DOESNT RETURN (fetch_album does)
        # display_data[ pl ]['release_date'] = data['release_date']

    return flask.render_template('indivisual_group_listing.html' , display_data = display_data)

# ALMBUM FINAL ANALYSIS
@application.route('/indivisual-album-analysis', methods=['POST'])
def indivisual_album_analysis():
    spotify_token = flask.session.get('spotify_token')



    # grab context from form POST  from /indivisual-playlist-display 
    user_form_args = flask.request.form
    # print(user_form_args)
    
    # display page passed in list of songs from the form
    music_list = flask.request.form.get('songs[]') 

    # convert string return from form into list
    music_list = ast.literal_eval(music_list)
    # music_list = music_list.strip('][').split(', ')


    # clean list into format that fits the liked_group_average() format
    for x in range(0 , len(music_list) , 1):
        # print(   music_list[x] )

        song_info = {
            "artists"  : music_list[x][2],
            "name"  :  music_list[x][1] ,
            "id"  :  music_list[x][0],
        }

        # replace music list with song info
        music_list[x] = song_info


    # this function returns two for parallel display of each (song) & grouped ai
    song_stats , each_song_stats = liked_group_average(spotify_token , music_list)
    
    # Add amount to total analyized
    flask.session['amount'] += song_stats['ai']['amount']

    # GRAPHING

    # DATA POINTS FOR BAR GRAPH
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        # 'instrumentalness',
        'liveness',
        'valence',
    ]

    # PIE CHART
    ai_response = False
    if song_stats['ai'] is not None : 
        ai_response = True
        emotionsLabels = list(song_stats['ai']['averageEmotion'].keys())
        emotionValues = [    song_stats['ai']['averageEmotion'][i] for i in emotionsLabels  ]

    # No point to change as it is the same code as the song analysis from here to the components in html...
    USERNAME = fetch_spotify_data( spotify_token , 'https://api.spotify.com/v1/me' )
    song_stats['song_title'] = USERNAME['display_name']
    song_stats['song_artist_name'] = user_form_args["group_name"]


    #kinda redundant but i mean.... why not have the modularity?
    if ai_response:
        content = {
            'stats'  : song_stats,
            'ai_response'  : ai_response,
            'each_song_stats'  : each_song_stats,

            # spotify data
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,

            # watson data
            'emotionLabels' : emotionsLabels,
            'emotionValues' : emotionValues,
        }

    #NO LYRICS
    else:
        content = {
            'stats'  : song_stats,
            'each_song_stats'  : each_song_stats,
            'ai_response'  : ai_response,
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,
            # watson data
            'emotionLabels' : None,
            'emotionValues' : None,
        }


    # sessions for passed songs on html

    return flask.render_template('Liked_Group_analysis.html' , content = content)

# Playlist FINAL ANALYSIS
@application.route('/indivisual-playlist-analysis', methods=['POST'])
def indivisual_playlist_analysis():
    spotify_token = flask.session.get('spotify_token')



    # grab context from form POST  from /indivisual-playlist-display 
    user_form_args = flask.request.form
    # print(user_form_args)
    
    # display page passed in list of songs from the form
    music_list = flask.request.form.get('songs[]') 

    # convert string return from form into list
    music_list = ast.literal_eval(music_list)
    # music_list = music_list.strip('][').split(', ')


    # clean list into format that fits the liked_group_average() format
    for x in range(0 , len(music_list) , 1):
        # print(   music_list[x] )

        song_info = {
            "artists"  : music_list[x][2],
            "name"  :  music_list[x][1] ,
            "id"  :  music_list[x][0],
        }

        # replace music list with song info
        music_list[x] = song_info


    # this function returns two for parallel display of each (song) & grouped ai
    song_stats , each_song_stats = liked_group_average(spotify_token , music_list)
    
    # Add amount to total analyized
    flask.session['amount'] += song_stats['ai']['amount']

    # GRAPHING

    # DATA POINTS FOR BAR GRAPH
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        # 'instrumentalness',
        'liveness',
        'valence',
    ]

    # PIE CHART
    ai_response = False
    if song_stats['ai'] is not None : 
        ai_response = True
        emotionsLabels = list(song_stats['ai']['averageEmotion'].keys())
        emotionValues = [    song_stats['ai']['averageEmotion'][i] for i in emotionsLabels  ]

    # No point to change as it is the same code as the song analysis from here to the components in html...
    USERNAME = fetch_spotify_data( spotify_token , 'https://api.spotify.com/v1/me' )
    song_stats['song_title'] = USERNAME['display_name']
    song_stats['song_artist_name'] = user_form_args["group_name"]


    #kinda redundant but i mean.... why not have the modularity?
    if ai_response:
        content = {
            'stats'  : song_stats,
            'ai_response'  : ai_response,
            'each_song_stats'  : each_song_stats,

            # spotify data
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,

            # watson data
            'emotionLabels' : emotionsLabels,
            'emotionValues' : emotionValues,
        }

    #NO LYRICS
    else:
        content = {
            'stats'  : song_stats,
            'each_song_stats'  : each_song_stats,
            'ai_response'  : ai_response,
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,
            # watson data
            'emotionLabels' : None,
            'emotionValues' : None,
        }


    # sessions for passed songs on html

    return flask.render_template('Liked_Group_analysis.html' , content = content)


# Recently played tracks analysis
@application.route('/recent-analysis', methods=['GET'])
def recent_analysis():
    spotify_token = flask.session.get('spotify_token')
    if not spotify_token:
        return flask.redirect('/')
    
    # Get recently played tracks
    recent_tracks = user_recently_played(spotify_token, limit=50)
    
    if not recent_tracks:
        return "No recently played tracks found.", 404
    
    # Convert to format expected by liked_group_average
    tracks_for_analysis = []
    for track in recent_tracks:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artists': track['artists']
        }
        tracks_for_analysis.append(track_info)
    
    # Analyze tracks using existing function
    song_stats, each_song_stats = liked_group_average(spotify_token, tracks_for_analysis)
    
    # Add amount to total analyzed
    flask.session['amount'] += song_stats['ai']['amount'] if song_stats.get('ai') else 0
    
    # Prepare chart data
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        'liveness',
        'valence',
    ]
    
    # Check if we have AI analysis
    ai_response = False
    emotionsLabels = None
    emotionValues = None
    
    if song_stats.get('ai') and song_stats['ai']:
        ai_response = True
        if song_stats['ai'].get('averageEmotion'):
            emotionsLabels = list(song_stats['ai']['averageEmotion'].keys())
            emotionValues = [song_stats['ai']['averageEmotion'][i] for i in emotionsLabels]
    
    # Prepare context
    if ai_response:
        content = {
            'stats': song_stats,
            'ai_response': ai_response,
            'spotty_chart_labels': spotty_chart_datapoint_labels,
            'spotty_chart_data': [song_stats[i] for i in spotty_chart_datapoint_labels],
            'emotionLabels': emotionsLabels,
            'emotionValues': emotionValues,
        }
    else:
        content = {
            'stats': song_stats,
            'ai_response': ai_response,
            'spotty_chart_labels': spotty_chart_datapoint_labels,
            'spotty_chart_data': [song_stats[i] for i in spotty_chart_datapoint_labels],
            'emotionLabels': None,
            'emotionValues': None,
        }
    
    # Add metadata
    USERNAME = fetch_spotify_data(spotify_token, 'https://api.spotify.com/v1/me')
    song_stats['song_title'] = USERNAME['display_name']
    song_stats['song_artist_name'] = "Recently Played Tracks"
    
    return flask.render_template('Liked_Group_analysis.html', content=content)

# liked songs Analysis
@application.route('/liked-analysis', methods=['GET'])
def liked_analysis():
    spotify_token = flask.session.get('spotify_token')
    likes = user_likes(spotify_token)

    # this function returns two for parallel display of each (song) & grouped ai
    song_stats , each_song_stats = liked_group_average(spotify_token , likes)
    
    # Add amount to total analyized
    flask.session['amount'] += song_stats['ai']['amount']



    # GRAPHING

    # DATA POINTS FOR BAR GRAPH
    spotty_chart_datapoint_labels = [
        'danceability',
        'energy',
        'speechiness',
        'acousticness',
        # 'instrumentalness',
        'liveness',
        'valence',
    ]

    # PIE CHART
    ai_response = False
    if song_stats['ai'] is not None : 
        ai_response = True
        emotionsLabels = list(song_stats['ai']['averageEmotion'].keys())
        emotionValues = [    song_stats['ai']['averageEmotion'][i] for i in emotionsLabels  ]

    # No point to change as it is the same code as the song analysis from here to the components in html...
    USERNAME = fetch_spotify_data( spotify_token , 'https://api.spotify.com/v1/me' )
    song_stats['song_title'] = USERNAME['display_name']
    song_stats['song_artist_name'] = "❤"


    #kinda redundant but i mean.... why not have the modularity?
    if ai_response:
        content = {
            'stats'  : song_stats,
            'ai_response'  : ai_response,
            'each_song_stats'  : each_song_stats,

            # spotify data
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,

            # watson data
            'emotionLabels' : emotionsLabels,
            'emotionValues' : emotionValues,
        }

    #NO LYRICS
    else:
        content = {
            'stats'  : song_stats,
            'each_song_stats'  : each_song_stats,
            'ai_response'  : ai_response,
            'spotty_chart_labels' : spotty_chart_datapoint_labels    ,
            'spotty_chart_data' :  [song_stats[i] for i in spotty_chart_datapoint_labels   ]  ,
            # watson data
            'emotionLabels' : None,
            'emotionValues' : None,
        }


    # sessions for passed songs on html

    return flask.render_template('Liked_Group_analysis.html' , content = content)











# FLASK ERRORS
@application.errorhandler(404)
def page_not_found(e):
    return flask.render_template('error.html', 
                               error_title='Page Not Found',
                               error_message='The page you are looking for does not exist.'), 404

@application.errorhandler(500)
def handle_internal_error(e):
    return flask.redirect('/Dashboard')

@application.errorhandler(400)
def handle_bad_request(e):
    return flask.render_template('error.html',
                               error_title='Bad Request',
                               error_message='The request could not be processed. Please check your input and try again.')

@application.errorhandler(401)
def handle_unauthorized(e):
    return flask.redirect('/')

# Custom error route
@application.route('/error')
def show_error():
    error_title = flask.request.args.get('title', 'An error occurred')
    error_message = flask.request.args.get('message', 'Something went wrong')
    error_details = flask.request.args.get('details', '')
    return flask.render_template('error.html', error_title=error_title, error_message=error_message, error_details=error_details)


if __name__ == '__main__':
    application.run(debug=application.config.get('DEBUG', False))

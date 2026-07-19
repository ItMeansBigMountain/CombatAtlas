#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os
from pathlib import Path
from google_auth_oauthlib.flow import Flow

WORKSPACE_CLIENT = Path('/opt/data/google_client_secret.json')
YOUTUBE_CLIENT = Path('/opt/data/secrets/youtube-main/youtube_client_secret.json')

FULL_WORKSPACE_SCOPES = [
    # Gmail: read, label/archive/trash, send, filter/settings automation
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    # Calendar: create/update/delete scheduling events + list calendars
    'https://www.googleapis.com/auth/calendar',
    # Drive/Docs/Sheets: read/write project files, cache artifacts, docs/sheets dashboards
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    # Contacts/identity lookup
    'https://www.googleapis.com/auth/contacts.readonly',
]

READONLY_WORKSPACE_SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/contacts.readonly',
]

YOUTUBE_AUTOMATION_SCOPES = [
    # Full channel management plus upload, metadata/comments/captions, and read access
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly',
    # Performance loop
    'https://www.googleapis.com/auth/yt-analytics.readonly',
]

ACCOUNTS = {
    # User said: fareed320 is personal-secondary; full automation allowed.
    'personal-secondary': {
        'email': 'fareed320@gmail.com',
        'workspace': 'full',
        'purpose': 'Read newsletter inbox, sort/delete processed emails, use docs/sheets/drive if needed.',
    },
    # User said: trapiistan is Hermes main Gmail workspace account.
    'trapiistan': {
        'email': 'trapiistan@gmail.com',
        'workspace': 'full',
        'youtube': True,
        'purpose': 'Hermes main workspace: calendar scheduling, automation docs, YouTube/content ops.',
    },
    'classicalechos': {
        'email': 'classicalechos@gmail.com',
        'workspace': 'full',
        'youtube': True,
        'purpose': 'Classical Echos content/channel operations; currently owns recent uploaded videos.',
    },
    'burner': {
        'email': 'laflametoast@gmail.com',
        'workspace': 'full',
        'purpose': 'Burner/disposable sending and automation account.',
    },
    # User said all except affan.fareed are full; affan.fareed read-only everything.
    'personal-main': {
        'email': 'affan.fareed@gmail.com',
        'workspace': 'readonly',
        'purpose': 'Primary personal account, read-only only.',
    },
}

def make_workspace_url(profile: str, email: str, mode: str):
    scopes = FULL_WORKSPACE_SCOPES if mode == 'full' else READONLY_WORKSPACE_SCOPES
    home = Path('/opt/data/google_profiles') / profile
    home.mkdir(parents=True, exist_ok=True)
    client_dest = home / 'google_client_secret.json'
    if WORKSPACE_CLIENT.exists() and not client_dest.exists():
        client_dest.write_bytes(WORKSPACE_CLIENT.read_bytes())
        client_dest.chmod(0o600)
    pending = home / 'google_oauth_pending.json'
    token = home / 'google_token.json'
    flow = Flow.from_client_secrets_file(str(client_dest), scopes=scopes)
    flow.redirect_uri = 'http://localhost:1'
    auth_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='false',
        login_hint=email,
    )
    pending.write_text(json.dumps({
        'kind': 'workspace',
        'profile': profile,
        'email': email,
        'mode': mode,
        'state': state,
        'redirect_uri': flow.redirect_uri,
        'client_secret': str(client_dest),
        'token': str(token),
        'scopes': scopes,
        'code_verifier': getattr(flow, 'code_verifier', None),
    }, indent=2))
    pending.chmod(0o600)
    return auth_url, scopes, str(token)

def make_youtube_url(profile: str, email: str):
    base = Path('/opt/data/secrets') / f'youtube-{profile}'
    base.mkdir(parents=True, exist_ok=True)
    client = base / 'youtube_client_secret.json'
    token = base / 'youtube_upload_token.json'
    pending = base / 'youtube_oauth_pending.json'
    if YOUTUBE_CLIENT.exists() and not client.exists():
        client.write_bytes(YOUTUBE_CLIENT.read_bytes())
        client.chmod(0o600)
    flow = Flow.from_client_secrets_file(str(client), scopes=YOUTUBE_AUTOMATION_SCOPES)
    flow.redirect_uri = 'http://localhost:5000/'
    auth_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='false',
        login_hint=email,
    )
    pending.write_text(json.dumps({
        'kind': 'youtube',
        'profile': profile,
        'email': email,
        'state': state,
        'redirect_uri': flow.redirect_uri,
        'client_secret': str(client),
        'token': str(token),
        'scopes': YOUTUBE_AUTOMATION_SCOPES,
        'code_verifier': getattr(flow, 'code_verifier', None),
    }, indent=2))
    pending.chmod(0o600)
    return auth_url, YOUTUBE_AUTOMATION_SCOPES, str(token)

def main():
    out = []
    for profile, cfg in ACCOUNTS.items():
        w_url, w_scopes, w_token = make_workspace_url(profile, cfg['email'], cfg['workspace'])
        out.append({
            'profile': profile,
            'email': cfg['email'],
            'purpose': cfg['purpose'],
            'oauth_kind': 'workspace',
            'access_level': cfg['workspace'],
            'token_path': w_token,
            'scopes': w_scopes,
            'auth_url': w_url,
        })
        if cfg.get('youtube'):
            y_url, y_scopes, y_token = make_youtube_url(profile, cfg['email'])
            out.append({
                'profile': profile,
                'email': cfg['email'],
                'purpose': 'YouTube channel upload/edit/analytics automation.',
                'oauth_kind': 'youtube',
                'access_level': 'automation',
                'token_path': y_token,
                'scopes': y_scopes,
                'auth_url': y_url,
            })
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()

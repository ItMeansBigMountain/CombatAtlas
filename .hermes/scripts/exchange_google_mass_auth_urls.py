#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path
from google_auth_oauthlib.flow import Flow

INPUT = Path('/opt/data/cache/documents/doc_af94552c827f_message.txt')

ROUTES = {
    'fareed320': ('workspace', 'personal-secondary', '/opt/data/google_profiles/personal-secondary/google_oauth_pending.json'),
    'trapiistan workspace': ('workspace', 'trapiistan', '/opt/data/google_profiles/trapiistan/google_oauth_pending.json'),
    'trapiistan youtube': ('youtube', 'trapiistan', '/opt/data/secrets/youtube-trapiistan/youtube_oauth_pending.json'),
    'classical echos workspace': ('workspace', 'classicalechos', '/opt/data/google_profiles/classicalechos/google_oauth_pending.json'),
    'classical echos youtube': ('youtube', 'classicalechos', '/opt/data/secrets/youtube-classicalechos/youtube_oauth_pending.json'),
    'burner account workspace': ('workspace', 'burner', '/opt/data/google_profiles/burner/google_oauth_pending.json'),
    'affan.fareed': ('workspace', 'personal-main', '/opt/data/google_profiles/personal-main/google_oauth_pending.json'),
}

def parse_blocks(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = {}
    i = 0
    while i < len(lines):
        label = lines[i].lower()
        if i + 1 < len(lines) and lines[i+1].startswith('http://localhost:'):
            out[label] = lines[i+1]
            i += 2
        else:
            i += 1
    return out

def exchange(label, url, pending_path):
    p = Path(pending_path)
    data = json.loads(p.read_text())
    client = Path(data['client_secret'])
    token = Path(data['token'])
    scopes = data['scopes']
    flow = Flow.from_client_secrets_file(str(client), scopes=scopes)
    flow.redirect_uri = data['redirect_uri']
    if data.get('code_verifier'):
        flow.code_verifier = data['code_verifier']
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow.fetch_token(authorization_response=url)
    token.parent.mkdir(parents=True, exist_ok=True)
    token.write_text(flow.credentials.to_json())
    token.chmod(0o600)
    p.unlink(missing_ok=True)
    return {'label': label, 'token_path': str(token), 'scopes': sorted(flow.credentials.scopes or scopes), 'has_refresh_token': bool(flow.credentials.refresh_token)}

def main():
    blocks = parse_blocks(INPUT.read_text())
    results = []
    for label, (kind, profile, pending) in ROUTES.items():
        url = blocks.get(label)
        if not url:
            results.append({'label': label, 'status': 'missing_redirect'})
            continue
        try:
            r = exchange(label, url, pending)
            r.update({'status': 'saved', 'kind': kind, 'profile': profile})
            results.append(r)
        except Exception as e:
            results.append({'label': label, 'status': 'error', 'error': type(e).__name__, 'detail': str(e)[:500]})
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

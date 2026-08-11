#!/usr/bin/env python3
"""Sanitize public YouTube metadata for test uploads that exposed production method."""
from __future__ import annotations
import json, os, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from creator_links import support_block

TOKEN = os.getenv('YOUTUBE_UPLOAD_TOKEN') or '/opt/data/secrets/youtube-fareed320/youtube_upload_token.json'
SCOPE = 'https://www.googleapis.com/auth/youtube'
ITEMS = [
    {
        'id': 'vYIO5ELTtBI',
        'title': 'The AI Policy Signal Everyone Is Missing #Shorts',
        'description': "Dario Amodei, DiffusionGemma, and WhatsApp bots all point to the same thing: the next wave is not just smarter tools — it is who controls the rules, the rails, and the workflow.\n\nMy read: don't just collect the headline. Turn the signal into one useful move today." + support_block() + "\n\n#Shorts",
        'tags': ['ai news','technology','motivation','discipline','shorts'],
    },
    {
        'id': 'YHaZ8Jh4AZQ',
        'title': 'Choose To See What It Gave You #Shorts',
        'description': "Sometimes the thing that tested you also trained you. The win is not pretending it was easy — it is finding the strength it forced you to build.\n\nMy read: take one hard thing from today and turn it into a rep instead of a complaint." + support_block() + "\n\n#Shorts",
        'tags': ['stoicism','motivation','discipline','self improvement','shorts'],
    },
]

def main():
    creds = Credentials.from_authorized_user_file(TOKEN, scopes=[SCOPE])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        pathlib.Path(TOKEN).write_text(creds.to_json())
        os.chmod(TOKEN, 0o600)
    yt = build('youtube','v3',credentials=creds, cache_discovery=False)
    results=[]
    for item in ITEMS:
        body = {
            'id': item['id'],
            'snippet': {
                'title': item['title'],
                'description': item['description'],
                'tags': item['tags'],
                'categoryId': '22',
            }
        }
        resp = yt.videos().update(part='snippet', body=body).execute()
        results.append({'id': item['id'], 'updated_title': resp['snippet'].get('title'), 'status': 'updated'})
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

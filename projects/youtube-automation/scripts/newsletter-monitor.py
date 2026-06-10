#!/usr/bin/env python3
"""
Monitor Gmail for newsletter emails that can inspire YouTube shorts.
Searches for TLDR, Kino, Daily Stoic, and other self-help newsletters.
"""

import json, os, sys, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Keywords that indicate content suitable for YouTube shorts (context-aware)
VIDEO_KEYWORDS = {
    'stoic': ['stoic', 'seneca', 'epictetus', 'marcus', 'wisdom', 'virtue', 'discipline'],
    'motivation': ['motivation', 'inspire', 'success', 'habit', 'productivity'],
    'career_tech': ['career', 'remote work', 'job', 'salary', 'interview', 'skills'],
    'content_creation': ['content', 'audience', 'followers', 'lead magnet'],
    'self_help': ['focus', 'mindset', 'growth', 'personal development']
}

def get_header(headers, name):
    """Safely retrieve a header value."""
    for h in headers:
        if h['name'] == name:
            return h['value']
    return ''

def main():
    profile = sys.argv[1] if len(sys.argv) > 1 else 'personal-main'
    token_path = f"/opt/data/secrets/google/tokens/{profile}/google_token.json"
    cred = Credentials.from_authorized_user_file(token_path)
    
    service = build('gmail', 'v1', credentials=cred)
    
    # Search for newsletter emails
    results = service.users().messages().list(
        userId='me',
        q='newsletter OR tldr OR kino OR "daily stoic"',
        maxResults=15
    ).execute()
    
    messages = results.get('messages', [])
    
    print(f"Found {len(messages)} newsletter emails for {profile}")
    
    for msg in messages:
        msg_id = msg['id']
        try:
            message = service.users().messages().get(
                userId='me',
                id=msg_id,
                format='metadata',
                metadataHeaders=['Subject', 'From', 'Date', 'Snippet']
            ).execute()
            
            headers = message['payload']['headers']
            subject = get_header(headers, 'Subject') or ''
            sender = get_header(headers, 'From') or ''
            date = get_header(headers, 'Date') or ''
            snippet = get_header(headers, 'Snippet') or message.get('snippet', '') or ''
            
            print(f"\n- Subject: {subject}")
            print(f"  From: {sender}")
            print(f"  Date: {date}")
            print(f"  Snippet: {snippet[:200]}...")
            
            # Check which category matches
            combined_text = (subject + ' ' + snippet + ' ' + sender).lower()
            matched_categories = []
            
            for category, keywords in VIDEO_KEYWORDS.items():
                if any(kw in combined_text for kw in keywords):
                    matched_categories.append(category)
            
            if matched_categories:
                print(f"  -> VIDEO CANDIDATE (categories: {', '.join(matched_categories)})")
            else:
                print(f"  -> Skip: no matching categories")
                
        except Exception as e:
            print(f"\n- Message {msg_id}: ERROR - {str(e)}")

if __name__ == '__main__':
    main()

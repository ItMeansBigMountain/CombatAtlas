#!/usr/bin/env python3
"""
Monitor Gmail for newsletter emails and create calendar events for video production tasks.
"""

import json, os, sys, datetime, subprocess
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Keywords that indicate content suitable for YouTube shorts
VIDEO_KEYWORDS = {
    'stoic': ['stoic', 'seneca', 'epictetus', 'marcus', 'wisdom', 'virtue', 'discipline'],
    'motivation': ['motivation', 'inspire', 'success', 'habit', 'productivity'],
    'career_tech': ['career', 'remote work', 'job', 'salary', 'interview', 'skills'],
    'content_creation': ['content', 'audience', 'followers', 'lead magnet'],
    'self_help': ['focus', 'mindset', 'growth', 'personal development']
}

def get_header(headers, name):
    for h in headers:
        if h['name'] == name:
            return h['value']
    return ''

def create_calendar_event(profile, subject, description, start_time):
    """Create a calendar event using the specified profile."""
    token_path = f"/opt/data/secrets/google/tokens/{profile}/google_token.json"
    cred = Credentials.from_authorized_user_file(token_path)
    service = build('calendar', 'v3', credentials=cred)
    
    start_dt = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    end_dt = start_dt + datetime.timedelta(minutes=30)
    
    event = {
        'summary': subject,
        'description': description,
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': 'America/Chicago'
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': 'America/Chicago'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [{
                'method': 'email',
                'minutes': 30
            }]
        }
    }
    
    created_event = service.events().insert(
        calendarId='primary',
        body=event,
        sendUpdates='all'
    ).execute()
    
    return created_event.get('htmlLink')

def main():
    profile = sys.argv[1] if len(sys.argv) > 1 else 'personal-main'
    calendar_profile = 'hermes-agent'  # Use the main account for calendar
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
            
            # Check which category matches
            combined_text = (subject + ' ' + snippet + ' ' + sender).lower()
            matched_categories = []
            
            for category, keywords in VIDEO_KEYWORDS.items():
                if any(kw in combined_text for kw in keywords):
                    matched_categories.append(category)
            
            if matched_categories:
                print(f"  -> VIDEO CANDIDATE (categories: {', '.join(matched_categories)})")
                print(f"     Subject: {subject}")
                print(f"     From: {sender}")
                print(f"     Date: {date}")
                
                # Create calendar event for video production
                start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
                event_link = create_calendar_event(
                    profile=calendar_profile,
                    subject=f"Create YouTube Short: {subject[:80]}",
                    description=f"From newsletter: {sender}\n\n{snippet[:500]}",
                    start_time=start_time
                )
                print(f"     Calendar event: {event_link}")
            else:
                print(f"  -> Skip: no matching categories")
                
        except Exception as e:
            print(f"\n- Message {msg_id}: ERROR - {str(e)}")

if __name__ == '__main__':
    main()

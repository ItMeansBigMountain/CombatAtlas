#!/usr/bin/env python3
"""Prepend the configured Stoic offer block to existing Daily Stoic uploads."""
from __future__ import annotations
import json, os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT=Path(__file__).resolve().parents[1]
LOG=ROOT/'UPLOADS/newsletter_youtube_uploads.jsonl'
TOKEN=Path('/opt/data/secrets/youtube-fareed320/youtube_upload_token.json')
EXPECTED_CHANNEL='UCX_nUA3Yr9VR884DNanyMYA'

def offer_block():
    return (
        'Go deeper with Daily Stoic Life: ' + os.getenv('DAILY_STOIC_AFFILIATE_URL','https://dailystoic.com/life').strip() + '\n'
        'Ryan Holiday — The Obstacle Is the Way: ' + os.getenv('RYAN_HOLIDAY_AFFILIATE_URL','https://geni.us/rAlqw').strip() + '\n'
        'Robert Greene — The 48 Laws of Power: ' + os.getenv('ROBERT_GREENE_AFFILIATE_URL','https://www.amazon.com/48-Laws-Power-Robert-Greene/dp/0140280197').strip() + '\n'
        'Affiliate disclosure: Some links may be affiliate links. If you purchase through them, I may earn a commission at no extra cost to you.\n'
        'As an Amazon Associate I earn from qualifying purchases.'
    )

def ids_from_log():
    out=[]
    for line in LOG.read_text(errors='ignore').splitlines():
        try: row=json.loads(line)
        except json.JSONDecodeError: continue
        if row.get('video_id') and 'Marcus Aurelius kept returning' in row.get('description',''):
            out.append(row['video_id'])
    return list(dict.fromkeys(out))

def main():
    creds=Credentials.from_authorized_user_file(str(TOKEN))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request()); TOKEN.write_text(creds.to_json()); os.chmod(TOKEN,0o600)
    yt=build('youtube','v3',credentials=creds,cache_discovery=False)
    mine=yt.channels().list(part='id',mine=True).execute()['items'][0]['id']
    if mine != EXPECTED_CHANNEL: raise RuntimeError(f'channel mismatch: {mine}')
    results=[]
    for start in range(0,len(ids_from_log()),50):
        rows=yt.videos().list(part='snippet',id=','.join(ids_from_log()[start:start+50])).execute().get('items',[])
        for row in rows:
            sn=row['snippet']; desc=sn.get('description','')
            if desc.startswith('📚 Go deeper with Daily Stoic Life:'):
                results.append({'id':row['id'],'status':'already_present'}); continue
            body={'id':row['id'],'snippet':{'title':sn['title'],'description':offer_block()+'\n\n'+desc,'tags':sn.get('tags',[]),'categoryId':sn.get('categoryId','22')}}
            updated=yt.videos().update(part='snippet',body=body).execute()
            results.append({'id':row['id'],'status':'updated','url':'https://youtu.be/'+row['id'],'description_prefix':updated['snippet']['description'].splitlines()[:4]})
    print(json.dumps(results,indent=2,ensure_ascii=False))
if __name__=='__main__': main()

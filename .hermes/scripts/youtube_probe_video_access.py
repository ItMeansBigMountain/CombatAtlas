#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

videos=sys.argv[1:] or ['L6TSaK4avFk','-VZGU-BL40k','tlbC-Bfk38M']
tokens=[
'/opt/data/secrets/youtube-main/youtube_upload_token.json',
'/opt/data/secrets/google/youtube/youtube-main-upload-token.json',
'/opt/data/secrets/google/youtube/faceless-youtube-channel-upload-token.json',
'/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json',
]
scopes=['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/youtube.readonly']
out=[]
for t in tokens:
    p=Path(t)
    rec={'token':t,'exists':p.exists()}
    if not p.exists():
        out.append(rec); continue
    try:
        creds=Credentials.from_authorized_user_file(str(p), scopes=scopes)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            p.write_text(creds.to_json()); p.chmod(0o600)
        yt=build('youtube','v3',credentials=creds,cache_discovery=False)
        ch=yt.channels().list(part='snippet',mine=True).execute()
        rec['channels']=[{'id':i.get('id'),'title':i.get('snippet',{}).get('title')} for i in ch.get('items',[])]
        v=yt.videos().list(part='snippet,status',id=','.join(videos)).execute()
        rec['visible_videos']=[{'id':i.get('id'),'title':i.get('snippet',{}).get('title'),'privacy':i.get('status',{}).get('privacyStatus')} for i in v.get('items',[])]
    except Exception as e:
        rec['error']=str(e)[:500]
    out.append(rec)
print(json.dumps(out,indent=2))

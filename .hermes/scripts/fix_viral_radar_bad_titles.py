#!/usr/bin/env python3
from __future__ import annotations
import json, os, pathlib, re
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
TOKEN='/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json'
SCOPE='https://www.googleapis.com/auth/youtube.force-ssl'
LOG=pathlib.Path('/opt/data/HeRmEz/projects/viral-clip-radar/UPLOADS/viral_radar_enriched_uploads.jsonl')

def pkg(row):
    text=((row.get('creator') or '')+' '+(row.get('source_url') or '')).lower()
    # Use available filename/title-ish data from upload log when source title is absent.
    if any(x in text for x in ['kinobody','fitness','hormone']): return 'Why Your Fitness Plan Feels Rigged'
    if any(x in text for x in ['hormozi','business','entrepreneur']): return 'The Business Trap Nobody Warns You About'
    if any(x in text for x in ['williamson','sex','women','men']): return 'The Desire Gap Nobody Admits'
    if any(x in text for x in ['tate']): return 'The Part They Say Quietly'
    if any(x in text for x in ['hamza']): return 'Why This Hits Harder Than Expected'
    if any(x in text for x in ['belmar']): return 'The Money Mistake That Looks Smart'
    return 'The Uncomfortable Truth Hiding Here'

def creds():
    c=Credentials.from_authorized_user_file(TOKEN)
    if c.expired and c.refresh_token:
        c.refresh(Request()); pathlib.Path(TOKEN).write_text(c.to_json()); os.chmod(TOKEN,0o600)
    return c
rows=[]
for line in LOG.read_text().splitlines():
    try: rows.append(json.loads(line))
    except: pass
m={r.get('video_id'):r for r in rows if r.get('video_id')}
yt=build('youtube','v3',credentials=creds(),cache_discovery=False)
ids=list(m.keys())[-30:]
resp=yt.videos().list(part='snippet', id=','.join(ids)).execute()
out=[]
for item in resp.get('items',[]):
    vid=item['id']; sn=item['snippet']; title=sn.get('title') or ''
    if 'the part people will replay' not in title.lower(): continue
    new_title=pkg(m.get(vid,{}))
    desc=sn.get('description') or ''
    # Replace first line if it was the old title.
    lines=desc.splitlines()
    if lines: lines[0]=new_title
    desc='\n'.join(lines)
    body={'id':vid,'snippet':{'title':new_title,'description':desc,'tags':sn.get('tags',[]),'categoryId':sn.get('categoryId','22')}}
    try:
        yt.videos().update(part='snippet', body=body).execute()
        out.append({'video_id':vid,'url':f'https://youtu.be/{vid}','title':new_title,'updated':True})
    except Exception as e:
        out.append({'video_id':vid,'updated':False,'error':str(e)[:200]})
print(json.dumps({'updated_count':sum(1 for x in out if x.get('updated')),'results':out},indent=2))

#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, pathlib, re, datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES=[
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def load_token(path: str):
    creds=Credentials.from_authorized_user_file(path, scopes=SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        pathlib.Path(path).write_text(creds.to_json())
        os.chmod(path,0o600)
    return creds

def iter_latest_metrics(metrics_path: pathlib.Path):
    latest={}
    for line in metrics_path.read_text(encoding='utf-8', errors='ignore').splitlines():
        try: row=json.loads(line)
        except Exception: continue
        yt=row.get('youtube') or {}
        upload=row.get('upload') or {}
        vid=yt.get('id') or upload.get('video_id') or upload.get('youtube_video_id')
        if vid:
            latest[vid]=row
    return latest

def token_from_metrics_account(s: str) -> str | None:
    m=re.search(r"via\s+(/\S+youtube_upload_token\.json)", s or '')
    return m.group(1) if m else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--metrics', default='/opt/data/HeRmEz/projects/faceless-youtube-channel/ANALYTICS/youtube_metrics.jsonl')
    ap.add_argument('--audit', default='/opt/data/HeRmEz/projects/_ops/youtube-automation/delete-zero-view-audit.json')
    ap.add_argument('--execute', action='store_true')
    args=ap.parse_args()
    latest=iter_latest_metrics(pathlib.Path(args.metrics))
    candidates=[]
    for vid,row in latest.items():
        yt=row.get('youtube') or {}
        stats=yt.get('statistics') or {}
        vc=str(stats.get('viewCount',''))
        if vc != '0':
            continue
        token=token_from_metrics_account(row.get('metrics_account',''))
        candidates.append({
            'video_id': vid,
            'title': (yt.get('snippet') or {}).get('title') or (row.get('upload') or {}).get('title'),
            'url': f'https://youtu.be/{vid}',
            'viewCount': 0,
            'channelId': (yt.get('snippet') or {}).get('channelId'),
            'channelTitle': (yt.get('snippet') or {}).get('channelTitle'),
            'metrics_account': row.get('metrics_account'),
            'token': token,
            'publishedAt': (yt.get('snippet') or {}).get('publishedAt'),
        })
    result={'generated_at':datetime.datetime.now(datetime.UTC).isoformat(),'execute':args.execute,'candidate_count':len(candidates),'candidates':candidates,'deleted':[],'errors':[]}
    if args.execute:
        by_token={}
        for c in candidates:
            by_token.setdefault(c.get('token'),[]).append(c)
        for token, items in by_token.items():
            if not token or not pathlib.Path(token).exists():
                result['errors'].append({'token':token,'error':'token missing','count':len(items)})
                continue
            yt=build('youtube','v3',credentials=load_token(token),cache_discovery=False)
            for c in items:
                vid=c['video_id']
                try:
                    yt.videos().delete(id=vid).execute()
                    # Verify deletion / inaccessible status.
                    check=yt.videos().list(part='id,statistics', id=vid).execute()
                    gone=not check.get('items')
                    result['deleted'].append({**c,'verified_gone':gone})
                except HttpError as e:
                    result['errors'].append({**c,'error':str(e)[:1000]})
                except Exception as e:
                    result['errors'].append({**c,'error':repr(e)})
    audit=pathlib.Path(args.audit); audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['generated_at','execute','candidate_count','deleted','errors']},indent=2))
if __name__=='__main__': main()

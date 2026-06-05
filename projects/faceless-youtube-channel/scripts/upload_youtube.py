#!/usr/bin/env python3
"""Upload an MP4 to YouTube using stored OAuth token. Private-first by default.

Generated media can be deleted after YouTube returns an upload ID. This only
removes the exact video file passed to the uploader; per-job workspaces are
cleaned by the production runner after a confirmed upload.
"""
from __future__ import annotations
import argparse, json, mimetypes, os, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPE="https://www.googleapis.com/auth/youtube.upload"
DEFAULT_TOKEN="/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json"

def load_token(path):
    creds=Credentials.from_authorized_user_file(path, scopes=[SCOPE])
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        pathlib.Path(path).write_text(creds.to_json())
        os.chmod(path, 0o600)
    return creds

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--title', required=True)
    ap.add_argument('--description', default='')
    ap.add_argument('--tags', default='', help='comma-separated')
    ap.add_argument('--privacy', choices=['private','unlisted','public'], default='private')
    ap.add_argument('--category-id', default='22')
    ap.add_argument('--token', default=os.getenv('YOUTUBE_UPLOAD_TOKEN') or DEFAULT_TOKEN)
    ap.add_argument('--delete-after-upload', action='store_true', help='Delete the uploaded local MP4 after YouTube returns a video ID')
    ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args()
    video=pathlib.Path(args.video)
    if not video.exists(): raise SystemExit(f'Missing video: {video}')
    body={
      'snippet': {'title': args.title, 'description': args.description, 'tags': [t.strip() for t in args.tags.split(',') if t.strip()], 'categoryId': args.category_id},
      'status': {'privacyStatus': args.privacy, 'selfDeclaredMadeForKids': False}
    }
    if args.dry_run:
        print(json.dumps({'mode':'dry-run','video':str(video),'bytes':video.stat().st_size,'body':body,'token_present':pathlib.Path(args.token).exists()}, indent=2)); return
    creds=load_token(args.token)
    yt=build('youtube','v3',credentials=creds, cache_discovery=False)
    media=MediaFileUpload(str(video), mimetype=mimetypes.guess_type(video.name)[0] or 'video/mp4', resumable=True)
    req=yt.videos().insert(part='snippet,status', body=body, media_body=media)
    response=None
    while response is None:
        status, response=req.next_chunk()
        if status: print(json.dumps({'upload_progress': int(status.progress()*100)}))
    video_id=response['id']
    result={'status':'UPLOADED','video_id':video_id,'url':f'https://youtu.be/{video_id}','privacy':args.privacy}
    if args.delete_after_upload:
        try:
            video.unlink()
            result['deleted_after_upload']=str(video)
        except Exception as exc:
            result['delete_after_upload_error']=str(exc)
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()

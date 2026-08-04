#!/usr/bin/env python3
"""Clean Viral Radar YouTube descriptions.

- Remove internal cron cohort text.
- Reformat with blank lines for readability.
- Put original source URL on its own line so YouTube renders it as a hyperlink.
"""
from __future__ import annotations
import json, os, pathlib, re
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN = '/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json'
SCOPE = 'https://www.googleapis.com/auth/youtube.force-ssl'
ENRICHED = pathlib.Path('/opt/data/HeRmEz/projects/viral-clip-radar/UPLOADS/viral_radar_enriched_uploads.jsonl')


def load_token():
    creds = Credentials.from_authorized_user_file(TOKEN)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        pathlib.Path(TOKEN).write_text(creds.to_json())
        os.chmod(TOKEN, 0o600)
    return creds


def recent_source_map(limit: int = 60) -> dict[str, dict]:
    rows = []
    if ENRICHED.exists():
        for line in ENRICHED.read_text(encoding='utf-8', errors='ignore').splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    out = {}
    for row in rows[-limit:]:
        vid = row.get('video_id')
        if vid:
            out[vid] = row
    return out


def clean_text(s: str) -> str:
    return re.sub(r'\s+', ' ', s or '').strip(' .')


def relevant_hashtags(*texts: str) -> str:
    blob = ' '.join(t for t in texts if t).lower()
    rules = [
        (('sex','dating','women','men','desire','attraction','bedroom','relationship'), ['DatingAdvice','Relationships','Attraction','MaleFemaleDynamics']),
        (('money','business','sales','entrepreneur','broke','rich','profit'), ['Business','Entrepreneurship','Sales','MoneyMindset']),
        (('fat','muscle','fitness','hormone','diet','body','testosterone','lean'), ['Fitness','FatLoss','Muscle','Hormones']),
        (('discipline','confidence','mindset','focus','motivation','habit'), ['SelfImprovement','Mindset','Discipline','Motivation']),
        (('dog','calm','assertive','cesar','training'), ['DogTraining','CalmEnergy','Leadership']),
        (('numerology','lifepath','astrology','spiritual'), ['Numerology','LifePath','Spirituality']),
        (('dopamine','brain','neuroscience','huberman','sleep','protocol'), ['Neuroscience','Huberman','Health','Dopamine']),
    ]
    tokens = set(re.findall(r'[a-z0-9]+', blob))
    def matches(needle: str) -> bool:
        return (' ' in needle and needle in blob) or needle in tokens
    tags=[]
    for needles, vals in rules:
        if any(matches(n) for n in needles):
            for v in vals:
                if v not in tags: tags.append(v)
    if not tags:
        for w in re.findall(r'[A-Za-z][A-Za-z]{3,}', blob):
            tag=w.title()[:28]
            if tag not in tags and tag.lower() not in {'shorts','viral','radar','source','original'}:
                tags.append(tag)
            if len(tags)>=4: break
    return ' '.join('#'+t for t in ['Shorts', *tags[:5], 'ViralRadar'])


def rebuild_description(title: str, old: str, row: dict) -> str:
    old_flat = clean_text(old)
    # Strip internal cohort marker and anything after it.
    old_flat = re.sub(r'\s*Cron cohort:\s*viral-radar-\d+\.?', '', old_flat, flags=re.I).strip()
    old_flat = re.sub(r'\s*#Shorts.*$', '', old_flat, flags=re.I).strip()

    source_url = row.get('source_url') or ''
    source_line = ''
    context = ''

    m = re.search(r'Source:\s*(.*?)\s*Original source:', old_flat, flags=re.I)
    if m:
        source_line = clean_text(m.group(1))
    m2 = re.search(r'Original source:\s*(https?://\S+)', old_flat, flags=re.I)
    if m2 and not source_url:
        source_url = m2.group(1).rstrip('.')

    before_source = re.split(r'\s*Source:\s*', old_flat, maxsplit=1, flags=re.I)[0]
    # Remove repeated title sentence from the context block.
    if before_source.lower().startswith(title.lower()):
        context = clean_text(before_source[len(title):])
    else:
        context = clean_text(before_source)
    if context == title:
        context = ''

    if not source_line:
        creator = row.get('creator') or 'Source creator'
        source_line = creator

    parts = [title]
    if context:
        parts += ['', context]
    parts += ['', 'Source:', source_line]
    if source_url:
        parts += ['', 'Original source:', source_url]
    hashtags = relevant_hashtags(title, context, source_line, row.get('creator') or '', row.get('source_url') or '')
    parts += ['', 'Edited with vertical framing, burned captions, context, and source attribution.', '', hashtags]
    return '\n'.join(parts)


def main():
    source_map = recent_source_map()
    if not source_map:
        print(json.dumps({'status': 'no_recent_upload_rows'})); return
    yt = build('youtube', 'v3', credentials=load_token(), cache_discovery=False)
    ids = list(source_map.keys())[-30:]
    resp = yt.videos().list(part='snippet', id=','.join(ids)).execute()
    results = []
    for item in resp.get('items', []):
        vid = item['id']
        sn = item['snippet']
        old_desc = sn.get('description') or ''
        needs = ('Cron cohort:' in old_desc or 'Original source:' in old_desc or 'Transformative additions:' in old_desc)
        if not needs:
            continue
        new_desc = rebuild_description(sn.get('title') or '', old_desc, source_map.get(vid, {}))
        body = {
            'id': vid,
            'snippet': {
                'title': sn.get('title') or '',
                'description': new_desc,
                'tags': sn.get('tags', []),
                'categoryId': sn.get('categoryId', '22'),
            }
        }
        try:
            updated = yt.videos().update(part='snippet', body=body).execute()
            results.append({'video_id': vid, 'url': f'https://youtu.be/{vid}', 'updated': True, 'title': updated['snippet'].get('title')})
        except Exception as exc:
            results.append({'video_id': vid, 'url': f'https://youtu.be/{vid}', 'updated': False, 'error': f'{type(exc).__name__}: {str(exc)[:300]}'})
    print(json.dumps({'status': 'ok', 'updated_count': sum(1 for r in results if r.get('updated')), 'results': results}, indent=2))


if __name__ == '__main__':
    main()

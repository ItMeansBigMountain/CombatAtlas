#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re, datetime
ROOT=Path('/opt/data/HeRmEz/projects')
allr=ROOT/'DEPLOY_ALL_REPORT.md'
retry=ROOT/'DEPLOY_RETRY_REPORT.md'
final=ROOT/'DEPLOY_FINAL_URLS.md'
urls={}
mode={}

def parse(path):
    for line in path.read_text().splitlines():
        if not line.startswith('| `'): continue
        parts=[p.strip() for p in line.strip('|').split('|')]
        if len(parts)<3: continue
        name=parts[0].strip('`')
        if name=='Project': continue
        if len(parts)>=5:
            mode[name]=parts[1]
            http=parts[2]; url=parts[3]
        else:
            http=parts[1]; url=parts[2]
            mode.setdefault(name, 'static MVP shell')
        if url and url!='—': urls[name]=url
parse(allr)
if retry.exists(): parse(retry)
# Prefer stable/known aliases after successful redeploys
urls.update({
 'Codology':'https://codology-three.vercel.app',
 'muscleMadness':'https://musclemadness-theta.vercel.app',
 'ticVoter':'https://ticvoter.vercel.app',
 'card-intel-scanner':'https://card-intel-scanner.vercel.app',
 '3d-react-web':'https://3d-react-web.vercel.app',
 'stockNews':'https://stocknews-sentiment.vercel.app',
})

def verify(u):
    try:
        with urlopen(Request(u,headers={'User-Agent':'HermesFinalVerifier/1.0'}),timeout=30) as r: return str(r.status)
    except HTTPError as e: return str(e.code)
    except Exception as e: return 'ERR '+str(e)[:50]
rows=[]
for name in sorted(urls, key=str.lower):
    h=verify(urls[name])
    rows.append((name, mode.get(name,'deployed/static shell'), h, urls[name]))
lines=['# Final Vercel Deployment URLs','',f'Updated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}','', '| Project | Type | HTTP | URL |','|---|---|---:|---|']
for name,m,h,u in rows:
    lines.append(f'| `{name}` | {m} | {h} | {u} |')
lines.append('')
lines.append('Note: many legacy/script/plan-only folders are deployed as safe static review shells so they are visible and editable from a live baseline without secrets, accounts, payments, or paid integrations.')
final.write_text('\n'.join(lines))
print(final)
print('\n'.join(f'{h} {name} {u}' for name,m,h,u in rows if h!='200'))

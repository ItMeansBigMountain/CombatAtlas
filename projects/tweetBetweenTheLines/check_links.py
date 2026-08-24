import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

sources = json.loads(Path('research_sources.json').read_text())

def check(src):
    req = Request(src['url'], headers={'User-Agent':'Mozilla/5.0 Hermes research link checker'})
    try:
        with urlopen(req, timeout=20) as r:
            return {**src, 'status': r.status, 'final_url': r.geturl(), 'content_type': r.headers.get('content-type','')[:80]}
    except HTTPError as e:
        return {**src, 'status': e.code, 'final_url': getattr(e, 'url', src['url']), 'content_type': e.headers.get('content-type','')[:80] if e.headers else '', 'error': str(e)}
    except Exception as e:
        return {**src, 'status': None, 'final_url': src['url'], 'content_type':'', 'error': repr(e)}

results=[]
with ThreadPoolExecutor(max_workers=12) as ex:
    futs=[ex.submit(check,s) for s in sources]
    for fut in as_completed(futs):
        results.append(fut.result())
results.sort(key=lambda r: sources.index(next(s for s in sources if s['key']==r['key'])))
Path('research_source_link_check.json').write_text(json.dumps(results, indent=2)+'\n')
for r in results:
    print(f"{r['status']} {r['key']} -> {r.get('final_url')}")

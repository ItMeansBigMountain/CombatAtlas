#!/usr/bin/env python3
import json, sys, traceback
from pathlib import Path

ROOT=Path('/opt/data/HeRmEz/projects/faceless-youtube-channel')
sys.path.insert(0, str(ROOT/'scripts'))
import newsletter_batch_upload as n

PATTERNS=[
 'openbsd-auth-bypass',
 'irhythm-data-ransom',
 'europe-council-hack',
 'splunk-pre-auth-rce',
]

OLD_URLS={
 '19edae71b000c594':'https://youtu.be/sQI4BZ97Mlo',
 '19ed5c99e5eebecb':'https://youtu.be/q8Jm54K2iJk',
 '19ed09888de59f7a':'https://youtu.be/txoIfKSR_58',
 '19ecb7a320777b1b':'https://youtu.be/YPBCiyLuE8Y',
 '19ebbf9d5b917085':'https://youtu.be/nKsyQsNAaYE',
 '19eb6ddb90acaee0':'https://youtu.be/7KoejAU0oI8',
}

def latest_source(pattern):
    base=ROOT/'videos'
    dirs=sorted([p for p in base.iterdir() if p.is_dir() and pattern in p.name and not p.name.startswith('corrected-')], key=lambda p:p.name)
    if not dirs:
        raise FileNotFoundError(pattern)
    src_path=dirs[-1]/'source_email.json'
    if not src_path.exists():
        raise FileNotFoundError(str(src_path))
    return dirs[-1], json.loads(src_path.read_text(encoding='utf-8'))

def main():
    n.load_dotenv()
    results=[]
    for pat in PATTERNS:
        try:
            old_dir, src=latest_source(pat)
            script=n.build_script(src)
            # Use short proven stock search terms; long sentence-like queries make providers fail.
            stock_terms=['cyber security','server room','data center','hacker','computer security','security operations center','cyber attack','laptop alert','network security','ransomware']
            script['visual_queries']=[stock_terms[i % len(stock_terms)] for i,_ in enumerate(script.get('beats',[]))]
            # Guardrails: fail fast if old advice language sneaks back in.
            bad=['build one proof', 'your move', 'turn this into', 'so the move is simple', 'do not just consume', 'my read:']
            joined=(script.get('narration','')+' '+script.get('description','')).lower()
            hits=[b for b in bad if b in joined]
            if hits:
                raise RuntimeError(f'grounding guard failed: {hits}')
            work=old_dir.parent / ('corrected-' + n.slugify(script['title']))
            work.mkdir(parents=True, exist_ok=True)
            video=n.render(work, script)
            up=n.upload(video, script)
            result={
                'source_message_id': src.get('id'),
                'title': script.get('title'),
                'old_url': OLD_URLS.get(src.get('id')),
                'new_video_path': str(video),
                'upload': up,
                'status': 'uploaded' if up.get('status')=='UPLOADED' else 'blocked',
            }
            if up.get('video_id'):
                with n.UPLOAD_LOG.open('a',encoding='utf-8') as f:
                    f.write(json.dumps({
                        'source_profile':src.get('profile'),
                        'source_message_id':src.get('id'),
                        'youtube_video_id':up.get('video_id'),
                        'url':up.get('url'),
                        'replacement_for':OLD_URLS.get(src.get('id')),
                        'correction':'grounded_newsletter_relay_no_advice'
                    },separators=(',',':'))+'\n')
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
        except Exception as e:
            err={'pattern':pat,'status':'error','error':type(e).__name__,'detail':str(e),'traceback':traceback.format_exc()[-2000:]}
            results.append(err); print(json.dumps(err), flush=True)
    summary={'processed':len(results),'uploaded':sum(1 for r in results if r.get('status')=='uploaded'),'results':results}
    out=ROOT/'UPLOADS'/'corrected_replacements_20260618.json'
    out.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'summary_path':str(out), **summary}, indent=2, ensure_ascii=False))

if __name__=='__main__':
    main()

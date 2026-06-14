#!/usr/bin/env python3
"""Batch render and upload newsletter emails as 9:16 faceless videos.

One Gmail message -> one video -> upload -> trash message only after verified video_id.
Uses Google TTS and dynamic multi-scene cinematic visuals when stock API keys are absent.
"""
from __future__ import annotations
import argparse, base64, datetime as dt, html, json, math, os, re, shutil, subprocess, sys, textwrap, urllib.parse, urllib.request
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
TOKEN_BASE = Path('/opt/data/google_profiles')
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
YOUTUBE_TOKEN = Path('/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json')
UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'newsletter_youtube_uploads.jsonl'

SAFE_TAGS = 'discipline,self improvement,technology,finance,stoicism,motivation,shorts'


def load_dotenv(path=Path('/opt/data/.env')):
    # .env is source of truth for stock-provider keys; override stale inherited
    # process env so a revoked Pexels key does not block/fallback-delay renders.
    managed={'PEXELS_API_KEY','PIXABAY_API_KEY','PIXELS_API_KEY','STORYBLOCKS_PUBLIC_KEY','STORYBLOCKS_PRIVATE_KEY','SHUTTERSTOCK_CONSUMER_KEY','SHUTTERSTOCK_CONSUMER_SECRET','SHUTTERSTOCK_TOKEN'}
    seen=set()
    if path.exists():
        for line in path.read_text(errors='ignore').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k,v=line.split('=',1); k=k.strip(); val=v.strip().strip('"').strip("'")
                if k in managed:
                    os.environ[k]=val; seen.add(k)
                else:
                    os.environ.setdefault(k, val)
    for k in managed-seen:
        os.environ.pop(k, None)


def sh(cmd: list[str], timeout=300) -> str:
    p=subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p.stdout.strip()


def gmail(profile: str):
    token=TOKEN_BASE/profile/'google_token.json'
    creds=Credentials.from_authorized_user_file(str(token), scopes=[GMAIL_SCOPE])
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request()); token.write_text(creds.to_json()); os.chmod(token,0o600)
    return build('gmail','v1',credentials=creds,cache_discovery=False)


def hdr(payload,name):
    for h in payload.get('headers',[]):
        if h.get('name','').lower()==name.lower(): return h.get('value','')
    return ''


def decode(part):
    data=part.get('body',{}).get('data')
    if not data: return ''
    return base64.urlsafe_b64decode(data + '='*(-len(data)%4)).decode('utf-8','replace')


def walk(part):
    yield part
    for c in part.get('parts',[]) or []: yield from walk(c)


def clean_text(s):
    s=re.sub(r'<(script|style).*?</\1>',' ',s,flags=re.I|re.S)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'https?://\S+',' ',s)
    s=re.sub(r'[\u200b\u200c\u200d\ufeff\u034f\xa0]+',' ',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s


def get_email(g, profile, msg_id):
    msg=g.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload=msg['payload']; bodies=[]; htmls=[]
    for p in walk(payload):
        body=decode(p)
        if p.get('mimeType')=='text/plain': bodies.append(body)
        elif p.get('mimeType')=='text/html': htmls.append(body)
    body=clean_text('\n'.join(bodies or htmls) or msg.get('snippet',''))
    return {'profile':profile,'id':msg_id,'threadId':msg.get('threadId'),'from':hdr(payload,'From'),'subject':hdr(payload,'Subject'),'date':hdr(payload,'Date'),'snippet':clean_text(msg.get('snippet','')),'body':body}


def source_type(src):
    t=(src['from']+' '+src['subject']).lower()
    if 'daily stoic' in t: return 'stoic'
    if 'kino' in t: return 'fitness'
    if 'crypto' in t: return 'crypto'
    if 'fintech' in t or 'robinhood' in t: return 'finance'
    if 'infosec' in t or 'security' in t: return 'security'
    if 'ai' in t: return 'ai'
    return 'tech'


def sentence_candidates(body):
    bits=re.split(r'(?<=[.!?])\s+', body)
    out=[]
    junk=('unsubscribe','advertise','sponsor','privacy policy','manage preferences','view in browser')
    for b in bits:
        b=b.strip()
        if 55 <= len(b) <= 240 and not any(j in b.lower() for j in junk):
            out.append(b)
    return out[:12]


def build_script(src):
    typ=source_type(src); subject=clean_text(src['subject'])
    sents=sentence_candidates(src['body'])
    key1=sents[0] if sents else src['snippet'][:180]
    key2=sents[1] if len(sents)>1 else 'The bigger point is not the headline. It is what the headline lets you do next.'
    key3=sents[2] if len(sents)>2 else 'Most people consume the update and move on. Operators turn it into a decision, a workflow, or a receipt.'
    if typ=='stoic':
        hook=f"This is the kind of Stoic lesson people agree with, then completely fail to live. {subject}."
        angle='The lesson only matters if it changes your next uncomfortable choice.'
        cta='Pick one hard thing today and do it before you negotiate with yourself.'
    elif typ=='fitness':
        hook=f"This is not really about fitness tips. It is about the standard you keep when nobody is watching: {subject}."
        angle='Your body follows the receipts: meals logged, walks done, lifts completed, sleep protected.'
        cta='Make the standard visible today: one meal, one walk, one lift, one proof.'
    elif typ in ('finance','crypto'):
        hook=f"Money is moving toward agents, payments, and rails faster than most people are noticing: {subject}."
        angle='The edge is not predicting every headline. The edge is spotting where behavior is becoming infrastructure.'
        cta='Write down the one business or skill this makes more valuable, then build a tiny proof.'
    elif typ=='security':
        hook=f"This security update is not background noise. It is a warning about how fragile modern systems really are: {subject}."
        angle='Every exploit story is also a career signal: someone has to understand the blast radius before it becomes the incident.'
        cta='Turn the headline into one lab, one note, or one control you can explain clearly.'
    elif typ=='ai':
        hook=f"AI is moving from demos into actual workflows, and this headline is another signal: {subject}."
        angle='The winners will not be the people collecting tools. They will be the people converting tools into shipped output.'
        cta='Pick one task you avoid and use the new leverage to ship it today.'
    else:
        hook=f"This tech update looks like news, but it is really a signal about where the next leverage is forming: {subject}."
        angle='Headlines are cheap. Interpretation is where the advantage starts.'
        cta='Save the signal, turn it into one workflow, and move before it becomes obvious.'
    beats=[
        ('STOP SCROLLING', hook),
        ('THE SIGNAL', key1),
        ('WHAT IT MEANS', key2),
        ('THE OPERATOR ANGLE', angle),
        ('THE PROOF', key3),
        ('MOVE FIRST', cta),
    ]
    subject_phrases=[clean_text(p) for p in re.split(r'[,|•]+', subject) if clean_text(p)]
    base_visual={
        'stoic':'stoic discipline morning journaling running alone philosophy',
        'fitness':'gym workout meal prep athletic discipline transformation',
        'finance':'fintech payment technology office money banking app',
        'crypto':'cryptocurrency finance payment technology bank office',
        'security':'cybersecurity hacker server room security operations center',
        'ai':'artificial intelligence engineers working laptop data center startup office',
        'tech':'software engineers working startup office laptop server room technology',
    }.get(typ,'technology office workers laptop')
    visual_queries=[]
    for idx,(cap,body) in enumerate(beats):
        phrase=subject_phrases[idx % len(subject_phrases)] if subject_phrases else subject
        if idx == 0:
            q=f"{phrase} company office workers technology"
        elif idx in (1,2):
            q=f"{phrase} {base_visual}"
        elif idx == 3:
            q=base_visual
        elif idx == 4:
            q=f"people working on {phrase} laptop office"
        else:
            q="focused person working laptop city night motivation"
        visual_queries.append(re.sub(r'[^A-Za-z0-9 ]+',' ',q).strip()[:110])
    narration=' '.join([b[1] for b in beats])
    title=safe_title(subject)
    desc=(f"{title}\n\nMy read: {angle} Build one proof today.\n\n"
          "More from me: https://linktr.ee/sosai.oyama\n"
          "Support the channel: https://buymeacoffee.com/affanfareev\n"
          "Cash App: https://cash.app/$sosaioyama\n"
          "Venmo: https://venmo.com/u/SosaiOyama\n\n#Shorts")
    return {'type':typ,'beats':beats,'visual_queries':visual_queries,'narration':narration,'title':title,'description':desc}


def safe_title(subject):
    s=re.sub(r'[\U00010000-\U0010ffff]','',subject)
    s=re.sub(r'[^A-Za-z0-9 $%&:;,.!?+\-—’\'()]',' ',s)
    s=re.sub(r'\s+',' ',s).strip(' -')
    if len(s)>72: s=s[:72].rsplit(' ',1)[0]
    return s or 'The Signal Everyone Else Missed'


def slugify(s): return re.sub(r'[^a-zA-Z0-9]+','-',s.lower()).strip('-')[:80] or 'newsletter'


def google_tts(text, out:Path):
    creds_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or os.getenv('GOOGLE_TTS_CREDENTIALS')
    creds=service_account.Credentials.from_service_account_file(creds_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
    creds.refresh(Request())
    payload=json.dumps({
        'input': {'text': text},
        'voice': {'languageCode': os.getenv('GOOGLE_TTS_LANGUAGE','en-US'), 'name': os.getenv('GOOGLE_TTS_VOICE','en-US-Neural2-J')},
        'audioConfig': {'audioEncoding':'MP3','speakingRate': float(os.getenv('GOOGLE_TTS_SPEAKING_RATE','1.0'))},
    }).encode()
    req=urllib.request.Request('https://texttospeech.googleapis.com/v1/text:synthesize',data=payload,headers={'Authorization':'Bearer '+creds.token,'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=60) as r: data=json.loads(r.read().decode())
    out.write_bytes(base64.b64decode(data['audioContent']))


def fftext(path:Path): return str(path).replace('\\','/').replace(':','\\:').replace("'","\\'")


def api_json(url: str, headers: dict | None = None, timeout=25):
    req=urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def download(url: str, out: Path, timeout=90) -> bool:
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'Hermes faceless video renderer'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out.write_bytes(r.read())
        return out.exists() and out.stat().st_size > 2048
    except Exception:
        return False


def pexels_video(query: str, out: Path) -> tuple[Path | None, dict | None]:
    key=os.getenv('PEXELS_API_KEY')
    if not key: return None, None
    url='https://api.pexels.com/videos/search?'+urllib.parse.urlencode({'query':query,'orientation':'portrait','per_page':8})
    try:
        data=api_json(url, {'Authorization':key})
        for vid in data.get('videos',[]):
            files=sorted(vid.get('video_files',[]), key=lambda f: abs((f.get('height') or 1080)-1920)+abs((f.get('width') or 1080)-1080))
            for f in files:
                link=f.get('link')
                if link and download(link,out):
                    return out, {'provider':'pexels_video','query':query,'id':vid.get('id'),'url':vid.get('url')}
    except Exception as e:
        return None, {'provider':'pexels_video','query':query,'error':str(e)[:200]}
    return None, {'provider':'pexels_video','query':query,'error':'no_downloadable_result'}


def pixabay_video(query: str, out: Path) -> tuple[Path | None, dict | None]:
    key=os.getenv('PIXABAY_API_KEY')
    if not key: return None, None
    url='https://pixabay.com/api/videos/?'+urllib.parse.urlencode({'key':key,'q':query,'orientation':'vertical','per_page':10,'safesearch':'true'})
    try:
        data=api_json(url)
        for hit in data.get('hits',[]):
            videos=hit.get('videos',{})
            candidates=[videos.get(k,{}) for k in ('large','medium','small','tiny')]
            for f in candidates:
                link=f.get('url')
                if link and download(link,out):
                    return out, {'provider':'pixabay_video','query':query,'id':hit.get('id'),'url':hit.get('pageURL')}
    except Exception as e:
        return None, {'provider':'pixabay_video','query':query,'error':str(e)[:200]}
    return None, {'provider':'pixabay_video','query':query,'error':'no_downloadable_result'}


def shutterstock_video(query: str, out: Path) -> tuple[Path | None, dict | None]:
    token=os.getenv('SHUTTERSTOCK_TOKEN')
    if not token: return None, None
    url='https://api.shutterstock.com/v2/videos/search?'+urllib.parse.urlencode({'query':query,'per_page':8,'sort':'popular'})
    try:
        data=api_json(url, {'Authorization':'Bearer '+token})
        for item in data.get('data',[]):
            assets=item.get('assets',{})
            link=(assets.get('preview_mp4') or assets.get('thumb_mp4') or {}).get('url')
            if link and download(link,out):
                return out, {'provider':'shutterstock_preview_video','query':query,'id':item.get('id'),'url':item.get('url'),'note':'preview asset'}
    except Exception as e:
        return None, {'provider':'shutterstock_preview_video','query':query,'error':str(e)[:200]}
    return None, {'provider':'shutterstock_preview_video','query':query,'error':'no_downloadable_result'}


def pexels_photo(query: str, out: Path) -> tuple[Path | None, dict | None]:
    key=os.getenv('PEXELS_API_KEY')
    if not key: return None, None
    url='https://api.pexels.com/v1/search?'+urllib.parse.urlencode({'query':query,'orientation':'portrait','per_page':8})
    try:
        data=api_json(url, {'Authorization':key})
        for photo in data.get('photos',[]):
            src=photo.get('src',{})
            link=src.get('portrait') or src.get('large2x') or src.get('large')
            if link and download(link,out):
                return out, {'provider':'pexels_photo','query':query,'id':photo.get('id'),'url':photo.get('url')}
    except Exception as e:
        return None, {'provider':'pexels_photo','query':query,'error':str(e)[:200]}
    return None, {'provider':'pexels_photo','query':query,'error':'no_downloadable_result'}


def wikimedia_image(query: str, out: Path) -> tuple[Path | None, dict | None]:
    # No-key fallback for company/topic imagery. Pexels/Pixabay remain preferred
    # for true stock footage when keys are configured.
    clean=re.sub(r'\b(company|office|workers|technology|laptop|people working on)\b',' ',query,flags=re.I)
    clean=re.sub(r'\s+',' ',clean).strip() or query
    url='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({
        'action':'query','generator':'search','gsrsearch':clean,'gsrnamespace':6,'gsrlimit':8,
        'prop':'imageinfo','iiprop':'url|mime|size|extmetadata','iiurlwidth':1200,'format':'json','origin':'*'
    })
    try:
        data=api_json(url, {'User-Agent':'Hermes faceless video renderer'})
        pages=list((data.get('query',{}) or {}).get('pages',{}).values())
        for page in pages:
            title=(page.get('title') or '').lower()
            if any(bad in title for bad in ['logo','icon','svg','map','seal']):
                continue
            info=(page.get('imageinfo') or [{}])[0]
            if not str(info.get('mime','')).startswith('image/'):
                continue
            if (info.get('width') or 0) < 500 or (info.get('height') or 0) < 500:
                continue
            link=info.get('thumburl') or info.get('url')
            if link and download(link,out):
                return out, {'provider':'wikimedia_image','query':query,'search':clean,'title':page.get('title'),'url':info.get('descriptionurl') or link}
    except Exception as e:
        return None, {'provider':'wikimedia_image','query':query,'error':str(e)[:200]}
    return None, {'provider':'wikimedia_image','query':query,'error':'no_downloadable_result'}


def visual_asset(query: str, out_base: Path) -> tuple[Path | None, dict]:
    safe=re.sub(r'[^a-zA-Z0-9]+','-',query.lower()).strip('-')[:45] or 'visual'
    attempts=[]
    for fn, ext in ((pexels_video,'.mp4'), (pixabay_video,'.mp4'), (pexels_photo,'.jpg'), (shutterstock_video,'.mp4'), (wikimedia_image,'.jpg')):
        path=out_base.with_name(out_base.name+'-'+safe+ext)
        got, meta=fn(query,path)
        if meta: attempts.append(meta)
        if got: return got, meta or {'provider':fn.__name__,'query':query}
    return None, {'provider':'fallback_dynamic','query':query,'attempts':attempts}


def background_input(asset: Path | None, dur: float) -> tuple[list[str], list[str]]:
    if asset and asset.suffix.lower() in ('.mp4','.mov','.webm'):
        return ['-stream_loop','-1','-i',str(asset)], [f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={dur:.2f},setpts=PTS-STARTPTS,boxblur=2:1,eq=contrast=1.08:saturation=1.12:brightness=-0.05[bg]']
    if asset:
        return ['-loop','1','-i',str(asset)], [f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={dur:.2f},setpts=PTS-STARTPTS,zoompan=z=1+0.0008*on:d=1:s=1080x1920:fps=30,boxblur=1:1,eq=contrast=1.08:saturation=1.1:brightness=-0.04[bg]']
    return ['-f','lavfi','-i',f'color=c=black:s=1080x1920:d={dur:.2f}'], ['[0:v]scale=1080:1920[bg]']


def render(work:Path, script):
    scenes=work/'scenes'; scenes.mkdir(exist_ok=True)
    assets_dir=work/'visual_assets'; assets_dir.mkdir(exist_ok=True)
    final_parts=[]; visual_manifest=[]
    queries=script.get('visual_queries') or []
    for i,(cap,body) in enumerate(script['beats'],1):
        audio=scenes/f'{i:02d}.mp3'; google_tts(f'{cap}. {body}', audio)
        dur=float(sh(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)],60)) + 0.8
        query=queries[i-1] if i-1 < len(queries) else f"{script.get('type','technology')} people working laptop"
        asset, meta=visual_asset(query, assets_dir/f'{i:02d}')
        visual_manifest.append({'scene':i,'caption':cap,'query':query,'asset':str(asset) if asset else None,'meta':meta})
        titlef=scenes/f'{i:02d}_title.txt'; bodyf=scenes/f'{i:02d}_body.txt'
        titlef.write_text('\n'.join(textwrap.wrap(cap,16)),encoding='utf-8')
        bodyf.write_text('\n'.join(textwrap.wrap(body,31))[:520],encoding='utf-8')
        accent=['0x38BDF8','0xFACC15','0x22C55E','0xF97316','0xA78BFA','0xEF4444'][i-1]
        bg_args,bg_filters=background_input(asset,dur)
        filters=bg_filters + [
          f'[bg]drawbox=x=0:y=0:w=1080:h=1920:color=0x020617@0.30:t=fill,'
          f'drawbox=x=50:y=95:w=980:h=330:color=0x020617@0.62:t=fill,'
          f'drawbox=x=80:y=435:w=900*min(t/3\\,1):h=14:color={accent}:t=fill,'
          f'drawbox=x=70:y=1120:w=940:h=520:color=0x020617@0.74:t=fill,'
          f"drawtext=textfile='{fftext(titlef)}':font=DejaVuSans-Bold:fontcolor=0xF8FAFC:fontsize=72:x=80:y=135:line_spacing=10:shadowcolor=black:shadowx=3:shadowy=3,"
          f"drawtext=textfile='{fftext(bodyf)}':font=DejaVuSans:fontcolor=0xE2E8F0:fontsize=41:x=105:y=1150:line_spacing=16:shadowcolor=black:shadowx=2:shadowy=2,"
          f"drawtext=text='BUILD ONE PROOF TODAY':font=DejaVuSans-Bold:fontcolor={accent}:fontsize=32:x=95:y=1745:shadowcolor=black:shadowx=2:shadowy=2,"
          f'drawbox=x=80:y=1810:w=920*{i}/6:h=12:color={accent}:t=fill[v]'
        ]
        out=scenes/f'{i:02d}.mp4'
        sh(['ffmpeg','-y','-hide_banner',*bg_args,'-i',str(audio),'-filter_complex',';'.join(filters),'-map','[v]','-map','1:a','-t',f'{dur:.2f}','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(out)],300)
        final_parts.append(out)
    (work/'visual_manifest.json').write_text(json.dumps(visual_manifest,indent=2),encoding='utf-8')
    concat=work/'concat.txt'; concat.write_text(''.join(f"file {p.resolve()}\n" for p in final_parts),encoding='utf-8')
    final=work/'final.mp4'; sh(['ffmpeg','-y','-hide_banner','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(final)],300)
    return final


def parse_uploader_json(raw: str):
    raw=raw.strip()
    if raw.startswith('{'):
        try: return json.loads(raw)
        except Exception: pass
    marker='\n{\n  "status"'
    idx=raw.rfind(marker)
    if idx >= 0:
        return json.loads(raw[idx+1:])
    # fallback: find the last JSON object opener
    idx=raw.rfind('{')
    if idx >= 0:
        return json.loads(raw[idx:])
    raise ValueError('No JSON object found in uploader output: '+raw[-500:])


def upload(video:Path, script):
    raw=sh([sys.executable,str(UPLOADER),str(video),'--title',script['title'],'--description',script['description'],'--tags',SAFE_TAGS,'--privacy','public','--token',str(YOUTUBE_TOKEN),'--project','faceless-youtube-newsletters','--log-jsonl',str(UPLOAD_LOG),'--delete-after-upload'],600)
    return parse_uploader_json(raw)


def already_done(msg_id):
    if not UPLOAD_LOG.exists(): return False
    return msg_id in UPLOAD_LOG.read_text(errors='ignore')


def process(profile,msg_id, upload_enabled=True):
    g=gmail(profile); src=get_email(g,profile,msg_id); script=build_script(src)
    stamp=dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S')
    work=ROOT/'videos'/f"{stamp}-{slugify(src['subject'])}"
    work.mkdir(parents=True, exist_ok=True)
    (work/'source_email.json').write_text(json.dumps({k:v for k,v in src.items() if k!='body'} | {'body_excerpt':src['body'][:5000]},indent=2),encoding='utf-8')
    (work/'script.json').write_text(json.dumps(script,indent=2),encoding='utf-8')
    video=render(work,script)
    probe=json.loads(sh(['ffprobe','-v','error','-show_entries','stream=width,height','-show_entries','format=duration,size','-of','json',str(video)],60))
    result={'profile':profile,'message_id':msg_id,'subject':src['subject'],'workspace':str(work),'video':str(video),'probe':probe,'uploaded':False}
    if upload_enabled:
        up=upload(video,script); result['upload']=up; result['uploaded']=up.get('status')=='UPLOADED'
        if result['uploaded'] and up.get('video_id'):
            g.users().messages().trash(userId='me', id=msg_id).execute(); result['trashed_source_email']=True
            # append source id marker to upload log for idempotency
            with UPLOAD_LOG.open('a',encoding='utf-8') as f: f.write(json.dumps({'source_profile':profile,'source_message_id':msg_id,'youtube_video_id':up.get('video_id'),'url':up.get('url')},separators=(',',':'))+'\n')
    (work/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


def discover(profile, limit):
    g=gmail(profile)
    queries=['from:tldrnewsletter.com newer_than:30d -in:trash','from:info@dailystoic.com newer_than:30d -in:trash','from:news@kinobody.com newer_than:30d -in:trash']
    out=[]; seen=set()
    for q in queries:
        resp=g.users().messages().list(userId='me',q=q,maxResults=limit).execute()
        for m in resp.get('messages',[]):
            if m['id'] not in seen and not already_done(m['id']):
                seen.add(m['id']); out.append(m['id'])
                if len(out)>=limit: return out
    return out


def main():
    load_dotenv(); ap=argparse.ArgumentParser()
    ap.add_argument('--profile',default='personal-secondary')
    ap.add_argument('--limit',type=int,default=3)
    ap.add_argument('--message',action='append',help='explicit Gmail message id; can repeat')
    ap.add_argument('--no-upload',action='store_true')
    args=ap.parse_args()
    ids=args.message or discover(args.profile,args.limit)
    results=[]
    for mid in ids:
        try:
            results.append(process(args.profile,mid,not args.no_upload))
            print(json.dumps(results[-1],indent=2))
        except Exception as e:
            err={'profile':args.profile,'message_id':mid,'error':type(e).__name__,'detail':str(e)[:1000]}
            results.append(err); print(json.dumps(err,indent=2))
    print(json.dumps({'processed':len(results),'uploaded':sum(1 for r in results if r.get('uploaded')),'results':results},indent=2))

if __name__=='__main__': main()

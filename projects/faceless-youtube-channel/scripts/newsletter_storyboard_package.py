#!/usr/bin/env python3
"""Create a quality-gated storyboard package from one newsletter email.

This does not upload. It creates the assets/specs required before rendering with
ElevenLabs + an AI video provider.
"""
from __future__ import annotations
import argparse, base64, html, json, os, re, textwrap, datetime as dt
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT=Path(__file__).resolve().parents[1]
TOKEN_BASE=Path('/opt/data/google_profiles')
SCOPE='https://www.googleapis.com/auth/gmail.modify'

def load_dotenv(path=Path('/opt/data/.env')):
    if path.exists():
        for line in path.read_text(errors='ignore').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k,v=line.split('=',1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def service(profile):
    token=TOKEN_BASE/profile/'google_token.json'
    creds=Credentials.from_authorized_user_file(str(token), scopes=[SCOPE])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request()); token.write_text(creds.to_json()); os.chmod(token,0o600)
    return build('gmail','v1',credentials=creds, cache_discovery=False)

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
    s=re.sub(r'<(script|style).*?</\\1>',' ',s,flags=re.I|re.S)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[\u200b\u200c\u200d\ufeff\u034f]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()

def get_email(profile,msg_id):
    g=service(profile)
    msg=g.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload=msg['payload']
    bodies=[]; htmls=[]
    for p in walk(payload):
        body=decode(p)
        if p.get('mimeType')=='text/plain': bodies.append(body)
        elif p.get('mimeType')=='text/html': htmls.append(body)
    body=clean_text('\n'.join(bodies or htmls) or msg.get('snippet',''))
    return {'profile':profile,'id':msg_id,'threadId':msg.get('threadId'),'from':hdr(payload,'From'),'subject':hdr(payload,'Subject'),'date':hdr(payload,'Date'),'snippet':msg.get('snippet',''),'body_excerpt':body[:3500]}

def slugify(t): return re.sub(r'[^a-zA-Z0-9]+','-',t.lower()).strip('-')[:80] or 'newsletter'

def topic_type(src):
    text=(src['from']+' '+src['subject']).lower()
    if 'daily stoic' in text: return 'daily_stoic'
    if 'kino' in text: return 'kino_body'
    if 'infosec' in text: return 'tldr_infosec'
    if 'dev' in text: return 'tldr_dev'
    if 'ai' in text: return 'tldr_ai'
    return 'tldr_news'

def build_package(src):
    typ=topic_type(src); subject=src['subject']; body=src['body_excerpt']
    first_sentence=(re.split(r'(?<=[.!?])\s+', body) or [body])[0][:220]
    hook=f"This email is easy to skim past — but it is actually a signal: {subject}"
    if typ=='daily_stoic':
        vibe='disciplined solitude, morning grit, stoic reflection'
        takeaway='Turn the lesson into one uncomfortable rep today.'
        broll=['lone man running before sunrise on empty city street','close-up hand writing in worn notebook beside black coffee','cinematic gym rep slow motion sweat and discipline','ancient marble statue shadowed by modern city lights','person walking alone in rain with calm determined posture']
    elif typ=='kino_body':
        vibe='fitness transformation, masculine discipline, clean lifestyle'
        takeaway='Make the body-standard visible through today’s meal, walk, and lift.'
        broll=['cinematic gym bench press close up dramatic lighting','meal prep containers on kitchen counter morning sunlight','athlete tying shoes before sunrise cardio','mirror physique check silhouette not explicit','scale and tape measure beside notebook progress tracker']
    else:
        vibe='operator motivation, tech leverage, high-stakes future'
        takeaway='Convert the signal into a workflow, note, or shipped proof before it becomes trivia.'
        broll=['cinematic server room with blue light and moving data reflections','engineer at dark workstation terminal code close up','AI agent workflow nodes floating over laptop screen','policy hearing room dramatic shallow depth of field','futuristic smartphone chat bots and payment rails visualized']
    narration=[
        hook,
        f"The useful part: {first_sentence}",
        "Most people collect headlines. Operators extract leverage.",
        takeaway,
        "Save this signal, build one proof, then move before everyone else calls it obvious."
    ]
    captions=['DON’T SKIM THIS','THE REAL SIGNAL','HEADLINES ≠ LEVERAGE','BUILD ONE PROOF','MOVE FIRST']
    shots=[]
    for i,p in enumerate(broll,1):
        shots.append({'shot':i,'duration_sec':3.0,'caption':captions[i-1],'ai_video_prompt':f"vertical 9:16 motivational faceless YouTube b-roll, {p}, {vibe}, cinematic lighting, realistic, shallow depth of field, slow camera push, high contrast, no text, no logos"})
    return {'source':{k:src[k] for k in ['profile','id','from','subject','date','snippet']}, 'type':typ, 'narration':'\n\n'.join(narration), 'captions':captions, 'broll_prompts':shots, 'quality_gate':['one_email_one_video','actual_email_content_used','elevenlabs_required','ai_video_broll_required','no_static_text_placeholder','upload_only_after_manual_or_automated_quality_pass']}

def main():
    load_dotenv(); ap=argparse.ArgumentParser(); ap.add_argument('--message', required=True, help='profile:message_id'); args=ap.parse_args()
    profile,msg_id=args.message.split(':',1); src=get_email(profile,msg_id); package=build_package(src)
    stamp=dt.datetime.now(dt.UTC).strftime('%Y%m%d-%H%M%S'); work=ROOT/'videos'/f"{stamp}-{slugify(src['subject'])}-storyboard"
    work.mkdir(parents=True, exist_ok=True)
    (work/'source_email.json').write_text(json.dumps(src,indent=2),encoding='utf-8')
    (work/'script.md').write_text('# Narration\n\n'+package['narration']+'\n',encoding='utf-8')
    (work/'broll_prompts.json').write_text(json.dumps(package['broll_prompts'],indent=2),encoding='utf-8')
    (work/'package.json').write_text(json.dumps(package,indent=2),encoding='utf-8')
    print(json.dumps({'workspace':str(work),'type':package['type'],'source_subject':src['subject'],'broll_prompt_count':len(package['broll_prompts']),'upload_blocked_until_ai_broll_and_elevenlabs_rendered':True},indent=2))
if __name__=='__main__': main()

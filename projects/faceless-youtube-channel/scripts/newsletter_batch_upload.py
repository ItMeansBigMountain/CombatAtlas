#!/usr/bin/env python3
"""Batch render and upload newsletter emails as 9:16 faceless videos.

One Gmail message -> one video -> upload -> trash message only after verified video_id.
Uses Google TTS and dynamic multi-scene cinematic visuals when stock API keys are absent.
"""
from __future__ import annotations
import argparse, base64, datetime as dt, html, json, math, os, random, re, shutil, subprocess, sys, textwrap, traceback, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
TOKEN_BASE = Path('/opt/data/google_profiles')
GMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
# Faceless/newsletter videos must always upload to A F (fareed320).
# Do not honor an inherited YOUTUBE_UPLOAD_TOKEN here: Viral Radar jobs export
# the Classical Echos token, and a shared process environment once caused a
# newsletter Short to land on the wrong channel.
YOUTUBE_TOKEN = Path('/opt/data/secrets/youtube-fareed320/youtube_upload_token.json')
UPLOADER = Path('/opt/data/HeRmEz/projects/_ops/youtube-automation/scripts/upload_youtube.py')
UPLOAD_LOG = ROOT / 'UPLOADS' / 'newsletter_youtube_uploads.jsonl'
VISUAL_HISTORY = ROOT / 'UPLOADS' / 'visual_asset_history.jsonl'
BACKLOG = ROOT / 'BACKLOG_DAILY_STOIC'
BACKLOG_LOG = ROOT / 'UPLOADS' / 'daily_stoic_backlog.jsonl'

SAFE_TAGS = 'discipline,self improvement,technology,finance,stoicism,motivation,shorts'
TARGET_SHORT_SECONDS = (45, 95)  # full newsletter shorts can run longer, but avoid draggy 2+ min renders
MAX_SCENES = 8
VIRAL_HOOK_CAPTIONS = [
    'YOU MISSED THIS', 'NOT THE HEADLINE', 'WATCH THE SHIFT', 'THE REAL SIGNAL',
    'FOLLOW THE MONEY', 'THE RECEIPT', 'WHY IT MATTERS', 'YOUR MOVE'
]


def load_dotenv(path=Path('/opt/data/.env')):
    # /opt/data/.env plus project-local stock files are the source of truth for
    # stock-provider keys; override stale inherited process env so revoked keys
    # do not block/fallback-delay renders. Later files win, letting .env.pexels
    # supply the dedicated Pexels key without exposing it in the global env.
    managed={'PEXELS_API_KEY','PIXABAY_API_KEY','PIXELS_API_KEY','STORYBLOCKS_PUBLIC_KEY','STORYBLOCKS_PRIVATE_KEY','SHUTTERSTOCK_CONSUMER_KEY','SHUTTERSTOCK_CONSUMER_SECRET','SHUTTERSTOCK_TOKEN'}
    seen=set()
    for env_path in [path, ROOT/'.env', ROOT/'.env.pexels']:
        if env_path.exists():
            for line in env_path.read_text(errors='ignore').splitlines():
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
    if not token.exists():
        pending=TOKEN_BASE/profile/'pending.json'
        hint=f"missing Gmail OAuth token for profile {profile}: {token}"
        if pending.exists():
            hint += f"; reauthentication is pending at {pending}"
        raise RuntimeError(hint)
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
    if 'kino' in t or 'fitness' in t or 'workout' in t or 'gym' in t: return 'fitness'
    if 'martial' in t or 'karate' in t or 'bjj' in t or 'boxing' in t or 'mma' in t or 'ufc' in t or 'muay thai' in t: return 'martial_arts'
    if 'crypto' in t: return 'crypto'
    if 'fintech' in t or 'robinhood' in t: return 'finance'
    if 'infosec' in t or 'security' in t: return 'security'
    if 'ai' in t: return 'ai'
    return 'tech'


def scene_keyword(text: str, fallback: str='story') -> str:
    """Pick one concrete keyword/phrase from a spoken beat for visual search."""
    stop={'about','after','again','already','because','before','being','could','every','their','there','these','thing','those','through','today','under','where','which','while','would','people','really','still','start','right','headline','details','story','this','that'}
    candidates=[]
    for m in re.finditer(r'\b[A-Z][A-Za-z0-9+.&-]{2,}(?:\s+[A-Z][A-Za-z0-9+.&-]{2,}){0,2}\b', text):
        cand=m.group(0)
        if cand.lower() not in stop:
            candidates.append(cand)
    for w in re.findall(r'\b[a-zA-Z][a-zA-Z0-9+-]{4,}\b', text.lower()):
        if w not in stop:
            candidates.append(w)
    return clean_text(candidates[0] if candidates else fallback)[:42]


def narrator_persona(typ: str, subject: str) -> dict:
    """Internal tone target; we do not claim or clone celebrity voices in metadata."""
    if typ in ('fitness','martial_arts'):
        return {'archetype':'Denzel Washington training-montage mentor','pace':'controlled, intense, inspirational'}
    if typ=='stoic':
        return {'archetype':'Morgan Freeman wise narrator','pace':'warm, reflective, grounded'}
    if typ in ('finance','crypto'):
        return {'archetype':'Matthew McConaughey smooth strategist','pace':'confident, sly, conversational'}
    if typ=='security':
        return {'archetype':'Jason Statham heist briefing','pace':'urgent, clipped, no-nonsense'}
    if typ=='ai':
        return {'archetype':'Robert Downey Jr. fast-talking inventor','pace':'witty, sharp, energetic'}
    return {'archetype':'Ryan Reynolds sarcastic explainer','pace':'quick, playful, clear'}


def sentence_candidates(body):
    bits=re.split(r'(?<=[.!?])\s+', body)
    out=[]
    junk=('unsubscribe','advertise','sponsor','sponsored','privacy policy','manage preferences','view in browser','sign up','presented by','tldr together with','readers will learn','read the report','flashpoint')
    for b in bits:
        b=b.strip()
        if 55 <= len(b) <= 240 and not any(j in b.lower() for j in junk):
            out.append(b)
    return out[:12]


def interesting_terms(subject: str, body: str) -> list[str]:
    raw=' '.join(re.split(r'[,|•:;\-–—]+', subject))+' '+body[:1200]
    terms=[]
    for m in re.finditer(r'\b(?:[A-Z][A-Za-z0-9+.&-]{2,}|[A-Z]{2,}|\$\d+[a-zA-Z]*|\d+%|\d+x)\b', raw):
        t=m.group(0).strip('.,()[]')
        if t.lower() not in {'the','and','for','with','from','this','that'} and t not in terms:
            terms.append(t)
    return terms[:8]


def humanize_fact(sentence: str, max_len: int = 190) -> str:
    s=clean_text(sentence)
    s=re.sub(r'\[[0-9]+\]|\[link\]|\(\s*\[link\]\s*\)', '', s, flags=re.I)
    s=re.sub(r'^\s*\d+\s+', '', s)
    s=re.sub(r'\b(HEADLINES|TRENDS|SPONSOR|PRESENTED BY)\b.*', '', s, flags=re.I).strip()
    s=re.sub(r'\bSee how it works\b.*', '', s, flags=re.I).strip()
    s=re.sub(r'[\U00010000-\U0010ffff]', '', s)
    s=re.sub(r'\b(newsletter|read more|sponsored|advertisement)\b.*','',s,flags=re.I).strip()
    s=re.sub(r'\s+',' ',s).strip(' -–—:;,.')
    s=re.sub(r'\b(from|with|and|or|to|of|for)$', '', s, flags=re.I).strip(' -–—:;,.')
    if len(s) > max_len:
        s=s[:max_len].rsplit(' ',1)[0].rstrip(',;:')+'.'
    elif s and s[-1] not in '.!?':
        s += '.'
    return s or 'The details are still moving, but the shift is loud enough to pay attention.'


def loosen_story_voice(text: str) -> str:
    """Keep narration feeling like one charismatic monologue, not an outline."""
    swaps={
        'Here’s what caught me:':'The part that made me stop was this:',
        'Here’s the thing:':'And this is where it gets interesting:',
        'Here’s why this matters:':'This is why I would not shrug this off:',
        'You can see it in the details:':'The receipts are already sitting in the details:',
        'Then the details start to stack up:':'Then the receipts start stacking up:',
        'The signal around':'The quiet shift around',
        'So do not just watch the headline.':'So do not let this stay as just another headline.',
        'So do not just consume the update.':'So do not let this become another thing you consumed and forgot.',
    }
    for old,new in swaps.items():
        text=text.replace(old,new)
    return re.sub(r'\s+',' ',text).strip()


def stoic_affiliate_block() -> str:
    """Top-of-description Stoic offers; env URLs can carry the owner's affiliate IDs."""
    daily_stoic_url=os.getenv('DAILY_STOIC_AFFILIATE_URL','https://dailystoic.com/life').strip()
    ryan_url=os.getenv('RYAN_HOLIDAY_AFFILIATE_URL','https://geni.us/rAlqw').strip()
    greene_url=os.getenv('ROBERT_GREENE_AFFILIATE_URL','https://www.amazon.com/48-Laws-Power-Robert-Greene/dp/0140280197').strip()
    return (
        "Go deeper with Daily Stoic Life: " + daily_stoic_url + "\n"
        "Ryan Holiday — The Obstacle Is the Way: " + ryan_url + "\n"
        "Robert Greene — The 48 Laws of Power: " + greene_url + "\n"
        "Affiliate disclosure: Some links may be affiliate links. If you purchase through them, I may earn a commission at no extra cost to you.\n"
        "As an Amazon Associate I earn from qualifying purchases."
    )


def build_stoic_retention_script(src):
    """Build a tension-first Stoic story instead of stitching facts with boilerplate."""
    subject=clean_text(src['subject']); body=clean_text(src.get('body',''))
    persona=narrator_persona('stoic', subject)
    facts=[humanize_fact(s) for s in sentence_candidates(body)]
    joined=' '.join(facts)

    if 'Marcus Aurelius' in joined:
        hook="Marcus Aurelius never outgrew the same lessons—and that may be why they saved him."
    else:
        concrete=scene_keyword(joined, safe_title(subject))
        hook=f"The Stoics never treated {concrete} as a lesson you learn once."

    selected=[]
    for fact in facts:
        low=fact.lower()
        if any(k in low for k in ('marcus aurelius','epictetus','rusticus','meditations','true freedom','control','anger','difficult people','duty')):
            if fact not in selected:
                selected.append(fact)
        if len(selected) >= 5:
            break
    if len(selected) < 4:
        selected=(selected + [f for f in facts if f not in selected])[:5]

    # Hook -> historical image -> escalating proof -> reversal -> practical payoff.
    story=[hook]
    if selected:
        story.append(selected[0])
    if len(selected)>1:
        story.append(selected[1])
    story.append("He returned to those ideas on anger, death, difficult people, and duty—not because he had mastered them, but because he had not.")
    if len(selected)>2:
        story.append(selected[2])
    story.append("That is the part most people miss: reading can introduce an idea, but repetition is what makes it available when pressure arrives.")
    story.append("You do not stop when the words sound familiar. You stop when your behavior finally does.")

    captions=['HE STILL FAILED','ONE BOOK. AGAIN.','THE IDEAS RETURNED','NOT MASTERY','PRESSURE WAS THE TEST','FAMILIAR ISN’T ENOUGH','WHEN YOU CAN STOP']
    beats=[(captions[i], line) for i,line in enumerate(story[:7])]
    visual_queries=[
        'Marcus Aurelius statue dramatic close up',
        'ancient philosophy book candle hands',
        'Roman emperor statue dark cinematic',
        'angry man calming down alone',
        'person under pressure rain cinematic',
        'journaling repeated practice morning',
        'disciplined person walking sunrise',
    ][:len(beats)]
    narration=' '.join(line for _,line in beats)
    title=safe_title(subject)
    desc=(stoic_affiliate_block() + "\n\n" +
          f"{title}\n\nMarcus Aurelius kept returning to the same lessons for a reason: recognition is not mastery.\n\n"
          "More from me: https://linktr.ee/sosai.oyama\n"
          "Support the channel: https://buymeacoffee.com/affanfareev\n"
          "Cash App: https://cash.app/$sosaioyama\n"
          "Venmo: https://venmo.com/u/SosaiOyama\n\n#Shorts")
    return {'type':'stoic','persona':persona,'beats':beats,'visual_queries':visual_queries,'narration':narration,'title':title,'description':desc}


def build_script(src):
    typ=source_type(src); subject=clean_text(src['subject'])
    if typ == 'stoic':
        return build_stoic_retention_script(src)
    persona=narrator_persona(typ, subject)
    spoken_subject=safe_title(subject)
    body=clean_text(src.get('body',''))
    sents=[humanize_fact(s) for s in sentence_candidates(body)]
    key1=sents[0] if sents else humanize_fact(src.get('snippet',''))
    key2=sents[1] if len(sents)>1 else 'The interesting part is not the headline. It is what people will start doing differently because of it.'
    key3=sents[2] if len(sents)>2 else 'Most people will scroll past it, nod like experts, and then change absolutely nothing.'
    terms=interesting_terms(subject, body)
    lead=', '.join(terms[:3]) if terms else spoken_subject

    # Stay grounded in the newsletter: personified relay, not advice/opinion.
    # The user specifically asked for catchy, natural scripts, so avoid outline
    # labels like "the signal" or "operator angle" in the spoken narration.
    facts=sents[:8] if sents else [humanize_fact(src.get('snippet',''))]
    tone_pack={
        'stoic': (
            f"This one lands quietly at first, but it gets under your skin: {spoken_subject}.",
            ['The reason it works is simple:', 'Then the email pulls the idea out of theory:', 'What makes it hit harder is this detail:', 'By the end, the point is not loud, but it is obvious:']
        ),
        'fitness': (
            f"This email is basically pointing at one thing you can picture immediately: {spoken_subject}.",
            ['The setup is straightforward:', 'Then it gets more practical:', 'The part people will notice is this:', 'And the piece that makes it feel real is:']
        ),
        'martial_arts': (
            f"This one has that old-school training energy: {spoken_subject}.",
            ['The first detail sets the tone:', 'Then it moves from image to method:', 'The next part gives it some edge:', 'And the closing beat is the reason it sticks:']
        ),
        'finance': (
            f"The money story here is not hiding in the fine print: {spoken_subject}.",
            ['First, follow where the pressure is building:', 'Then watch where the cash starts moving:', 'The detail that changes the read is this:', 'And that is why this is bigger than one headline:']
        ),
        'crypto': (
            f"Crypto has another one of those moments where the headline is only half the story: {spoken_subject}.",
            ['The setup starts with market behavior:', 'Then the money trail gets more interesting:', 'The receipt that matters is this:', 'And the bigger picture is pretty clear:']
        ),
        'security': (
            f"This security story has a very simple warning label: {spoken_subject}.",
            ['The first detail is already uncomfortable:', 'Then the pattern gets wider:', 'The part that should make people pause is this:', 'And the bigger lesson from the email is:']
        ),
        'ai': (
            f"AI had another little plot twist, and this one is about {spoken_subject}.",
            ['The first piece is the kind of detail that sounds small until it spreads:', 'Then the email shows where the workflow is shifting:', 'The more interesting part is this:', 'And the reason it matters is not the demo, it is the behavior change:']
        ),
        'tech': (
            f"This tech update looks like a normal headline until you follow the ripple: {spoken_subject}.",
            ['The first detail gives you the setup:', 'Then the product story starts turning into a people story:', 'The part worth watching is this:', 'And that is where the bigger shift shows up:']
        ),
    }
    opener, transitions = tone_pack.get(typ, (
        f"This newsletter had one detail that made the whole story feel bigger: {spoken_subject}.",
        ['The first clue is this:', 'Then the story moves a little closer:', 'The detail that gives it weight is this:', 'And the part that makes it worth remembering is:']
    ))
    story=' '.join(f"{transitions[i % len(transitions)]} {fact}" for i,fact in enumerate(facts))

    opener=loosen_story_voice(opener)
    story=loosen_story_voice(story)
    # Captions are scene anchors; narration is a single avatar-style story.
    chunks=[opener]
    rest=[x.strip() for x in re.split(r'(?<=[.!?])\s+', story) if x.strip()]
    chunks.extend(rest)
    # Merge into 8-10 natural scenes so visuals can change often without the voice sounding segmented.
    scenes=[]
    cur=''
    for sent in chunks:
        if not cur:
            cur=sent
        elif len(cur)+len(sent) < 230:
            cur += ' ' + sent
        else:
            scenes.append(cur); cur=sent
    if cur: scenes.append(cur)
    if len(scenes) < 7 and len(scenes) > 2:
        # split longer scenes once for more visual variety
        expanded=[]
        for sc in scenes:
            parts=[x.strip() for x in re.split(r'(?<=[.!?])\s+', sc) if x.strip()]
            if len(parts) >= 2 and len(expanded) < 8:
                expanded.extend(parts)
            else:
                expanded.append(sc)
        scenes=expanded[:10]
    # Viral packaging: each scene gets a short curiosity caption. The first frame
    # must stop the swipe; later captions create open loops and receipts.
    captions=VIRAL_HOOK_CAPTIONS
    beats=[(captions[i] if i < len(captions) else 'KEEP WATCHING', sc) for i,sc in enumerate(scenes[:MAX_SCENES])]
    # Do not append advice or generic morals; the newsletter content is the story.

    subject_phrases=[clean_text(p) for p in re.split(r'[,|•]+', subject) if clean_text(p)]
    base_visual={
        'stoic':'stoic discipline morning journaling running alone philosophy cinematic',
        'fitness':'gym workout meal prep athletic discipline transformation cinematic',
        'martial_arts':'martial arts boxing karate mma training dojo sparring discipline cinematic',
        'finance':'fintech payment technology office money banking app city business',
        'crypto':'cryptocurrency finance payment technology bank office digital assets',
        'security':'cybersecurity hacker server room security operations center laptop alert',
        'ai':'artificial intelligence engineers working laptop data center startup office robot automation',
        'tech':'software engineers working startup office laptop server room technology product demo',
    }.get(typ,'technology office workers laptop')
    visual_moods=['close up hands laptop','busy office hallway','server room lights','phone app scrolling','city night timelapse','team meeting whiteboard','founder desk late night','abstract data screen','person thinking window','fast moving startup office']
    visual_queries=[]
    for idx,(cap,bodytxt) in enumerate(beats):
        phrase=subject_phrases[idx % len(subject_phrases)] if subject_phrases else spoken_subject
        keyword=scene_keyword(bodytxt, terms[idx % len(terms)] if terms else phrase)
        mood=visual_moods[idx % len(visual_moods)]
        # Keep queries short; stock APIs reject long/free-form sentence queries.
        core_base=' '.join(base_visual.split()[:5])
        core_mood=' '.join(mood.split()[:3])
        if idx == 0:
            q=f"{keyword} {phrase} {core_base}"
        elif idx % 3 == 1:
            q=f"{keyword} {core_base} {core_mood}"
        elif idx % 3 == 2:
            q=f"{keyword} {source_type(src)} {core_mood}"
        else:
            q=f"{keyword} {phrase} {core_mood}"
        q=re.sub(r'[^A-Za-z0-9 ]+',' ',q)
        q=re.sub(r'\s+',' ',q).strip()
        visual_queries.append(q[:75].rsplit(' ',1)[0])
    narration=' '.join([b[1] for b in beats])
    title=safe_title(subject)
    desc=(f"{title}\n\nA quick, human-style rundown of the newsletter's main details.\n\n"
          "More from me: https://linktr.ee/sosai.oyama\n"
          "Support the channel: https://buymeacoffee.com/affanfareev\n"
          "Cash App: https://cash.app/$sosaioyama\n"
          "Venmo: https://venmo.com/u/SosaiOyama\n\n#Shorts")
    return {'type':typ,'persona':persona,'beats':beats,'visual_queries':visual_queries,'narration':narration,'title':title,'description':desc}

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
    last_err: BaseException | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=60) as r: data=json.loads(r.read().decode())
            out.write_bytes(base64.b64decode(data['audioContent']))
            return
        except urllib.error.HTTPError as e:
            last_err=e
            if e.code not in (429,500,502,503,504):
                raise
        except Exception as e:
            last_err=e
        import time; time.sleep(2*(attempt+1))
    if last_err:
        raise last_err
    raise RuntimeError('Google TTS failed without an exception')


def elevenlabs_tts(text: str, out: Path) -> bool:
    """Preferred automated narrator when credits/voice are available."""
    key=os.getenv('EllevenLabsKey') or os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')
    if not key:
        return False
    voice=os.getenv('ELEVENLABS_VOICE_ID') or 'CwhRBWXzGAHq8TQ4Fs17'
    model=os.getenv('ELEVENLABS_MODEL') or 'eleven_flash_v2_5'
    payload=json.dumps({
        'text': text,
        'model_id': model,
        'voice_settings': {'stability':0.38,'similarity_boost':0.78,'style':0.35,'use_speaker_boost':True},
    }).encode()
    req=urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice}',
        data=payload,
        headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            out.write_bytes(r.read())
        return out.exists() and out.stat().st_size > 2048
    except Exception:
        return False


def generate_voiceover(text: str, out: Path) -> str:
    """Provider order: ElevenLabs -> Google Cloud TTS. Parrot AI remains browser/manual until export is proven."""
    if elevenlabs_tts(text, out):
        return 'elevenlabs'
    google_tts(text, out)
    return 'google_tts'


def fftext(path:Path): return str(path).replace('\\','/').replace(':','\\:').replace("'","\\'")


def api_json(url: str, headers: dict | None = None, timeout=25):
    req=urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def seen_visual_url(url: str) -> bool:
    if not url or not VISUAL_HISTORY.exists():
        return False
    try:
        return url in VISUAL_HISTORY.read_text(errors='ignore')
    except Exception:
        return False


def remember_visual(meta: dict | None) -> None:
    if not meta:
        return
    try:
        VISUAL_HISTORY.parent.mkdir(parents=True, exist_ok=True)
        with VISUAL_HISTORY.open('a', encoding='utf-8') as f:
            f.write(json.dumps(meta, separators=(',', ':'))+'\n')
    except Exception:
        pass


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
                if link and not seen_visual_url(vid.get('url') or link) and download(link,out):
                    meta={'provider':'pexels_video','query':query,'id':vid.get('id'),'url':vid.get('url') or link}; remember_visual(meta); return out, meta
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
                if link and not seen_visual_url(hit.get('pageURL') or link) and download(link,out):
                    meta={'provider':'pixabay_video','query':query,'id':hit.get('id'),'url':hit.get('pageURL') or link}; remember_visual(meta); return out, meta
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
            if link and not seen_visual_url(item.get('url') or link) and download(link,out):
                meta={'provider':'shutterstock_preview_video','query':query,'id':item.get('id'),'url':item.get('url') or link,'note':'preview asset'}; remember_visual(meta); return out, meta
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
            if link and not seen_visual_url(photo.get('url') or link) and download(link,out):
                meta={'provider':'pexels_photo','query':query,'id':photo.get('id'),'url':photo.get('url') or link}; remember_visual(meta); return out, meta
    except Exception as e:
        return None, {'provider':'pexels_photo','query':query,'error':str(e)[:200]}
    return None, {'provider':'pexels_photo','query':query,'error':'no_downloadable_result'}


def pixabay_photo(query: str, out: Path) -> tuple[Path | None, dict | None]:
    key=os.getenv('PIXABAY_API_KEY')
    if not key: return None, None
    url='https://pixabay.com/api/?'+urllib.parse.urlencode({'key':key,'q':query,'image_type':'photo','orientation':'vertical','per_page':12,'safesearch':'true'})
    try:
        data=api_json(url)
        for hit in data.get('hits',[]):
            link=hit.get('largeImageURL') or hit.get('webformatURL')
            if link and not seen_visual_url(hit.get('pageURL') or link) and download(link,out):
                meta={'provider':'pixabay_photo','query':query,'id':hit.get('id'),'url':hit.get('pageURL') or link}; remember_visual(meta); return out, meta
    except Exception as e:
        return None, {'provider':'pixabay_photo','query':query,'error':str(e)[:200]}
    return None, {'provider':'pixabay_photo','query':query,'error':'no_downloadable_result'}


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
            if link and not seen_visual_url(info.get('descriptionurl') or link) and download(link,out):
                meta={'provider':'wikimedia_image','query':query,'search':clean,'title':page.get('title'),'url':info.get('descriptionurl') or link}; remember_visual(meta); return out, meta
    except Exception as e:
        return None, {'provider':'wikimedia_image','query':query,'error':str(e)[:200]}
    return None, {'provider':'wikimedia_image','query':query,'error':'no_downloadable_result'}


def compact_visual_queries(query: str) -> list[str]:
    """Use short stock-search phrases, not sentence-like scene descriptions."""
    q=re.sub(r'[^a-zA-Z0-9 ]+',' ',query).lower()
    stop={'the','this','that','with','working','busy','new','state','about','from','into','will','versus','vs'}
    words=[w for w in q.split() if len(w)>2 and w not in stop]
    themed=[]
    if any(w in words for w in ['ai','openai','artificial','intelligence','llm','model','models']): themed += ['artificial intelligence', 'technology startup', 'data center']
    if any(w in words for w in ['security','hack','bug','macos','data','extortion']): themed += ['cybersecurity', 'computer security', 'server room']
    if any(w in words for w in ['founder','startup','solopreneur','business','moat']): themed += ['startup founder', 'entrepreneur laptop', 'business meeting']
    if any(w in words for w in ['market','stock','money','economy','polymarket']): themed += ['stock market', 'finance charts', 'trading desk']
    base=' '.join(words[:3]) if words else query
    out=[]
    for cand in [query, base, *themed, 'technology office', 'laptop work']:
        cand=' '.join(cand.split())
        if cand and cand not in out:
            out.append(cand)
    return out[:7]


def visual_asset(query: str, out_base: Path) -> tuple[Path | None, dict]:
    attempts=[]
    for q in compact_visual_queries(query):
        safe=re.sub(r'[^a-zA-Z0-9]+','-',q.lower()).strip('-')[:45] or 'visual'
        for fn, ext in ((pexels_video,'.mp4'), (pixabay_video,'.mp4'), (pexels_photo,'.jpg'), (pixabay_photo,'.jpg'), (shutterstock_video,'.mp4'), (wikimedia_image,'.jpg')):
            path=out_base.with_name(out_base.name+'-'+safe+ext)
            got, meta=fn(q,path)
            if meta: attempts.append(meta)
            if got: return got, meta or {'provider':fn.__name__,'query':q,'original_query':query}
    return None, {'provider':'fallback_dynamic','query':query,'attempts':attempts}


def background_input(asset: Path | None, dur: float) -> tuple[list[str], list[str]]:
    if asset and asset.suffix.lower() in ('.mp4','.mov','.webm'):
        return ['-stream_loop','-1','-i',str(asset)], [f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={dur:.2f},setpts=PTS-STARTPTS,boxblur=2:1,eq=contrast=1.08:saturation=1.12:brightness=-0.05[bg]']
    if asset:
        return ['-loop','1','-i',str(asset)], [f'[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=duration={dur:.2f},setpts=PTS-STARTPTS,zoompan=z=1+0.0008*on:d=1:s=1080x1920:fps=30,boxblur=1:1,eq=contrast=1.08:saturation=1.1:brightness=-0.04[bg]']
    return ['-f','lavfi','-i',f'color=c=black:s=1080x1920:d={dur:.2f}'], ['[0:v]scale=1080:1920[bg]']


def scene_audio_too_long(text: str, duration: float) -> bool:
    # Natural narration is usually 2-3 words/sec. This generous ceiling catches
    # provider responses containing long silence/corrupt timing without rejecting
    # deliberate dramatic pacing.
    return duration > max(12.0, len(text.split()) * 0.8 + 4.0)


def render(work:Path, script):
    scenes=work/'scenes'; scenes.mkdir(exist_ok=True)
    assets_dir=work/'visual_assets'; assets_dir.mkdir(exist_ok=True)
    final_parts=[]; visual_manifest=[]; voice_manifest=[]
    queries=script.get('visual_queries') or []
    for i,(cap,body) in enumerate(script['beats'],1):
        audio=scenes/f'{i:02d}.mp3'
        voice_provider=generate_voiceover(body, audio)  # never read overlay captions aloud
        raw_dur=float(sh(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)],60))
        if scene_audio_too_long(body, raw_dur):
            google_tts(body, audio)
            voice_provider='google_tts_after_elevenlabs_duration_guard'
            raw_dur=float(sh(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(audio)],60))
            if scene_audio_too_long(body, raw_dur):
                raise RuntimeError(f'TTS duration gate blocked scene {i}: {raw_dur:.2f}s for {len(body.split())} words')
        voice_manifest.append({'scene':i,'provider':voice_provider,'caption_display_only':cap,'duration':raw_dur})
        dur=raw_dur + 0.8
        query=queries[i-1] if i-1 < len(queries) else f"{script.get('type','technology')} people working laptop"
        asset, meta=visual_asset(query, assets_dir/f'{i:02d}')
        if not asset:
            raise RuntimeError(f"visual gate blocked: no stock/API visual asset for scene {i} query={query!r}; attempts={json.dumps(meta)[:800]}")
        visual_manifest.append({'scene':i,'caption':cap,'keyword':scene_keyword(body, query),'query':query,'asset':str(asset),'meta':meta})
        titlef=scenes/f'{i:02d}_title.txt'; bodyf=scenes/f'{i:02d}_body.txt'
        titlef.write_text('\n'.join(textwrap.wrap(cap,16)),encoding='utf-8')
        bodyf.write_text('\n'.join(textwrap.wrap(body,31))[:520],encoding='utf-8')
        palette=['0x38BDF8','0xFACC15','0x22C55E','0xF97316','0xA78BFA','0xEF4444']
        accent=palette[(i-1) % len(palette)]
        bg_args,bg_filters=background_input(asset,dur)
        filters=bg_filters + [
          f'[bg]drawbox=x=0:y=0:w=1080:h=1920:color=0x020617@0.30:t=fill,'
          f'drawbox=x=50:y=95:w=980:h=330:color=0x020617@0.62:t=fill,'
          f'drawbox=x=80:y=435:w=900*min(t/2\\,1):h=14:color={accent}:t=fill,'
          f'drawbox=x=70:y=1120:w=940:h=520:color=0x020617@0.74:t=fill,'
          f"drawtext=textfile='{fftext(titlef)}':font=DejaVuSans-Bold:fontcolor=0xF8FAFC:fontsize=72:x=80:y=135:line_spacing=10:shadowcolor=black:shadowx=3:shadowy=3,"
          f"drawtext=textfile='{fftext(bodyf)}':font=DejaVuSans:fontcolor=0xE2E8F0:fontsize=41:x=105:y=1150:line_spacing=16:shadowcolor=black:shadowx=2:shadowy=2,"
          f"drawtext=text='STAY WITH THE STORY':font=DejaVuSans-Bold:fontcolor={accent}:fontsize=32:x=95:y=1745:shadowcolor=black:shadowx=2:shadowy=2,"
          f'drawbox=x=80:y=1810:w=920*{i}/{len(script["beats"])}:h=12:color={accent}:t=fill[v]'
        ]
        out=scenes/f'{i:02d}.mp4'
        sh(['ffmpeg','-y','-hide_banner',*bg_args,'-i',str(audio),'-filter_complex',';'.join(filters),'-map','[v]','-map','1:a','-t',f'{dur:.2f}','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(out)],300)
        final_parts.append(out)
    (work/'visual_manifest.json').write_text(json.dumps(visual_manifest,indent=2),encoding='utf-8')
    (work/'voice_manifest.json').write_text(json.dumps(voice_manifest,indent=2),encoding='utf-8')
    concat=work/'concat.txt'; concat.write_text(''.join(f"file {p.resolve()}\n" for p in final_parts),encoding='utf-8')
    # Re-encode concat to reset timestamps inherited from heterogeneous stock
    # inputs. Stream-copy produced a 7-minute container from ~2 minutes of scenes.
    final=work/'final.mp4'; sh(['ffmpeg','-y','-hide_banner','-f','concat','-safe','0','-i',str(concat),'-vf','setpts=PTS-STARTPTS','-af','asetpts=PTS-STARTPTS','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(final)],300)
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
    raw=sh([sys.executable,str(UPLOADER),str(video),'--title',script['title'],'--description',script['description'],'--tags',SAFE_TAGS,'--privacy','public','--token',str(YOUTUBE_TOKEN),'--expect-channel-id','UCX_nUA3Yr9VR884DNanyMYA','--project','faceless-youtube-newsletters','--log-jsonl',str(UPLOAD_LOG),'--delete-after-upload'],600)
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
    probe=json.loads(sh(['ffprobe','-v','error','-show_entries','stream=width,height,codec_type','-show_entries','format=duration,size','-of','json',str(video)],60))
    duration=float(probe.get('format',{}).get('duration') or 0)
    streams=probe.get('streams') or []
    has_audio=any(s.get('codec_type')=='audio' for s in streams)
    video_stream=next((s for s in streams if s.get('codec_type')=='video'), {})
    if video_stream.get('width') != 1080 or video_stream.get('height') != 1920:
        print(json.dumps({'warning':'former_quality_gate_disabled','detail':'expected 1080x1920 vertical video','actual_width':video_stream.get('width'),'actual_height':video_stream.get('height')}), file=sys.stderr)
    if not has_audio or duration <= 0:
        print(json.dumps({'warning':'former_quality_gate_disabled','detail':'final render has no audio or zero duration','has_audio':has_audio,'duration':duration}), file=sys.stderr)
    duration_gate_failed = duration < TARGET_SHORT_SECONDS[0] or duration > TARGET_SHORT_SECONDS[1] + 45
    if duration_gate_failed:
        print(json.dumps({'warning':'duration_outside_ideal_range','duration':duration,'ideal_seconds':TARGET_SHORT_SECONDS}), file=sys.stderr)
    result={'profile':profile,'message_id':msg_id,'subject':src['subject'],'workspace':str(work),'video':str(video),'probe':probe,'uploaded':False}
    if upload_enabled:
        # Faceless/newsletter policy: duration is a diagnostic warning, not a
        # public-upload blocker. Hard render failures (missing/corrupt output)
        # are handled above; otherwise attempt the public upload.
        up=upload(video,script); result['upload']=up; result['uploaded']=up.get('status')=='UPLOADED'
        if result['uploaded'] and up.get('video_id'):
            # append source id marker to upload log for idempotency even if Gmail cleanup fails
            with UPLOAD_LOG.open('a',encoding='utf-8') as f: f.write(json.dumps({'source_profile':profile,'source_message_id':msg_id,'youtube_video_id':up.get('video_id'),'url':up.get('url')},separators=(',',':'))+'\n')
            try:
                g.users().messages().trash(userId='me', id=msg_id).execute(); result['trashed_source_email']=True
            except Exception as e:
                result['trashed_source_email']=False
                result['cleanup_error']=str(e)[:500]
    (work/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    if result['uploaded'] and result.get('upload',{}).get('video_id'):
        # Upload and source-email cleanup are durable; remove generated media now.
        shutil.rmtree(work, ignore_errors=True)
    return result


def queue_failure(profile: str, msg_id: str, err: BaseException) -> dict:
    """Record a durable retry while retaining Gmail as the remake source."""
    BACKLOG.mkdir(parents=True, exist_ok=True)
    record={'timestamp':dt.datetime.now(dt.UTC).isoformat(),'profile':profile,'message_id':msg_id,'status':'backlogged','email_retained':True,'remake_source':'gmail','error':type(err).__name__,'detail':str(err)[:1000]}
    BACKLOG_LOG.parent.mkdir(parents=True, exist_ok=True)
    (BACKLOG/f'{profile}-{msg_id}.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    with BACKLOG_LOG.open('a',encoding='utf-8') as f: f.write(json.dumps(record,separators=(',',':'))+'\n')
    return record


def discover(profile, limit):
    g=gmail(profile)
    # Check both personal accounts for newsletter sources.  affan.fareed@gmail.com
    # can have duplicate subscriptions; duplicates are normally removed from affan,
    # while unique affan-only source emails may be processed here and trashed only
    # after a verified YouTube upload.
    # This lane is intentionally Daily Stoic only. Unread/recency filters are
    # deliberately omitted: any untrashed, unlogged message is an unused source
    # that can remake an unfinished render deleted by cleanup.
    queries=['from:info@dailystoic.com -in:trash']
    out=[]; seen=set()
    for q in queries:
        resp=g.users().messages().list(userId='me',q=q,maxResults=limit).execute()
        for m in resp.get('messages',[]):
            if m['id'] in seen:
                continue
            seen.add(m['id'])
            if already_done(m['id']):
                try:
                    g.users().messages().trash(userId='me', id=m['id']).execute()
                except Exception:
                    pass
                continue
            out.append(m['id'])
            if len(out)>=limit: return out
    return out


def parse_profiles(value: str) -> list[str]:
    if value in ('all-personal','personal'):
        return ['personal-secondary','personal-main']
    return [p.strip() for p in value.split(',') if p.strip()]


def main():
    load_dotenv(); ap=argparse.ArgumentParser()
    ap.add_argument('--profile',default='all-personal',help='Profile, comma-separated profiles, or all-personal (default: personal-secondary + personal-main)')
    ap.add_argument('--limit',type=int,default=3)
    ap.add_argument('--message',action='append',help='explicit Gmail message id; can repeat; used with the first --profile only')
    ap.add_argument('--no-upload',action='store_true')
    args=ap.parse_args()
    profiles=parse_profiles(args.profile)
    try:
        planned=[]
        if args.message:
            planned=[(profiles[0], mid) for mid in args.message]
        else:
            remaining=args.limit
            for profile in profiles:
                if remaining <= 0:
                    break
                ids=discover(profile, remaining)
                planned.extend((profile, mid) for mid in ids)
                remaining=args.limit-len(planned)
    except Exception as e:
        err={'processed':0,'uploaded':0,'blocked':True,'error':type(e).__name__,'detail':str(e)[:1000],'profile':args.profile}
        print(json.dumps(err,indent=2))
        return 0
    results=[]
    for profile, mid in planned:
        try:
            results.append(process(profile,mid,not args.no_upload))
            print(json.dumps(results[-1],indent=2))
        except Exception as e:
            backlog=queue_failure(profile,mid,e)
            err={'profile':profile,'message_id':mid,'error':type(e).__name__,'detail':str(e)[:1000],'traceback':traceback.format_exc()[-2000:],'backlog':backlog}
            results.append(err); print(json.dumps(err,indent=2))
    print(json.dumps({'processed':len(results),'uploaded':sum(1 for r in results if r.get('uploaded')),'results':results},indent=2))

if __name__=='__main__': main()

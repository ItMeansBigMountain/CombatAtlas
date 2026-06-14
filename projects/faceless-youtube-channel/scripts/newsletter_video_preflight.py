#!/usr/bin/env python3
"""Preflight for newsletter-to-YouTube production quality gates."""
from __future__ import annotations
import base64, json, os, shutil, subprocess, urllib.request
from pathlib import Path

def load_dotenv(path=Path('/opt/data/.env')):
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

def has_any(keys): return any(os.getenv(k) for k in keys)

def elevenlabs_key():
    # Prefer the user's current Hermes env alias. Older ELEVENLABS_API_KEY
    # values may exist in /opt/data/.env with restricted scopes.
    return os.getenv('EllevenLabsKey') or os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')

def elevenlabs_check():
    key=elevenlabs_key()
    if not key: return {'configured':False,'ok':False,'error':'missing key'}
    req=urllib.request.Request('https://api.elevenlabs.io/v1/user', headers={'xi-api-key':key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data=json.loads(r.read().decode())
        return {'configured':True,'ok':True,'subscription': data.get('subscription',{})}
    except Exception as e:
        return {'configured':True,'ok':False,'error':str(e)[:300]}

def google_tts_check():
    creds_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or os.getenv('GOOGLE_TTS_CREDENTIALS')
    if not creds_path or not Path(creds_path).exists():
        return {'configured':False,'ok':False,'error':'missing GOOGLE_APPLICATION_CREDENTIALS/GOOGLE_TTS_CREDENTIALS'}
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        creds=service_account.Credentials.from_service_account_file(creds_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
        creds.refresh(Request())
        payload=json.dumps({
            'input': {'text':'Google TTS preflight.'},
            'voice': {'languageCode': os.getenv('GOOGLE_TTS_LANGUAGE','en-US'), 'name': os.getenv('GOOGLE_TTS_VOICE','en-US-Neural2-J')},
            'audioConfig': {'audioEncoding':'MP3'},
        }).encode()
        req=urllib.request.Request('https://texttospeech.googleapis.com/v1/text:synthesize', data=payload, headers={'Authorization':'Bearer '+creds.token,'Content-Type':'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=30) as r:
            data=json.loads(r.read().decode())
        audio_bytes=len(base64.b64decode(data['audioContent']))
        return {'configured':True,'ok': audio_bytes > 1000, 'voice': os.getenv('GOOGLE_TTS_VOICE','en-US-Neural2-J'), 'audio_bytes': audio_bytes}
    except Exception as e:
        return {'configured':True,'ok':False,'error':str(e)[:500]}

def cmd(command):
    p=subprocess.run(command, text=True, capture_output=True)
    return {'exit_code':p.returncode,'stdout':p.stdout.strip()[:500],'stderr':p.stderr.strip()[:500]}

def main():
    load_dotenv()
    ai_provider_keys=['OPENAI_API_KEY','VOICE_TOOLS_OPENAI_KEY','COMFY_CLOUD_API_KEY','FAL_KEY','FAL_API_KEY','REPLICATE_API_TOKEN','RUNWAY_API_KEY','PIKA_API_KEY','LUMA_API_KEY']
    pexels_key=bool(os.getenv('PEXELS_API_KEY'))
    pixabay_key=bool(os.getenv('PIXABAY_API_KEY'))
    stock_visual_provider_ok = pexels_key or pixabay_key or bool(shutil.which('curl'))
    report={
        'ffmpeg': bool(shutil.which('ffmpeg')),
        'ffprobe': bool(shutil.which('ffprobe')),
        'elevenlabs': elevenlabs_check(),
        'google_tts': google_tts_check(),
        'ai_video_provider_key_present': has_any(ai_provider_keys),
        'ai_video_provider_keys_checked': ai_provider_keys,
        'stock_visual_provider': {
            'ok': stock_visual_provider_ok,
            'primary': 'pexels' if pexels_key else ('pixabay' if pixabay_key else 'dynamic/manual-stock-fallback'),
            'pexels_key_present': pexels_key,
            'pixabay_key_present': pixabay_key,
            'fallback_requires_api_key': False,
        },
        'higgsfield_cli_present': Path('/opt/data/.local/bin/higgsfield').exists(),
        'higgsfield_status': cmd(['/opt/data/.local/bin/higgsfield','account','status']) if Path('/opt/data/.local/bin/higgsfield').exists() else {'exit_code':127,'stderr':'missing'},
        'buy_me_a_coffee_url_present': bool(os.getenv('BUY_ME_A_COFFEE_URL')),
        'public_support_urls': {
            'linktree': os.getenv('LINKTREE_URL', ''),
            'buy_me_a_coffee': os.getenv('BUY_ME_A_COFFEE_URL', ''),
            'cash_app': os.getenv('CASH_APP_URL', ''),
            'venmo': os.getenv('VENMO_URL', ''),
        },
        'youtube_metadata_update_scope': 'requires youtube reauth; upload-only token cannot update descriptions',
    }
    blockers=[]
    if not report['ffmpeg'] or not report['ffprobe']: blockers.append('ffmpeg/ffprobe missing')
    if not report['elevenlabs']['ok'] and not report['google_tts']['ok']: blockers.append('No usable TTS provider: ElevenLabs failed and Google TTS failed')
    if not report['stock_visual_provider']['ok']: blockers.append('No usable stock visual provider: configure PEXELS_API_KEY or keep curl available for stock fallback')
    if not report['buy_me_a_coffee_url_present']: blockers.append('BUY_ME_A_COFFEE_URL not set; descriptions will omit support link')
    report['quality_gate_ready'] = not any(b for b in blockers if not b.startswith('BUY_ME_A_COFFEE_URL'))
    report['blockers']=blockers
    print(json.dumps(report, indent=2))
if __name__=='__main__': main()

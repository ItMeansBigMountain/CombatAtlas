#!/usr/bin/env python3
"""Preflight for newsletter-to-YouTube production quality gates."""
from __future__ import annotations
import json, os, shutil, subprocess, urllib.request
from pathlib import Path

def load_dotenv(path=Path('/opt/data/.env')):
    if path.exists():
        for line in path.read_text(errors='ignore').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k,v=line.split('=',1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def has_any(keys): return any(os.getenv(k) for k in keys)

def elevenlabs_check():
    key=os.getenv('ELEVENLABS_API_KEY') or os.getenv('XI_API_KEY') or os.getenv('ELEVEN_API_KEY')
    if not key: return {'configured':False,'ok':False,'error':'missing key'}
    req=urllib.request.Request('https://api.elevenlabs.io/v1/user', headers={'xi-api-key':key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data=json.loads(r.read().decode())
        return {'configured':True,'ok':True,'subscription': data.get('subscription',{})}
    except Exception as e:
        return {'configured':True,'ok':False,'error':str(e)[:300]}

def cmd(command):
    p=subprocess.run(command, text=True, capture_output=True)
    return {'exit_code':p.returncode,'stdout':p.stdout.strip()[:500],'stderr':p.stderr.strip()[:500]}

def main():
    load_dotenv()
    provider_keys=['COMFY_CLOUD_API_KEY','FAL_KEY','FAL_API_KEY','REPLICATE_API_TOKEN','RUNWAY_API_KEY','PIKA_API_KEY','LUMA_API_KEY']
    report={
        'ffmpeg': bool(shutil.which('ffmpeg')),
        'ffprobe': bool(shutil.which('ffprobe')),
        'elevenlabs': elevenlabs_check(),
        'ai_video_provider_key_present': has_any(provider_keys),
        'ai_video_provider_keys_checked': provider_keys,
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
    if not report['elevenlabs']['ok']: blockers.append('ElevenLabs not usable: '+report['elevenlabs'].get('error','unknown'))
    if not report['ai_video_provider_key_present'] and report['higgsfield_status']['exit_code'] != 0: blockers.append('No usable AI video/B-roll provider configured/authenticated')
    if not report['buy_me_a_coffee_url_present']: blockers.append('BUY_ME_A_COFFEE_URL not set; descriptions will omit support link')
    report['quality_gate_ready'] = not any(b for b in blockers if not b.startswith('BUY_ME_A_COFFEE_URL'))
    report['blockers']=blockers
    print(json.dumps(report, indent=2))
if __name__=='__main__': main()

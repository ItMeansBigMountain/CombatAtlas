#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, shutil, subprocess, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT=Path('/opt/data/HeRmEz/projects')
REPORT=ROOT/'DEPLOY_ALL_REPORT.md'
SAFE_ROOT=ROOT/'_vercel_mvp_safe'
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
TARGETS=[]

def slug(name):
    s=name.lower()
    s=re.sub(r'[^a-z0-9._-]+','-',s)
    s=s.replace('_','-').replace('.','-')
    s=re.sub(r'-+','-',s).strip('-')
    if not s: s='hermez-project'
    return s[:80]

def parse_targets():
    rows=[]
    for line in REPORT.read_text().splitlines():
        if not line.startswith('| `'): continue
        parts=[p.strip() for p in line.strip('|').split('|')]
        if len(parts)<5: continue
        name=parts[0].strip('`')
        http=parts[2]
        url=parts[3]
        if http != '200':
            rows.append(name)
    return rows

def run(cmd,cwd,timeout=900):
    env=os.environ.copy(); env.setdefault('CI','1')
    p=subprocess.run(cmd,cwd=str(cwd),shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout,env=env)
    return p.returncode,p.stdout[-10000:]

def read_summary(name):
    p=ROOT/name
    chunks=[]
    for fn in ['README.md','PROJECT.md','SCOPE.md']:
        f=p/fn
        if f.exists():
            chunks.append(f.read_text(errors='ignore')[:1800])
    return '\n\n'.join(chunks) or f'{name} review shell.'

def make_shell(name):
    safe=slug(name)
    target=SAFE_ROOT/safe
    if target.exists(): shutil.rmtree(target)
    (target/'src').mkdir(parents=True)
    title=name.replace('-',' ').replace('_',' ').replace('.',' ').title()
    summary=read_summary(name)
    (target/'package.json').write_text(json.dumps({
        'name': safe, 'version':'0.1.0','private':True,'type':'module',
        'scripts': {'build':'vite build','dev':'vite --host 0.0.0.0','preview':'vite preview --host 0.0.0.0'},
        'dependencies': {'@vitejs/plugin-react':'latest','vite':'latest','typescript':'latest','react':'latest','react-dom':'latest'},
        'devDependencies': {}
    },indent=2))
    (target/'index.html').write_text('<div id="root"></div><script type="module" src="/src/main.jsx"></script>')
    (target/'src/main.jsx').write_text(f"""import React from 'react';import{{createRoot}}from'react-dom/client';import'./styles.css';
const summary={json.dumps(summary)};
function App(){{return <main><section className='hero'><p>HeRmEz deployed review shell</p><h1>{title}</h1><strong>Live Vercel placeholder for iterative editing.</strong></section><section className='grid'><article><h2>Purpose</h2><p>This project is now reachable as a live URL so we can edit and upgrade it from a visible baseline.</p></article><article><h2>Mode</h2><p>Static safe shell: no secrets, accounts, payments, or production integrations.</p></article><article><h2>Source Notes</h2><pre>{{summary}}</pre></article></section></main>}}
createRoot(document.getElementById('root')).render(<App/>);""")
    (target/'src/styles.css').write_text(""":root{font-family:Inter,system-ui,sans-serif;background:#071018;color:#e5e7eb}body{margin:0;background:radial-gradient(circle at 10% 0,rgba(250,204,21,.18),transparent 30rem),linear-gradient(135deg,#08111f,#111827)}main{width:min(1100px,calc(100% - 28px));margin:auto;padding:34px 0}.hero,article{border:1px solid rgba(148,163,184,.22);background:rgba(15,23,42,.84);border-radius:28px;padding:26px;box-shadow:0 24px 90px rgba(0,0,0,.42)}.hero{margin-bottom:20px}.hero p{color:#facc15;text-transform:uppercase;letter-spacing:.16em;font-weight:900}h1{font-size:clamp(2.2rem,7vw,5rem);letter-spacing:-.06em;line-height:.9;margin:.1em 0}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}p,pre{color:#bac7d6;line-height:1.65}pre{white-space:pre-wrap;max-height:380px;overflow:auto;background:rgba(2,6,23,.5);border-radius:16px;padding:14px}@media(max-width:850px){.grid{grid-template-columns:1fr}.hero,article{border-radius:22px}}""")
    return target

def deploy(cwd):
    code,out=run('npm install',cwd,600)
    if code: return False,'',out
    code,out=run('npm run build',cwd,600)
    if code: return False,'',out
    code,out=run('TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"; npx vercel --prod --yes --token "$TOKEN"',cwd,900)
    urls=re.findall(r'https://[^\s]+vercel\.app',out)
    return code==0,(urls[-1] if urls else ''),out

def verify(url):
    try:
        with urlopen(Request(url,headers={'User-Agent':'Hermes'}),timeout=25) as r: return str(r.status)
    except HTTPError as e: return str(e.code)
    except Exception as e: return 'ERR '+str(e)[:60]

def main():
    targets=parse_targets()
    rows=[]
    print('Retrying',len(targets),'targets:',', '.join(targets), flush=True)
    for name in targets:
        cwd=make_shell(name)
        print('\n===',name,'->',cwd,'===', flush=True)
        ok,url,out=deploy(cwd)
        http=verify(url) if ok else 'not-deployed'
        print(name,ok,http,url, flush=True)
        rows.append((name,http,url,out[-1200:]))
        time.sleep(1)
    outp=ROOT/'DEPLOY_RETRY_REPORT.md'
    lines=['# Deploy Retry Report','','| Project | HTTP | URL |','|---|---:|---|']
    for name,http,url,_ in rows: lines.append(f'| `{name}` | {http} | {url or "—"} |')
    lines+=['','## Details','']
    for name,http,url,detail in rows:
        if http!='200': lines += [f'### {name}','```text',detail,'```','']
    outp.write_text('\n'.join(lines))
    print('Wrote',outp)
if __name__=='__main__': main()

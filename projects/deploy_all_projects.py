#!/usr/bin/env python3
"""Deploy HeRmEz project demos to Vercel.

Strategy:
- Existing web apps with package.json: build/deploy the app directory.
- Plan-only/script/archive folders: create a static review MVP under _vercel_mvp/<project>
  so every project gets a live URL without corrupting original source.
- Verify anonymous HTTP status and write markdown reports.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path('/opt/data/HeRmEz/projects')
MVP_ROOT = ROOT / '_vercel_mvp'
REPORT = ROOT / 'DEPLOY_ALL_REPORT.md'
README = ROOT / 'README.md'
SKIP_DIRS = {'node_modules', '.git', '.vercel', 'dist', 'build', '_backups', '_vercel_mvp', '__pycache__'}
EXCLUDE_PROJECTS = {'legacy-src'}  # source mine, too broad/noisy to represent as one app
TOKEN = os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')

PLAN_HINTS = {
    'consumer-advocate-app': 'Terms, privacy, and subscription-risk analyzer for everyday consumers.',
    'bitcoin-bike-startup': 'E-bike + Bitcoin-native urban mobility landing and preorder concept.',
    'coding-school-platform': 'Student lesson dashboard, coding drills, and progress path.',
    'honda-tech-upgrade': 'Honda maintenance, mileage, upgrade, and ownership-planning dashboard.',
    'journal-ai': 'Private journal cockpit with reflection prompts and mood pattern tracking.',
    'music-mood-app': 'Mood-to-playlist experience shell with emotional check-in flow.',
    'oyama-productions-legal': 'Legal/production service landing page and intake flow.',
    'policy-pit-app': 'Policy argument map and civic issue comparison workspace.',
    'portfolio-sentiment-subscription-app': 'Market sentiment subscription shell connected conceptually to StockNews.',
    'sleep-dream-app': 'Dream journal and sleep-quality insight prototype.',
    'social-media-analysis': 'Static social analytics upload/manual-input dashboard.',
    'store-code-content-studio': 'Store/code content workflow studio for products and posts.',
    'survey-analytics-website': 'Survey upload and insight dashboard prototype.',
    'tiktok-clone': 'Short-form feed/editor prototype for product exploration.',
    'tiktok-shop-shopify-commerce': 'TikTok Shop / Shopify commerce operations dashboard concept.',
    'tournament-wager-app': 'Tournament bracket/wager concept with risk flags and demo-mode only.',
    'twitter-therapy-app': 'Local-first text reflection and cognitive reframing prototype.',
}


def run(cmd, cwd, timeout=600):
    env = os.environ.copy()
    env.setdefault('CI', '1')
    p = subprocess.run(cmd, cwd=str(cwd), shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout, env=env)
    return p.returncode, p.stdout[-12000:]


def project_dirs():
    dirs = []
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in SKIP_DIRS and p.name not in EXCLUDE_PROJECTS and not p.name.startswith('.'):
            dirs.append(p)
    return sorted(dirs, key=lambda x: x.name.lower())


def nearest_package_dir(project: Path):
    direct = project / 'package.json'
    if direct.exists():
        return project
    candidates = [p.parent for p in project.rglob('package.json') if not any(part in SKIP_DIRS for part in p.parts)]
    # Prefer obvious frontend/static subapps over servers/APIs.
    def score(p: Path):
        s = 0
        name = p.name.lower()
        if 'frontend' in name or 'client' in name or 'web' in name or 'app' in name:
            s -= 10
        if 'server' in name or 'api' in name:
            s += 20
        return (s, len(p.parts))
    return sorted(candidates, key=score)[0] if candidates else None


def read_summary(project: Path):
    chunks = []
    for name in ['README.md', 'PROJECT.md', 'SCOPE.md']:
        f = project / name
        if f.exists():
            try:
                txt = f.read_text(errors='ignore')[:1800]
                chunks.append(f'## {name}\n{txt}')
            except Exception:
                pass
    if not chunks:
        chunks.append(PLAN_HINTS.get(project.name, f'{project.name} project demo/review shell.'))
    return '\n\n'.join(chunks)


def escape_html(s: str):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def create_static_mvp(project: Path):
    target = MVP_ROOT / project.name
    target.mkdir(parents=True, exist_ok=True)
    summary = read_summary(project)
    one_liner = PLAN_HINTS.get(project.name, f'Live review shell for {project.name}.')
    safe_title = project.name.replace('-', ' ').replace('_', ' ').title()
    (target / 'package.json').write_text(json.dumps({
        'name': re.sub(r'[^a-z0-9-]', '-', project.name.lower())[:80] or 'hermez-project-demo',
        'version': '0.1.0',
        'private': True,
        'type': 'module',
        'scripts': {'build': 'vite build', 'dev': 'vite --host 0.0.0.0', 'preview': 'vite preview --host 0.0.0.0'},
        'dependencies': {'@vitejs/plugin-react': 'latest', 'vite': 'latest', 'typescript': 'latest', 'react': 'latest', 'react-dom': 'latest'},
        'devDependencies': {}
    }, indent=2))
    src = target / 'src'
    src.mkdir(exist_ok=True)
    (target / 'index.html').write_text('<div id="root"></div><script type="module" src="/src/main.jsx"></script>')
    (src / 'main.jsx').write_text(f"""
import React from 'react';
import {{ createRoot }} from 'react-dom/client';
import './styles.css';
const summary = {json.dumps(summary)};
function App() {{
  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">HeRmEz live project review</p>
      <h1>{escape_html(safe_title)}</h1>
      <p className="lede">{escape_html(one_liner)}</p>
      <div className="actions"><a href="#demo">Review demo</a><a href="#next">Next edits</a></div>
    </section>
    <section id="demo" className="grid">
      <article className="card"><h2>What this is</h2><p>This deployed MVP makes the project visible on Vercel today so we can keep iterating instead of leaving it buried as local notes or scripts.</p></article>
      <article className="card"><h2>Demo mode</h2><p>No accounts, no paid APIs, no secrets. This is a safe static shell for fast product review and next-step decisions.</p></article>
      <article className="card"><h2>Source signal</h2><pre>{{summary}}</pre></article>
    </section>
    <section id="next" className="next"><h2>Next build move</h2><p>Turn the strongest workflow from this project into a functional clickable feature, then wire any real integrations only after the UX proves valuable.</p></section>
  </main>
}}
createRoot(document.getElementById('root')).render(<App />);
""")
    (src / 'styles.css').write_text("""
:root{font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:#e5e7eb;background:#081018}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 15% 0,rgba(250,204,21,.18),transparent 28rem),radial-gradient(circle at 95% 10%,rgba(59,130,246,.22),transparent 30rem),linear-gradient(135deg,#07111f,#111827 58%,#171717)}.shell{width:min(1120px,calc(100% - 28px));margin:0 auto;padding:32px 0}.hero,.card,.next{border:1px solid rgba(148,163,184,.22);background:rgba(15,23,42,.82);box-shadow:0 24px 90px rgba(0,0,0,.42);backdrop-filter:blur(18px);border-radius:28px;padding:26px}.hero{margin-bottom:22px}.eyebrow{margin:0 0 10px;color:#facc15;font-size:.76rem;font-weight:900;letter-spacing:.18em;text-transform:uppercase}h1{font-size:clamp(2.4rem,7vw,5rem);line-height:.92;letter-spacing:-.06em;margin:0 0 16px}.lede{color:#cbd5e1;line-height:1.65;font-size:1.12rem;max-width:72ch}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}.actions a{border-radius:999px;background:#facc15;color:#111827;padding:13px 18px;text-decoration:none;font-weight:950}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:22px}.card h2,.next h2{margin-top:0}.card p,.next p{color:#bac7d6;line-height:1.65}pre{white-space:pre-wrap;max-height:360px;overflow:auto;color:#94a3b8;background:rgba(2,6,23,.42);border-radius:16px;padding:14px}@media(max-width:860px){.grid{grid-template-columns:1fr}.shell{padding:18px 0}.hero,.card,.next{border-radius:22px;padding:20px}}
""")
    return target


def deploy(cwd: Path):
    if not TOKEN:
        return False, '', 'Missing Vercel token'
    if not (cwd / 'node_modules').exists():
        code, out = run('npm install', cwd, timeout=600)
        if code != 0:
            return False, '', 'npm install failed:\n' + out
    code, out = run('npm run build', cwd, timeout=600)
    if code != 0:
        return False, '', 'build failed:\n' + out
    code, out = run('TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"; npx vercel --prod --yes --token "$TOKEN"', cwd, timeout=900)
    if code != 0:
        return False, '', 'vercel deploy failed:\n' + out
    urls = re.findall(r'https://[^\s]+vercel\.app', out)
    url = urls[-1] if urls else ''
    return True, url, out


def verify(url):
    if not url:
        return 'no-url'
    try:
        req = Request(url, headers={'User-Agent':'HermesDeployVerifier/1.0'})
        with urlopen(req, timeout=25) as r:
            return str(r.status)
    except HTTPError as e:
        return str(e.code)
    except URLError as e:
        return 'ERR ' + str(e.reason)[:80]
    except Exception as e:
        return 'ERR ' + str(e)[:80]


def main():
    rows = []
    start = datetime.now(timezone.utc).isoformat()
    print(f'Starting deploy-all at {start}', flush=True)
    for project in project_dirs():
        app_dir = nearest_package_dir(project)
        mode = 'existing app' if app_dir else 'static MVP shell'
        if app_dir is None:
            app_dir = create_static_mvp(project)
        print(f'\n=== {project.name} ({mode}) -> {app_dir} ===', flush=True)
        ok, url, detail = deploy(app_dir)
        status = verify(url) if ok else 'not-deployed'
        rows.append({'project': project.name, 'mode': mode, 'app_dir': str(app_dir), 'ok': ok, 'url': url, 'http': status, 'detail': detail[-1500:]})
        print(f'{project.name}: ok={ok} http={status} url={url}', flush=True)
        time.sleep(1)
        REPORT.write_text(render_report(rows, start))
    REPORT.write_text(render_report(rows, start))
    print(f'\nReport written: {REPORT}', flush=True)


def render_report(rows, start):
    lines = [
        '# Deploy All Projects Report', '',
        f'Started: {start}',
        f'Updated: {datetime.now(timezone.utc).isoformat()}', '',
        '| Project | Mode | HTTP | URL | Notes |',
        '|---|---|---:|---|---|',
    ]
    for r in rows:
        notes = 'deployed' if r['ok'] else 'blocked/failing — see detail below'
        lines.append(f"| `{r['project']}` | {r['mode']} | {r['http']} | {r['url'] or '—'} | {notes} |")
    lines += ['', '## Failure / detail snippets', '']
    for r in rows:
        if not r['ok']:
            lines += [f"### {r['project']}", '```text', r['detail'][:2000], '```', '']
    return '\n'.join(lines)

if __name__ == '__main__':
    main()

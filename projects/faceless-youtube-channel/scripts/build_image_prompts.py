#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
STYLE = ('simple beginner-style drawing made in MS Paint, white background, black outline, '
         'minimal flat colors, slightly rough human-drawn look, no photorealism, no cinematic lighting, '
         'no detailed shading, no text unless explicitly needed')
TS_RE = re.compile(r'^\s*\[?(?P<ts>(?:\d{1,2}:)?\d{1,2}:\d{2}(?:[.,]\d+)?|\d+(?:[.,]\d+)?)\]?\s*[-–—:]?\s*(?P<text>.+?)\s*$')
def parse_seconds(ts):
    ts = ts.replace(',', '.')
    parts = ts.split(':')
    if len(parts) == 1: return float(parts[0])
    if len(parts) == 2: return int(parts[0]) * 60 + float(parts[1])
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
def make_prompt(text):
    clean = re.sub(r'\s+', ' ', text).strip()
    return f'{STYLE}. Draw this narration beat: {clean}'
parser = argparse.ArgumentParser(description='Convert timestamped transcript to Higgsfield image prompts JSONL.')
parser.add_argument('transcript')
parser.add_argument('--out', required=True)
args = parser.parse_args()
rows=[]
for line in Path(args.transcript).read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    m=TS_RE.match(line)
    if not m: continue
    seconds=parse_seconds(m.group('ts'))
    text=m.group('text').strip()
    rows.append({'timestamp': f'{seconds:.2f}', 'seconds': seconds, 'text': text, 'prompt': make_prompt(text)})
if not rows:
    raise SystemExit('No timestamped lines found. Use lines like: 00:07 narration text')
out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows)+'\n', encoding='utf-8')
print(f'wrote {len(rows)} prompts -> {out}')

#!/usr/bin/env python3
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.request import urlopen, Request
URL_RE = re.compile(r"https?://[^\s\"']+")
def timestamp_filename(ts): return f"{float(ts):.2f}.png"
def extract_urls(obj):
    found=[]
    def walk(x):
        if isinstance(x, str): found.extend(URL_RE.findall(x))
        elif isinstance(x, dict):
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(obj)
    return [u.rstrip(',.') for u in found if any(ext in u.lower().split('?')[0] for ext in ['.png','.jpg','.jpeg','.webp'])]
def download(url, path):
    req=Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urlopen(req, timeout=120) as r: data=r.read()
    path.write_bytes(data)
parser=argparse.ArgumentParser(description='Generate one Higgsfield image per timestamp and save as timestamp.png')
parser.add_argument('prompts_jsonl')
parser.add_argument('--out-dir', required=True)
parser.add_argument('--model', default='gpt_image_2')
parser.add_argument('--higgsfield', default=os.environ.get('HIGGSFIELD_BIN','/opt/data/.local/bin/higgsfield'))
parser.add_argument('--sleep', type=float, default=0.0)
parser.add_argument('--dry-run', action='store_true')
args=parser.parse_args()
out_dir=Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
rows=[json.loads(line) for line in Path(args.prompts_jsonl).read_text(encoding='utf-8').splitlines() if line.strip()]
for i,row in enumerate(rows,1):
    out=out_dir/timestamp_filename(row['seconds'])
    cmd=[args.higgsfield,'generate','create',args.model,'--prompt',row['prompt'],'--aspect_ratio','16:9','--wait','--json']
    print(f'[{i}/{len(rows)}] {row["timestamp"]} -> {out.name}')
    if args.dry_run:
        print('DRY:', ' '.join(cmd[:5]), '...')
        continue
    proc=subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)
    try: data=json.loads(proc.stdout)
    except json.JSONDecodeError: data={'stdout':proc.stdout}
    urls=extract_urls(data)
    if not urls:
        (out_dir/f'{out.stem}.raw.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
        raise SystemExit(f'No downloadable image URL found for {row["timestamp"]}. Raw output saved.')
    download(urls[0], out)
    out.with_suffix('.json').write_text(json.dumps({'row':row,'url':urls[0],'raw':data}, indent=2), encoding='utf-8')
    if args.sleep: time.sleep(args.sleep)
print('done')

#!/usr/bin/env python3
import argparse, re
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def slugify(s):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')
    return s[:60] or 'untitled-video'
parser = argparse.ArgumentParser(description='Create a per-video workspace.')
parser.add_argument('title')
args = parser.parse_args()
folder = ROOT / 'videos' / f"{date.today().isoformat()}-{slugify(args.title)}"
for sub in ['audio', 'transcript', 'prompts', 'images', 'exports']:
    (folder / sub).mkdir(parents=True, exist_ok=True)
brief = folder / 'brief.md'
if not brief.exists():
    brief.write_text(f"# {args.title}\n\n## Promise\n\n## Target viewer\n\n## Hook\n\n## Sources\n\n## Notes\n", encoding='utf-8')
print(folder)

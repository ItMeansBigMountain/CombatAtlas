#!/usr/bin/env python3
import argparse, json, time
import urllib.request as req
def fetch_json(url):
    with req.urlopen(url, timeout=60) as r: return json.loads(r.read())
parser = argparse.ArgumentParser(description='Fetch trending topics from free sources')
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()
hn = fetch_json(f'http://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={args.limit}')
print("=== Hacker News Front Page ===")
for h in hn.get('hits', [])[:args.limit]:
    print(f"- {h.get('title', '')}: {h.get('url', 'no url')}")
print(f"\nSaved to /tmp/hn_trends.json")
with open('/tmp/hn_trends.json', 'w') as f: json.dump(hn, f, indent=2)

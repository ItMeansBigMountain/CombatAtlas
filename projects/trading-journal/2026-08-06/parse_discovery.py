import json
x=json.load(open('discovery-raw.json'))
for r in x:
 print(r['args']['list_id'], [i['symbol'] for i in r['structuredContent']['data']['items']])

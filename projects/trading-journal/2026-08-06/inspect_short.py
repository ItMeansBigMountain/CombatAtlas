import json
x=json.load(open('shortlist-raw.json'))
for r in x:
 print('\n',r['tool'],r['args'], 'err',r.get('isError'),r.get('exception'))
 d=(r.get('structuredContent') or {}).get('data',{})
 print('keys',d.keys() if isinstance(d,dict) else type(d))
 print(json.dumps(d,default=str)[:1500])

import json
p='open-state-raw.json'
x=json.load(open(p))
def data(r):
 s=r.get('structuredContent')
 if s: return s.get('data',s)
 for c in r.get('content',[]):
  try:
   y=json.loads(c); z=y.get('result',y)
   if isinstance(z,str): z=json.loads(z)
   return z.get('data',z)
  except: pass
 return {'error':r}
for r in x:
 d=data(r); t=r['tool']; print('\n##',t,r.get('args'))
 if t=='get_accounts':
  print([a for a in d.get('accounts',[]) if a.get('account_number')=='433711041'])
 elif t=='get_portfolio': print(d)
 elif t=='get_equity_positions': print(d)
 elif t=='get_equity_orders':
  oo=d.get('orders',[]); print('count',len(oo)); print(oo[:15])
 elif t=='get_equity_quotes':
  for q in d.get('results',[]): print(q.get('quote',q))
 elif t in ('get_popular_watchlists','get_earnings_calendar'): print(json.dumps(d)[:30000])
 else: print(json.dumps(d)[:5000])

import json
x=json.load(open('final-verify-raw.json'))
for r in x:
 d=(r.get('structuredContent') or {}).get('data',{})
 print('\n',r['tool'],r['args'])
 if r['tool']=='get_equity_quotes':
  for z in d.get('results',[]):
   q=z.get('quote',z); p=float(q['last_trade_price']); pc=float(q['previous_close']); print(q['symbol'],p,round((p/pc-1)*100,2),q['bid_price'],q['ask_price'])
 elif r['tool']=='get_equity_orders': print(len(d.get('orders',[])))
 else: print(d)

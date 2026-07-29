import json
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-28/open-state-raw.json'
x=json.load(open(p))
for r in x:
 print('\nTOOL',r['tool'],r.get('args'))
 if r.get('isError') or r.get('exception'): print('ERROR',r.get('content'),r.get('exception')); continue
 d=(r.get('structuredContent') or {}).get('data',{})
 if r['tool']=='get_accounts': print([a for a in d.get('accounts',[]) if a.get('account_number')=='433711041'])
 elif r['tool']=='get_portfolio': print(d)
 elif r['tool']=='get_equity_positions': print(d)
 elif r['tool']=='get_equity_orders':
  oo=d.get('orders',[])
  print([{k:o.get(k) for k in ['id','symbol','side','state','quantity','cumulative_quantity','average_price','dollar_based_amount','created_at','last_transaction_at']} for o in oo])
 elif r['tool']=='get_equity_quotes':
  for z in d.get('results',[]):
   q=z.get('quote',z); print(q.get('symbol'),q.get('last_trade_price'),q.get('previous_close'),q.get('bid_price'),q.get('ask_price'))
 elif r['tool']=='get_popular_watchlists': print(json.dumps(d,indent=2)[:15000])
 elif r['tool']=='get_earnings_calendar': print(json.dumps(d,indent=2)[:15000])
 else: print(json.dumps(d,indent=2)[:5000])

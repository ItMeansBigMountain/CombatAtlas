import json
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-27/midday-state-raw.json'
x=json.load(open(p))
for r in x:
 print('\nTOOL',r['tool'],r.get('args'))
 if r.get('isError') or r.get('exception'): print('ERROR',r.get('content'),r.get('exception')); continue
 d=(r.get('structuredContent') or {}).get('data',{})
 if r['tool']=='get_accounts':
  print([a for a in d.get('accounts',[]) if a.get('account_number')=='433711041'])
 elif r['tool']=='get_portfolio': print(d)
 elif r['tool']=='get_equity_positions': print(d)
 elif r['tool']=='get_equity_orders':
  for o in d.get('orders',[]): print({k:o.get(k) for k in ['id','symbol','side','state','quantity','cumulative_quantity','average_price','dollar_based_amount','created_at','last_transaction_at']})
  if not d.get('orders'): print('[]')
 elif r['tool']=='get_equity_quotes':
  for z in d.get('results',[]):
   q=z.get('quote',z)
   print(q.get('symbol'),q.get('last_trade_price'),q.get('previous_close'),q.get('bid_price'),q.get('ask_price'),q.get('venue_last_trade_time'))
 elif r['tool']=='get_equity_tradability': print(json.dumps(d,indent=2))
 elif r['tool']=='get_earnings_calendar':
  print(json.dumps(d,indent=2)[:10000])
 else: print(json.dumps(d,indent=2)[:5000])

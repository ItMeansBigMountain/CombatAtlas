import json,datetime
p='/opt/data/HeRmEz/projects/trading-journal/order-review-raw.json';d=json.load(open(p))
qs={x['quote']['symbol']:x['quote'] for x in d['quotes']['results']}
pos={x['symbol']:x for x in d['positions']['positions']}
print('PORTFOLIO',d['portfolio'])
print('OPEN_COUNTS',{k:len(v.get('orders',[])) for k,v in d.items() if k.startswith('open_')})
print('\nCURRENT')
for s,x in pos.items():
 q=qs[s]; qty=float(x['quantity']); avg=float(x['average_buy_price']); px=float(q['last_trade_price']); pnl=(px-avg)*qty
 print(s,'qty',qty,'avg',avg,'px',px,'pnl$',round(pnl,4),'pnl%',round((px/avg-1)*100,2),'quote_time',q.get('venue_last_trade_time'))
print('\nORDERS',len(d['orders']['orders']))
for o in d['orders']['orders']:
 print(json.dumps(o,separators=(',',':')))
print('\nOTHER_QUOTES')
for s in ['HOOD','NVDA','SOFI','SPY','QQQ','IWM']:
 q=qs[s]; print(s,q['last_trade_price'],q.get('venue_last_trade_time'),q.get('previous_close'))

import json, os
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-31/post-open-raw.json'
x=json.load(open(p))
for r in x:
 d=(r.get('structuredContent') or {}).get('data',{})
 t=r['tool']
 print('\nTOOL',t,r.get('args'))
 if t=='get_accounts': print([a for a in d.get('accounts',[]) if a.get('account_number')=='433711041'])
 elif t=='get_portfolio': print(d)
 elif t=='get_equity_positions': print(json.dumps(d,default=str))
 elif t=='get_equity_orders':
  print([{k:o.get(k) for k in ['id','symbol','side','type','state','quantity','cumulative_quantity','average_price','dollar_based_amount','created_at','last_transaction_at']} for o in d.get('orders',[])])
 elif t=='get_equity_quotes':
  for z in d.get('results',[]):
   q=z.get('quote',z); keys=['symbol','last_trade_price','previous_close','bid_price','ask_price','updated_at','last_trade_size','trading_halted']; print({k:q.get(k) for k in keys})
 elif t=='get_equity_historicals':
  results=d.get('results',[])
  if isinstance(results,dict): results=list(results.values())
  for z in results:
   b=z.get('bars',[])
   if not b: print(z.get('symbol'),'NO_BARS'); continue
   c=[float(a['close_price']) for a in b]; h=[float(a['high_price']) for a in b]; l=[float(a['low_price']) for a in b]; v=[float(a['volume']) for a in b]
   tr=[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,len(b))]
   sma=lambda n: sum(c[-n:])/min(n,len(c))
   print(z.get('symbol'),f"bars={len(b)} first={c[0]:.2f} last={c[-1]:.2f} sma10={sma(10):.2f} sma20={sma(20):.2f} sma50={sma(50):.2f} atr14={sum(tr[-14:])/max(1,min(14,len(tr))):.2f} hi20={max(h[-20:]):.2f} lo20={min(l[-20:]):.2f} avgvol20={sum(v[-20:])/min(20,len(v)):.0f} ret20={(c[-1]/c[-min(21,len(c))]-1)*100:.2f}% range={l[-1]:.2f}-{h[-1]:.2f} vol={v[-1]:.0f}")
 elif t=='get_equity_fundamentals':
  for z in d.get('results',[]): print({k:z.get(k) for k in ['symbol','market_cap','pe_ratio','pb_ratio','dividend_yield','average_volume','high_52_weeks','low_52_weeks','sector','industry','volume','open','high','low']})
 elif t=='get_equity_tradability': print(json.dumps(d,default=str))
 elif t=='get_earnings_results': print(json.dumps(d,default=str)[:4000])
 elif t=='get_financials':
  rs=d.get('results',[]); rs=[rs] if isinstance(rs,dict) else rs
  for z in rs: print((z or {}).get('symbol'),json.dumps(z,default=str)[:2500])

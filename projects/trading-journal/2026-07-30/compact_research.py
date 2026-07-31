import json, statistics
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-30/open-research2-raw.json'
x=json.load(open(p))
for r in x:
 d=(r.get('structuredContent') or {}).get('data',{})
 if r['tool']=='get_watchlist_items':
  print('MOVERS', [i.get('symbol') for i in d.get('items',[])])
 elif r['tool']=='get_equity_historicals':
  for z in d.get('results',[]):
   b=z.get('bars',[])
   if not b: print(z.get('symbol'),'NO_BARS'); continue
   c=[float(a['close_price']) for a in b]; h=[float(a['high_price']) for a in b]; l=[float(a['low_price']) for a in b]; v=[float(a['volume']) for a in b]
   tr=[]
   for i in range(1,len(b)): tr.append(max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])))
   sma=lambda n: sum(c[-n:])/min(n,len(c))
   print('TECH',z['symbol'],f"close={c[-1]:.2f} sma10={sma(10):.2f} sma20={sma(20):.2f} sma50={sma(50):.2f} atr14={sum(tr[-14:])/min(14,len(tr)):.2f} hi20={max(h[-20:]):.2f} lo20={min(l[-20:]):.2f} avgvol20={sum(v[-20:])/min(20,len(v)):.0f} volratio={v[-1]/(sum(v[-20:-1])/max(1,len(v[-20:-1]))):.2f} ret20={(c[-1]/c[-21]-1)*100:.2f}%")
 elif r['tool']=='get_equity_fundamentals':
  for z in d.get('results',[]):
   keep=['symbol','market_cap','pe_ratio','pb_ratio','dividend_yield','average_volume','high_52_weeks','low_52_weeks','sector','industry']
   print('FUND', {k:z.get(k) for k in keep})
 elif r['tool']=='get_financials':
  results=d.get('results',[])
  if isinstance(results,dict): results=[results]
  for z in results:
   if z is not None: print('FIN',z.get('symbol'),json.dumps(z,default=str)[:1200])

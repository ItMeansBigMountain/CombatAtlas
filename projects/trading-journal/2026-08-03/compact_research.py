import json
p='/opt/data/HeRmEz/projects/trading-journal/2026-08-03/post-open-research-raw.json'
x=json.load(open(p))
for r in x:
 print('\nTOOL',r['tool'],r.get('args'),'ERR',r.get('isError'),r.get('exception'))
 if not r.get('content'): continue
 try: d=json.loads(r['content'][0]).get('data',{})
 except Exception as e: print('PARSE',e); continue
 t=r['tool']
 if t=='get_equity_historicals':
  results=d.get('results',[])
  if isinstance(results,dict): results=list(results.values())
  for z in results:
   b=z.get('bars',[])
   if not b: print(z.get('symbol'),'NO_BARS'); continue
   c=[float(a['close_price']) for a in b]; h=[float(a['high_price']) for a in b]; l=[float(a['low_price']) for a in b]; v=[float(a['volume']) for a in b]
   tr=[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,len(b))]
   sma=lambda n:sum(c[-n:])/min(n,len(c))
   print(z.get('symbol'),f'bars={len(b)} last={c[-1]:.2f} sma10={sma(10):.2f} sma20={sma(20):.2f} sma50={sma(50):.2f} atr14={sum(tr[-14:])/max(1,min(14,len(tr))):.2f} hi20={max(h[-20:]):.2f} lo20={min(l[-20:]):.2f} avgvol20={sum(v[-20:])/min(20,len(v)):.0f} ret20={(c[-1]/c[-min(21,len(c))]-1)*100:.2f}% range={l[-1]:.2f}-{h[-1]:.2f} vol={v[-1]:.0f}')
 elif t=='get_equity_fundamentals':
  for z in d.get('results',[]): print({k:z.get(k) for k in ['symbol','market_cap','pe_ratio','pb_ratio','dividend_yield','average_volume','high_52_weeks','low_52_weeks','sector','industry','volume','open','high','low']})
 elif t=='get_equity_tradability': print(json.dumps(d)[:6000])
 elif t=='get_earnings_results': print(json.dumps(d)[:6000])
 elif t=='get_financials':
  rs=d.get('results',[]); rs=[rs] if isinstance(rs,dict) else rs
  for z in rs: print((z or {}).get('symbol'),json.dumps(z)[:3500])
 else: print(json.dumps(d)[:5000])

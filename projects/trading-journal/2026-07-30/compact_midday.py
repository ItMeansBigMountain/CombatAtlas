import json
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-30/midday-research-raw.json'
x=json.load(open(p))
for r in x:
 d=(r.get('structuredContent') or {}).get('data',{})
 if r.get('isError') or r.get('exception'): print('ERROR',r['tool'],r.get('content'),r.get('exception')); continue
 if r['tool']=='get_equity_quotes':
  rs=d.get('results',d.get('quotes',[])); rs=list(rs.values()) if isinstance(rs,dict) else rs
  for z in rs: print('QUOTE',z.get('symbol'),z.get('last_trade_price'),z.get('previous_close'),z.get('bid_price'),z.get('ask_price'),z.get('updated_at'))
 elif r['tool']=='get_equity_tradability': print('TRAD',json.dumps(d,default=str))
 elif r['tool']=='get_equity_historicals':
  rs=d.get('results',[]); rs=list(rs.values()) if isinstance(rs,dict) else rs
  for z in rs:
   b=z.get('bars',[])
   if not b: print('NO_BARS',z.get('symbol')); continue
   c=[float(a['close_price']) for a in b]; h=[float(a['high_price']) for a in b]; l=[float(a['low_price']) for a in b]; v=[float(a['volume']) for a in b]
   tr=[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,len(b))]
   sma=lambda n: sum(c[-n:])/min(n,len(c))
   if len(b)>40: print('DAILY',z['symbol'],f'close={c[-1]:.2f} sma10={sma(10):.2f} sma20={sma(20):.2f} sma50={sma(50):.2f} atr14={sum(tr[-14:])/min(14,len(tr)):.2f} hi20={max(h[-20:]):.2f} lo20={min(l[-20:]):.2f} avgvol20={sum(v[-20:])/min(20,len(v)):.0f} volratio={v[-1]/(sum(v[-20:-1])/max(1,len(v[-20:-1]))):.2f} ret20={(c[-1]/c[-21]-1)*100:.2f}%')
   else: print('INTRA',z['symbol'],f'open={c[0]:.2f} last={c[-1]:.2f} high={max(h):.2f} low={min(l):.2f} bars={len(b)} volume={sum(v):.0f}')
 elif r['tool']=='get_equity_fundamentals':
  rs=d.get('results',[]); rs=list(rs.values()) if isinstance(rs,dict) else rs
  for z in rs: print('FUND',json.dumps({k:z.get(k) for k in ['symbol','market_cap','pe_ratio','pb_ratio','dividend_yield','average_volume','volume','high_52_weeks','low_52_weeks','sector','industry']},default=str))
 elif r['tool']=='get_earnings_results': print('EARN',json.dumps(d,default=str)[:1800])

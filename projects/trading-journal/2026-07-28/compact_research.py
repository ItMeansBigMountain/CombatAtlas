import json
x=json.load(open('/opt/data/HeRmEz/projects/trading-journal/2026-07-28/open-research-raw.json'))
def data(r): return (r.get('structuredContent') or {}).get('data',{})
for i,r in enumerate(x):
 print('\nTOOL',i,r['tool'],'ERR',r.get('isError'),r.get('exception'))
 if r.get('isError') or r.get('exception'): print(r.get('content')); continue
 d=data(r)
 if r['tool']=='get_equity_quotes':
  for z in d.get('results',[]):
   q=z.get('quote',z); print(q.get('symbol'),q.get('last_trade_price'),q.get('previous_close'),q.get('bid_price'),q.get('ask_price'))
 elif r['tool']=='get_equity_historicals':
  for z in d.get('results',[]):
   b=z.get('bars',[]); sym=z.get('symbol');
   if not b: print(sym,'EMPTY'); continue
   c=[float(v['close_price']) for v in b]; h=[float(v['high_price']) for v in b]; l=[float(v['low_price']) for v in b]; vol=[float(v['volume']) for v in b]
   if r['args']['interval']=='day':
    tr=[max(h[j]-l[j],abs(h[j]-c[j-1]),abs(l[j]-c[j-1])) for j in range(1,len(b))]
    print(sym,'last',c[-1],'sma',*[round(sum(c[-n:])/min(n,len(c)),2) for n in (10,20,50)],'atr14',round(sum(tr[-14:])/min(14,len(tr)),2),'20hi/lo',round(max(h[-20:]),2),round(min(l[-20:]),2),'volrat',round(vol[-1]/(sum(vol[-21:-1])/max(1,len(vol[-21:-1]))),2))
   else: print(sym,'bars',len(b),'open',b[0]['open_price'],'last',c[-1],'hi/lo',max(h),min(l),'vol',sum(vol))
 elif r['tool']=='get_equity_fundamentals':
  for z in d.get('results',[]): print(z)
 elif r['tool']=='get_financials':
  for z in d.get('results',[]):
   if not z: print('NULL_RESULT'); continue
   print(z.get('symbol'),[{k:f.get(k) for k in ['fiscal_year','fiscal_quarter','revenue','net_income','operating_cash_flow','free_cash_flow','total_debt','cash_and_equivalents']} for f in z.get('financials',[])[:2]])
 else: print(json.dumps(d,indent=2)[:15000])

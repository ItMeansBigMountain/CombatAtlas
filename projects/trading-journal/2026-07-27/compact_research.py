import json,statistics
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-27/midday-research-raw.json'; x=json.load(open(p))
def data(r): return (r.get('structuredContent') or {}).get('data',{})
# historicals
for idx,label in [(0,'DAILY'),(1,'INTRADAY')]:
 print('\n'+label)
 for z in data(x[idx]).get('results',[]):
  b=z.get('bars',[]); sym=z['symbol']
  if label=='DAILY':
   c=[float(v['close_price']) for v in b]; h=[float(v['high_price']) for v in b]; l=[float(v['low_price']) for v in b]; vol=[float(v['volume']) for v in b]
   trs=[]
   for i in range(1,len(b)): trs.append(max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])))
   print(sym,'last',c[-1],'SMA10/20/50',*[round(sum(c[-n:])/n,2) for n in (10,20,50)],'ATR14',round(sum(trs[-14:])/14,2),'20hi/lo',round(max(h[-20:]),2),round(min(l[-20:]),2),'20ret%',round((c[-1]/c[-21]-1)*100,2),'volratio',round(vol[-1]/(sum(vol[-21:-1])/20),2),'bar',b[-1])
  else:
   c=[float(v['close_price']) for v in b]; h=[float(v['high_price']) for v in b]; l=[float(v['low_price']) for v in b]; vol=[float(v['volume']) for v in b]
   print(sym,'bars',len(b),'open',b[0]['open_price'],'last',c[-1],'high/low',max(h),min(l),'VWAPapprox',round(sum(float(v['close_price'])*float(v['volume']) for v in b)/sum(vol),2),'last6',c[-6:])
print('\nFUNDAMENTALS')
for z in data(x[2]).get('results',[]): print(z)
print('\nFINANCIALS compact')
for z in data(x[3]).get('results',[]):
 fs=z.get('financials',[])
 print(z['symbol'],[{k:f.get(k) for k in ['fiscal_year','fiscal_quarter','report_date','revenue','net_income','operating_cash_flow','free_cash_flow','total_debt','cash_and_equivalents']} for f in fs[:2]])
print('\nEARNINGS CALENDAR relevant')
for z in data(x[4]).get('results',[]):
 if z.get('symbol') in ['NVDA','JPM','SLB','GOOGL','PLTR','RTX','VZ','BAC','GE','UNH','AAPL','MSFT','META','AMZN','AMD','XOM','CVX','COP']: print(z)
print('\nEARNINGS RESULTS latest')
for r in x[5:8]: print(r['args']['symbol'],data(r).get('results',[])[:2])
print('\nBOOKS')
for z in data(x[8]).get('books',[]): print(z)

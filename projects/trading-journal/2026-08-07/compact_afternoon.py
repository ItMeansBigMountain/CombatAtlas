import json, statistics
raw=json.load(open('afternoon-raw.json'))
retry=json.load(open('afternoon-retry-raw.json'))
raw=[x for x in raw if not x.get('isError')] + retry
def payload(x):
    return json.loads(x['content'][0])['data']
def results(x):
    d=payload(x); r=d.get('results',d)
    return list(r.values()) if isinstance(r,dict) else r
by={}
for x in raw: by.setdefault(x['tool'],[]).append(x)
out={'accounts':payload(by['get_accounts'][0]),'portfolio':payload(by['get_portfolio'][0]),'positions':payload(by['get_equity_positions'][0]),'orders':[payload(x) for x in by['get_equity_orders']],'quotes':results(by['get_equity_quotes'][0])}
def metrics(rows):
 o={}
 for row in rows:
  bars=row['bars']; c=[float(b['close_price']) for b in bars]; h=[float(b['high_price']) for b in bars]; l=[float(b['low_price']) for b in bars]; v=[float(b['volume']) for b in bars]
  if len(c)>=21:
   tr=[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,len(c))]
   o[row['symbol']]={'last':c[-1],'sma10':statistics.mean(c[-10:]),'sma20':statistics.mean(c[-20:]),'sma50':statistics.mean(c[-50:]),'atr14':statistics.mean(tr[-14:]),'support20':min(l[-21:-1]),'resistance20':max(h[-21:-1]),'ret5':(c[-1]/c[-6]-1)*100,'ret20':(c[-1]/c[-21]-1)*100,'vol_ratio':v[-1]/statistics.mean(v[-21:-1])}
  else:
   tv=sum(v); typ=[(a+b+d)/3 for a,b,d in zip(h,l,c)]; vw=sum(a*b for a,b in zip(typ,v))/tv if tv else 0
   o[row['symbol']]={'last':c[-1],'first':c[0],'high':max(h),'low':min(l),'vwap':vw,'from_first':(c[-1]/c[0]-1)*100,'above_vwap':(c[-1]/vw-1)*100 if vw else 0,'bars':len(c),'last_time':bars[-1]['begins_at']}
 return o
out['intraday']=metrics(sum((results(x) for x in by['get_equity_historicals'][:2]),[])); out['daily']=metrics(sum((results(x) for x in by['get_equity_historicals'][2:]),[])); out['fundamentals']=sum((results(x) for x in by['get_equity_fundamentals']),[]); out['financials']=results(by['get_financials'][0]); out['earnings']={x['args']['symbol']:payload(x) for x in by['get_earnings_results']}; out['scans']=payload(by['get_scans'][0])
json.dump(out,open('afternoon-compact.json','w'),indent=2)
print(json.dumps({'accounts':out['accounts'],'portfolio':out['portfolio'],'positions':out['positions'],'orders':out['orders'],'quotes':out['quotes'],'intraday':out['intraday'],'daily':out['daily'],'scans':out['scans']},indent=2))

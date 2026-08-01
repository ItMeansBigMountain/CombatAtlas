import json,statistics
p='/opt/data/HeRmEz/projects/trading-journal/2026-07-31/midday-shortlist-raw.json'; D=json.load(open(p))
def payload(x): return json.loads(x['content'][0]).get('data',{})
for x in D:
 t=x['tool']; d=payload(x)
 if t=='get_equity_quotes':
  print('QUOTES')
  for r in d.get('results',[]):
   q=r['quote']; print(q['symbol'],q['last_trade_price'],q['previous_close'],q['bid_price'],q['ask_price'])
 elif t=='get_equity_historicals':
  print('DAILY')
  for r in d.get('results',[]):
   b=r.get('bars',[]); closes=[float(z['close_price']) for z in b]; highs=[float(z['high_price']) for z in b]; lows=[float(z['low_price']) for z in b]; vols=[float(z['volume']) for z in b]
   if len(b)<21: print(r['symbol'],'INSUFFICIENT',len(b)); continue
   prev=closes[-1]; trs=[]
   for i in range(1,len(b)): trs.append(max(highs[i]-lows[i],abs(highs[i]-closes[i-1]),abs(lows[i]-closes[i-1])))
   print(r['symbol'],'n',len(b),'last',prev,'sma10',round(sum(closes[-10:])/10,2),'sma20',round(sum(closes[-20:])/20,2),'sma50',round(sum(closes[-50:])/50,2),'atr14',round(sum(trs[-14:])/14,2),'hi20prev',max(highs[-21:-1]),'lo20prev',min(lows[-21:-1]),'ret20%',round((closes[-1]/closes[-21]-1)*100,2),'avgvol20',round(sum(vols[-20:])/20))
 elif t in ('get_equity_fundamentals','get_financials'):
  print(t.upper(),json.dumps(d)[:10000])
 elif t=='get_equity_tradability': print('TRADABILITY',json.dumps(d))
 elif t=='get_earnings_results': print('EARN',x['args']['symbol'],json.dumps(d)[:1500])

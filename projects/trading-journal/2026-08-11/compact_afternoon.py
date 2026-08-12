import json,sys,statistics,math
p=json.load(open(sys.argv[1]))
def payload(x):
 try:return json.loads(x.get('content',['{}'])[0]).get('data',{})
 except Exception as e:return {'_parse_error':str(e)}
for x in p:
 d=payload(x); t=x['tool']; a=x.get('args',{})
 if t in ('get_accounts','get_portfolio','get_equity_positions','get_equity_orders'):
  print('\n',t,a,json.dumps(d,separators=(',',':')))
 elif t=='get_equity_quotes':
  print('\nQUOTES')
  q=d.get('results',d.get('quotes',d))
  if isinstance(q,list):
   out=[]
   for z in q:
    v=z.get('quote',z); out.append({k:v.get(k) for k in ('symbol','last_trade_price','previous_close','bid_price','ask_price','venue_last_trade_time')})
   print(json.dumps(out,separators=(',',':')))
  else: print(json.dumps(q,separators=(',',':')))
 elif t=='get_equity_tradability': print('\nTRAD',json.dumps(d,separators=(',',':')))
 elif t=='get_equity_historicals':
  r=d.get('results',d.get('historicals',{})); print('\nHIST',a.get('interval'))
  if isinstance(r,list):
   groups={z.get('symbol','?'):z.get('bars',z.get('historicals',[])) for z in r}
  elif isinstance(r,dict): groups=r
  else: groups={}
  for s,bars in groups.items():
   if isinstance(bars,dict): bars=bars.get('historicals',bars.get('bars',bars.get('results',[])))
   try:
    closes=[float(b.get('close_price',b.get('close'))) for b in bars if b.get('close_price',b.get('close')) is not None]
    highs=[float(b.get('high_price',b.get('high'))) for b in bars if b.get('high_price',b.get('high')) is not None]
    lows=[float(b.get('low_price',b.get('low'))) for b in bars if b.get('low_price',b.get('low')) is not None]
    vols=[float(b.get('volume',0)) for b in bars]
    if not closes: continue
    sma=lambda n:sum(closes[-n:])/min(n,len(closes))
    tr=[]
    for i in range(1,len(closes)):tr.append(max(highs[i]-lows[i],abs(highs[i]-closes[i-1]),abs(lows[i]-closes[i-1])))
    atr=sum(tr[-14:])/min(14,len(tr)) if tr else 0
    out={'n':len(closes),'last':closes[-1],'sma20':sma(20),'sma50':sma(50),'ret20':closes[-1]/closes[-21]-1 if len(closes)>20 else None,'ret60':closes[-1]/closes[-61]-1 if len(closes)>60 else None,'atr14':atr,'hi20':max(highs[-20:]),'lo20':min(lows[-20:]),'avgvol20':sum(vols[-20:])/min(20,len(vols))}
    print(s,json.dumps(out,separators=(',',':')))
   except Exception as e: print(s,'ERR',e)
 elif t in ('get_equity_fundamentals','get_financials','get_earnings_results'):
  print('\n',t,a,json.dumps(d,separators=(',',':'))[:12000])

import json, math
p=json.load(open('midday_research_raw.json'))
def data(c): return (c.get('structuredContent') or {}).get('data',{})
for c in p:
 d=data(c); t=c['tool']
 if t=='get_equity_quotes':
  print('\nQUOTES')
  for x in d.get('results',[]):
   q=x['quote']; last=float(q['last_trade_price']); prev=float(q['adjusted_previous_close']); print(q['symbol'],last,round((last/prev-1)*100,2),'bidask',q.get('bid_price'),q.get('ask_price'),q.get('venue_last_trade_time'))
 elif t=='run_scan':
  print('\nSCAN KEYS',d.keys()); print(json.dumps(d,indent=2)[:15000])
 elif t=='get_watchlist_items':
  print('\nMOVERS',json.dumps(d,indent=2)[:8000])
 elif t=='get_equity_historicals':
  res=d.get('results',{})
  if isinstance(res,list):
   groups={x.get('symbol'):x.get('historicals') or x.get('bars') or x.get('data') or [] for x in res}
  else: groups=res
  print('\nHIST',c['args']['interval'])
  for s,raw in groups.items():
   bars=raw.get('historicals',raw.get('data',[])) if isinstance(raw,dict) else raw
   vals=[]
   for b in bars:
    try: vals.append({k:float(b[k]) for k in ['open_price','high_price','low_price','close_price','volume']})
    except: pass
   if not vals: print(s,'EMPTY'); continue
   cl=[x['close_price'] for x in vals]; vol=[x['volume'] for x in vals]
   out={'n':len(vals),'last':cl[-1],'sma10':sum(cl[-10:])/min(10,len(cl)),'sma20':sum(cl[-20:])/min(20,len(cl)),'sma50':sum(cl[-50:])/min(50,len(cl)),'high20':max(x['high_price'] for x in vals[-20:]),'low20':min(x['low_price'] for x in vals[-20:]),'avgvol20':sum(vol[-20:])/min(20,len(vol))}
   if c['args']['interval']=='30minute': out.update({'first':cl[0],'session_high':max(x['high_price'] for x in vals[-6:]),'session_low':min(x['low_price'] for x in vals[-6:]),'lastvol':vol[-1]})
   print(s,{k:round(v,4) if isinstance(v,float) else v for k,v in out.items()})
 elif t=='get_equity_fundamentals':
  print('\nFUNDS',json.dumps(d,indent=2)[:15000])
 elif t=='get_earnings_results':
  print('\nEARN',c['args']['symbol'],json.dumps(d,indent=2)[:3000])
 elif t=='get_equity_tradability': print('\nTRAD',json.dumps(d,indent=2))

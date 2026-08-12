import json,statistics
base=json.load(open('midday-raw.json')); res=json.load(open('midday-research-raw.json'))
def payload(r):
 s=''.join(r.get('content',[])); return json.loads(s)['data'] if s else {}
def results(r): return payload(r).get('results',[])
quotes={z['quote']['symbol']:z['quote'] for z in results(base[9])}
daily={}
for r in res[:2]:
 for z in results(r): daily[z['symbol']]=z['bars']
intra={}
for r in res[2:4]:
 for z in results(r): intra[z['symbol']]=z['bars']
fund={}
for r in res[4:6]:
 for z in results(r): fund[z['symbol']]=z
def metrics(sym):
 b=daily.get(sym,[]); cs=[float(x['close_price']) for x in b]; vs=[float(x.get('volume',0)) for x in b]
 q=quotes.get(sym,{}); p=float(q.get('last_trade_price',cs[-1] if cs else 0)); prev=float(q.get('adjusted_previous_close',cs[-1] if cs else p))
 ib=intra.get(sym,[]); ic=[float(x['close_price']) for x in ib]; iv=[float(x.get('volume',0)) for x in ib]
 return {'price':p,'day_pct':round((p/prev-1)*100,2) if prev else None,'sma20':round(sum(cs[-20:])/min(20,len(cs)),2) if cs else None,'sma50':round(sum(cs[-50:])/min(50,len(cs)),2) if cs else None,'ret20_pct':round((p/cs[-21]-1)*100,2) if len(cs)>20 else None,'ret60_pct':round((p/cs[-61]-1)*100,2) if len(cs)>60 else None,'high20':round(max(cs[-20:]),2) if cs else None,'low20':round(min(cs[-20:]),2) if cs else None,'avgvol20':round(sum(vs[-20:])/min(20,len(vs))) if vs else None,'intraday_open':ic[0] if ic else None,'intraday_high':max(ic) if ic else None,'intraday_low':min(ic) if ic else None,'vwap_proxy':round(sum(float(x['close_price'])*float(x.get('volume',0)) for x in ib)/sum(iv),2) if sum(iv) else None}
out={'portfolio':payload(base[1]),'positions':payload(base[2]),'metrics':{s:metrics(s) for s in sorted(set(quotes)&set(daily))},'fundamentals':fund}
scan=payload(res[6]).get('result',{}).get('results',[])
out['scan_top']=[x for x in scan if float(x.get('price') or 0)>=5 and float(x.get('volume') or 0)>=500000][:30]
json.dump(out,open('midday-compact.json','w'),indent=2)

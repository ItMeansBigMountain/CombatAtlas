import json,statistics
x=json.load(open('shortlist-raw.json'))
r=next(a for a in x if a['tool']=='get_equity_historicals')
for z in r['structuredContent']['data']['results']:
 b=z['bars']; c=[float(a['close_price']) for a in b]; h=[float(a['high_price']) for a in b]; l=[float(a['low_price']) for a in b]; v=[float(a['volume']) for a in b]
 tr=[]
 for i in range(1,len(b)): tr.append(max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])))
 print(z['symbol'],f"close={c[-1]:.2f} dayH/L={h[-1]:.2f}/{l[-1]:.2f} sma10={statistics.mean(c[-10:]):.2f} sma20={statistics.mean(c[-20:]):.2f} sma50={statistics.mean(c[-50:]):.2f} atr14={statistics.mean(tr[-14:]):.2f} prior20H={max(h[-21:-1]):.2f} prior20L={min(l[-21:-1]):.2f} vol={v[-1]:.0f} avg20v={statistics.mean(v[-21:-1]):.0f} ret20={(c[-1]/c[-21]-1)*100:.1f}%")

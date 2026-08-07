import json
x=json.load(open('universe-quote-raw.json'))
for r in x:
 d=r.get('structuredContent',{}).get('data',{})
 for z in d.get('results',[]):
  q=z.get('quote',z); p=float(q['last_trade_price']); pc=float(q['previous_close']); bid=float(q['bid_price'] or 0); ask=float(q['ask_price'] or 0)
  print(f"{q['symbol']:5} {p:9.3f} {(p/pc-1)*100:7.2f}% spread={(ask-bid)/p*100 if p else 0:.3f}%")

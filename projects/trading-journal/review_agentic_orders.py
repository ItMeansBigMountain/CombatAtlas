import sys,json,yaml,datetime
sys.path.insert(0,'/opt/data/hermes-agent')
from tools.mcp_tool import register_mcp_servers
from tools.registry import registry
cfg=yaml.safe_load(open('/opt/data/config.yaml'))['mcp_servers']
register_mcp_servers({'robinhood_trading':cfg['robinhood_trading']})
def c(n,a):
 r=registry.dispatch('mcp_robinhood_trading_'+n,a)
 try:
  j=json.loads(r); return j.get('structuredContent',{}).get('data',j)
 except Exception as e:return {'error':str(e),'raw':str(r)[:3000]}
a='433711041'; o={}
o['portfolio']=c('get_portfolio',{'account_number':a})
o['positions']=c('get_equity_positions',{'account_number':a})
o['orders']=c('get_equity_orders',{'account_number':a,'created_at_gte':'2026-06-01T00:00:00Z'})
for s in ['new','queued','confirmed','unconfirmed','partially_filled']:
 o['open_'+s]=c('get_equity_orders',{'account_number':a,'state':s})
syms=['AVGO','MA','BAC','SHOP','NESR','HOOD','NVDA','SOFI','SPY','QQQ','IWM','SHEL','XOM','UL','JPM','SLB','UNH','AMD']
o['quotes']=c('get_equity_quotes',{'symbols':syms})
o['historicals']=c('get_equity_historicals',{'symbols':syms[:10],'start_time':'2026-06-01T00:00:00Z','interval':'day','bounds':'regular','adjustment_type':'split'})
print(json.dumps(o))

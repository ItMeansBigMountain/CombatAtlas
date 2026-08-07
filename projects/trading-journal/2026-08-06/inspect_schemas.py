import asyncio,json
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
import httpx2 as httpx
TOKEN=json.load(open('/opt/data/mcp-tokens/robinhood_trading.json'))['access_token']
async def main():
 c=httpx.AsyncClient(headers={'Authorization':f'Bearer {TOKEN}'})
 async with streamable_http_client('https://agent.robinhood.com/mcp/trading',http_client=c) as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize(); z=await s.list_tools()
   for t in z.tools:
    if t.name in ['get_watchlist_items','run_scan','get_equity_historicals','get_equity_technical_indicators','get_equity_fundamentals','get_financials','get_equity_tradability','review_equity_order','place_equity_order']:
     print(t.name,json.dumps(t.input_schema))
 await c.aclose()
asyncio.run(main())

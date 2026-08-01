import asyncio, json, sys
from mcp.client.streamable_http import streamable_http_client as streamablehttp_client
from mcp import ClientSession
import httpx2 as httpx
TOKEN=json.load(open('/opt/data/mcp-tokens/robinhood_trading.json'))['access_token']
URL='https://agent.robinhood.com/mcp/trading'
async def main():
    calls=json.load(open(sys.argv[1])); out=[]
    client=httpx.AsyncClient(headers={'Authorization':f'Bearer {TOKEN}'})
    async with streamablehttp_client(URL,http_client=client) as (read,write):
      async with ClientSession(read,write) as s:
        await s.initialize()
        for c in calls:
          try:
            r=await s.call_tool(c['tool'],c.get('args',{}))
            out.append({'tool':c['tool'],'args':c.get('args',{}),'isError':getattr(r,'isError',getattr(r,'is_error',False)),'content':[getattr(x,'text',str(x)) for x in (r.content or [])], 'structuredContent':getattr(r,'structuredContent',getattr(r,'structured_content',None))})
          except Exception as e: out.append({'tool':c['tool'],'args':c.get('args',{}),'exception':repr(e)})
    await client.aclose()
    print(json.dumps(out,indent=2,default=str))
asyncio.run(main())

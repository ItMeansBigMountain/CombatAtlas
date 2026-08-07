import asyncio,json,sys
import httpx
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
TOKEN=json.load(open('/opt/data/mcp-tokens/robinhood_trading.json'))['access_token']; URL='https://agent.robinhood.com/mcp/trading'
async def main():
 calls=json.load(open(sys.argv[1])); out=[]
 client=httpx.AsyncClient(headers={'Authorization':f'Bearer {TOKEN}'},timeout=120)
 try:
  async with streamable_http_client(URL,http_client=client) as streams:
   read,write=streams[0],streams[1]
   async with ClientSession(read,write) as s:
    await s.initialize()
    for c in calls:
     try:
      r=await s.call_tool(c['tool'],c.get('args',{})); out.append({'tool':c['tool'],'args':c.get('args',{}),'isError':getattr(r,'isError',False),'content':[getattr(x,'text',str(x)) for x in (r.content or [])], 'structuredContent':getattr(r,'structuredContent',None)})
     except Exception as e: out.append({'tool':c['tool'],'args':c.get('args',{}),'exception':repr(e)})
 finally:
  await client.aclose()
 print(json.dumps(out,indent=2,default=str))
asyncio.run(main())

import asyncio,json,sys
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
TOKEN=json.load(open('/opt/data/mcp-tokens/robinhood_trading.json'))['access_token']; URL='https://agent.robinhood.com/mcp/trading'
async def main():
 calls=json.load(open(sys.argv[1])); out=[]
 async with streamablehttp_client(URL,headers={'Authorization':f'Bearer {TOKEN}'}) as (read,write,_):
  async with ClientSession(read,write) as s:
   await s.initialize()
   for c in calls:
    try:
     r=await s.call_tool(c['tool'],c.get('args',{})); out.append({'tool':c['tool'],'args':c.get('args',{}),'isError':r.isError,'content':[getattr(x,'text',str(x)) for x in (r.content or [])]})
    except Exception as e: out.append({'tool':c['tool'],'args':c.get('args',{}),'exception':repr(e)})
 print(json.dumps(out,indent=2,default=str))
asyncio.run(main())

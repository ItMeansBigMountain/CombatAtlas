import asyncio, json, sys
sys.path.insert(0,'/opt/hermes')
from tools.mcp_tool import _load_mcp_config, _connect_server

async def main():
    cfg=_load_mcp_config()['robinhood_trading']
    s=await _connect_server('robinhood_trading',cfg)
    try:
        if len(sys.argv)==1:
            tools=await s.session.list_tools()
            print(json.dumps([{'name':t.name,'inputSchema':t.inputSchema} for t in tools.tools],indent=2))
        else:
            calls=json.loads(open(sys.argv[1]).read())
            out=[]
            for c in calls:
                try:
                    r=await s.session.call_tool(c['tool'],arguments=c.get('args',{}))
                    texts=[getattr(x,'text',None) for x in (r.content or []) if getattr(x,'text',None)]
                    out.append({'tool':c['tool'],'args':c.get('args',{}),'isError':r.isError,'content':texts,'structuredContent':getattr(r,'structuredContent',None)})
                except Exception as e:
                    out.append({'tool':c['tool'],'args':c.get('args',{}),'exception':repr(e)})
            print(json.dumps(out,indent=2,default=str))
    finally:
        await s.shutdown()
asyncio.run(main())

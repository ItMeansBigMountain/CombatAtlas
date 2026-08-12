import os,json,urllib.request,urllib.error,concurrent.futures,datetime,time
TOKEN=os.environ.get('VERCEL_TOKEN') or os.environ.get('VERCEL_API_TOKEN')
TEAM='team_9IP8D1xXFQSrBMZrMjRnl9sD'
BASE='https://api.vercel.com'
def api(path):
 req=urllib.request.Request(BASE+path,headers={'Authorization':'Bearer '+TOKEN,'User-Agent':'Hermes-nondestructive-audit'})
 with urllib.request.urlopen(req,timeout=40) as r:return json.load(r)
def get_all_projects():
 out=[]; until=None
 while True:
  p=f'/v9/projects?limit=100&teamId={TEAM}'+(f'&until={until}' if until else '')
  d=api(p); out += d.get('projects',[])
  until=d.get('pagination',{}).get('next')
  if not until: return out
def check(host):
 if not host:return None
 url='https://'+host
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 HermesAudit'},method='GET')
 try:
  with urllib.request.urlopen(req,timeout=20) as r:
   body=r.read(120000).decode('utf-8','replace')
   return {'status':r.status,'final_url':r.url,'content_type':r.headers.get('content-type'),'title':(body.split('<title>',1)[1].split('</title>',1)[0][:200] if '<title>' in body.lower() else None),'bytes_sampled':len(body)}
 except urllib.error.HTTPError as e:return {'status':e.code,'final_url':e.url,'error':str(e)}
 except Exception as e:return {'status':None,'error':type(e).__name__+': '+str(e)[:160]}
projects=get_all_projects(); rows=[]
for i,p in enumerate(projects,1):
 pid=p['id']; name=p['name']
 try: dep=api(f'/v6/deployments?projectId={pid}&teamId={TEAM}&target=production&limit=1').get('deployments',[])
 except Exception as e: dep=[]
 d=dep[0] if dep else {}
 try: envs=api(f'/v10/projects/{pid}/env?teamId={TEAM}').get('envs',[])
 except Exception: envs=[]
 try: domains=api(f'/v9/projects/{pid}/domains?teamId={TEAM}').get('domains',[])
 except Exception: domains=[]
 prod=(p.get('targets') or {}).get('production') or {}
 aliases=prod.get('alias') or d.get('alias') or []
 primary=next((a for a in aliases if a==name+'.vercel.app'),aliases[0] if aliases else None)
 rows.append({'name':name,'id':pid,'framework':p.get('framework'),'updatedAt':p.get('updatedAt'),'gitRepository':p.get('link'),'protection':{'deploymentType':p.get('deploymentType'),'passwordProtection':bool(p.get('passwordProtection')),'ssoProtection':p.get('ssoProtection'),'trustedIps':p.get('trustedIps'),'protectionBypass':bool(p.get('protectionBypass'))},'env_names':sorted(set(e.get('key') for e in envs if e.get('key'))),'env_targets':{k:sorted(set(t for e in envs if e.get('key')==k for t in (e.get('target') or []))) for k in sorted(set(e.get('key') for e in envs if e.get('key')))},'domains':[{'name':x.get('name'),'verified':x.get('verified'),'redirect':x.get('redirect')} for x in domains],'aliases':aliases,'primary_alias':primary,'latest':{'id':d.get('uid'),'url':d.get('url'),'state':d.get('state') or d.get('readyState'),'created':d.get('created'),'target':d.get('target'),'gitCommitSha':(d.get('meta') or {}).get('githubCommitSha') or (d.get('meta') or {}).get('gitCommitSha'),'gitCommitRef':(d.get('meta') or {}).get('githubCommitRef') or (d.get('meta') or {}).get('gitCommitRef')}})
 print(f'{i}/{len(projects)} {name}',flush=True)
hosts=set()
for r in rows:
 if r['primary_alias']:hosts.add(r['primary_alias'])
 if r['latest']['url']:hosts.add(r['latest']['url'])
 for a in r['aliases']:hosts.add(a)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex: checks=dict(zip(hosts,ex.map(check,hosts)))
for r in rows:
 r['health']={'primary':checks.get(r['primary_alias']),'latest':checks.get(r['latest']['url']),'aliases':{a:checks.get(a) for a in r['aliases']}}
out={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'team':TEAM,'project_count':len(rows),'projects':rows}
with open('/opt/data/HeRmEz/projects/_ops/vercel-live-audit-2026-08-12.json','w') as f:json.dump(out,f,indent=2)

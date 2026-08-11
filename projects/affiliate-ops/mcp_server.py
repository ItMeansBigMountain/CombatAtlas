#!/usr/bin/env python3
"""Amazon Affiliate MCP server for authenticated Hermes chat operations."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))

def load_secret_env(path=Path('/opt/data/secrets/affiliate-ops/creators.env')):
 """Load the MCP's dedicated 0600 credential file without logging values."""
 if not path.exists(): return
 for raw in path.read_text(encoding='utf-8').splitlines():
  line=raw.strip()
  if not line or line.startswith('#') or '=' not in line: continue
  key,value=line.split('=',1)
  key=key.removeprefix('export ').strip(); value=value.strip().strip('"').strip("'")
  if key.startswith('AMAZON_') and key not in __import__('os').environ: __import__('os').environ[key]=value

load_secret_env()
from mcp.server.fastmcp import FastMCP
import affiliate_ops as ops
from creators_api import CreatorsAPI, NotConfigured

mcp=FastMCP('amazon-affiliate')

def rows(sql,args=()):
 with ops.connect() as db: return [dict(r) for r in db.execute(sql,args).fetchall()]

@mcp.tool()
def account_status() -> str:
 """Show Amazon affiliate accounts, tracking/payment/tax readiness, and active-link counts without secrets."""
 return json.dumps(rows('''SELECT p.slug program,p.marketplace,a.alias,a.status,a.tracking_id,a.payment_method,a.payment_status,a.last_verified_at,t.interview_status tax_status,t.form_type,t.submitted_on,t.renewal_due,(SELECT count(*) FROM links l WHERE l.account_id=a.id AND l.active=1) active_links FROM accounts a JOIN programs p ON p.id=a.program_id LEFT JOIN tax_profiles t ON t.account_id=a.id ORDER BY a.alias'''),indent=2)

@mcp.tool()
def list_links(account_alias: str='amazon-us-primary') -> str:
 """List registered approved affiliate links and their campaign/channel attribution."""
 return json.dumps(rows('''SELECT l.label,l.destination_url,l.affiliate_url,l.asin,l.campaign,l.channel,l.active,l.verified_at FROM links l JOIN accounts a ON a.id=l.account_id WHERE a.alias=? ORDER BY l.label''',(account_alias,)),indent=2)

@mcp.tool()
def set_tracking_id(account_alias: str, tracking_id: str) -> str:
 """Record a real public Amazon tracking ID read from Associates Central. Never pass passwords or tax/bank data."""
 tracking_id=tracking_id.strip()
 if not tracking_id or len(tracking_id)>100 or any(c.isspace() for c in tracking_id): raise ValueError('invalid tracking ID')
 with ops.connect() as db:
  a=db.execute('SELECT id FROM accounts WHERE alias=?',(account_alias,)).fetchone()
  if not a: raise ValueError('unknown account alias')
  db.execute('UPDATE accounts SET tracking_id=?,last_verified_at=? WHERE id=?',(tracking_id,ops.now(),a['id']))
  ops.audit(db,'update','account',a['id'],{'tracking_id_updated':True}); db.commit()
 return json.dumps({'status':'updated','account_alias':account_alias,'tracking_id':tracking_id})

@mcp.tool()
def register_amazon_link(account_alias: str,label: str,destination_url: str,asin: str='',campaign: str='',channel: str='youtube') -> str:
 """Create and register a tagged amazon.com Special Link using the account's verified tracking ID."""
 with ops.connect() as db:
  a=db.execute('SELECT id,tracking_id FROM accounts WHERE alias=?',(account_alias,)).fetchone()
  if not a: raise ValueError('unknown account alias')
  if not a['tracking_id']: raise ValueError('tracking ID missing; read it from Associates Central first')
  url=ops.safe_affiliate_url(destination_url,a['tracking_id'])
  cur=db.execute('''INSERT INTO links(account_id,label,destination_url,affiliate_url,asin,campaign,channel,verified_at,created_at) VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(account_id,label,channel) DO UPDATE SET destination_url=excluded.destination_url,affiliate_url=excluded.affiliate_url,asin=excluded.asin,campaign=excluded.campaign,active=1,verified_at=excluded.verified_at''',(a['id'],label,destination_url,url,asin or None,campaign or None,channel,ops.now(),ops.now()))
  ops.audit(db,'upsert','link',cur.lastrowid,{'label':label,'channel':channel}); db.commit()
 return json.dumps({'status':'registered','affiliate_url':url,'label':label,'channel':channel})

@mcp.tool()
def set_tax_interview_status(account_alias: str,status: str,form_type: str='',jurisdiction: str='US',submitted_on: str='',renewal_due: str='',secure_document_ref: str='') -> str:
 """Record tax-interview metadata only. Never pass TIN/SSN, tax answers, or document contents."""
 allowed={'unknown','not_started','pending','validated','completed','needs_action','invalid'}
 if status not in allowed: raise ValueError('invalid status')
 if any(x in secure_document_ref.upper() for x in ('SSN','TIN=')): raise ValueError('do not store tax identifiers')
 with ops.connect() as db:
  a=db.execute('SELECT id FROM accounts WHERE alias=?',(account_alias,)).fetchone()
  if not a: raise ValueError('unknown account alias')
  db.execute('''INSERT INTO tax_profiles(account_id,interview_status,form_type,jurisdiction,submitted_on,renewal_due,secure_document_ref) VALUES(?,?,?,?,?,?,?) ON CONFLICT(account_id) DO UPDATE SET interview_status=excluded.interview_status,form_type=excluded.form_type,jurisdiction=excluded.jurisdiction,submitted_on=excluded.submitted_on,renewal_due=excluded.renewal_due,secure_document_ref=excluded.secure_document_ref''',(a['id'],status,form_type or None,jurisdiction,submitted_on or None,renewal_due or None,secure_document_ref or None))
  ops.audit(db,'update','tax_profile',a['id'],{'status':status,'form_type':form_type}); db.commit()
 return json.dumps({'status':'updated','account_alias':account_alias,'tax_status':status})

@mcp.tool()
def set_payment_status(account_alias: str,method: str,status: str) -> str:
 """Record payment readiness metadata only. Never pass bank/routing/account numbers."""
 if method not in {'unknown','direct_deposit','gift_certificate','check'}: raise ValueError('invalid payment method')
 if status not in {'unknown','not_started','pending','configured','verified','needs_action','failed'}: raise ValueError('invalid payment status')
 with ops.connect() as db:
  a=db.execute('SELECT id FROM accounts WHERE alias=?',(account_alias,)).fetchone()
  if not a: raise ValueError('unknown account alias')
  db.execute('UPDATE accounts SET payment_method=?,payment_status=?,last_verified_at=? WHERE id=?',(method,status,ops.now(),a['id']))
  ops.audit(db,'update','account',a['id'],{'payment_method':method,'payment_status':status}); db.commit()
 return json.dumps({'status':'updated','account_alias':account_alias,'payment_method':method,'payment_status':status})

@mcp.tool()
def creators_api_status() -> str:
 """Report whether Amazon Creators API credentials and partner tag are configured; never reveal secrets."""
 c=CreatorsAPI()
 return json.dumps({'configured':c.ready(),'marketplace':c.marketplace,'partner_tag_present':bool(c.partner_tag),'credential_id_present':bool(c.client_id),'credential_secret_present':bool(c.secret)})

@mcp.tool()
def amazon_get_items(asins: list[str]) -> str:
 """Fetch current Amazon product title, image URL, offers, and exact vended affiliate links using authenticated Creators API."""
 return json.dumps(CreatorsAPI().get_items(asins))

if __name__=='__main__':
 ops.seed(ops.connect())
 mcp.run(transport='stdio')

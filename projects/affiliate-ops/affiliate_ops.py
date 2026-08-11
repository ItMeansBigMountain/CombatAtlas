#!/usr/bin/env python3
"""Local Amazon-first affiliate registry. Stores metadata, never raw tax IDs or API secrets."""
from __future__ import annotations
import argparse, json, os, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

ROOT=Path(__file__).resolve().parent
DB=Path(os.getenv('AFFILIATE_OPS_DB', ROOT/'data/affiliate_ops.db'))
SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS programs(id INTEGER PRIMARY KEY, slug TEXT UNIQUE NOT NULL, name TEXT NOT NULL, marketplace TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'active', dashboard_url TEXT, terms_url TEXT, payment_cycle TEXT, notes TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY, program_id INTEGER NOT NULL REFERENCES programs(id), alias TEXT UNIQUE NOT NULL, account_ref TEXT, tracking_id TEXT, status TEXT NOT NULL DEFAULT 'unknown', payment_method TEXT NOT NULL DEFAULT 'unknown', payment_status TEXT NOT NULL DEFAULT 'unknown', payee_country TEXT, secret_ref TEXT, last_verified_at TEXT, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tax_profiles(id INTEGER PRIMARY KEY, account_id INTEGER UNIQUE NOT NULL REFERENCES accounts(id), interview_status TEXT NOT NULL DEFAULT 'unknown', form_type TEXT, jurisdiction TEXT, submitted_on TEXT, renewal_due TEXT, secure_document_ref TEXT, notes TEXT, CHECK(secure_document_ref IS NULL OR secure_document_ref NOT LIKE '%SSN%'));
CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), label TEXT NOT NULL, destination_url TEXT NOT NULL, affiliate_url TEXT NOT NULL, asin TEXT, campaign TEXT, channel TEXT, active INTEGER NOT NULL DEFAULT 1, verified_at TEXT, created_at TEXT NOT NULL, UNIQUE(account_id,label,channel));
CREATE TABLE IF NOT EXISTS earnings(id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), period_start TEXT NOT NULL, period_end TEXT NOT NULL, clicks INTEGER, ordered_items INTEGER, shipped_items INTEGER, revenue REAL, commissions REAL, currency TEXT DEFAULT 'USD', source TEXT, imported_at TEXT NOT NULL, UNIQUE(account_id,period_start,period_end,source));
CREATE TABLE IF NOT EXISTS audit_log(id INTEGER PRIMARY KEY, at TEXT NOT NULL, action TEXT NOT NULL, entity TEXT NOT NULL, entity_id INTEGER, details TEXT);
'''

def now(): return datetime.now(timezone.utc).isoformat()
def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(DB); db.row_factory=sqlite3.Row; db.executescript(SCHEMA); return db

def audit(db,action,entity,entity_id=None,details=None):
    db.execute('INSERT INTO audit_log(at,action,entity,entity_id,details) VALUES(?,?,?,?,?)',(now(),action,entity,entity_id,json.dumps(details or {})))

def seed(db):
    db.execute("INSERT OR IGNORE INTO programs(slug,name,marketplace,status,dashboard_url,terms_url,payment_cycle,created_at) VALUES(?,?,?,?,?,?,?,?)",('amazon-us','Amazon Associates','amazon.com','active','https://affiliate-program.amazon.com/home','https://affiliate-program.amazon.com/help/operating/agreement','approximately 60 days after month end',now()))
    db.commit()

def safe_affiliate_url(destination,tracking_id):
    p=urlparse(destination)
    if p.scheme!='https' or p.netloc.lower() not in {'amazon.com','www.amazon.com'}: raise ValueError('Amazon destination must be an https amazon.com URL')
    q=dict(parse_qsl(p.query,keep_blank_values=True)); q['tag']=tracking_id
    return urlunparse((p.scheme,p.netloc,p.path,p.params,urlencode(q),''))

def add_account(db,args):
    pid=db.execute('SELECT id FROM programs WHERE slug=?',(args.program,)).fetchone()
    if not pid: raise ValueError('unknown program')
    cur=db.execute('INSERT INTO accounts(program_id,alias,account_ref,tracking_id,status,payment_method,payment_status,payee_country,secret_ref,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(pid['id'],args.alias,args.account_ref,args.tracking_id,args.status,args.payment_method,args.payment_status,args.country,args.secret_ref,now()))
    audit(db,'create','account',cur.lastrowid,{'alias':args.alias}); db.commit()

def add_link(db,args):
    account=db.execute('SELECT id,tracking_id FROM accounts WHERE alias=?',(args.account,)).fetchone()
    if not account: raise ValueError('unknown account')
    tracking=args.tracking_id or account['tracking_id']
    if not tracking: raise ValueError('tracking ID required; do not invent one')
    affiliate=safe_affiliate_url(args.destination,tracking)
    cur=db.execute('INSERT INTO links(account_id,label,destination_url,affiliate_url,asin,campaign,channel,verified_at,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(account['id'],args.label,args.destination,affiliate,args.asin,args.campaign,args.channel,now(),now()))
    audit(db,'create','link',cur.lastrowid,{'label':args.label,'channel':args.channel}); db.commit(); print(affiliate)

def set_tax(db,args):
    a=db.execute('SELECT id FROM accounts WHERE alias=?',(args.account,)).fetchone()
    if not a: raise ValueError('unknown account')
    db.execute('INSERT INTO tax_profiles(account_id,interview_status,form_type,jurisdiction,submitted_on,renewal_due,secure_document_ref,notes) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(account_id) DO UPDATE SET interview_status=excluded.interview_status,form_type=excluded.form_type,jurisdiction=excluded.jurisdiction,submitted_on=excluded.submitted_on,renewal_due=excluded.renewal_due,secure_document_ref=excluded.secure_document_ref,notes=excluded.notes',(a['id'],args.status,args.form,args.jurisdiction,args.submitted,args.renewal,args.document_ref,args.notes))
    audit(db,'update','tax_profile',a['id'],{'status':args.status,'form':args.form}); db.commit()

def report(db):
    seed(db)
    rows=db.execute('''SELECT p.name,p.marketplace,a.alias,a.status,a.tracking_id,a.payment_method,a.payment_status,a.last_verified_at,t.interview_status tax_status,t.form_type,t.renewal_due,(SELECT count(*) FROM links l WHERE l.account_id=a.id AND l.active=1) links FROM accounts a JOIN programs p ON p.id=a.program_id LEFT JOIN tax_profiles t ON t.account_id=a.id ORDER BY a.alias''').fetchall()
    print(json.dumps([dict(r) for r in rows],indent=2))

def export_env(db,args):
    rows=db.execute('SELECT label,affiliate_url FROM links l JOIN accounts a ON a.id=l.account_id WHERE a.alias=? AND l.active=1',(args.account,)).fetchall()
    mapping={'daily-stoic-life':'DAILY_STOIC_AFFILIATE_URL','ryan-obstacle':'RYAN_HOLIDAY_AFFILIATE_URL','robert-48-laws':'ROBERT_GREENE_AFFILIATE_URL'}
    for r in rows:
        if r['label'] in mapping: print(f"{mapping[r['label']]}={r['affiliate_url']}")

def parser():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest='cmd',required=True)
    s.add_parser('init'); s.add_parser('report')
    a=s.add_parser('add-account'); a.add_argument('--program',default='amazon-us'); a.add_argument('--alias',required=True); a.add_argument('--account-ref'); a.add_argument('--tracking-id'); a.add_argument('--status',default='active'); a.add_argument('--payment-method',default='unknown'); a.add_argument('--payment-status',default='unknown'); a.add_argument('--country',default='US'); a.add_argument('--secret-ref')
    l=s.add_parser('add-link'); l.add_argument('--account',required=True); l.add_argument('--label',required=True); l.add_argument('--destination',required=True); l.add_argument('--tracking-id'); l.add_argument('--asin'); l.add_argument('--campaign'); l.add_argument('--channel',default='youtube')
    t=s.add_parser('set-tax'); t.add_argument('--account',required=True); t.add_argument('--status',required=True); t.add_argument('--form'); t.add_argument('--jurisdiction',default='US'); t.add_argument('--submitted'); t.add_argument('--renewal'); t.add_argument('--document-ref'); t.add_argument('--notes')
    e=s.add_parser('export-env'); e.add_argument('--account',required=True)
    return p

def main():
    args=parser().parse_args(); db=connect(); seed(db)
    {'init':lambda: print(DB),'report':lambda: report(db),'add-account':lambda: add_account(db,args),'add-link':lambda: add_link(db,args),'set-tax':lambda: set_tax(db,args),'export-env':lambda: export_env(db,args)}[args.cmd]()
if __name__=='__main__': main()

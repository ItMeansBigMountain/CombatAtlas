#!/usr/bin/env python3
"""Localhost-only dashboard for affiliate operational status."""
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from affiliate_ops import connect, seed

CSS='''body{font-family:system-ui;background:#0f172a;color:#e2e8f0;margin:0}main{max-width:1100px;margin:auto;padding:32px}h1{color:#f59e0b}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}.card,table{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px}table{width:100%;border-collapse:collapse;margin-top:24px}th,td{text-align:left;padding:12px;border-bottom:1px solid #334155}.ok{color:#4ade80}.warn{color:#fbbf24}.bad{color:#fb7185}code{color:#93c5fd}'''
def cls(v): return 'ok' if str(v).lower() in {'active','complete','completed','verified','paid'} else 'warn' if v else 'bad'
class H(BaseHTTPRequestHandler):
 def do_GET(self):
  db=connect(); seed(db)
  ac=db.execute('''SELECT p.name,a.alias,a.status,a.tracking_id,a.payment_method,a.payment_status,t.interview_status tax_status,t.form_type,t.renewal_due FROM accounts a JOIN programs p ON p.id=a.program_id LEFT JOIN tax_profiles t ON t.account_id=a.id''').fetchall()
  links=db.execute('''SELECT a.alias,l.label,l.affiliate_url,l.channel,l.verified_at FROM links l JOIN accounts a ON a.id=l.account_id WHERE l.active=1''').fetchall()
  money=db.execute('SELECT COALESCE(SUM(commissions),0) total,COALESCE(SUM(clicks),0) clicks FROM earnings').fetchone()
  rows=''.join(f"<tr><td>{escape(r['alias'])}</td><td class={cls(r['status'])}>{escape(r['status'])}</td><td><code>{escape(r['tracking_id'] or 'MISSING')}</code></td><td class={cls(r['tax_status'])}>{escape(r['tax_status'] or 'unknown')}</td><td>{escape(r['payment_method'])} / {escape(r['payment_status'])}</td></tr>" for r in ac) or '<tr><td colspan=5>No account metadata yet. Add it with the CLI.</td></tr>'
  lrows=''.join(f"<tr><td>{escape(r['alias'])}</td><td>{escape(r['label'])}</td><td><a href='{escape(r['affiliate_url'])}' style='color:#60a5fa'>link</a></td><td>{escape(r['channel'])}</td><td>{escape(r['verified_at'] or 'not verified')}</td></tr>" for r in links) or '<tr><td colspan=5>No tracked links yet.</td></tr>'
  body=f'''<!doctype html><title>Affiliate Ops</title><style>{CSS}</style><main><h1>Affiliate Operations</h1><div class=cards><div class=card><h3>Accounts</h3><b>{len(ac)}</b></div><div class=card><h3>Tracked links</h3><b>{len(links)}</b></div><div class=card><h3>Imported clicks</h3><b>{money['clicks']}</b></div><div class=card><h3>Imported commissions</h3><b>${money['total']:.2f}</b></div></div><h2>Account readiness</h2><table><tr><th>Alias</th><th>Status</th><th>Tracking ID</th><th>Tax interview</th><th>Payment</th></tr>{rows}</table><h2>Links</h2><table><tr><th>Account</th><th>Label</th><th>URL</th><th>Channel</th><th>Verified</th></tr>{lrows}</table><p>Local operational metadata only. Raw TIN/SSN, bank details, passwords, and API keys are intentionally excluded.</p></main>'''
  b=body.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def log_message(self, format, *args):
  pass
if __name__=='__main__':
 print('Affiliate Ops UI: http://127.0.0.1:8765'); HTTPServer(('127.0.0.1',8765),H).serve_forever()

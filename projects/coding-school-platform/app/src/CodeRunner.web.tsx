import { useMemo } from 'react';

export function CodeRunner({ code }: { code: string }) {
  const document = useMemo(() => `<!doctype html><meta charset="utf-8"><style>body{font:14px system-ui;background:#0f172a;color:#dbeafe;padding:16px}pre{white-space:pre-wrap;color:#d1fae5}.note{color:#93c5fd}</style><strong>Secure practice preview</strong><p class="note">Code is displayed in a sandboxed, script-free frame. Execution belongs in a separately audited runner service.</p><pre>${escapeHtml(code)}</pre>`, [code]);
  return (
    <iframe
      title="Secure coding sandbox preview"
      sandbox=""
      srcDoc={document}
      style={{ width: '100%', height: 220, border: 0, borderRadius: 16, background: '#0f172a' }}
    />
  );
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' })[character] ?? character);
}

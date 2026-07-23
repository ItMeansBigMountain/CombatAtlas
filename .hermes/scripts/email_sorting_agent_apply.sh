#!/usr/bin/env bash
set -euo pipefail
OUT=$(python3 /opt/data/scripts/email_sorting_agent.py --apply --max-results 250)
EMAIL_SORT_OUT="$OUT" python3 - <<'PY'
import json, os

d = json.loads(os.environ.get("EMAIL_SORT_OUT", "{}"))
profiles = d.get("profiles", [])
count = sum(p.get("match_count", 0) for p in profiles)
blocked = [p for p in profiles if not p.get("ok")]
lines = []
if count:
    lines.append(f"**Email sorting agent** moved {count} newsletter/source emails into Hermes labels.")
    for p in profiles:
        matches = p.get("matches", [])
        if not matches:
            continue
        account = p.get("email", "unknown")
        lines.append(f"\n**{p['profile']} — {account}** ({len(matches)} sorted)")
        for m in matches:
            sender = m.get("from") or "Unknown sender"
            subject = m.get("subject") or "(no subject)"
            label = m.get("label") or "Hermes"
            lines.append(f"- **{subject}** — {sender} → `{label}`")
if blocked:
    lines.append("**Email sorting agent auth/service blocks:**")
    for p in blocked:
        reason = p.get("blocked") or "error"
        err = str(p.get("error", ""))[:220]
        lines.append(f"- **{p['profile']}** ({p.get('email','unknown')}): {reason} — {err}")
if lines:
    print("\n".join(lines))
PY

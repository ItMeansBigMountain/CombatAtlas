#!/usr/bin/env bash
set -euo pipefail
OUT=$(python3 /opt/data/scripts/email_sorting_agent.py --apply --max-results 250)
COUNT=$(printf '%s' "$OUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(p.get("match_count",0) for p in d.get("profiles",[])))')
if [ "$COUNT" != "0" ]; then
  printf '%s' "$OUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("**Email sorting agent** moved %s newsletter/source emails into Hermes labels." % sum(p.get("match_count",0) for p in d.get("profiles",[])));\
[print(f"- **{p[\"profile\"]}**: {p.get(\"match_count\",0)}") for p in d.get("profiles",[]) if p.get("match_count",0)]'
fi

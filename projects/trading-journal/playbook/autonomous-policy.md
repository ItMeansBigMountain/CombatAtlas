# Autonomous Trading Policy — Robinhood Agentic Account 1041

Status: ACTIVE as of 2026-06-12 by user message: "Activate autonomous trading for Agentic account 1041 with the policy above and kill switch below $10."
Account: Robinhood Agentic account ending 1041
Account number: 433711041
Starting capital: about $200 cash

## Authority
Hermes is authorized to research, preview, place, manage, and exit trades without per-trade approval for this Agentic account only, provided every action stays within this policy.

## Scope
- Account: 1041 / 433711041 only
- Equities only by default
- Fractional shares allowed
- Options disabled unless separately authorized
- Shorts disabled unless separately authorized
- Avoid low-liquidity names, wide spreads, unclear stops, forced trades, and revenge trades

## Risk / Budget
- Max risk per trade: target about $2 unless user changes
- Max aggregate planned open risk: target about $6 unless user changes
- Prefer starter positions around $25-$50
- Max initial single position allocation: $50 unless a later policy update changes this
- Keep some cash available for better entries/adds unless a plan justifies deployment
- Minimum R:R: 1.5:1, prefer 2:1+

## Kill Switch
- Stop trading if account value drops below $10.
- Stop if broker/account/tool state is uncertain.
- Stop if risk cannot be calculated from live data.
- Stop if no clean setup exists.

## Workflow
1. Inspect account, positions, open orders, buying power.
2. Inspect broad market and candidate quotes/historicals.
3. Select liquid fractional-tradable equity setups.
4. Review orders before placement when available.
5. Place only inside policy.
6. Journal every preview, placement, fill, management action, and exit.

## Management
- Do not add to losing trades unless the original plan included scaling and the live setup remains valid.
- Never move stops farther away from original risk.
- If stop/exit cannot be automated directly, monitor and execute exits during scans/management checks.
- If tools fail during management, stop and report tool failure.

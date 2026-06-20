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
- User update 2026-06-19: use most available funds when clean setups exist, maximizing leverage of the Agentic stock-market sandbox while staying inside live risk controls.
- Target deployment: 70%–90% of account value across open equity positions when account/market state is clear and trade plans justify entries.
- Avoid idle cash as the default; do not force trades when no clean setup exists.
- Max risk per trade: target about $2 by default; may increase only when a written trade plan shows clear invalidation and higher deployment is justified.
- Max aggregate planned open risk: target about $6 by default; may increase only with written plan, live account verification, and clear stop/invalidation math.
- Fractional-share starter positions may exceed the old $25-$50 guideline when liquidity, risk, and buying power support it.
- No fixed $50 initial-position cap after the 2026-06-19 user update; size from risk, buying power, liquidity, and plan quality.
- Keep enough cash available for exits, broker buffers, and superior entries unless a written plan justifies fuller deployment.
- Minimum R:R: 1.5:1, prefer 2:1+
- Daily drawdown pause: if account is down 5%+ in one day or 10%+ from recent high, pause new entries and write a review before resuming

## Kill Switch
- Stop trading if account value drops below $10.
- Stop if broker/account/tool state is uncertain.
- Stop if risk cannot be calculated from live data.
- Stop if no clean setup exists.

## Workflow
1. Inspect account, positions, open orders, buying power.
2. Inspect broad market and sector regime: SPY/QQQ/IWM plus relevant sector ETFs when applicable.
3. Combine technical analysis with fundamental/news context before selecting or managing trades:
   - Technicals: trend, support/resistance, breakout/pullback/retest, relative strength, volume confirmation, volatility, invalidation.
   - Fundamentals/news: earnings/revenue growth, margin/cash-flow quality where available, balance-sheet stress, guidance, analyst/institutional catalysts, macro/sector flows, and asset/sector cash-flow rotation.
4. Select liquid fractional-tradable equity setups where both chart structure and fundamental/news/sector context support the trade.
5. Build a concrete thesis with entry, stop/invalidation, target, position size, max loss, potential reward, R:R, technical basis, fundamental/news basis, sector/cash-flow basis, and reason to avoid/exit.
6. Review orders before placement when available.
7. Place only inside policy.
8. Journal every preview, placement, fill, management action, exit, no-trade decision, and tool failure.

## Management
- Treat Robinhood MCP as connectivity, not the strategy; Hermes must run the policy/playbook explicitly each scan.
- Do not add to losing trades unless the original plan included scaling and the live setup remains valid.
- Never average down just because price is lower.
- Never move stops farther away from original risk.
- If a position loses ~8% from entry or breaches thesis/invalidation, review for exit rather than adding.
- If stop/exit cannot be automated directly, monitor and execute exits during scans/management checks.
- If tools fail during management, stop and report tool failure.

## Research notes
- See `agentic-trading-research-notes.md` for source review and patterns to mimic/avoid.

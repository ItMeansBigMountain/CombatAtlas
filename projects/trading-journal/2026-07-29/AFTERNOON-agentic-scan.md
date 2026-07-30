# AFTERNOON Agentic Swing/Rotation Scan — 2026-07-29

- Scan time: 17:31–17:33 UTC / 13:31–13:33 ET
- Account: Robinhood Agentic 433711041 / ending 1041 only
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only
- Decision: **HOLD JPM and UL; accept/reconcile the earlier SLB stop exit; NO NEW ENTRY OR ROTATION immediately before the 14:00 ET FOMC decision.** No stop was widened and no losing position was added.

## Live broker state and kill switches

- MCP connected; account 433711041 is active, cash, Agentic, and `agentic_allowed=true`. No other account was operated.
- Portfolio: total value **$181.8071**, equity value **$102.0171**, cash **$79.79**, but broker-reported liquid/unleveraged buying power only **$8.46** (the SLB sale proceeds appear not yet available as buying power). Pending deposits $0.
- Positions: JPM 0.195159 @ $341.67 and UL 0.508952 @ $66.47; both fully sellable.
- Open-ish equity states separately checked and empty: `new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`. Pending notional $0; liquid buying power after pending orders **$8.46**.
- Recent fills: **SLB sell 1.443558 @ $49.4126 at 16:03:01 UTC, filled, $71.33 proceeds, $0 fees**; UL buy 0.508952 @ $66.4699 on July 28; NVDA sell 0.121165 @ $198.0666 on July 27.
- Kill switch clear: account value >$10; about **-1.05%** versus the post-open $183.7372 reference and **-3.99%** from the recent observed $189.3684 high, below both drawdown pauses. Broker state is coherent enough to manage, but buying power—not cash—is used for sizing.

## Market/sector regime

- Live SPY $735.94 (-0.66%), QQQ $669.51 (-0.89%), IWM $289.83 (-1.21%); all are below their completed 10/20-day averages. QQQ/XLK and semiconductors are the weakest pocket; SMH was -3.26% with a roughly -18.9% 20-day return.
- Rotation favors energy and defensives: XLE $58.79 (+2.12%), XLP $87.49 (+0.49%); XOM +2.80%. Financials remain in an intermediate uptrend but weakened today (XLF -0.76%; JPM -2.06%).
- Macro risk is binary and imminent: FOMC statement at 14:00 ET and press conference at 14:30 ET amid elevated inflation/oil/geopolitical uncertainty. Major technology earnings and next-day GDP/PCE add gap risk. This prevents a clean pre-event entry despite mechanically deployable buying power.

## Position management

### JPM — HOLD
- Live $349.94, bid/ask $349.92/$350.05; value **$68.29**; unrealized **+$1.61**.
- Still above SMA10 ~$346.57 and SMA20 ~$340.25 with +6.2% 20-day strength, but rejected below $356–359 resistance and weakened with financials ahead of FOMC.
- Fundamentals remain supportive: strong Q2 revenue/EPS growth and upward 2026 estimate revisions; key risks are rate-path surprise and credit/capital-markets sensitivity.
- Binding reassessment/exit **$346**; targets **$365/$375**. Mark-to-stop risk ~$0.77. Do not widen or add.

### UL — HOLD
- Live $66.285, bid/ask $66.28/$66.29; value **$33.74**; unrealized **-$0.09**.
- Above SMA10/20/50 (~$61.45/$61.48/$59.18); earnings-gap structure remains intact. ATR14 ~$1.50 and the narrow spread support manageability.
- Q2 underlying sales growth reportedly 5.8%, power-brand growth 6.9%, stronger volume, margin resilience, and upgraded 4%–6% full-year outlook support the thesis; currency/inflation and post-gap supply are risks.
- Binding reassessment/exit **$63.70**; targets **$70.75/$74.90**. Mark-to-stop risk ~$1.32. No averaging down.

## Ranked candidates

1. **UL — 7.8/10, existing hold.** Catalyst-backed defensive strength, clean failed-gap invalidation, and tight liquidity.
2. **JPM — 7.4/10, existing hold.** Positive earnings revisions and intermediate trend, but today's rejection and FOMC sensitivity reduce score.
3. **AAPL — 7.2/10, wait.** $342.59, +21.6% 20-day strength and above SMA10/20, but at a fresh 20-day/52-week high, low partial-day volume, rich ~40x P/E, weak tech tape, and earnings due July 30 make entry extended.
4. **XOM — 7.0/10, wait for retest.** $157.32, +15.2% 20-day strength, energy leadership and geopolitical oil support; near breakout resistance with earnings July 31, so chasing fails entry-risk discipline.
5. **RTX — 6.9/10, wait.** $218.83, +16.8% 20-day strength and defense catalyst support, but near resistance and industrial sector weakness argue for a retest.
6. **CRM — 6.6/10, wait.** $188.13 (+3.65%), +19.1% 20-day strength, but 4.4% ATR and a sharp one-day extension without strong volume confirmation create poor immediate invalidation.

## Allocation and order actions

- Current equity exposure **$102.02 / 56.1%** of account value; total cash $79.79, but only **$8.46** is liquid buying power.
- Policy split of current liquid buying power: **$6.768 deployable / $1.692 reserve**. No pending orders.
- Existing planned mark-to-stop risk is approximately **$2.08**, within the ~$6 aggregate soft target.
- **Orders reviewed this scan: none. Orders placed/cancelled this scan: none. New cash deployed: $0. Liquid reserve: $8.46.** The exact 80% deployment target is deferred because no candidate offers clean pre-FOMC event risk; forcing a $6.77 fractional entry would violate the no-forced-trade gate.
- Existing stops are written reassessment levels, not confirmed broker-native stop orders; gap losses can exceed planned amounts.

## Tool/source record

Robinhood MCP supplied live account, portfolio, positions, five open-ish order-state checks, recent fills, quotes, daily OHLCV, fundamentals, earnings calendar, and tradability. Current web checks corroborated the FOMC timing/uncertainty, semiconductor weakness, energy strength, JPM estimate revisions/Q2 growth, and UL's upgraded outlook. No order-tool failure occurred.

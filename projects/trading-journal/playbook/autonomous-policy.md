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

## Strategy / Risk / Budget
- User update 2026-07-17: operate with a professional hedge-fund-style research process focused on technical analysis and swing trades, while incorporating current fundamental, earnings, macro, catalyst, and sector-flow trends. This describes the rigor and process; do not claim licensed hedge-fund status or guarantee returns.
- Seek more frequent high-quality swing-trade opportunities and manage turnover actively when technical structure or the thesis changes. "More frequent" never means forced trades, churning, or bypassing risk gates.
- Holding period: normally several days to several weeks, but exit or rotate sooner when stop/invalidation triggers, relative strength deteriorates, catalysts change, or a materially better risk-adjusted setup appears.
- At each decision-quality scan, calculate current liquid buying power after accounting for pending/open orders. Target deployment of exactly 80% of available liquid buying power into qualifying liquid equity setups, retaining a 20% cash buffer. Existing open-position exposure counts separately from currently available liquid balance; never spend the reserved buffer merely to hit a target.
- Deploy across 1–4 liquid, fractional-tradable equities when diversification and setup quality justify it. Concentrate only when one setup is materially superior and total planned risk remains acceptable.
- Avoid idle deployable cash beyond the 20% buffer as the default, but do not force trades when no clean setup exists.
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
0. Before each scan, load the active policy and any date-specific plan at `playbook/YYYY-MM-DD-trading-plan.md`; live broker/market data always overrides stale plan assumptions.
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

## 2026 evidence-based strategy overlay (ACTIVE 2026-08-10)

This overlay operationalizes current factor evidence without chasing whatever led most recently. It is subordinate to every account, kill-switch, and risk rule above.

### 1. Regime first
At every decision-quality scan, classify the tape before ranking stocks:
- **Trend/risk-on:** SPY and the candidate's sector ETF above rising SMA20 and SMA50, with healthy breadth/relative strength. Favor continuation, earnings-gap holds, and orderly pullback/retest entries.
- **Mixed/rotation:** indexes disagree or sector leadership changes quickly. Reduce starter size to 50%–75% of normal, demand sector-relative strength, and prefer retests over first-breakout chases.
- **Risk-off:** SPY below a falling SMA20/50, breadth weak, or event volatility disorderly. No new marginal longs; preserve cash and manage exits.
Do not infer regime from one index or one session alone. Record the evidence and classification.

### 2. Sector-neutral momentum plus revision/catalyst confirmation
Rank candidates against both the broad market and their own sector peers, not on raw percentage gain alone. A qualifying long should normally have:
- positive 20-day and 60-day relative strength versus SPY and its sector ETF;
- price above rising SMA20 and preferably SMA50;
- improving/positive earnings guidance, analyst estimate revisions, a verified earnings/revenue catalyst, or other material fundamental change;
- adequate liquidity, fractional tradability, and a clear invalidation.
Reject momentum caused only by an unverified headline, thin liquidity, or a one-day spike without follow-through.

### 3. Quality guardrail
Momentum is the entry engine; quality is a crash and durability filter. Prefer positive free cash flow, credible revenue/earnings growth, manageable leverage, and improving margins/guidance. Speculative or loss-making names require a direct catalyst, half-size starter, tighter time stop, and materially better expected reward. Never treat a low valuation by itself as a catalyst.

### 4. Entry tactics
Use only one of these labeled setups:
- **Earnings/catalyst gap hold:** direct verified catalyst, strong relative volume, price holds above VWAP or the first-day midpoint, then enters on consolidation/retest—not an opening chase.
- **Breakout-retest continuation:** close or sustained hold above defined resistance with volume confirmation, followed by a successful retest.
- **20-day trend pullback:** orderly pullback toward rising EMA20/SMA20 or prior breakout support while sector-relative strength remains intact.
A breakout without a catalyst or volume confirmation is a watch, not an entry. Avoid entries more than roughly 1 ATR above the chosen support/retest level unless the catalyst and intraday structure justify a smaller starter.

### 5. Crowding and concentration controls
2026 momentum leadership has been unusually strong and dispersed, increasing unwind risk. Therefore:
- do not hold more than two positions whose primary thesis is the same sector/theme unless written correlation and aggregate-risk analysis justifies it;
- when a position is extended, do not add solely because it is winning;
- if momentum leaders reverse together, sector ETF relative strength breaks, or breadth deteriorates sharply, reduce gross exposure rather than rotating among correlated leaders;
- compare every new candidate with the weakest holding and rotate only when the expected improvement clearly exceeds spread/slippage, tax, and thesis uncertainty.

### 6. Adaptive risk and exits
- Size from the binding technical stop using the existing dollar-risk limits; use ATR only to test whether the stop is realistic, never to widen it after entry.
- Start at 50%–75% normal size in mixed regimes, around major scheduled macro events, or for high-gap/high-beta setups; scale only after confirmation and only if total risk remains within policy.
- Add a **time stop**: if a breakout/gap setup shows no follow-through within 3–5 sessions or loses sector-relative strength, review for exit/rotation even before the price stop.
- At +1R, review whether to protect capital or trail beneath a new higher low; do not mechanically tighten into ordinary noise.
- Preserve winners while their trend/catalyst remains valid; cut invalidated positions instead of averaging down.

### 7. Scorecard and learning loop
Score every serious candidate from 0–2 on each dimension: market regime, sector-relative strength, 20/60-day momentum, catalyst/revisions, quality/cash flow, volume/entry confirmation, invalidation clarity, and reward-to-risk. Maximum 16.
- **13–16:** full-policy candidate (subject to risk and concentration).
- **10–12:** watch or reduced-size starter only.
- **Below 10:** no trade.
Journal the score at entry and outcome at exit. Review rolling results by setup type after every 20 closed trades; do not change rules from a handful of wins or losses.

### 8. Active-operator mandate (ACTIVE 2026-08-10)
The user wants greater activity, meaning faster evidence-based action—not more noise or forced turnover.
- Every market scan must produce a ranked **hold/trim/exit/rotate/add** decision for every position and score at least three fresh candidates when live data supports it.
- Maintain a weakest-holding ranking. A held position scoring below 10, losing its sector-relative trend, failing its 3–5-session time stop, or breaching invalidation should be exited or rotated promptly rather than passively carried.
- A 13+ candidate may replace the weakest valid holding when its setup is confirmed and the written expected improvement is material. A 10–12 candidate may receive a 50% starter only when there is available risk/buying power and no concentration violation.
- Use the opening scan for price discovery and triggers; use post-open/midday for confirmed entries and rotations; use afternoon/power hour for second-chance setups, profit protection, and overnight-risk decisions.
- Take partial or full profits when a target is reached and momentum/volume stalls; do not let a winner round-trip merely to avoid activity. For tiny fractional positions, prefer a full exit when a partial would be operationally trivial.
- Recycle proceeds only into a confirmed higher-scoring setup. Cash is acceptable when no setup qualifies.
- Never create activity by widening stops, averaging down, chasing >1 ATR extensions, adding a sixth holding, or recursively spending the 20% reserve.

## Research notes
- See `agentic-trading-research-notes.md` for source review and patterns to mimic/avoid.
- 2026 overlay evidence and citations are recorded in `2026-strategy-overlay-sources.md`.

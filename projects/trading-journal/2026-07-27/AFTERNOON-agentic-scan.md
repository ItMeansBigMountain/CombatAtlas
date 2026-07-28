# Robinhood Agentic AFTERNOON Swing Scan — 2026-07-27

- Scan: 17:31–17:35 UTC / 13:31–13:35 ET
- Authorized account only: **433711041 / ending 1041**
- Policy: `playbook/autonomous-policy.md` ACTIVE
- Scope: long fractional equities only; no options, shorts, crypto, or other accounts
- Decision: **HOLD JPM and SLB; no new entry or rotation.**

## Live account and kill switches

- Account verified active cash/individual with `agentic_allowed=true`; no other account operated.
- Portfolio: **$186.8902 total**, **$144.6002 equity**, **$42.29 cash**, broker-authoritative **$18.29 buying power**. The difference is unsettled NVDA sale proceeds and is not treated as liquid.
- Positions: JPM 0.195159 @ $341.67 and SLB 1.443558 @ $50.67; both fully sellable.
- Filled today: NVDA sell order `6a678172-01bf-4d3d-951a-850ba041bc21`, 0.121165 shares @ **$198.0666**, filled 16:04:02 UTC; no additional fills.
- Open-ish equity order states checked separately (`new`, `queued`, `confirmed`, `unconfirmed`, `partially_filled`): all empty. Pending-order notional $0.
- Kill switches clear: account value >$10; about **-6.55%** versus conservative $200 funding/high-water proxy, below the 10% pause; broker/account/quote/order/risk state certain. No new risk was added.

## Market and sector regime

- Risk appetite deteriorated after the open: SPY **$736.54 (-0.32%)**, below SMA10/20/50 (~$746.47/$746.15/$745.07); QQQ **$677.85 (-0.93%)**, below all three averages and below its prior $682.48 20-day low intraday; IWM **$291.72 (+0.19%)** held better but remained below SMA10/20.
- Semiconductor/technology liquidation remained the dominant negative flow: SMH **-3.95%**, 20-day return **-11.87%**, ATR ~4.58%; XLK **-1.78%** and below SMA10/20/50.
- Leadership rotated toward financials XLF **+0.67%**, healthcare XLV **+0.84%**, staples XLP **+1.36%**, and communication XLC **+1.72%**. Energy XLE **-1.45%** as Brent/oil fell sharply on the US-Iran diplomatic pause.
- Current reporting corroborated stocks wavering, chip weakness, oil down roughly 7%, and a heavy Fed/mega-cap earnings week. Event risk remains elevated around the 7/29 Fed decision and MSFT/META earnings, followed by AAPL/AMZN 7/30.

## Position management

### JPM — HOLD
- Live **$353.785 (+0.16%)**; value **$69.04**, unrealized approximately **+$2.36**.
- Above SMA10/20/50 ($344.40/$338.89/$322.36), 20-day return +7.52%, with XLF leadership. Latest Q2 reporting showed record profit, 27% managed-revenue growth, and raised interest-income guidance; ~14.7 PE remains moderate.
- Price backed off the $359.05 intraday high and was near the prior breakout area, so adding/chasing is not justified.
- **Stop/reassessment $346; targets $365 / $375.** Marked risk to stop **$1.52**. Exit review on a $346 failure or material loss of XLF leadership; do not widen.

### SLB — HOLD
- Live **$52.3401 (-0.15%)**; value **$75.56**, unrealized approximately **+$2.41**.
- Above SMA10/20 ($47.68/$47.07) and marginally above SMA50 $51.48; 20-day return +11.36%. Friday's earnings breakout remains constructive, but today's XLE/oil decline weakens confirmation.
- **Stop/reassessment $50.00; targets $54.80 / $57.00.** Marked risk to stop **$3.38**. Exit on $50 breach or failed breakout with sustained energy weakness; no add and no widened stop.

## Ranked opportunities

1. **JPM — 8.0/10, hold existing.** Cleanest trend/fundamental/sector alignment, but no chase below the intraday high.
2. **SLB — 7.6/10, hold existing.** Strong post-earnings structure; oil/XLE reversal prevents adding.
3. **CRM — 7.4/10, wait for retest.** $175.81, +7.42%, reclaimed SMA10/20/50 and exceeded the prior 20-day high, with reasonable ~20 PE; however, the one-day gap and ~4.3% ATR make an afternoon chase poor R:R. Preferred retest ~$171–173, stop ~$166, targets ~$182/$188.
4. **PLTR — 7.1/10, no entry.** $131.75, +7.18%, reclaimed SMA10/20/50 with strong volume, but ~151 PE, ~4.9% ATR, resistance toward $138.90 and 8/3 earnings gap risk make the current location unsuitable.
5. **VZ — 7.0/10, wait.** $47.505, +2.43%, defensive/post-earnings momentum and ~10.7 PE, but extended above the prior $46.585 20-day high; preferred retest remains ~$46.4–46.7 with ~$45.6 invalidation.
6. **RTX — 6.9/10, no chase.** $218.82, +2.83%, fresh breakout and industrial/defense momentum, but ~10.6% above SMA10 and a stretched entry.

AAPL/MSFT/META/AMZN were rejected as new swings due imminent earnings; AMD/NVDA/AVGO due semiconductor breakdown; XOM/CVX/COP due oil weakness and 7/31 earnings; BAC duplicated JPM exposure. No candidate offered a clean immediate entry with at least 1.5:1 R:R that was materially superior to retaining liquidity.

## Allocation and actions

- Equity exposure: **$144.6002 / 77.37%** of total account value; cash: **$42.29 / 22.63%**.
- Liquid buying power after pending orders: **$18.29**. Mechanical 80% qualifying deployment slice: **$14.632**; minimum 20% reserve: **$3.658**.
- Actual new deployment: **$0**. The $18.29 remains reserved because the best unowned candidates were extended/gap-driven or carried imminent event risk. Existing equity exposure is already close to the whole-account 80/20 objective.
- Aggregate marked risk to working stops: JPM **$1.52** + SLB **$3.38** = **$4.90**, within the ~$6 soft target.
- Orders reviewed/placed/cancelled: **none**. No setup qualified for an order review; no forced trade or churn.

## Tool record

Robinhood MCP returned account identity, portfolio, positions, today's fill, all five open-ish order states, live quotes, daily/intraday OHLCV, fundamentals, tradability, and earnings calendar. Web checks corroborated macro/sector headlines. No broker/tool failure or unresolved uncertainty occurred. This no-trade/hold decision is journaled under policy.

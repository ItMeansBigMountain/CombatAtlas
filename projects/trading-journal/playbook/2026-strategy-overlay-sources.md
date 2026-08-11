# 2026 Strategy Overlay — Evidence and Implementation

Date adopted: 2026-08-10
Scope: Robinhood Agentic account 433711041 / ending 1041 only

## What the evidence says

1. **Momentum has been the clearest 2026 equity factor, but it is crowded.** J.P. Morgan's 3Q 2026 factor review says equity momentum led again, had its best multi-year run since the dot-com period, and showed exceptionally wide winner/loser dispersion. The same source warns that unusually wide dispersion raises sudden-unwind risk. Implementation: retain momentum as the primary selection factor, but use smaller starters when extended, cap correlated themes, and require retests rather than chasing.

2. **Earnings revisions and fundamental change improve the signal.** Counterpoint's March 11, 2026 factor scoreboard described North American momentum leadership alongside earnings revisions, AI leadership, and persistent sector trends; quality also performed positively in North America. Implementation: require verified earnings/guidance/revision/catalyst support and use free cash flow, leverage, margins, and earnings quality as guardrails.

3. **Factor and sector leadership changes with regime.** LSEG's Q1 2026 review found broad value strength helped by Energy, with Tech moderation and within-industry preference for value, yield, and quality. This differs from sources/snapshots showing momentum dominance, demonstrating why a fixed one-factor strategy is fragile. Implementation: classify trend/mixed/risk-off regimes and rank a stock against its sector, not merely the whole market.

4. **Trend following is robust across long samples, but not guaranteed.** AQR's century study reports time-series momentum profitability across a reconstructed 1880–2016-style historical span and multiple modern asset classes. Implementation: cut invalidated trends, allow winners to run, and avoid forecasting reversals without price confirmation.

5. **Current promotional swing-trading pages consistently emphasize catalyst + volume + retest, but their claimed win rates are not treated as reliable evidence.** These pages were used only to formulate testable execution rules—not to accept advertised performance. Implementation: label setups, require volume/catalyst confirmation, use VWAP/first-day midpoint or prior resistance retests, and track our own realized results.

## Active implementation

The autonomous policy now requires:

- market/sector regime classification;
- sector-relative 20-day and 60-day momentum;
- verified catalyst or revisions plus a quality check;
- one of three explicit setups: catalyst-gap hold, breakout-retest, or 20-day trend pullback;
- no unconfirmed breakout chasing and caution above 1 ATR from support;
- correlated-theme concentration controls;
- 50%–75% starters in mixed/event/high-gap conditions;
- 3–5 session time stops for failed follow-through;
- a 16-point candidate scorecard and setup-level review every 20 closed trades.

## Sources

- J.P. Morgan Asset Management, **Factor Views 3Q 2026**: https://am.jpmorgan.com/us/en/asset-management/institutional/insights/portfolio-insights/asset-class-views/factor
- FTSE Russell / LSEG, **Equity Factor Insights — April 2026**: https://www.lseg.com/en/ftse-russell/market-insights/equity-factor/april-2026
- Counterpoint Funds, **Momentum Leads While Value and Stability Factors Lag** (data through 2026-03-11): https://counterpointfunds.com/momentum-leads-while-value-and-stability-factors-lag-factor-performance-ytd
- AQR, **A Century of Evidence on Trend-Following Investing**: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
- TradeZella, **5 Swing Trading Strategies With Exact Entry and Exit Rules (2026)**, used only as a practitioner-rule reference: https://www.tradezella.com/blog/swing-trading-strategies

## Limitations

- Year-to-date leadership is not proof of future returns.
- Publisher methodologies differ, and factor snapshots can conflict because dates, regions, and definitions differ.
- No advertised win rate is imported into sizing or expected-value assumptions.
- The strategy must be judged from live, journaled, net-of-friction account outcomes; no rule should be changed from a small sample.

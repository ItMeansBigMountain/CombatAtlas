# Autonomous Agentic Midday Decision — 2026-08-20

- Timestamp: 2026-08-20 16:01 UTC market snapshot
- Account: Robinhood Agentic ••••1041 (433711041)
- Mode: pre-authorized autonomous equities-only management
- Policy: `playbook/autonomous-policy.md` ACTIVE; no date-specific plan found

## Broker and kill-switch checks

- Account active, cash type, agentic_allowed=true; no other account accessed for trading.
- Account value: $326.7742; equity value: $256.9842; buying power/cash: $69.79; unsettled funds: $0.
- Kill switch below $10: clear.
- Daily 5% / recent-high 10% pause: no evidence of trigger in available live state; account-level recent-high series was not provided, so no new entry was taken in the mixed tape.
- Open-ish orders checked separately: new, queued, confirmed, unconfirmed, partially_filled — all empty.
- Filled orders since 2026-08-19: none.
- No options, shorts, pending deposits, or held-for-sale shares.

## Regime

Classified **mixed/rotation / risk-averse midday**. At 16:01 UTC: SPY 765.70 (-0.44%), QQQ 711.52 (-0.64%), IWM 297.98 (-1.24%). SPY remained above SMA20/SMA50 (759.77/750.43), IWM above SMA20/SMA50 (297.88/296.07), while QQQ was above SMA20 but slightly below SMA50 (706.78/712.98). Intraday, all three benchmarks were below VWAP. XLF -0.23%, XLK -0.08%, XLY -1.55%; this is not a clean broad risk-on confirmation.

## Position decisions

1. **MA — HOLD, score 13/16.** 0.113541 shares; average $572.48; quote $578.54; value $65.69; unrealized +$0.69 (+1.06%). Daily trend is strong: above SMA20 $564.03 and SMA50 $534.28, +7.85%/20d and +15.08%/60d; intraday above VWAP $576.18 and outperforming SPY. Support/invalidation: close below ~$564 (SMA20) or decisive break of ~$571.80 intraday support with continued XLF weakness. Target zone $583.70 then $601.77. Fundamentals support durability: Q2 revenue $9.277B, net income $4.388B, margin 47.3%; EPS $5.04 beat $4.76 estimate.
2. **BAC — HOLD / weakest holding, score 11/16.** 1.046363 shares; average $62.12; quote $62.56; value $65.46; unrealized +$0.46 (+0.71%). Above SMA20 $63.01 only marginally on prior close and above SMA50 $60.23; +2.52%/20d and +21.95%/60d, but below intraday VWAP $62.95 and underperforming MA. XLF remains near flat. Support/invalidation: sustained break below ~$60.70 (20-day low) or loss of ~$62 with sector-relative weakness. Target $65.23 then breakout continuation. Q2 revenue $31.558B, net income $9.074B, margin 28.75%; EPS $1.21 beat $1.11.
3. **SHOP — HOLD, score 12/16.** 0.862075 shares; average $144.09; quote $146.04; value $125.90; unrealized +$1.68 (+1.35%). Strong daily momentum above SMA20 $137.39/SMA50 $125.02; +23.78%/20d and +42.31%/60d. Intraday recovered above VWAP $145.19 after touching $144.12, though XLY is weak and valuation is elevated (~98.9x P/E). Invalidation: decisive close below ~$137.40; nearer warning below $144.12 with weak volume/sector RS. Targets $158.87 then $182.19. Q2 revenue $3.583B and EPS $0.42 beat $0.37; net income improved to $1.502B, but earnings quality/valuation warrant discipline.

No stop was widened; no averaging down.

## Broad scan and ranked opportunities

Daily Movers was scanned beyond stale personal watchlists. Most movers were rejected for negative gap structure, low liquidity/wide spreads, price below $5, or speculative/uncorroborated catalyst risk.

1. **TEM — 11/16, WATCH only.** +9.6%, 13.6M shares versus ~5.7M average; liquid, but loss-making and already extended from the opening base after a one-day catalyst-style move. Require consolidation/retest near $64–65 and verified catalyst; no chase.
2. **MRVI — 10/16, WATCH only.** +15.0%, 6.7M versus ~2.6M 30-day average, new 52-week high; loss-making biotech with headline/catalyst uncertainty. Require a retest/hold around $7.80–8.00 and direct news confirmation.
3. **MARA — 9/16, NO TRADE.** +10.0%, excellent liquidity, but loss-making and crypto-correlated; below policy score threshold and adds high-beta thematic risk in a mixed tape.
4. **SCSC — 9/16, NO TRADE.** +17.6% and new 52-week high, but average volume only ~229k (<500k policy preference), wide-ish spread and a substantial fade from $66.78 high.
5. **SCTX — 7/16, NO TRADE.** +21.4% but thin (~240k average), clinical-stage biotech, wide spread, no verified catalyst in this scan.

## Capital and action

- Available liquid buying power after pending orders: $69.79.
- Policy 80% deployable tranche: $55.83; required 20% reserve: $13.96.
- Current equity deployment: 78.64% of account value; cash: 21.36%.
- If a qualifying entry used the tranche, total account deployment would rise to ~95.73%; however, the policy explicitly forbids forcing trades and the mixed regime requires reduced sizing/confirmation.
- **Action: no orders reviewed or placed; no exits/rotations.** Existing holdings remain valid, and no fresh candidate reached 13/16 with a confirmed retest and verified catalyst. Preserve the full $69.79 until a clean setup confirms; the mandatory $13.96 reserve remains untouched.

## Next management triggers

- Reassess BAC first if it loses $62 and XLF relative strength weakens.
- Protect SHOP if it loses $144.12 intraday and fails to recover; thesis invalidation remains near the rising SMA20 rather than a widened stop.
- MA remains strongest; watch $583.70 resistance and consider profit protection if momentum stalls there.
- Fresh entries only after a confirmed retest, score >=10 (reduced starter) or >=13 (full-policy), calculable stop, and >=1.5:1 reward/risk.

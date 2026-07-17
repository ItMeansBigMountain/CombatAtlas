# Robinhood Agentic 1041 — Afternoon Scan

- Timestamp: 2026-07-17 17:42–17:46 UTC / 13:42–13:46 ET
- Account: `433711041` only (ending 1041)
- Authority: `/opt/data/HeRmEz/projects/trading-journal/playbook/autonomous-policy.md`
- Asset scope: equities/fractionals only; no options, shorts, margin, crypto, or event contracts
- Broker status: active; `agentic_allowed=true`

## Executive decision

**HOLD / NO NEW TRADE. No order was reviewed, placed, replaced, or cancelled.**

The account is below the policy's preferred deployment band, but deployment is conditional rather than mandatory. The afternoon tape remained risk-off outside energy, the existing positions had recovered from their opening lows without producing add signals, and the strongest scanner names were either event-gap chases, extended/overbought, or technically damaged. No fresh candidate offered a clean entry, structural stop, portfolio fit, and at least 1.5:1 reward/risk without chasing. The policy explicitly permits holding cash when no qualifying setup exists.

## Verified broker state

Final live broker verification was performed at approximately 17:46 UTC.

- Portfolio value: **$186.64150665**
- Equity value: **$103.29150665**
- Cash / liquid buying power: **$83.35 / $83.35**
- Pending deposits: **$0**
- Options, futures, crypto, event contracts, mutual funds, fixed income: **$0**
- Current equity deployment: **55.34%**
- 80% of liquid buying power: **$66.68**
- 20% reserve: **$16.67**
- Actual cash retained because no setup passed: **$83.35**
- Change from the 09:30–09:32 ET opening-monitor account value of $183.49: **+$3.1515 / +1.72%**
- Kill switch: **not triggered**; no material daily drawdown and no broker anomaly observed.

### Open-order verification

The following states were checked separately and were empty:

- `new`: 0
- `queued`: 0
- `confirmed`: 0
- `unconfirmed`: 0
- `partially_filled`: 0

No duplicate or conflicting order exists.

### Recent fills

No fill occurred on 2026-07-17. The two fills found in the preceding seven-day window were:

1. 2026-07-16 19:02:02 UTC — AVGO sell 0.137376 shares, market, filled at $376.01, agentic, $0 fees, order `6a592aa9-60e7-4b0e-9a2c-8ba25ec705de`.
2. 2026-07-14 13:32:19 UTC — NVDA buy $25.00 / 0.121165 shares, market, filled at $206.33, agentic, $0 fees, order `6a563a62-8720-4902-87c5-c0365567e859`.

## Current positions and management

Live quotes below were observed around 17:46:41 UTC.

| Symbol | Qty | Avg cost | Live | Value | Unrealized P/L | Day | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| NVDA | 0.121165 | $206.33 | $205.2207 | $24.8656 | -$0.1344 (-0.54%) | -1.05% | Hold; no add. |
| SOFI | 4.477580 | $17.87 | $17.505 | $78.3800 | -$1.6343 (-2.04%) | +1.07% | Hold; no add. |

### NVDA plan

- Technical state: $205.2207 is above prior-day 20-day SMA $202.217; RSI(14) 52.12; ATR(14) $7.33. NVDA recovered above the morning $201–$202 reassessment zone but SMH remained weak.
- Fundamental state: latest reported quarterly revenue and earnings remained strongly positive; next verified earnings date is 2026-08-26 after market.
- Risk: watch $203/$200; **exit review on a sustained break below $198 with QQQ/SMH confirmation**. This is a management level, not a resting broker stop.
- Targets/watch zones: **$214**, then **$224**.
- Current price-to-$198 risk: approximately **$0.87** on the position. Reward to $214 is approximately $1.06 (1.22:1); reward to $224 approximately $2.28 (2.60:1).

### SOFI plan

- Technical state: $17.505 is below prior-day 20-day SMA $17.9185; RSI(14) 46.74; ATR(14) $0.95. Price recovered from the morning low but has not reclaimed trend confirmation.
- Fundamental state: latest reported quarter showed revenue $1.100368B and net income $166.731M; verified earnings are 2026-07-29 before market, so event risk is close.
- Risk: review on sustained loss of $16.70; **hard thesis invalidation below $16.47**. This is a management level, not a resting broker stop.
- Targets/watch zones: **$19.20**, then **$19.70–$19.75**.
- Current price-to-$16.47 risk: approximately **$4.63**. Reward to $19.20 is approximately $7.59 (1.64:1); reward to $19.75 approximately $10.05 (2.17:1).

Aggregate current price-to-written-invalidation risk is approximately **$5.51**, inside the policy's default ~$6 aggregate planned-risk target. Stops are intentionally not widened.

## Market and sector regime

Live changes versus the official 2026-07-16 close:

| Instrument | Change |
|---|---:|
| SPY | -0.69% |
| QQQ | -0.86% |
| IWM | -0.21% |
| XLK | -0.17% |
| XLF | -0.64% |
| SMH | -1.13% |
| XLY | -1.35% |
| XLV | -0.45% |
| XLE | +0.93% |
| XLI | -0.02% |

Regime: broad risk-off rotation with energy as the only clear sector leader. Semiconductors and consumer discretionary remained the weakest reviewed groups. This did not support adding NVDA or deploying cash into another high-beta growth name.

Current market reporting reviewed during the scan linked the selloff to renewed technology/AI-infrastructure pressure, higher Treasury yields after firm economic data, and geopolitical uncertainty. Company-specific reports were also checked for NVDA, SOFI, TRV, UNH, ABT, and RKLB. News was used only as context and not as a standalone trigger.

## Candidate discovery and rejection log

Robinhood scanners and the high-market-cap 14-day earnings calendar were reviewed. Two live saved scans were created during this run:

- `Agentic 1041 Afternoon Daily Gainers 2026-07-17` — scan `4cf21940-9de9-40c7-95db-f41b3436b73d`
- `Agentic 1041 Afternoon Upcoming Earnings 2026-07-17` — scan `00221368-a7ac-4ca7-8b4d-1b9f1c1f7af4`

Broad liquid candidates included mega-cap technology, semiconductors, financials, energy, industrials, healthcare, and selected liquid scanner names. Tradability was verified for NVDA, SOFI, RKLB, UNH, ABT, XOM, CAT, AMD, AVGO, and JPM.

| Candidate | Live/day | Key evidence | Decision |
|---|---:|---|---|
| XOM | $147.97 / +1.38% | XLE leader; above SMA20 $138.89, but prior-day RSI 73.86 and price faded from an intraday high near $150. | Reject chase; wait for pullback/base. |
| UNH | $434.64 / +2.66% | Beat verified Q2 EPS ($6.38 vs $4.85); RSI 56.33, above SMA20 $418.86. | Attractive recovery, but already extended after earnings and bid/ask wider than core ETFs; wait for higher-low/retest. |
| TRV | $365.26 / +8.12% | Verified Q2 EPS $10.04 vs $4.94; RSI 61.30 before the gap, SMA20 $329.47. | Reject event-gap chase; no structurally efficient entry after +8%. |
| RKLB | $69.79 / +3.62% | Revenue growth continues, but still loss-making; RSI 30.92 and far below SMA20 $89.20 with ATR $8.33. | Oversold bounce, not a confirmed swing reversal. |
| ASTS | about +5.7% | Scanner/news momentum and strong liquidity. | High-beta space exposure; no clean low-risk entry in risk-off tape. |
| STX | about +5.6% | Scanner strength. | Extended same-day momentum; avoid chasing. |
| BE / GEV / FCX | positive scanner/sector interest | Liquid or reasonably liquid growth/industrial names. | No superior entry/stop/R:R versus holding cash. |
| NVDA / SOFI | existing holdings | Both recovered from opening stress, but neither produced a policy-valid add trigger. | Hold only; no averaging down. |

## Actions and verification

- Orders reviewed: **0**
- Orders placed: **0**
- Orders cancelled/replaced: **0**
- New fills: **0**
- Position changes: **none**
- Final open orders: **0 across every required active state**
- Final positions: **NVDA 0.121165; SOFI 4.477580**
- Final deployment: **55.34%**
- Final cash/reserve: **$83.35 retained; minimum modeled reserve $16.67**

The low deployment is deliberate. No qualifying clean days-to-weeks swing was forced into a weak, event-driven afternoon tape.

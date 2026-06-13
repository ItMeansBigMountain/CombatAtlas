# HOOD Execution — 2026-06-12

Timestamp: 2026-06-12T15:58:38+00:00
Account: Robinhood Agentic account 433711041 / ending 1041
Mode: Autonomous trading active under playbook/autonomous-policy.md

## Account state before trade
- Portfolio value: $200
- Cash / buying power: $200
- Positions: none
- Open orders: none

## Market context
- SPY: $740.21, above prior close $737.76
- QQQ: $718.474, above prior close $717.12
- IWM: $293.45, above prior close $290.41
- Market read: risk-on but off earlier highs; small caps leading.

## Thesis
HOOD remained the cleanest liquid fractional-tradable candidate from the broader market/news scan. It had strong recent relative strength and pulled back from the earlier intraday quote, giving a better starter entry than the prior $95.80 continuation plan.

## Order preview
- Symbol: HOOD
- Side: Buy
- Type: Market
- Dollar amount: $50.00
- Broker alerts: none
- Preview quote disclosure: Bid $93.19 × 100 Z · Ask $93.27 × 100 Q · Last $93.225 × 260 P. Updated 11:58 AM ET.

## Execution
- Order ID: 6a2c2c8f-e73e-47ca-bec4-124cdd754390
- State: filled
- Side/type: buy market
- Dollar amount: $50.00
- Quantity: 0.535786 shares
- Average fill: $93.3208
- Fees: $0.00
- Placed agent: agentic
- Fill time: 2026-06-12T15:58:07.645Z

## Risk plan
- Initial invalidation / manual stop level: $91.75
- Approx per-share risk: $1.5708
- Approx dollar risk: $0.84
- Target zone: $104.00
- Approx potential profit: $5.72
- Approx R:R: 6.8:1 from actual fill to target vs stop

## Stop order attempt
A protective stop-market sell was reviewed successfully with no broker alerts at stop $91.75 for 0.535786 shares. Placement failed because Robinhood rejected fractional stop order: `Invalid trigger for fractional order.`

Management note: position requires manual/agent monitoring and market sell if invalidation is hit; fractional stop order could not be placed.

## Post-trade account state
- Portfolio value reported: $199.9620445
- Equity value: $49.9620445
- Cash / buying power: $150
- Position: HOOD 0.535786 shares long, average buy price about $93.32

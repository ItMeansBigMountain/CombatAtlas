# Robinhood Agentic Trading — Research Notes

Last reviewed: 2026-06-13

## Sources reviewed

- Robinhood Agentic Trading overview/support docs
- Robinhood “Trading with your agent” support doc
- Robinhood Agentic Trading landing page
- Robinhood newsroom launch post
- TechCrunch and CNBC launch coverage
- Ryan Doser / Claude Code Robinhood agent writeup and video metadata
- Julius AI Robinhood portfolio experiment writeup + Reddit day-4 update
- Reddit discussions from r/AI_Agents, r/ClaudeAI, r/RobinhoodApp, r/wallstreetbets

## What the feature actually is

Robinhood provides a Trading MCP connector and a dedicated Agentic account. The AI/model is not “inside Robinhood”; the user supplies the agent through Claude Code/Desktop, Codex, ChatGPT, Cursor, Grok, Hermes, etc. Robinhood’s MCP gives account/market/order tools and constrains placement to the Agentic account.

Key implication: success comes from building an operating system around the MCP — policy, prompts, scans, logs, risk controls, and review loops — not from merely connecting a chatbot.

## Successful patterns to mimic

1. Dedicated small sandbox capital only
   - Keep agent money separate from main accounts.
   - Treat the beta as an experiment, not income.
   - Fund only what can be lost.

2. Explicit strategy and constraints
   - Define what can be traded, when to stay out, allocation caps, fractional-share use, risk limits, and preferred sectors/themes.
   - Do not ask the agent to “make money”; give it a playbook.

3. Live account/market checks before action
   - Check account value, buying power, positions, open orders, tradability, quotes, and relevant historicals before sizing or placing.
   - Stop if broker/tool state is uncertain.

4. Order review + activity trail
   - Use order review before placement where available.
   - Keep an audit trail: thesis, entry, stop, target, size, expected loss/reward, fill/result, and later post-trade review.

5. Human feedback loop
   - Daily/weekly review the agent’s behavior.
   - Correct policy after mistakes.
   - Store lessons as playbook updates, not vague memories.

6. Transparency about losses
   - Julius experiment’s useful part is not performance; it is public reporting of positions, P/L, cash, and decisions, including losses.
   - Mirror this locally with honest journal entries.

7. Prefer practical automation over hype
   - Strongest near-term use is research + disciplined execution + journaling + portfolio/risk monitoring.
   - Fully autonomous alpha is unproven.

## Issues and failure modes to avoid

1. Expecting Robinhood to provide the agent
   - Reddit users repeatedly note: MCP gives connectivity; the user must build/provide the agent.
   - Avoid assuming a connected chat will monitor markets 24/7 unless a scheduler/cron is actually running.

2. Weak/vague instructions
   - “Trade for me” produces poor behavior.
   - Treat the agent like an employee: exact scope, rules, tools, reporting cadence, and escalation rules.

3. Over-deployment of cash
   - Julius day-4 example showed ~11.4% drawdown and only ~$21 buying power left from $1,000 after holding longs and adding RGTI.
   - Avoid using most buying power early; reserve cash for better entries and risk control.

4. Chasing volatile/story stocks without invalidation
   - Quantum/AI/theme names can move fast; require liquidity, support/invalidation, and controlled risk.

5. Platform/model refusals or incomplete autonomy
   - Some users reported Claude/ChatGPT refusing actionable trades or only providing read access.
   - Hermes should verify actual tool availability each session and pause rather than infer capability.

6. Mobile/desktop auth friction
   - Robinhood docs and user writeups indicate desktop auth is required; OAuth may involve browser/mobile handoffs and localhost callback quirks.
   - If auth breaks, fix connector/auth before trading.

7. Options before equities are proven
   - Robinhood docs say options are rolling out and not available to everyone.
   - Keep options disabled unless separately authorized and tested.

8. No real-time stop automation assumption
   - If stops cannot be left as broker-side orders through available tools, management depends on scheduled scans/checks.
   - Size accordingly and do not pretend risk is continuously controlled.

## Operating changes for Hermes sandbox

- Continue using account 433711041 / ending 1041 only.
- Keep equities/fractional shares as default; options off.
- Maintain max starter allocation of $50 and prefer $25-$50 only for clean setups.
- Add cash-reserve rule: do not deploy more than 60% of account value across open positions unless a written plan justifies it.
- Add per-position loss kill: if a live position loses ~8% from entry or breaches thesis/invalidation, review/exit instead of averaging down.
- Add daily drawdown pause: if account is down 5%+ in one day or 10%+ from recent high, pause new entries and produce a review.
- Require a “no trade” outcome when the edge is unclear.
- Journal every decision, including no-trade decisions and tool failures.

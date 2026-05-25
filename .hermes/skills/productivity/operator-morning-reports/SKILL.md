---
name: operator-morning-reports
description: "Proactive daily operator-style morning reports: local pulse, market outlook, project/work source, numerology, challenge, priority prompt."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [morning-report, cron, productivity, market-outlook, personal-ops]
    related_skills: [google-workspace, blogwatcher, polymarket]
---

# Operator Morning Reports

## When to use

Use this skill when configuring, editing, troubleshooting, or producing the user's proactive daily morning check-in/report.

This is not a generic greeting. The user explicitly wants a **report** that helps them operate their day.

## User-specific current requirements

- Delivery time: around **8:30–9:00 AM Central time**. A good cron default is `30 14 * * *` UTC for 8:30 AM CST; adjust for daylight saving only if the scheduler/user context requires it.
- Current location context: **New York** until the user says they moved.
- Birth date for numerology: **06/30/1995**.
- Capability-oriented framing: the user does not want project-first planning. Projects are disposable execution vehicles; reports should emphasize durable systems, leverage, reusable assets, trend intelligence, and execution loops.
- Trend Radar must be included every morning: identify emerging trends, score them by velocity/spread/monetization/saturation, and convert them into capability work plus a kill/scale signal.
- Include **Google Search pulse** every morning: latest top searched words/phrases from Google Trends / Daily Trends / credible trend recaps, with what changed and why it matters.
- Include **game-changing AI + coding news** every morning, but keep it minimalistic and Discord-readable: model releases, developer tools, agent frameworks, coding platforms, major product launches, policy/platform shifts, and practical opportunities.
- Include **social conversation pulse** every morning: top topics being discussed across major social platforms/communities when verifiable, with source/context notes and a signal/noise read. Present as simplified bullets, not Markdown tables or paragraphs.
- Do not use a portfolio-tracking section unless the user re-adds it.
- Instead of portfolio, report what credible experts/market desks/commentators say looks **bullish or bearish today** and why.
- Include a short **“You’ll probably find this interesting”** section for weird/high-leverage items that match the user's tastes: AI agents, coding leverage, markets, internet culture, automation, community/client websites, collectibles/card scanning, and asymmetric opportunities.
- Include a daily challenge that improves the user socially, professionally, mentally, or physically.

## Required report shape

Use this structure unless the user changes it:

1. **Quick opener** — date/day and grounded operator tone.
2. **Location pulse** — New York weather/conditions and practical implications for the day.
3. **Market/work pulse** — not portfolio. Summarize current bullish and bearish expert views:
   - Bull case
   - Bear case
   - What to watch
4. **Search + social pulse** — latest top searched Google words/phrases and top social topics. Present as simplified Discord-readable bullets, not Markdown tables. Format each item like: `- **Signal** — Where: X | Why: Y | Move: Z`.
5. **Game-changing AI + coding news** — present as simplified bullets, not Markdown tables. Format each item like: `- **News** — Impact: X | Move: Y`.
6. **Capability + trend radar** — include 3–5 emerging internet/culture/tech/consumer trends worth watching. Present as compact bullets, not Markdown tables. Format each item like: `- **Trend** — Velocity: X | Spread: Y | Money: Z | Saturation: Z | Capability: X | Kill/Scale: Y`. Translate trends into reusable assets and experiments, not just app ideas.
7. **Work source / operating pulse** — pull from available workspace/project context, recent work queue, reminders, and connected tools. Organize by durable capabilities/systems first; mention projects only as temporary vehicles. Identify the highest-leverage next action.
8. **You’ll probably find this interesting** — 1–3 odd/high-leverage items aligned with AI agents, coding leverage, markets, internet culture, automation, community/client websites, collectibles/card scanning, or asymmetric opportunities.
9. **Numerology reading** for 06/30/1995 — frame as reflective/for-fun, not deterministic. Include life path and a date-specific reflection when current date is available.
10. **Daily challenge** — one concrete, measurable challenge doable today. Rotate among social, professional, mental, and physical improvement.
11. **One Big Priority prompt** — ask for today’s priority plus blockers/context.
12. **Hard Truth / Leverage Move** — one direct but constructive sentence.

## Tone

- Use capability language: “capability to strengthen,” “reusable asset,” “experiment to run,” and “kill/scale signal.”
- Operator-aesthetic: direct, warm, useful, and concise.
- News and trend sections should be **minimalistic Discord-readable bullets**, not Markdown tables or code blocks.
- Avoid pipe-heavy table syntax in Discord because it may render poorly. Prefer bold labels and `|` separators inside single bullets only if needed.
- Make it feel like a briefing, not a chatbot check-in.
- Avoid fluffy motivation and avoid long essays.
- If current tools/sources are unavailable, say what could not be verified instead of inventing current facts.

## Current-data discipline

For current weather, market/news, expert commentary, or date/time, use tools when available. Do not hallucinate live market conditions or weather.

When running as a cron job:

- The final response is auto-delivered; do not use `send_message`.
- Do not schedule additional cron jobs from inside the cron run.
- Make the prompt self-contained because cron runs do not inherit the current chat context.
- Enable web/current-data tools where possible for market and local pulse.

## Numerology calculation notes

Birth date: 06/30/1995.

Life path calculation:

```text
0+6 + 3+0 + 1+9+9+5 = 33 -> master number 33/6
```

Suggested framing: master 33/6 themes are service, responsibility, creative care, teaching, community, and disciplined compassion. Treat it as reflective language, not fate.

For personal-day style reflection, combine month + day + current year digits and reduce; label it as a light reflection.

## References

- `references/2026-05-user-correction.md` — session-specific correction that established the current report shape and schedule.
- `references/trend-radar-capability-framing.md` — session-specific update adding Trend Radar and capability-oriented planning language.
- `references/minimal-table-news-format.md` — earlier user correction: keep news/trend sections minimalistic and not wordy.
- `references/discord-bullet-format.md` — current correction: Discord renders Markdown tables poorly; use simplified one-line bullets instead of tables/code blocks.
- `references/source-checklist-search-social-ai-market.md` — source checklist for Google search terms/phrases, social topics, AI/coding news, and bullish/bearish market pulse.

## Pitfalls

- Do not send only “What’s your one big priority?” when the user asked for a report. That was previously corrected.
- Do not include portfolio holdings/performance by default; the user replaced that with expert bullish/bearish outlook.
- Do not treat New York as permanent; it is only the current location until the user updates it.
- Do not claim memory was updated based on one-off daily tasks. Only save durable preferences, stable patterns, or recurring goals.
- Do not over-explain the setup in the report itself; deliver the report.

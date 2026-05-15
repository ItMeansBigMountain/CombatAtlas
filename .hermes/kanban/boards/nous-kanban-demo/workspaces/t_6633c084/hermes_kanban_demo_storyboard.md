# Hermes Kanban Demo Video — Storyboard + Design Direction

## Format target
- Length: 15 seconds, optimized for X/Twitter, LinkedIn, and Discord embeds.
- Aspect ratios: design-safe for 16:9 first, crop-safe center column for 1:1 and 9:16.
- Audio: optional. The clip must read silently with captions, card labels, and visible motion causality.
- Core story: a director receives one creative brief, decomposes it into parallel specialist tasks, dependencies fan out/fan in, the dashboard shows work moving through todo → ready → running → blocked → done.

## Visual style

### Dashboard layout
- Background: deep graphite/blue-black canvas (#080B12) with a subtle radial glow behind the active board.
- Main object: a floating kanban dashboard, slightly tilted in 3D but mostly readable front-on.
- Columns: five vertical lanes labeled TODO, READY, RUNNING, BLOCKED, DONE.
- Top bar: “Hermes Kanban” left, small board selector “Demo launch video” center, live status pills right.
- Left rail: tiny agent icons stacked vertically (Director, Researcher, Designer, Animator, Editor, Reviewer).
- Center: card grid and dependency graph overlay.

### Colors
- Canvas: #080B12 / #0D111C.
- Dashboard panel: #111827 with 1px translucent border #2B3447.
- Todo cards: slate #293244.
- Ready cards: electric cyan #20D3FF.
- Running cards: violet #8B5CF6 with animated progress sheen.
- Blocked cards: amber/red #FFB020 / #FF5C7A with pulsing warning dot.
- Done cards: green #35D07F with checkmark stamp.
- Dependency lines: thin neon cyan lines with glowing moving dots; blocked dependency line turns amber; completed line fades to green.

### Typography
- Use a clean grotesk: Inter, Geist, or SF Pro.
- Column labels: uppercase, 11–12px, letter-spaced, muted gray.
- Card titles: 14–16px semibold, high contrast.
- Captions: 28–36px bold for social readability; max 6 words per caption.
- Metadata text on cards: 10–12px, secondary gray, use icons instead of long prose.

### Iconography
- Director: compass/starburst icon.
- Research: magnifying glass.
- Design: pen nib/sparkle.
- Animation: play button/keyframe diamond.
- Editor: scissors/sliders.
- Reviewer: shield/check.
- Blocked: small warning triangle.
- Dependencies: node dots with arrowheads or animated packets.

### Motion language
- Cards should feel like command objects: snap, glide, and magnetize into lanes.
- Dependency lines draw themselves quickly, with dots traveling from parent to child.
- Parallel work is shown by simultaneous card movement and staggered glows.
- Fan-in is shown by multiple lines converging into one larger card.
- Use micro-bounces only on state changes; keep camera motion smooth and restrained.

## Scene-by-scene storyboard (15 seconds)

### Scene 1 — “Brief lands” (0.0–1.8s)
Frame description:
- Start on dark canvas with one glowing card centered: “Creative brief: Kanban demo video”.
- A small Director avatar/compass icon drops onto the card.
- Caption appears bottom center: “One brief lands.”
- The dashboard grid fades in behind the card, columns visible but empty.
Animator notes:
- Card scale 92% → 100% with soft glow.
- Keep text large and centered; no tiny UI yet.

### Scene 2 — “Director decomposes” (1.8–4.0s)
Frame description:
- The brief card expands, then splits into five smaller task cards.
- Cards fan out horizontally from the Director node: Research, Storyboard, Animate, Edit, Review.
- Thin cyan dependency lines draw between them: Research + Storyboard → Animate → Edit → Review.
- Caption: “Hermes decomposes it.”
Animator notes:
- Use a particle/spark split rather than an explosion.
- The fan-out graph must be readable for at least 0.8s before cards move.

### Scene 3 — “Parallel lanes activate” (4.0–6.4s)
Frame description:
- Research and Storyboard cards slide into READY, then immediately into RUNNING in parallel.
- Researcher and Designer icons light up on the left rail.
- Animate, Edit, Review remain dimmed in TODO with dependency badges: “waiting on 2”, “waiting on 1”, “waiting on 1”.
- Caption: “Parallel agents start.”
Animator notes:
- Move Research and Storyboard simultaneously, not sequentially.
- Add animated violet progress sheen across running cards.

### Scene 4 — “Blocked is visible, not hidden” (6.4–8.6s)
Frame description:
- Storyboard card briefly jumps from RUNNING to BLOCKED.
- Its dependency line turns amber; a warning triangle pulse appears.
- A small comment bubble opens: “Need visual direction.”
- Director icon sends a tiny cyan packet to unblock it; the card returns to RUNNING.
- Caption: “Blockers surface fast.”
Animator notes:
- Keep blocked moment short but legible; this is a feature, not an error state.
- Use amber pulse, not harsh red alarm.

### Scene 5 — “Fan-in unlocks animation” (8.6–11.2s)
Frame description:
- Research and Storyboard cards stamp DONE with green checkmarks.
- Their cyan lines converge into the Animate card; Animate brightens and slides TODO → READY → RUNNING.
- Dashboard briefly zooms out to show the whole dependency structure.
- Caption: “Dependencies unlock.”
Animator notes:
- This is the key causality shot: completed parents visibly unlock the child card.
- Use traveling dots along both parent lines into Animate.

### Scene 6 — “Pipeline finishes” (11.2–13.4s)
Frame description:
- Animate finishes; Edit unlocks and runs; Review unlocks and runs.
- Cards move in a fast but readable cascade: RUNNING → DONE, next card activates.
- Done column stacks with green cards and small agent icons.
- Caption: “Work flows to done.”
Animator notes:
- Use speed ramp, but each state label should still be visible for a few frames.
- Avoid making it look like random card shuffling; dependency lines should lead the eye.

### Scene 7 — “Hero end frame” (13.4–15.0s)
Frame description:
- Final dashboard state: all cards DONE; dependency graph glows green.
- Top bar shows: “5 agents · 1 board · zero lost handoffs”.
- Hermes wordmark/logo or text lockup appears: “Hermes Kanban”.
- CTA caption: “Coordinate AI work visually.”
Animator notes:
- Hold final frame for at least 1.0s for social feed comprehension.
- Keep UI crisp; this frame may become the thumbnail.

## Readability without audio
- Every major beat has an on-screen caption under 6 words.
- Use visible state labels on columns and color-coded cards so the story works even muted.
- Dependency lines must animate causality: parent completion sends a visible packet to unlock child.
- Avoid dense card copy; use role names and 1–2 word state badges.
- Make the blocked state self-explanatory with a warning icon and short bubble, not a long explanation.
- Keep all essential action inside the center 70% of the frame for square/vertical crops.

## Tweet/social-media vibe
- First frame must be instantly understandable: one big card, one brief, one director icon.
- Use high-contrast captions like product launch clips; no corporate explainer clutter.
- Favor satisfying motion loops: cards snap into lanes, dependency lines light up, done checks land.
- Include one “aha” moment: fan-in unlocks Animate only after Research + Storyboard are both done.
- End on a clear product promise: “Coordinate AI work visually.”

## Concrete animator checklist
1. Build a dark dashboard with five labeled columns: TODO, READY, RUNNING, BLOCKED, DONE.
2. Create reusable task card component with title, assignee icon, status pill, and dependency badge.
3. Create dependency-line layer above cards but below captions; animate stroke draw and packet motion.
4. Implement seven timed scenes listed above; use captions as separate text layer.
5. Verify text readability at mobile size: captions readable at 360px width, card titles still recognizable.
6. Export versions: 16:9 master and crop-safe 1:1/9:16 variants if time allows.

## Design decisions summary
- Direction: premium dark product UI, not cartoon explainer.
- Primary metaphor: visible orchestration graph over kanban columns.
- Hero mechanic: fan-out/fan-in dependencies with animated unlock packets.
- State language: color + lane + icon for redundant readability.
- Pacing: one clear concept every ~2 seconds, with final 1-second hold.

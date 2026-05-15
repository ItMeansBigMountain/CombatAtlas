# Hermes Kanban — task card animation

Artifact: `index.html`

This is a square, browser-playable first cut for the Hermes Kanban launch video section focused on cards claiming and moving, dependency edges lighting up, parent tasks completing, and downstream cards unlocking.

## Open locally

```bash
xdg-open /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_bc4e3696/kanban-card-animation/index.html
```

No build step is required. The file is self-contained except for Google Fonts.

## What the animation shows

- Empty dark terminal/Kanban board becomes a live pipeline.
- The original brief card lands and the planning card is claimed.
- Dependency lines draw from brief to plan, then fan out to research and visual direction.
- Two agent badges claim upstream work in parallel.
- Research and design complete; green handoff packets flow into the animation card.
- The animation card unlocks after both parent dependencies complete.
- Edit and review appear downstream; review briefly blocks, then accepts.
- A final video tile appears with a traceable line back through the card graph.

## Controls

- Space: pause/resume
- R: restart timeline

## Design alignment

The animation follows the upstream visual direction:

- Canvas: near-black `#050507`
- Surfaces: dark terminal panels and lane dividers
- Cards: translucent amber, blue, and yellow fills with stronger borders
- Status badges: compact JetBrains Mono pills
- Dependencies: thin dashed SVG lines that draw left-to-right
- Motion: snappy cubic-bezier UI movement, no bouncy SaaS easing

## Timing map

The timeline loops over 90 seconds and mirrors the script beats:

| Time | Beat |
|---:|---|
| 0s | Brief appears |
| 7s | Agent claims planning card |
| 15s | Card decomposition and dependency fan-out |
| 27s | Research/design run in parallel |
| 43s | Parent cards complete and handoffs flow downstream |
| 58s | Animate card unlocks and runs |
| 70s | Edit/review flow, blocker visible |
| 82s | Final video tile assembles |

## Handoff note for editor

This is an interactive HTML animation rather than a rendered video. For final production, capture at 1080x1080 and crop the board/caption area as needed. The animation is designed to loop, so a renderer can start at t=0 and capture the full 90-second pass or use the listed beat timestamps for shorter clips.

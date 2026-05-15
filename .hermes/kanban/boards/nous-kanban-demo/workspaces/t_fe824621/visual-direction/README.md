# Hermes Kanban dark terminal visual direction

## Design stance

Make the board feel like a live terminal command center: near-black surfaces, monospace structure, compact badges, thin dependency wires, and selective amber/blue/yellow energy on task cards.

This direction blends:
- VoltAgent-style black engineering cockpit: #050507 canvas, #0f1218 surfaces, warm containment lines.
- OpenCode-style monospace credibility: JetBrains Mono for board chrome, task ids, badges, and status labels.
- Linear-style dark hierarchy: subtle luminance steps and very thin borders instead of heavy shadows.

## Artifacts

- `visual-direction/index.html` — self-contained styleboard/mock board for visual reference.
- `visual-direction/README.md` — this handoff and token guide.

Open locally:

```bash
xdg-open /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_fe824621/visual-direction/index.html
```

## Palette

| Role | Token | Hex | Usage |
|---|---:|---:|---|
| Canvas black | `--bg` | `#050507` | Full screen background; never use pure black. |
| Panel black | `--panel` | `#090b0f` | Terminal bar, board container. |
| Elevated lane/card | `--panel-2` | `#0f1218` | Lanes, cards, nested UI. |
| Structural line | `--line` | `#27313f` | Outer borders, column dividers, terminal chrome. |
| Primary text | `--text` | `#f3f7fb` | Card titles, headings, important UI. |
| Muted text | `--muted` | `#8d98a7` | Descriptions and secondary labels. |
| Amber | `--amber` | `#ffb86b` | Research/story/message cards; warm narrative energy. |
| Blue | `--blue` | `#72a7ff` | Design/system/control cards; dependency lines. |
| Yellow | `--yellow` | `#f7d65a` | Production/action/animation cards. |
| Green | `--green` | `#33d17a` | Live/complete/healthy status. |
| Red | `--red` | `#ff6b7a` | Error/blocked only; use sparingly. |

## Component rules

### Board shell
- Rounded 14px container with a one-pixel cool border.
- Top terminal bar with fake window controls and a `hermes@kanban ~/board` prompt.
- Add a very faint grid behind the board, but keep it subtle enough that cards remain readable.

### Column lanes
- Five-lane rhythm: Todo → Design → Animate → Edit → Review.
- Each lane gets a thin right divider at `rgba(148,163,184,.18)`.
- Lane titles are uppercase monospace, 12px, letter-spaced.
- Count badges are compact and squared, not pill-shaped.

### Task cards
- Base card: translucent surface, 8px radius, 1px border, compact internal padding.
- Colored cards are not solid fills. Use translucent colored background plus stronger colored border:
  - Amber: narrative/research/message.
  - Blue: design/system/control.
  - Yellow: production/action/animation.
- Card contents: title, one-line description, compact status badge, small task id.
- Hover/active: lift 2px and increase border contrast. In video animation this can become a claim pulse.

### Status badges
- Monospace, uppercase, 9–11px.
- Rounded pill with 1px semantic border.
- Suggested states:
  - `ready`: blue
  - `running`: amber
  - `done` / `accept`: green
  - `blocked`: dimmed card with neutral/red badge
  - `waiting`: neutral gray

### Dependency lines
- Thin, dashed, curved SVG paths.
- Default line: translucent blue `rgba(114,167,255,.45)`.
- Use amber/yellow only when the dependency type needs semantic emphasis.
- Lines should sit behind cards, never over text. Animate as draw-on strokes from parent to child.

## Motion direction for animator

1. Start on an empty black terminal grid.
2. Terminal topbar types in: `hermes@kanban ~/board render --dark --deps`.
3. Lanes fade/slide in as vertical panes.
4. Cards enter by column, 80–120ms stagger.
5. A running card receives one amber border pulse.
6. Dependency lines draw left-to-right after parent cards settle.
7. Completion badge snaps from `running` to `done` with a small green flash.
8. Camera can push from full board into one card, then pull back to reveal fan-out/fan-in graph.

Keep animation snappy and terminal-native: no bouncy SaaS easing. Prefer `cubic-bezier(.2,.8,.2,1)`, 120–240ms for UI changes, 400–700ms for dependency-line draws.

## Typography

- Board chrome, task ids, badges, code-like labels: JetBrains Mono.
- Long explanatory copy outside board: Inter.
- Do not introduce serif or decorative display fonts.
- Use weight and color, not large font variation, for hierarchy.

## Recommendation

Use the provided HTML styleboard as the primary visual target for the first cut. It hits the requested black terminal board, amber/blue/yellow cards, thin dependency lines, lanes, and compact status badges while leaving enough room for the animator to add motion and zooms.

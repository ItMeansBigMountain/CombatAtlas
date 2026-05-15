# Blocked handoff + unblock flow animation

Artifact: `index.html`

Purpose: a square, browser-playable motion study for the Hermes Kanban launch video beat where a downstream card receives upstream handoffs, blocks with a visible reason, and the user unblocks it from the same Kanban view.

What it shows:

- Parent handoff packets flowing from script/design cards into the animator card.
- The animator card shifting from running to blocked with a red blocker comment visible in the board.
- A user decision panel and cursor click on `unblock card`.
- The blocker clearing, dependency line resuming, and the downstream editor path lighting back up.

Timing:

- 12 second loop for fast review.
- Designed as the 70–80s review/blocking beat from the parent 90-second script.
- Includes a `Replay animation` control for screen recording.

Visual direction used:

- Near-black terminal board (#050507 / #0f1218).
- Amber, blue, yellow translucent cards.
- Green completion and red blocked state.
- Thin dashed dependency lines behind cards.
- Monospace terminal chrome and compact status badges.

Open locally:

```bash
xdg-open /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_5f06dce4/blocked-unblock-animation/index.html
```

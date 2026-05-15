# Hermes Kanban demo animation plan

Duration: 15 seconds at 15 fps, 1280x720, silent/social-friendly.

Narrative arc:
1. One large creative brief card lands on a dark dashboard: “Agent orchestration, visible.”
2. A director node decomposes the brief into specialist cards: Research, Storyboard, Animate, Edit, Review.
3. Cards move through TODO, READY, RUNNING, BLOCKED, DONE with readable captions and status colors.
4. Dependency lines fan out, amber on a blocker, then green as work completes.
5. Completed children fan back into a final output/review card and the dashboard holds on the product promise.

Visual treatment:
- Premium dark product UI, graphite canvas, floating dashboard panel.
- Five lanes: TODO, READY, RUNNING, BLOCKED, DONE.
- State colors: slate todo, cyan ready, violet running, amber blocked, green done.
- Thin neon dependency lines with moving packets and fan-out/fan-in structure.
- Captions under six words; essential action centered for social crops.

Implementation:
- Python stdlib generates SVG frames.
- ffmpeg with SVG/librsvg input renders the SVG sequence to H.264 MP4.
- HTML/SVG-style artifact is retained as individual frame sequence plus generator script.

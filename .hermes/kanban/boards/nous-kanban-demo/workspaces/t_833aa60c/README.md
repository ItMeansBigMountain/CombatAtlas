# Hermes Kanban final square cut

Artifacts:

- `hermes-kanban-launch-square.mp4` — final 1080x1080 H.264 MP4, 22 seconds, 24 fps, silent AAC track.
- `hermes-kanban-launch-poster.png` — poster frame at the final dashboard/control-plane beat.
- `render_final_cut.py` — reproducible SVG-frame renderer + ffmpeg encoder.

## Creative edit

The cut fans in the upstream research and animation beats into a tight square launch video:

1. Starts with terminal juggling as the problem.
2. Transitions into the Hermes Kanban board as the hero dashboard.
3. Shows cards being claimed and decomposed.
4. Shows research/design running in parallel and handing off into animation.
5. Includes a visible blocked/unblock moment on the board.
6. Ends with downstream edit/review/final-video cards complete and the line: “Hermes Kanban is the control plane. One board. Many agents. Visible progress.”

## Verification

Rendered with ffmpeg from generated SVG frames. `ffprobe` verification:

- Resolution: 1080x1080
- Duration: 22.000 seconds
- Frame rate: 24 fps
- Frames: 528
- Format: MP4 / H.264 / yuv420p

Poster frame was visually checked for square format, readable dashboard text, visible final-video card, and no obvious card title/status/body overlaps.

## Re-render

From this directory:

```bash
python3 render_final_cut.py
```

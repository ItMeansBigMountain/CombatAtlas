Hermes Kanban demo final cut

Primary deliverable:
/opt/data/kanban/boards/nous-kanban-demo/workspaces/t_0caeb0c6/hermes_kanban_demo_final.mp4

Specs:
- 14.466667 seconds
- 1280x720
- 30 fps H.264 MP4
- Silent/no audio track; designed to work with captions only
- Size: 457,010 bytes

Source reviewed:
/opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/hermes_kanban_demo_first_cut.mp4

Changes made for final cut:
- Re-rendered from the animator SVG-frame generator into this workspace.
- Tightened the runtime from 15.0s to 14.47s while keeping the full story inside the requested 10-20s social clip window.
- Reworded captions to make the fan-out/fan-in dependency story explicit:
  - "Fan-out: director splits parallel tasks."
  - "Dependencies unlock the next card."
  - "Fan-in: work flows to done."
- Moved the final "Final video card: DONE" hero card upward so it no longer overlaps the lower caption band.
- Verified the final contact sheet shows todo/ready/running/blocked/done columns, blocked/done states, dependency lines, fan-out, fan-in, and final CTA.

Artifacts:
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_0caeb0c6/hermes_kanban_demo_final.mp4
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_0caeb0c6/generate_final_frames.py
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_0caeb0c6/final_contact_sheet.png
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_0caeb0c6/frames/frame_0000.svg ... frame_0216.svg

Render/verification commands used:
python3 generate_final_frames.py
ffmpeg -y -v warning -framerate 15 -i frames/frame_%04d.svg -c:v libx264 -pix_fmt yuv420p -r 30 hermes_kanban_demo_final.mp4
ffprobe -v error -show_entries format=duration,size:stream=index,codec_type,width,height,r_frame_rate -of json hermes_kanban_demo_final.mp4
ffmpeg -y -v warning -i hermes_kanban_demo_final.mp4 -vf "fps=1/1.2,scale=320:180,tile=4x3" -frames:v 1 -update 1 final_contact_sheet.png

Export limitations:
- Silent video only; no music/VO/SFX added.
- 16:9 master only; no square or vertical variants exported.
- Render pipeline remains deterministic SVG frames + ffmpeg/libx264 rather than Manim, matching the first-cut environment limitation.

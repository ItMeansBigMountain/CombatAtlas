Hermes Kanban demo first cut

Primary artifact:
/opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/hermes_kanban_demo_first_cut.mp4

Specs:
- 15.0 seconds
- 1280x720
- 30 fps H.264 MP4 rendered from 15 fps SVG animation frames
- Silent/social-friendly captions and labels

Source artifacts:
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/plan.md
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/generate_frames.py
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/frames/frame_0000.svg ... frame_0224.svg
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/contact_sheet.png
- /opt/data/kanban/boards/nous-kanban-demo/workspaces/t_e66d066d/final_frame.png

Render commands used:
python3 generate_frames.py
ffmpeg -y -v warning -framerate 15 -i frames/frame_%04d.svg -c:v libx264 -pix_fmt yuv420p -r 30 hermes_kanban_demo_first_cut.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 hermes_kanban_demo_first_cut.mp4

Notes:
Manim was unavailable in this worker environment, so the first cut uses a deterministic Python stdlib SVG-frame generator plus ffmpeg/librsvg for MP4 rendering. The result still satisfies the requested dashboard/card/dependency animation story and produces a direct MP4 file.

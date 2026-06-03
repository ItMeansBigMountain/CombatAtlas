# Hermes YouTube Workflow

This adapts a generic "use Claude for a faceless YouTube channel" guide into a Hermes-led workflow.

## How to Use Hermes Instead of Claude

Ask Hermes to handle each production stage as a concrete deliverable:

1. **Niche research**
   - Prompt: "Research 20 faceless YouTube channels in [niche], summarize patterns, and give me 5 differentiated angles."

2. **Idea generation**
   - Prompt: "Generate 50 video ideas for this channel. Rank by click potential, audience pain, production difficulty, and fit with my story."

3. **Title + thumbnail packaging**
   - Prompt: "Create 10 title/thumbnail packages for idea #X. Include visual composition, text, curiosity gap, and why it works."

4. **Script writing**
   - Prompt: "Write a 7-minute faceless YouTube script with a 15-second hook, retention loops every 45 seconds, visual directions, and narration-only format."

5. **Production assets**
   - Prompt: "Create a shot list with b-roll keywords, AI image prompts, chart ideas, sound cues, and captions for this script."

6. **Editing checklist**
   - Prompt: "Turn this script into an editing timeline with timestamps, visuals, captions, zooms, SFX, and music notes."

7. **Upload metadata**
   - Prompt: "Write the YouTube title, description, chapters, tags, pinned comment, and Shorts repurposing ideas."

8. **Analytics review**
   - Prompt: "Analyze these YouTube metrics and tell me what to change in hooks, titles, pacing, and topic selection."

## Important Boundaries

- Hermes can draft, research, script, plan, generate assets, and automate files.
- Actual YouTube account/channel creation may require the user to complete browser login, 2FA, or verification manually.
- Use OAuth/API credentials for uploads/analytics when automation is needed; avoid storing passwords.
- Publish private/unlisted test uploads before public automation.

## Future Automation

Possible scripts/tools later:

- `scripts/new_video.py` — create a new video workspace from a title.
- `scripts/render_prompt_pack.py` — produce image/video prompt packs.
- `scripts/youtube_metadata.py` — generate upload metadata from script.
- `scripts/analytics_review.py` — ingest CSV/API analytics and produce recommendations.

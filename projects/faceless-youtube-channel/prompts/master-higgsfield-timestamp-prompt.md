# Master Prompt: Timestamped Faceless Images

```text
Read the timestamped transcript below. For every timestamp, create exactly one image prompt.

Goal: the images should match the voiceover pacing for a faceless YouTube video.

Style requirements:
- Simple beginner-style drawing made in MS Paint.
- White background.
- Black outline.
- Minimal flat colors.
- Slightly rough, human-drawn, not polished.
- No photorealism.
- No cinematic realism.
- No detailed shading.
- Avoid text inside the image unless the narration specifically requires a label.

For each timestamp, output JSONL with:
{"timestamp":"0.00","seconds":0.0,"text":"narration line","prompt":"image generation prompt"}

Transcript:
[PASTE TIMESTAMPED TRANSCRIPT HERE]
```

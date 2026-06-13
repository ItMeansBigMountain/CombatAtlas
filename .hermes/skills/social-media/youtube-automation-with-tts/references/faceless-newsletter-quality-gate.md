# Faceless newsletter video quality gate

Use this reference when turning TLDR, Daily Stoic, Kino Body, or similar Gmail newsletters into videos for the user's faceless YouTube channel.

## Corrections captured from user feedback

The user rejected generic static/text-slide uploads and metadata that exposes the production method. The channel standard is:

- **One email = one video.** Do not combine newsletters and do not make a generic trend clip from several signals.
- **Use the actual newsletter content.** Subject, body, and core points must drive the script, b-roll prompts, captions, and public description.
- **Motivational-video vibe.** Cinematic pacing, emotional narration, relevant high-contrast b-roll, punchy captions, and a clear personal/operator takeaway.
- **ElevenLabs-quality voice required.** Do not upload robotic/flite fallback audio as final channel content.
- **Relevant AI-generated b-roll required.** Do not upload static text-slide placeholders. If no video/B-roll provider is configured, stop at script/storyboard.
- **Public metadata must hide production details.** Titles/descriptions/tags must not say AI-generated, automation, faceless, ElevenLabs, source email/profile, pipeline, or similar behind-the-scenes wording.
- **Descriptions should sound like the user.** Reword the email's idea naturally and opinionatedly; do not disclose the newsletter source mechanics.
- **Support links belong in descriptions.** Include the user's configured public URLs: Linktree, Buy Me a Coffee, Cash App, Venmo. Affiliate links come later only after the user approves video quality.

## Public metadata pattern

```text
<Reworded idea from the email in the user's voice.>

My read: <strong opinion / practical takeaway>. Build one proof today.

More from me: https://linktr.ee/sosai.oyama
Support the channel: https://buymeacoffee.com/affanfareev
Cash App: https://cash.app/$sosaioyama
Venmo: https://venmo.com/u/SosaiOyama

#Shorts
```

Avoid:

- "AI-generated"
- "faceless automation"
- "ElevenLabs"
- "generated from newsletter"
- "source profile" / "source email"
- "pipeline" / bot wording

## Implementation pitfall

Do not confuse a gate with a working renderer. It is not enough for code to check that provider keys exist and then proceed to render text slides or flite audio. The upload path must actually produce and use realistic voiceover plus relevant B-roll clips. If either generation step fails, the correct output is a storyboard package only, with no upload and no source-email trash.

## Quality gate before upload

A final video may be uploaded only if all are true:

1. The video is based on exactly one source email.
2. The actual email content is visible in the hook, narration, captions, and b-roll prompts.
3. Voiceover is realistic ElevenLabs or equivalent quality.
4. B-roll is relevant to the email's topic and not a static text placeholder.
5. **Classical Echos faceless newsletter videos should be about 2 minutes long** (target ~120 seconds, minimum 110 seconds) unless the user explicitly requests a shorter Short.
6. **Use multiple relevant stock clips** matched to script beats; do not upload a one-clip video or black/static fallback. A normal 2-minute render should use at least 6 distinct relevant Pexels/Hugging Face visual segments.
7. Metadata hides production details and includes the user's support links.
8. The final MP4 is 9:16, plays with audio, and passes a quick local probe.
9. Source Gmail message is trashed only after YouTube returns a verified `video_id`.

# Parrot AI integration notes

Last checked: 2026-06-15.

## Login status

Parrot AI login works in browser at `https://www.tryparrotai.com` with the user's email/password flow. Do not store the password in repo/docs.

## Product capabilities observed

- Web app has a logged-in create UI.
- Main create page supports `AI Voice` and `AI Music`.
- Voice generation has a 500-character limit in the new UI and 300-character limit in classic UI.
- Voice selection includes premium/community voices, including entertainment-character-style voices.
- There is an `Audio only` toggle in the new UI.
- Result area appears to support generated media playback and copy/share/download style workflows.
- History page exists and recent creations are available.

## API / automation findings

The frontend uses internal endpoints, but no public documented API was found from web search.

Observed Next.js/client endpoints in JS bundles:

- `/api/create`
- `/api/create-public`
- `/api/create-voice-preview`
- `/api/get-voice-preview`
- `/api/save-voice-preview`

`/api/create` appears to require:

- Firebase authenticated user ID token in `Authorization: Bearer <token>`
- Firebase AppCheck token in `X-Firebase-AppCheck`
- JSON payload from the create UI

This means full API integration is probably possible but will require either:

1. Browser automation using an authenticated browser session, or
2. A small Parrot adapter that obtains Firebase auth + AppCheck tokens from the web app context and calls `/api/create`, then watches the generated clip/history for a downloadable media URL.

## Pipeline recommendation

Start with a semi-automated experiment:

1. Generate a short script segment under 500 chars.
2. Use browser automation to open Parrot create UI.
3. Select an approved voice/persona.
4. Toggle `Audio only`.
5. Generate.
6. Download/capture the output audio URL from result/history.
7. Save it under the video workspace as `voice_parrot.mp3` or equivalent.
8. Feed that audio into the existing renderer.

Only after we can reliably export one audio file should we make it part of batch upload.

## Public channel safety note

Parrot offers celebrity/character-style voices. For public YouTube uploads, prefer original/parody-inspired personas rather than exact protected character impersonation. Example: `energetic nautical cartoon tech host` is safer than explicitly branding the final video as SpongeBob.

## Open questions

- Whether Parrot provides any official paid/lifetime-account API.
- Whether generated results expose stable downloadable audio URLs in History.
- Whether long newsletter scripts need to be chunked into multiple 300–500 character Parrot generations and concatenated.
- Whether commercial/public use is allowed under the user's plan and Parrot terms.

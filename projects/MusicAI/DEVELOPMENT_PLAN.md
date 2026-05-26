# MusicAI Development Plan

Last updated: 2026-05-26

## Current role

Music analysis, mood, playlist, and lyrics-first Watson NLU app.

## Portfolio priority

High

## Detected context

- Classification: Node app
- Detected stack: Node/package app, Python, Vercel config, Product direction
- Current tracked URL: https://musicai-rouge.vercel.app
- Tracker note: Harden OAuth callbacks, add public health/demo mode, durable token storage; Privacy-first onboarding, gentle prompts, local/demo mode before accounts

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`

## Development phases

1. Unify MusicAI with music-mood-app direction.
2. Add persistent profile/auth and meme fallback avatars.
3. Cache playlist/song analyses with per-song and aggregate results.
4. Keep no-login demo path for Vercel review while OAuth credentials are configured.

## Vercel / hosting plan

Vercel demo should expose health/demo analysis without requiring Spotify callback.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.

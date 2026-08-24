# tweetBetweenTheLines Development Plan

Last updated: 2026-08-24

## Current role

Active TypeScript/Expo universal product for privacy-first personal data liberation.

## Portfolio priority

High — explicitly promoted to active development.

## Detected context

- Classification: Active product rebuild with preserved Python/Django prior art
- Detected stack: TypeScript workspaces, Expo Router universal app, legacy Python archive
- Current tracked URL: https://tweetbetweenthelines.vercel.app
- Tracker note: Build a new consent-first product surface under `tweetBetweenTheLines`; preserve `social-media-analysis`, MusicAI, Journal AI, watsonAI, and legacy Python ideas as source material.

## Existing direction artifacts

- `PRODUCT_DIRECTION.md`
- `PRODUCT_ARCHITECTURE.md`
- `PLATFORM_OAUTH_ARCHIVE_MATRIX.md`

## Development phases

1. Preserve prior-art audit and build-vs-rewrite map.
2. Establish TypeScript/Expo universal architecture with a tested domain package.
3. Implement connector registry, consent receipts, archive import sandbox, token vault, profile cards, and export/delete workflows in small TDD slices.

## Vercel / hosting plan

Do not deploy until consent, revoke, export/delete, source provenance, and no-diagnosis safety gates are implemented and reviewed.

## Review checklist

- [ ] Local build/test or deterministic script check passes.
- [ ] No secrets, tokens, private data, or real student/customer records committed.
- [ ] Public demo has clear empty/loading/error states.
- [ ] Mobile-first layout is reviewed.
- [ ] README / workspace trackers updated with live URL and blockers.

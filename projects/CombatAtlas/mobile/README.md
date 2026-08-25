# CombatAtlas mobile

Expo universal shell for the existing CombatAtlas drill database.

## iPhone test

1. Install Expo Go from the iOS App Store.
2. From this directory run `npm ci && npm start -- --tunnel`.
3. Scan the terminal QR code with the iPhone camera.

The app also exports a responsive web build with `npm run export:web`.

## Preserved product data

The checked-in `src/data/combatData.js` is the same generated atlas used by the Vite app: 22 martial arts and 882 drills. `npm test` fails if either total changes unexpectedly.

## Ads and remove-ads boundary

- Ads are off until consent is accepted.
- Development uses explicit test identifiers; no production ad ID is bundled.
- Interstitial policy: at least 8 qualifying actions and 10 minutes apart, maximum 3 per session.
- A remove-ads entitlement suppresses ads.
- Purchase and restoration are isolated behind `createBillingBoundary`; only a verified matching product receipt grants the entitlement.
- The current Expo Go shell simulates remove-ads for UX testing. Production must replace the adapter with App Store receipt verification before enabling purchase UI.
- Preferences and consent are device-local through AsyncStorage. Personalized ads are a separate opt-in.

## Verification

```bash
npm ci
npm test
npm run doctor
npm run export:web
npx expo export --platform ios
```

Production App Store ads/IAP need a development build (not Expo Go), real store products, server-side receipt verification, production ad unit IDs supplied outside source control, and platform privacy review.

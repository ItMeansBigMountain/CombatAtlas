# CombatAtlas mobile

Expo source shell for the existing CombatAtlas drill database. Web, iOS, and Android JavaScript exports are verified locally; no signed or installable native build is currently published.

## iPhone test

1. Install Expo Go from the iOS App Store.
2. From this directory run `npm ci && npm start -- --tunnel`.
3. Scan the terminal QR code with the iPhone camera.

The app also exports a responsive web build with `npm run export:web`. Android is currently source/export-only: there is no APK/AAB/install URL or verified native launch. iOS Expo Go testing is development-only and is not a signed preview build.

## Preserved product data

The checked-in `src/data/combatData.js` is the same bundle used by the Vite app: 22 martial arts, 882 total draft/source records, and 15 customer-published named drill guides. Generic generated templates are not shown in customer search or art pages. `npm test` guards these totals and publication semantics.

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
npx expo export --platform android
```

Production App Store or Play Store ads/IAP need development builds (not Expo Go or JS exports), real store products, server-side receipt verification, production ad unit IDs supplied outside source control, and platform privacy review.

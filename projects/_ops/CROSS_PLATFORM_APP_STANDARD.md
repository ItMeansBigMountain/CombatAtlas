# Cross-Platform Application Standard

## Mandate

Every consumer-facing HeRmEz application must ship to:

- Web
- iOS
- Android

A project is not production-complete while any required target is only a mock, placeholder, or untested build.

## Default architecture

Use **TypeScript + React Native + Expo + Expo Router** for new consumer applications unless a documented technical constraint requires another cross-platform framework.

Recommended shape:

```text
apps/
  universal/       # Expo Router: web, iOS, Android
packages/
  api-client/      # typed transport and auth
  domain/          # business rules; no UI dependency
  design-system/   # cross-platform tokens/components
  validation/      # shared schemas
  analytics/       # consent-aware event contracts
services/
  api/              # platform-neutral backend
```

Use platform-specific files only where capabilities genuinely differ:

```text
Component.web.tsx
Component.ios.tsx
Component.android.tsx
```

Do not fork the whole product into three unrelated codebases.

## Existing web applications

For substantial Next.js or web-only products, choose after an architecture audit:

1. Migrate the user experience to an Expo Router universal app; or
2. Preserve the mature web application and add an Expo iOS/Android client while extracting shared domain, API, validation, auth, and design-token packages.

Do not force web-only DOM libraries into React Native. Do not rewrite stable server-side or commerce logic solely for visual code sharing.

## Backend contract

- One platform-neutral API and authorization model
- Typed, versioned contracts
- OAuth uses PKCE and deep/universal-link callbacks on mobile
- Secure tokens use Keychain/Keystore on native and secure HTTP-only cookies or equivalent web protections
- Uploads, notifications, background work, payments, and subscriptions have explicit platform adapters
- Account export/delete and consent controls behave consistently everywhere

## Required release gates

### Shared

- Unit, integration, contract, and end-to-end tests
- Accessibility and keyboard/screen-reader coverage
- Responsive layout and safe-area handling
- Offline, slow-network, retry, and expired-session states
- Privacy, security, analytics consent, export, and deletion tests
- No secrets embedded in web bundles or mobile packages

### Web

- Production web build
- Browser smoke tests at mobile and desktop widths
- Deep-link and OAuth callback verification
- Deploy URL, error monitoring, and rollback

### iOS

- EAS or native iOS production build
- Simulator and physical-device smoke evidence
- Keychain, permissions, universal links, notifications, background behavior
- App privacy manifest, store metadata/screenshots, review readiness
- TestFlight verification before public release

### Android

- EAS or native Android App Bundle build
- Emulator and physical-device smoke evidence
- Keystore, permissions, app links, notifications, background behavior
- Data Safety metadata, store listing/screenshots, review readiness
- Internal testing track verification before public release

## Exceptions

- RuneLite plugins are desktop plugin artifacts and cannot themselves target iOS/Android. Any separate companion consumer app must follow this standard.
- Backend services, infrastructure, CLIs, cron jobs, and internal automation are not consumer apps.
- Client websites that are contractually web-only require an explicit exception recorded on their project card.

## Definition of done

A consumer app can be called complete only when:

- Shared functionality works across web, iOS, and Android
- Required platform differences are documented
- All three builds pass
- Web is deployed
- iOS is verified through TestFlight or an approved equivalent
- Android is verified through an internal testing track or approved equivalent
- Store submission blockers, fees, legal metadata, and user decisions are recorded honestly

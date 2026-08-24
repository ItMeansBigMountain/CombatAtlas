# BurnoutBoyz universal release evidence

## Implemented targets

One Expo Router SDK 57 TypeScript client in `apps/universal` renders responsive web, iOS, and Android UI. It includes garage/manual views, VIN/manual onboarding, mileage updates, due/upcoming/history/recalls/sources, receipt camera/document adapters, local reminders, offline AsyncStorage cache, secure native VIN/token storage, and optional connected-car consent copy.

## Security and platform boundaries

- Native secrets use Expo SecureStore (iOS Keychain / Android Keystore-backed encrypted preferences). Web intentionally does not persist VIN or OAuth secrets; production web authentication must use server-managed HttpOnly cookies.
- The OAuth callback scheme is `burnoutboyz://oauth/callback`; production universal/app-link domains require a controlled domain before association files can be configured.
- Camera is requested only when the owner taps receipt photo. Documents accept images/PDFs. Selected files are not uploaded until an authenticated API endpoint exists.
- Push permission is requested only on user action. Android remote push requires a development build, not Expo Go. Background recall refresh remains server-driven; the client preserves last-known data.
- Demo schedule entries are explicitly synthetic and are not automotive advice.

## Commands

```sh
npm ci
npm run typecheck
npm run lint
npm run build:web
npx expo prebuild --platform android --no-install
npx expo config --type public --json
```

Local web artifact: `apps/universal/dist/index.html` (local-only URL when served: `http://localhost:8081`).

## External release gates not claimable from this Linux workspace

The app is configured for `com.burnoutboyz.manual`, but production completion still requires owner-controlled external accounts and hardware:

- Expo/EAS project login and signing credentials.
- Apple Developer membership, macOS/iOS simulator, physical iPhone, privacy manifest review, screenshots, and verified TestFlight build.
- Google Play developer account, Android SDK/emulator and physical Android device, Data Safety declaration, screenshots, signed AAB, and internal-track verification.
- Production web hosting/domain, monitoring, rollback, universal/app-link association files, authenticated API, upload endpoint, and push credentials.

Do not label this release production until those gates have evidence and exact production/TestFlight/internal-track URLs on the Kanban release card.

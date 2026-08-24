# Mobile release matrix

Verified: 2026-08-24

## Android

- Verified installable artifact: `https://temporary-rushing-saffron-chouvqx.vercel.app/downloads/tweet-between-the-lines-android-arm64-v0.1.0.apk`
- Package: `com.tweetbetweenthelines.app`
- Version: `0.1.0` (`versionCode` 1)
- Compatibility: Android 7.0+ (`minSdk` 24), arm64-v8a devices
- SHA-256: `5fb92dcbd23f68bae9883822921127e7fbba7e930e5d5869f6d6c1e4e66c26fb`
- Signing: APK Signature Scheme v2, local Android debug certificate. This is an installable preview, not a Play Store release; Android will require explicit permission to install from the browser.
- Build command: `./android/gradlew -p android assembleRelease -PreactNativeArchitectures=arm64-v8a --no-daemon --console=plain`

## iOS

- Production installable web path: `https://tweetbetweenthelines.vercel.app`
- Verified PWA preview (manifest, icons, and service worker): `https://temporary-rushing-saffron-chouvqx.vercel.app`
- Installation: open in Safari, Share, then **Add to Home Screen**.
- Native bundle evidence: `npx expo export --platform ios --output-dir dist-ios-native` passes.
- Native `.ipa` / TestFlight: unavailable. No authenticated Expo/EAS session, Apple distribution certificate, provisioning profile, App Store Connect credential, or macOS/Xcode host was found. Apple does not permit a Linux-built unsigned `.ipa` to be installed on normal iOS devices.

## Store status

- Apple App Store/TestFlight: not submitted.
- Google Play: not submitted.
- `eas.json` includes internal-preview and production profiles for use after authenticated Expo and store-signing credentials are supplied.
- The verified mobile-preview deployment is anonymous and expires after 60 minutes unless claimed. Claim URL: `https://vercel.com/claim-deployment?code=04bfc722-e7ae-4781-811d-67e7ab2d40db`. The APK is also preserved at Git commit `ab8f65c17`.

## Shared privacy behavior

The Android binary, iOS JavaScript export, and installable web client use the same Expo Router TypeScript application. The client stores native session references through Secure Store, keeps provider tokens server-side, labels the current workflow as synthetic/consented normalized JSON, exposes provenance and limitations, supports correction and JSON export, and clears browser-session data through confirmed deletion. Domain/API privacy tests pass with 41 domain tests and 9 API tests (1 PostgreSQL test skipped when its external fixture is absent).

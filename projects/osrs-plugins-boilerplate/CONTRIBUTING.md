# Contributing to osrs-plugins-boilerplate

Thanks for improving the OSRS API helper library. Keep this project small, dependency-light, and easy to copy into RuneLite plugins.

## Local prerequisites

- Java 11 or newer.
- No API keys or secrets are required.
- Do not add credentials, local `.env` files, or token-bearing URLs to the repository.

## Before changing code

1. Read `README.md` and the generated JavaDoc entry point at `docs/index.html`.
2. Confirm whether your change belongs in this reusable helper library or in a specific RuneLite plugin.
3. Prefer OSRS-only references and APIs. Do not link RuneScape 3 docs for OSRS plugin behavior.

## Adding a new API call

1. Choose the right client:
   - `WOMApiClient` for `https://api.wiseoldman.net/v2`.
   - `TempleApiClient` for `https://templeosrs.com/api/v2`.
2. Add one small static method that mirrors the endpoint name and returns `String` raw JSON.
3. Use the existing shared `HttpClient`, `User-Agent`, and 15 second request timeout pattern.
4. URL-encode user-controlled path/query values before expanding this library beyond the current simple helpers.
5. Add JavaDoc with:
   - what the method fetches,
   - parameter meaning,
   - endpoint path,
   - returned raw JSON behavior,
   - thrown exception behavior.
6. Update `README.md` endpoint tables and usage examples when the new call changes developer-facing API surface.
7. Regenerate JavaDoc under `docs/`.

## Verification

From the repository root:

```bash
./gradlew clean build javadoc --no-daemon

javadoc -d docs \
  -sourcepath src/main/java \
  -subpackages com.itmeansbigmountain.osrsapi \
  -windowtitle "osrs-plugins-boilerplate API" \
  -doctitle "osrs-plugins-boilerplate API"
```

The Gradle `javadoc` task writes build-local docs under `build/docs/javadoc`; the second command refreshes the committed `/docs` site required for this repository.

## Documentation expectations

Every public helper method should have JavaDoc before merge. Keep generated JavaDoc committed in `docs/` until the repository has CI or Pages automation that publishes it.

## Review checklist

- [ ] Source compiles on Java 11.
- [ ] JavaDoc regenerates without errors.
- [ ] README endpoint table matches the public methods.
- [ ] No secrets, account-specific values, or credentials were added.
- [ ] Network calls stay off the RuneLite game thread in examples.
- [ ] New OSRS references use Old School RuneScape sources only.

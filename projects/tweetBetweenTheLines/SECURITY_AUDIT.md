# Security audit triage

Last verified: 2026-08-24

## Summary

`npm audit --omit=dev --json` currently reports 10 moderate entries and no high or critical entries after aligning the Expo web stack to the current Expo 57 package line:

- `expo`: 57.0.16
- `expo-router`: 57.0.16

The remaining audit cascade is one transitive build-time advisory path:

`expo` -> Expo config/build tooling -> `xcode@3.0.1` -> `uuid@7.0.3`

Root advisory: GHSA-w5hq-g745-h8pq, “uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided”.

## Triage decision

Accepted temporary moderate build-time risk; not a runtime web MVP blocker.

Rationale:

1. The remaining vulnerable package is reachable through Expo configuration/prebuild tooling, not the browser app runtime bundle or API server runtime path.
2. The affected advisory concerns `uuid` v3/v5/v6 calls with a caller-provided output buffer. The observed `xcode` dependency path uses UUID generation for project-file tooling, not user-provided web/API request data.
3. `npm audit fix --force` proposes dependency changes that are not appropriate for this product release gate without upstream Expo/xcode support.
4. Overriding `uuid` outside `xcode`'s declared semver range would create an invalid dependency tree and risks breaking native build tooling.

## Required follow-up

Re-check during every release candidate:

```text
npm view expo version
npm view expo-router version
npm audit --omit=dev --json
npm ls expo expo-router uuid xcode --all
npm test
npm run typecheck
npm run build
```

Remove this accepted-risk note once Expo or xcode publishes a compatible dependency path to `uuid >= 11.1.1` or otherwise removes the vulnerable package.

## Current release boundary

This audit note does not approve production OAuth, provider credentials, signed mobile store builds, monitoring, restore drills, incident drills, legal/privacy review, or safety review. Those remain separate production gates.

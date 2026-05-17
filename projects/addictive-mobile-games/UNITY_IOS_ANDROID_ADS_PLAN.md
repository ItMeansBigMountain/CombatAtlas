# Unity iOS/Android Ads Plan

- **Date:** 2026-05-03
- **Decision:** Build addictive mobile games for both iOS and Android using Unity as the preferred engine.
- **Revenue path:** mobile ads first; optional in-app purchases later.

## Why Unity fits

Affan already has Unity experience and old Unity/game projects in `D:\Affan\Coding\UNITY`. Unity remains a good fit for quick cross-platform mobile prototypes.

## Target platforms

| Platform | Build target | Store |
| --- | --- | --- |
| iOS | Unity iOS build -> Xcode archive | Apple App Store |
| Android | Unity Android build / AAB | Google Play Store |

## Monetization standard

Use Unity Ads/Unity LevelPlay mediation rather than old direct legacy ad integration.

Recommended ad placements:

| Ad format | Where it belongs | Rule |
| --- | --- | --- |
| Rewarded video | Continue after fail, bonus coins, revive, unlock skin | Highest priority; player chooses it |
| Interstitial | Between rounds / after every few attempts | Never during active gameplay |
| Banner | Menus only, if not ugly | Avoid on tiny fast-play screens |

## First MVP game pattern

Pick one simple addictive loop:

1. one-tap dodge / timing game
2. 60-second score chase
3. endless runner variant
4. puzzle-with-streaks

MVP success:

- playable on iOS + Android simulator/device
- 60-second repeatable loop
- local high score
- rewarded ad placeholder abstraction
- no real ad keys committed

## Env/config standard

Do not hardcode ad IDs. Use environment/config placeholders:

```text
UNITY_ANDROID_GAME_ID=
UNITY_IOS_GAME_ID=
UNITY_REWARDED_AD_UNIT_ID=
UNITY_INTERSTITIAL_AD_UNIT_ID=
UNITY_BANNER_AD_UNIT_ID=
UNITY_ADS_TEST_MODE=true
```

## Source references

- Unity Ads supports iOS and Android: https://support.unity.com/hc/en-us/articles/360000117543-What-platforms-does-Unity-Ads-support-
- Unity Ads docs: https://docs.unity.com/grow/ads
- Unity monetization dashboard docs: https://docs.unity.com/grow/dashboard
- Unity LevelPlay guidance: https://docs.unity.com/en-us/grow/levelplay/sdk/ios/networks/guides/unity-ads

## Next action

Inspect `D:\Affan\Coding\UNITY` read-only and choose one Unity project as the fastest monetizable prototype base.

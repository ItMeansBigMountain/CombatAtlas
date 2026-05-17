# Additional Source Inventory Report

- **Date:** 2026-05-03
- **Mode:** read-only inspection
- **Destination root:** `C:\Users\faree\Desktop\OpEnCLAw`

## Source directories checked

| Source | Status | Useful findings | Suggested mapping |
| --- | --- | --- | --- |
| `C:\Users\faree\Desktop\javaScript` | found | React/Expo/Angular/Django-adjacent projects: `stockNews`, `Codology`, `3d-js`, fetch/API scripts, RDP chat. | `portfolio-sentiment-subscription-app`, `coding-school-platform`, `store-code-content-studio`, possible `tiktok-clone` |
| `C:\Users\faree\Desktop\AI102` | found | Microsoft AI services learning repo plus notes. User says this tree includes GitHub Actions + Terraform/Azure deployment patterns. | `coding-school-platform`, reusable deployment pattern docs, Azure/GitHub Actions templates |
| `D:\Affan\Coding` | found | Django APIs, ecommerce/social/music/course apps, Honda_Boyz, Unity projects. | `honda-tech-upgrade`, `tiktok-clone`, `music-mood-app`, `coding-school-platform`, `addictive-mobile-games` |
| `C:\Users\faree\Desktop\algos` | found | Algorithm examples for FreeCodeCamp and school: search, sort, linked list, recursion, factorials, word/prefix exercises. | `coding-school-platform` curriculum and worksheets |

## Notable mappings

### Portfolio Sentiment Subscription App

Potential source:

- `C:\Users\faree\Desktop\javaScript\stockNews`
  - frontend: Angular/TypeScript project
  - backend: Django backend with `core`, serializers, stock/news service patterns

Use carefully: inspect for secrets before copying. This may be more directly aligned than some older market notebooks.

### Coding School Platform

Potential source:

- `C:\Users\faree\Desktop\javaScript\programs\Codology`
  - React Native/Expo-style app and server files
- `C:\Users\faree\Desktop\algos`
  - teaching-friendly algorithm exercises
- `C:\Users\faree\Desktop\AI102\mslearn-ai-services`
  - AI services lessons and Azure AI teaching material
- `D:\Affan\Coding\Django\un-zipped\VideoService`
  - course/membership app references

### Honda Tech Upgrade

Potential source:

- `D:\Affan\Coding\Django\un-zipped\Honda_Boyz`
  - accounts and `honda_miles_app` modules already exist

### TikTok-like Social Video App

Potential source:

- `D:\Affan\Coding\Django\un-zipped\Trapistan`
  - feed, chat, comments, notifications, music, accounts, websocket routing
- `D:\Affan\Coding\Django\un-zipped\Uploader`
- `D:\Affan\Coding\Django\un-zipped\VideoService`

### Music Mood App

Potential source:

- `D:\Affan\Coding\Django\un-zipped\Trapistan\music`
- Existing imported `SoundDoe`

### Quick Addictive Mobile Games

Potential source:

- `D:\Affan\Coding\UNITY\Projects`
  - 2D game, topDown, Multiplayer, Dark Souls-style experiments

## Safety notes

- Do not copy auth-heavy projects until reviewed for secrets.
- Do not copy `node_modules`, `.git`, `.env`, SQLite DBs, media uploads, caches, Unity build artifacts, or credential files.
- Treat Django settings and JavaScript API scripts as possible secret-risk areas.
- AI102 Azure/Terraform/GitHub Actions patterns should be copied as deployment references only after checking for subscription IDs, backend state config, or secrets.

## Recommended next copies

1. Copy `javaScript\stockNews` into `portfolio-sentiment-subscription-app\legacy-src\stock-news` after secret scan.
2. Copy `algos` teaching files into `coding-school-platform\legacy-src\algos` after excluding `.git`.
3. Copy `D:\Affan\Coding\Django\un-zipped\Honda_Boyz` into `honda-tech-upgrade\legacy-src\honda-boyz` after secret scan.
4. Copy `javaScript\programs\Codology` into `coding-school-platform\legacy-src\codology` after secret scan.

# tweetBetweenTheLines Platform OAuth and Archive Matrix

Last updated: 2026-08-24

## Connector policy

This matrix is intentionally conservative: a platform is `supported_api` only when official OAuth/API access exposes useful user-authorized history or profile/interest data without credential scraping, `supported_archive_import` when the official account export is the truthful full-history path, `manual_import_only` when users can upload official files but API coverage is too thin/restricted, and `blocked_or_restricted` when the platform's official developer path is not suitable for the requested connector. OAuth connectors must use authorization-code + PKCE wherever available, least-privilege scopes, a per-source consent receipt, refresh/revocation UX, and a deletion lineage for imported raw data.

## Executive decisions for implementation

| Platform | Initial connector decision | Why |
|---|---|---|
| Google / YouTube | `supported_api` + `supported_archive_import` | OAuth is mature, Google documents web/native OAuth and scopes, YouTube has a quota model, and Google Takeout is the official full-history lane.[1][2][3][4][5] |
| Facebook | `manual_import_first`, limited `supported_api` later | Facebook Login, permissions, app review, and token rules exist, but consumer full-history access belongs to the user archive rather than a broad third-party API.[7][8][9][10][11] |
| Instagram | `manual_import_first`, limited `supported_api` later | Instagram API with Instagram Login and Basic Display exist, but the official download is the safer full-history path for analysis.[12][13][14] |
| Threads | `blocked_or_restricted` for history; `supported_api` only for narrow authorized API features | Threads has official developer docs, but do not promise full-history personal import via OAuth unless the current app-review product actually exposes it.[15] |
| X / Twitter | `supported_archive_import`; `supported_api` only if paid/reviewed tier supports the required endpoints | X documents OAuth 2.0 PKCE, manage-post endpoints, archive download, and rate limits; historical completeness should come from archive import, not assumed API backfill.[16][17][18][19] |
| TikTok | `manual_import_first`, limited `supported_api` later | TikTok Login Kit and scopes exist, and TikTok documents user data requests; API scope/review should be treated as narrow and not full-history.[20][21][22][23] |
| Reddit | `supported_api` + `supported_archive_import` | Reddit OAuth/scopes and API rules exist, and Reddit documents account-data requests; API history may still be endpoint/rate limited.[24][25][26][27] |
| LinkedIn | `manual_import_first`, restricted `supported_api` | LinkedIn OAuth, profile API, and rate limits exist, but products are gated and full account data is via official download.[28][29][30][31] |
| Snapchat | `manual_import_first`, very limited `supported_api` | Snap Login Kit is mainly identity/profile, Snap documents data download, and developer terms constrain use; do not imply message/history API coverage.[32][33][34] |
| Discord | `supported_api` for identity/guild metadata + `supported_archive_import` | Discord OAuth2 and rate limits are official, but message/content history for a user should use the data package where available.[35][36][37] |
| Bluesky / AT Protocol | `supported_api` + repository export/import | AT Protocol documents OAuth and repository/account migration, and Bluesky docs describe API hosts; this is one of the strongest portability candidates.[38][39][40] |
| Pinterest | `supported_api` for boards/pins where authorized + privacy export path | Pinterest documents OAuth/API v5 and privacy access rights, but verify actual archive granularity before promising full-history analysis.[41][42][43] |
| Tumblr | `supported_api` + blog export | Tumblr has official OAuth/API docs and official blog export, plus API terms; archive import is good for owned blogs but not a complete cross-user activity history.[44][45][46] |
| Twitch | `supported_api` for channel/account data + privacy-request/manual import for broader data | Twitch documents OAuth, scopes, and rate limits; privacy choices/access rights are the data-portability lane, not a turnkey full-history OAuth connector.[47][48][49][50] |
| Spotify | `supported_api` + extended-streaming-history import | Spotify documents OAuth PKCE, scopes, and rate limits; extended streaming history comes through Spotify's data export support flow.[51][52][53][54] |
| Mastodon / Fediverse | `supported_api` + instance export/import | Mastodon documents OAuth, scopes, and import/export, but implementation must be per-instance and feature availability may vary.[55][56][57] |

## Detailed platform matrix

| Platform | OAuth / PKCE | Review, scopes, and access gates | Full-history limits | Official export/import path | Refresh / revoke | Rate / cost | Retention, deletion, ToS constraints | Connector decision |
|---|---|---|---|---|---|---|---|---|
| Google / YouTube | Use Google authorization-code flow for web apps and PKCE for installed/native clients; request only APIs needed for YouTube/profile signals.[1][2][3] | Sensitive/restricted Google scopes may require verification; YouTube API quota cost must be modeled before sync jobs are enabled.[3][4] | YouTube Data API is not a guaranteed complete watch/comment/history export; use API for authorized deltas and metadata, not full user archive claims.[4][5] | Google Takeout is the official export lane for full-history user-owned data, including selectable products.[5] | Provide Google connected-app removal instructions and token revocation cleanup.[6] | YouTube Data API has quota costs per request; design backoff and quota budgets.[4] | Store only consented categories, track source-product lineage, and delete raw Takeout imports on user request. | `supported_api` for authorized YouTube/account features; `supported_archive_import` for full-history. |
| Facebook | Facebook Login is available for user authorization.[7] | Permissions reference and App Review are mandatory for advanced fields; assume least privilege and review before production use.[8][9] | Do not assume full post/like/message history through Graph API for consumer analysis. | Facebook's official download-your-information flow is the full-history import lane.[11] | Token expiry/refresh behavior follows Facebook Login access-token guidance; connected-source deletion must purge tokens.[10] | API limits and product access vary by Meta product/app review status; capture as per-app config. | No scraping, no password/session collection, and archive parser must respect user-selected categories. | `manual_import_first`; implement limited API only after product review confirms scopes. |
| Instagram | Instagram API with Instagram Login and Basic Display are official OAuth-style entry points.[13][14] | Advanced fields and publishing/business features are Meta-reviewed; consumer history should not be assumed available.[8][9][13] | OAuth API is not a complete personal archive for likes, comments, DMs, and full activity history. | Instagram official data download is the durable import path.[12] | Use Meta token handling and source revocation UX.[10] | Rate/product access depends on Meta approval and selected API product.[9][13] | Avoid credential scraping and do not ingest private DMs unless present in user-provided official archive and explicitly consented. | `manual_import_first`; limited `supported_api` for profile/media where approved. |
| Threads | Threads has official developer documentation.[15] | Treat Threads API capabilities as product-gated and app-review dependent. | No full-history personal analysis promise from OAuth until official docs/scopes prove coverage. | If Meta account export includes Threads artifacts, support explicit archive parsing only after schema validation.[11][15] | Use Meta token/source deletion patterns. | Meta product limits apply; keep connector disabled by default until reviewed. | No automated scraping of Threads timelines or credentials. | `blocked_or_restricted` for history; narrow `supported_api` only for approved features. |
| X / Twitter | X supports OAuth 2.0 authorization-code flow with PKCE.[16] | Endpoint access and paid tiers determine what can be read or managed; manage-post docs are not a full-history read grant.[17][19] | API access is rate/tier limited and may not return complete historical posts/likes/bookmarks. | X archive download is the official full-history path for user-owned posts and account data.[18] | Implement token revocation/delete locally; surface X connected-app removal instructions. | X rate limits are explicit and tier-sensitive; cost must be a product gate.[19] | Respect X developer terms; no credential scraping, no timeline scraping, no promise of deleted/private data recovery. | `supported_archive_import`; API connector only for paid/reviewed endpoints. |
| TikTok | TikTok Login Kit is official and documents OAuth-style login.[20] | TikTok scopes are documented, but access is purpose/scope limited and app-review dependent.[21][23] | Login Kit should not be treated as full watch/like/comment history access. | TikTok's request-your-data support flow is the official archive path.[22] | Store tokens per TikTok source and delete on disconnect; surface platform revocation docs where available. | Developer access/rate rules must be checked per approved product before production. | Terms and scope approval constrain data use; no session automation or credential collection.[23] | `manual_import_first`; limited API for profile/creator data where approved. |
| Reddit | Reddit OAuth2 and scopes are official.[24][25] | Scope selection must be explicit; Reddit's API rules/rate limits apply.[26] | OAuth can read authorized account content but should not be promised as a complete cross-subreddit archive if endpoints/rates omit data. | Reddit documents account-data copy requests.[27] | Delete local tokens and show Reddit app authorization removal guidance. | Respect Reddit API rate guidance and backoff.[26] | Do not scrape logged-in pages; use OAuth/API or user archive only. | `supported_api` for authorized account activity; `supported_archive_import` for completeness. |
| LinkedIn | LinkedIn supports authorization-code OAuth.[28] | Profile and other APIs are product-gated; rate limits are documented.[29][30] | LinkedIn APIs are not a general full-history personal data feed. | LinkedIn's account-data download is the official full-history path.[31] | Token deletion and LinkedIn app revocation UX required. | LinkedIn rate limits must be enforced per application/product.[29] | No scraping profiles, connections, or messages; import only official downloads with user consent. | `manual_import_first`; restricted API for approved profile/product scopes. |
| Snapchat | Snap Login Kit is the official OAuth-like identity path.[32] | Login Kit is narrow; developer terms govern approved use.[32][34] | Do not promise snaps, chats, memories, or story history via API. | Snapchat My Data download is the official portability path.[33] | Remove local tokens on disconnect; provide Snapchat app/data deletion guidance. | Treat Snap API access as narrow and product-specific. | Developer terms and privacy expectations make credential/session scraping unacceptable.[34] | `manual_import_first`; Login Kit only for identity/linking. |
| Discord | Discord OAuth2 supports scopes and authorization flows.[35] | Scopes such as identity/guilds/email are consented; message-content access is not a general personal archive grant.[35] | OAuth bot/user APIs should not be used to reconstruct private message history for analysis. | Discord data package is the official account-data export.[37] | Local token deletion and Discord authorized-app revocation UX required. | Discord rate limits are documented and must be built into sync workers.[36] | Do not self-bot or scrape; parse only official data package content the user uploads. | `supported_api` for identity/guild metadata; `supported_archive_import` for user-history data. |
| Bluesky / AT Protocol | AT Protocol OAuth is specified, and Bluesky documents API hosts/auth patterns.[38][39] | App design must handle personal data servers and DID/account identity rather than a single central host.[38][39] | Repository export is broad for repo records, but off-repo server logs/DMs may not be covered. | AT Protocol account migration/repository export is an official portability mechanism.[40] | Support token/session revocation and per-PDS disconnect. | Rate limits may vary by PDS/service; configure connector per host. | Keep imported CAR/repo records source-linked and support deletion/reprocessing. | `supported_api` + `repository_export_import`; high-priority connector. |
| Pinterest | Pinterest documents app authorization and API v5.[41][42] | API access requires approved scopes and app configuration.[41][42] | API may cover boards/pins but should not be sold as a complete history of all searches/views. | Pinterest privacy policy is the official rights/access path; verify downloadable archive structure before parser claims.[43] | Delete tokens and direct users to Pinterest privacy controls. | Rate and endpoint rules must be enforced per API docs/app tier.[42] | No scraping logged-in feeds; only official API or user-provided privacy export. | `supported_api` for pins/boards; archive parser after export schema validation. |
| Tumblr | Tumblr documents OAuth/API v2.[44] | API use is governed by Tumblr API terms.[46] | API covers blogs/posts but not necessarily all private account activity. | Tumblr blog export is official for owned blog content.[45] | Store/revoke OAuth tokens per blog/account. | Respect Tumblr API limits and terms.[44][46] | Import only user-owned blog exports; do not crawl dashboards/private content. | `supported_api` + `blog_export_import`. |
| Twitch | Twitch documents authentication, scopes, and API rate limits.[47][48][49] | OAuth scopes are granular and channel/account oriented.[48] | OAuth is not a full viewer/chat/history export for all user behavior. | Broader personal data should use Twitch privacy/access request paths.[50] | Token revocation and source disconnect required. | Twitch rate limits are official and must be modeled.[49] | No chat/session scraping; keep channel data and personal-data imports separate. | `supported_api` for approved account/channel data; `manual_import` for privacy exports. |
| Spotify | Spotify supports authorization code with PKCE.[51] | Scopes are documented for library, listening, playlist, profile, and playback categories.[52] | Web API has current/recent/top/listening-library surfaces but extended streaming history is not simply OAuth backfill. | Spotify's data support flow includes extended streaming history requests.[54] | Delete tokens and direct users to Spotify app-access revocation. | Spotify rate limits apply and must drive retry/backoff.[53] | Separate API-derived interest signals from uploaded extended-history archive data. | `supported_api` + `extended_streaming_history_import`. |
| Mastodon / Fediverse | Mastodon instances expose OAuth and scopes.[55][56] | Each instance is an independent server; app registration and capabilities vary. | API can cover the user's account on an instance, but moderation/deletion/federation gaps mean history is not guaranteed complete. | Mastodon documents import/export for moving accounts.[57] | Revoke/delete per instance. | Rate limits and terms vary by instance; connector registry must store host-specific config. | No cross-instance scraping; respect robots/instance terms and user consent. | `supported_api` + `instance_export_import`, with per-instance caveats. |

## Implementation notes for connector registry

- Required enum: `supported_api`, `supported_archive_import`, `manual_import_first`, `blocked_or_restricted`, and `unsupported`.
- Required per-source fields: `platform`, `auth_flow`, `pkce`, `oauth_scopes`, `review_required`, `api_history_ceiling`, `archive_import`, `refresh_revoke`, `rate_cost_notes`, `retention_delete_notes`, `tos_constraints`, `decision`, `source_ids`, and `last_verified_at`.
- Product copy must say “official APIs and official exports where available,” never “connect every platform” or “full history from OAuth.”
- Archive parsers must be schema-versioned, run in a sandbox, reject zip bombs/path traversal, and store raw import provenance separately from normalized features.
- OAuth connectors must fail closed when a scope, review status, or paid tier is unavailable.

## Source retrieval notes

I registered 57 unique official-source URLs in `.citation-ledger.json` and ran `check_links.py` against the source list. Most sources returned HTTP 200; X, Reddit, and Discord support pages returned 403 to the automated checker but are official human-facing help URLs and should be manually spot-checked in a browser during legal/product review.

## Sources

[1] https://developers.google.com/identity/protocols/oauth2/web-server — Google Identity: OAuth 2.0 for Web Server Applications
[2] https://developers.google.com/identity/protocols/oauth2/native-app — Google Identity: OAuth 2.0 for Mobile & Desktop Apps
[3] https://developers.google.com/identity/protocols/oauth2/scopes — Google Identity: OAuth 2.0 Scopes for Google APIs
[4] https://developers.google.com/youtube/v3/determine_quota_cost — YouTube Data API: Quota Calculator
[5] https://support.google.com/accounts/answer/3024190 — Google Account Help: Download your data
[6] https://support.google.com/accounts/answer/3466521 — Google Account Help: Third-party apps and services with access
[7] https://developers.facebook.com/docs/facebook-login — Meta for Developers: Facebook Login
[8] https://developers.facebook.com/docs/permissions/reference — Meta for Developers: Permissions Reference
[9] https://developers.facebook.com/docs/app-review — Meta for Developers: App Review
[10] https://developers.facebook.com/docs/facebook-login/guides/access-tokens — Meta Facebook Login: Access Tokens
[11] https://www.facebook.com/help/212802592074644 — Facebook Help: Download a copy of your information
[12] https://help.instagram.com/181231772500920 — Instagram Help: Download a copy of your information
[13] https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login — Instagram Platform: API with Instagram Login
[14] https://developers.facebook.com/docs/instagram-basic-display-api — Instagram Basic Display API
[15] https://developers.facebook.com/docs/threads — Threads API Documentation
[16] https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code — X API: OAuth 2.0 Authorization Code Flow with PKCE
[17] https://docs.x.com/x-api/posts/manage-tweets/introduction — X API: Manage Posts Introduction
[18] https://help.x.com/en/managing-your-account/how-to-download-your-x-archive — X Help: How to download your X archive
[19] https://docs.x.com/x-api/fundamentals/rate-limits — X API: Rate limits
[20] https://developers.tiktok.com/doc/login-kit-web — TikTok for Developers: Login Kit Web
[21] https://developers.tiktok.com/doc/scopes-overview — TikTok for Developers: Scopes Overview
[22] https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data — TikTok Support: Requesting your data
[23] https://developers.tiktok.com/doc/overview — TikTok for Developers Documentation
[24] https://github.com/reddit-archive/reddit/wiki/OAuth2 — Reddit: OAuth2
[25] https://www.reddit.com/dev/api/oauth — Reddit: OAuth2 Scopes
[26] https://github.com/reddit-archive/reddit/wiki/API — Reddit API Wiki: API
[27] https://support.reddithelp.com/hc/en-us/articles/360043048352-How-do-I-request-a-copy-of-my-Reddit-data-and-information — Reddit Help: Request a copy of your Reddit data
[28] https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow — LinkedIn: Authorization Code Flow
[29] https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts/rate-limits — LinkedIn API: Rate Limits
[30] https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api — LinkedIn: Profile API
[31] https://www.linkedin.com/help/linkedin/answer/a1339364/downloading-your-account-data — LinkedIn Help: Download your account data
[32] https://developers.snap.com/snap-kit/login-kit/overview — Snap Kit: Login Kit Overview
[33] https://help.snapchat.com/hc/articles/7012305371156 — Snapchat Support: Download My Data
[34] https://www.snap.com/terms/developer — Snap Developer Terms
[35] https://discord.com/developers/docs/topics/oauth2 — Discord Developer Docs: OAuth2
[36] https://discord.com/developers/docs/topics/rate-limits — Discord Developer Docs: Rate Limits
[37] https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data — Discord Support: Requesting a Copy of your Data
[38] https://atproto.com/specs/oauth — AT Protocol: OAuth
[39] https://docs.bsky.app/docs/advanced-guides/api-directory — Bluesky Docs: API Hosts and Auth
[40] https://atproto.com/guides/account-migration — AT Protocol: Repository Export
[41] https://developers.pinterest.com/docs/getting-started/authentication-and-authorization — Pinterest Developers: Authorization
[42] https://developers.pinterest.com/docs/api/v5 — Pinterest Developers: API Overview
[43] https://policy.pinterest.com/en/privacy-policy — Pinterest Privacy Policy
[44] https://www.tumblr.com/docs/en/api/v2 — Tumblr API Documentation
[45] https://help.tumblr.com/export-your-blog — Tumblr Help: Export your blog
[46] https://www.tumblr.com/docs/en/api_agreement — Tumblr API License Agreement
[47] https://dev.twitch.tv/docs/authentication — Twitch Developer Docs: Authentication
[48] https://dev.twitch.tv/docs/authentication/scopes — Twitch Developer Docs: Scopes
[49] https://dev.twitch.tv/docs/api/guide — Twitch Developer Docs: Rate Limits
[50] https://www.twitch.tv/p/en/legal/privacy-notice — Twitch Privacy Choices
[51] https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow — Spotify Web API: Authorization Code with PKCE
[52] https://developer.spotify.com/documentation/web-api/concepts/scopes — Spotify Web API: Scopes
[53] https://developer.spotify.com/documentation/web-api/concepts/rate-limits — Spotify Web API: Rate limits
[54] https://support.spotify.com/us/article/understanding-my-data — Spotify Support: Understanding my data
[55] https://docs.joinmastodon.org/methods/oauth — Mastodon API: OAuth
[56] https://docs.joinmastodon.org/api/oauth-scopes — Mastodon API: OAuth Scopes
[57] https://docs.joinmastodon.org/user/moving — Mastodon User Guide: Import and export

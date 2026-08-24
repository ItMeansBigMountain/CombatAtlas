# tweetBetweenTheLines — Product Direction

> **Free the minds of the consumer with data.**

## Mission

tweetBetweenTheLines is a privacy-first personal data liberation platform. A user connects accounts or imports official account archives, chooses exactly which data categories may be analyzed, and receives an explainable personal profile built from their own digital history.

This is not a social listening product for advertisers. The user is the customer, controls the data, sees how every metric was derived, can revoke each source, and can export or permanently delete the complete profile.

## Product outcomes

The application should help a user explore:

- Interests and how they change over time
- Repeated topics, communities, creators, media, and activities
- Language style, vocabulary, tone, sentiment, and communication patterns
- Attention allocation and posting/consumption rhythms
- Values, motivations, and self-described goals
- Evidence-backed personality reflections
- Self-reported wellbeing and changes over time
- Conflicts between stated interests and observed attention
- Source-by-source provenance and confidence for every conclusion

## Mental-health safety boundary

The product must **not diagnose depression or another medical condition from social-media behavior**. Language and behavior signals are contextual and can be wrong, culturally biased, or affected by humor, role-playing, life events, missing data, and platform behavior.

The production design may provide:

- Clearly labeled, non-diagnostic wellbeing patterns
- User-initiated, validated self-report screening questionnaires
- Separate display of questionnaire results and observational signals
- Trend and uncertainty explanations
- A private reflection flow and links to qualified professional help
- Immediate crisis-resource guidance when a self-report indicates possible imminent harm

It must never state “you are depressed” based on posts, likes, messages, or model inference. It may say that a screening response suggests the user should consider speaking with a qualified professional, with the instrument, score, limitations, and date shown.

Personality must also be presented as a reflection rather than immutable truth. Prefer validated/open instruments and transparent trait dimensions over copying proprietary 16Personalities questions or branding.

## Data acquisition strategy

Each connector belongs to one of three lanes:

1. **Official OAuth/API** — least-privilege scopes, PKCE where supported, incremental sync, source-specific revocation.
2. **Official user archive/import** — the user requests a platform export and uploads it directly; parsing happens locally or in an isolated encrypted worker.
3. **Manual/user-provided source** — a transparent fallback for platforms that do not grant production API access to consumer-history data.

No credential scraping, session-cookie theft, ToS-violating automation, or pretending that login access includes full-history access.

“All platforms” means an extensible platform registry and honest coverage matrix across major networks—not a false promise that every platform exposes every category through OAuth.

Initial coverage research must include at least:

- Google and YouTube
- Meta: Facebook, Instagram, Threads
- X/Twitter
- TikTok
- Reddit
- LinkedIn
- Snapchat
- Discord
- Bluesky
- Pinterest
- Tumblr
- Twitch
- Spotify and other media-interest sources where user-authorized data is available

## Core architecture

- Web application with account/passkey or trusted OAuth sign-in
- Per-source consent receipts and scope ledger
- Encrypted token vault; tokens never reach analytics prompts
- Raw-data vault separated from normalized feature storage
- Import sandbox with malware/zip-bomb/schema validation
- Normalized personal-event schema with source, timestamp, provenance, and deletion lineage
- Deterministic feature extraction before LLM interpretation
- Explainable profile cards linking every claim to aggregate evidence
- Model/version/prompt provenance and reproducible profile snapshots
- Per-source reprocessing, revocation, export, and cryptographic deletion workflow
- Strong tenant isolation, audit logs, rate limits, retention controls, and red-team gates

## Prior-art consolidation

Use and modernize useful ideas/code from:

- `ItMeansBigMountain/tweetBetweenTheLines`
- `/opt/data/HeRmEz/projects/social-media-analysis`
- `ItMeansBigMountain/watsonAI`
- MusicAI OAuth/provider and interest-analysis patterns
- Journal AI reflection and personal-insight patterns

MusicAI remains a distinct music intelligence product. Reusable OAuth, token-vault, ingestion, profile, and explainability components may later become shared packages without forcing either app to depend on the other.

## Production gates

- Platform-by-platform official access and export matrix
- Legal/privacy/health-claim review
- Threat model and independent security review
- Bias and multilingual evaluation
- No diagnosis claims
- Explainability and confidence tests
- Consent, revoke, export, and delete tests
- Connector sandbox and archive-parser fuzzing
- Real deployment, observability, backup/restore, and incident-response verification
- Closed beta before broad public launch

# Twitter Therapy absorption record

## Decision

`tweetBetweenTheLines` is the canonical product. “Twitter Therapy App” is retired as an independent product direction. Its useful reflection concepts are absorbed here under an explicitly user-initiated, private, non-diagnostic model.

## Recoverable history audited

- Historical public deployment: `https://twitter-therapy-app.vercel.app`.
- At audit time it returned HTTP 200 from Vercel and served the static “HeRmEz live project review” shell built from `projects/_vercel_mvp/twitter-therapy-app`.
- Git source history is preserved in commits including `82372de83dc2217e23a3c47851b90a356c4cb9bc` and `4816462083f565ef421f83f5b77bffe156803f60`.
- Historical project source paths remain recoverable from Git under `projects/twitter-therapy-app/` and `projects/_vercel_mvp/twitter-therapy-app/`.
- The historical README described “NLP app to analyze tweets for depressive language and wellness signals.” The deployed shell reframed it as “Local-first text reflection and cognitive reframing prototype.”
- The legacy source was itself copied from `TweetBetweenTheLines` scripts and the Django `tweetDeleter` subproject. No credentials or historical secret material are carried into the canonical implementation.

## Concept map

| Historical concept | Canonical treatment |
| --- | --- |
| Tweet mood / depressive-language analysis | Descriptive observational language counts only; never a depression score, diagnosis, crisis prediction, or proof of wellbeing. |
| Therapy | Private reflection prompts and links to qualified help; the product does not claim to provide therapy. |
| Cognitive reframing | User-authored notes and prompts. No model rewrites the user’s experience as fact. |
| Breakup / heartbreak recovery | User explicitly creates and names a private period, selects records, and can delete/export it. Heartbreak is never inferred. |
| Emotion | Evidence-linked strain/supportive language categories with context limitations, not an emotional state label. |
| Narrative | Optional user-approved storylines remain a separate future consent plane; deterministic evidence comes first. |
| Progress | Earlier/later descriptive counts inside the user-selected period. Changes never establish recovery, healing, or causation. |
| Tweet deletion | Canonical source-specific deletion lineage, session deletion, export, and revocation controls. |
| Privacy | Private by default, sharing unavailable in this slice, selected evidence only, no upload in the static web MVP. |

## Implemented canonical slice

The private reflection vertical slice consists of:

- `packages/domain/src/privateReflection.ts`: fail-closed consent/private-visibility boundary, selected-event and time-window filtering, deterministic earlier/later counts, evidence, prompts, limitations, and deletion/export-ready output.
- `packages/domain/tests/privateReflection.test.ts`: consent, visibility, evidence minimization, progress, and non-diagnostic-copy tests.
- `apps/mobile/app/index.tsx`: mobile-first Reflection tab with explicit creation, private-only status, evidence, limitations, export inclusion, and one-tap session deletion.

## Retirement and redirect status

The legacy deployment is preserved as historical evidence until its Vercel project ownership and redirect target can be verified. Replacing it blindly could destroy provenance or alter an unrelated project. The safe retirement action is to configure that Vercel project to issue a permanent redirect to the canonical public URL after ownership verification; until then, this record and canonical product copy are the deprecation notice. No duplicate active development should occur under the historical paths.

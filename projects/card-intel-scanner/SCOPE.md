# Card Intel Scanner - MVP Scope

## Goal

Create a fast mobile-first web app that scans or searches Pokémon trading cards and aggregates price signals so the user can quickly decide whether a card is worth buying, selling, grading, or researching deeper.

## Core Features

1. **Image Scan / Upload** – User can take or upload a card photo from mobile.
2. **OCR Assist** – Browser-side OCR extracts visible card text as a starting search query.
3. **Manual Correction** – User can edit the OCR query because card scans are noisy.
4. **Card Matching** – Search the public Pokémon TCG API and list likely matches with set, number, rarity, and image.
5. **Price Aggregation** – Show available TCGplayer and Cardmarket price signals.
6. **Sold Comps Link** – Provide an eBay sold-comps query for reality-checking condition, grading, and hype.
7. **Blended Signal** – Calculate a simple median from available numeric price points.

## Constraints

- No backend for MVP.
- No paid API keys required.
- No accounts or inventory database yet.
- OCR is assistive, not authoritative.
- Condition and grading are not automated; user must validate against sold comps.
- App is unofficial and not affiliated with Pokémon, Nintendo, TCGplayer, Cardmarket, or eBay.

## Next Steps

- Deploy static app to Vercel after Vercel auth is restored.
- Add condition selector: raw LP/NM/MP, graded PSA/BGS/CGC.
- Add saved watchlist/local collection.
- Add backend only if we need durable portfolio tracking, alerts, or paid marketplace APIs.

## Validation Method

- `npm run build` passes.
- Preview server returns HTTP 200.
- Built bundle contains scanner/pricing source logic.
- Pokémon TCG API returns card metadata and pricing with browser-style request headers.

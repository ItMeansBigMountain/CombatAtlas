# music-mood-app live UI smoke test

Task: t_6933e8ae
URL tested: https://music-mood-app-chi.vercel.app/
Date: 2026-06-09

## Public HTTP status evidence

- `curl -I -L --max-time 20 https://music-mood-app-chi.vercel.app/` returned HTTP/2 200 from Vercel.
- Response content type: `text/html; charset=utf-8`.
- Vercel cache: HIT.
- HTML shell length fetched via Python urllib: 167 bytes, loading `/assets/index-skNp1l7j.js` and `/assets/index-W1fQKCAj.css` into `<div id="root"></div>`.

## Browser flows exercised

1. Loaded homepage in a real browser.
   - Visible hero: "HeRmEz live project review", "Music Mood App", subtitle "Mood-to-playlist experience shell with emotional check-in flow."
   - Visible CTA links: "Review demo" and "Next edits".
   - Visible content cards: "What this is", "Demo mode", "Source signal", and "Next build move".
   - Console after load: 0 console messages, 0 JS errors.

2. Clicked "Review demo".
   - Browser navigated to `https://music-mood-app-chi.vercel.app/#demo`.
   - Page scrolled to the `#demo` section.
   - Console after interaction: 0 console messages, 0 JS errors.

3. Navigated to "Next edits" / `#next`.
   - Direct anchor navigation to `https://music-mood-app-chi.vercel.app/#next` reached the "Next build move" section.
   - Console after navigation: 0 console messages, 0 JS errors.
   - Note: one direct browser-tool click on the already-loaded "Next edits" link did not change the hash from `#demo`; direct anchor navigation to `#next` worked. This may be a browser-tool flake or a minor click-target/scroll behavior worth rechecking after any UI change.

4. Keyboard spot check.
   - Pressing Tab focused the "Review demo" link.
   - Focus outline was present (`auto 1px`), so the first CTA is keyboard reachable.
   - The browser tool timed out on Enter after focus, so this part was not treated as a page defect; earlier mouse/anchor flow verified the same target.

## Observed results

What works:

- Public URL is anonymously accessible and renders successfully.
- Basic React/static shell loads with no observed JS console errors.
- Primary anchor flow to `#demo` works.
- Direct navigation to `#next` works.
- Layout is visually coherent at the tested desktop viewport: dark gradient background, cards, high-contrast yellow CTAs, and readable content blocks.

Unfinished / broken / usability issues:

1. Static review shell only; no real product flow.
   - The UI describes a "Mood-to-playlist experience" but provides no mood check-in, playlist analysis, song input, recommendation output, save/share action, or integration flow.
   - This is a product-completeness blocker, not a rendering bug.

2. Source content confirms implementation has not started.
   - The page itself exposes README text saying: "Implementation has not started in this scaffold."
   - This is useful for review, but it confirms the deployment is not a functional MVP.

3. Navigation is shallow.
   - Only two in-page anchors exist: `#demo` and `#next`.
   - There are no routes, forms, demos, API calls, or deeper click paths to test.

4. Missing/empty document title.
   - Browser navigation returned an empty page title. Add a meaningful `<title>` such as "Music Mood App – Mood-to-Playlist Demo" for accessibility, tabs, bookmarks, and SEO.

5. Direct click on "Next edits" after already being at `#demo` did not update the hash in one browser-tool interaction.
   - Direct URL navigation to `#next` worked, so this should be rechecked manually or after implementation work before filing as a hard bug.

## Console summary

- Homepage load: 0 console messages / 0 JS errors.
- After "Review demo" click: 0 console messages / 0 JS errors.
- After `#next` navigation: 0 console messages / 0 JS errors.

## Screenshots / report path

- Report path: `/opt/data/kanban/workspaces/t_6933e8ae/music-mood-smoke-report.md`
- Screenshot: browser visual inspection was performed on the homepage, but no durable screenshot path was returned by the browser tool; a later screenshot attempt for the `#next` view timed out.

## Recommended child fix PBIs created

- `t_ff8d5a08`: Fix PBI: choose standalone rebuild vs MusicAI merge for music-mood-app.
- `t_4f607795`: Fix PBI: replace music-mood static shell with clickable MVP flow.

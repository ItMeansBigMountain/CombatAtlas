
import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
const summary = "## README.md\n# Quick Addictive Mobile Games\n\nPipeline for fast, addictive mobile games prepared for app-store release and ad monetization.\n\n## Status\n\nBacklog imported on 2026-05-03. Implementation has not started in this scaffold.\n\n## Environment\n\nLocal configuration should come from `.env`. Do not commit real secrets. Keep committed examples in `.env.example`.\n\n\n## PROJECT.md\n# Project Plan - Quick Addictive Mobile Games\n\n- **Created:** 2026-05-03\n- **Source:** User merged todo lists from 2026-05-03\n- **Project path:** `C:\\Users\\faree\\Desktop\\OpEnCLAw\\addictive-mobile-games`\n- **Primary next action:** See `C:\\Users\\faree\\.openclaw\\workspace\\work-queue.md`.\n\n## Notes\n\nPipeline for fast, addictive mobile games prepared for app-store release and ad monetization.\n\n## Current decision\n\n- `FIRST_GAME_CONCEPT_SELECTION.md` compares 3 tiny game concepts and selects **Dodge Dot Rush** as the first prototype because it has the smallest playable loop.\n## Legacy source imported - 2026-05-03\n\n- `programs/clutter/VideoGames` copied to `legacy-src/video-games`.\n- Reason: Existing starter game scripts/assets.\n- Files copied: 9; skipped sensitive/generated/unreadable files: 0.\n- Next action: Review and modernize the copied source inside this project.\n## Legacy source imported - 2026-05-03\n\n- `AI/Self_Playing_Game` copied to `legacy-src/self-playing-game`.\n- Reason: Existing game AI experiment.\n- Files copied: 3; skipped sensitive/generated/unreadable files: 0.\n- Next action: Review and modernize the copied source inside this project.\n\n";
function App() {
  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">HeRmEz live project review</p>
      <h1>Addictive Mobile Games</h1>
      <p className="lede">Live review shell for addictive-mobile-games.</p>
      <div className="actions"><a href="#demo">Review demo</a><a href="#next">Next edits</a></div>
    </section>
    <section id="demo" className="grid">
      <article className="card"><h2>What this is</h2><p>This deployed MVP makes the project visible on Vercel today so we can keep iterating instead of leaving it buried as local notes or scripts.</p></article>
      <article className="card"><h2>Demo mode</h2><p>No accounts, no paid APIs, no secrets. This is a safe static shell for fast product review and next-step decisions.</p></article>
      <article className="card"><h2>Source signal</h2><pre>{summary}</pre></article>
    </section>
    <section id="next" className="next"><h2>Next build move</h2><p>Turn the strongest workflow from this project into a functional clickable feature, then wire any real integrations only after the UX proves valuable.</p></section>
  </main>
}
createRoot(document.getElementById('root')).render(<App />);

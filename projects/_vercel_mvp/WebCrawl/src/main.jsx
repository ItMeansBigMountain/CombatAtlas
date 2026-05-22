
import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
const summary = "## README.md\n# TRY TO FIND WEBSITE NETWORK API FIRST \n- GO ONTO THE INSPECT TOOL\n- NETWORK TAB\n- SORT INCOMMING WEB REQUESTS BY WATERFALL\n- CLEAR ALL  WEB CALLS A PAGE MAKES\n- USE JS BUTTON LIKE \"LOAD MORE\" TO SEE A JSON REQUEST\n- USE THE API'S DATA TO GET VARIABLES INSTEAD OF WEBSCRAPE\n- FIND THE PATTERN OF DATA FORMATTING\nby the way.... how does clearing chatGPT's API chat room work? does it remember everything on that api key?\n\n# SPIDER\n- Run Spider/main.py in order to extract all urls from a website\n\n\n how does clearing chatGPT's API chat room work? does it remember everything on that api key?\n you actually store the chat into a list that constantly populates... i wonder if we can pre-expose it to data then...";
function App() {
  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">HeRmEz live project review</p>
      <h1>Webcrawl</h1>
      <p className="lede">Live review shell for WebCrawl.</p>
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

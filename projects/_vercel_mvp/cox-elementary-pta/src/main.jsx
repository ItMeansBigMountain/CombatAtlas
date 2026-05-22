
import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
const summary = "## README.md\n# Cox Elementary PTA Website\n\nA modern, mobile-first, client-editable PTA website for **Cox Elementary PTA**.\n\nThe site is built to help parents quickly understand what is happening, volunteer with low friction, read newsletters, share announcements, print flyers with QR codes, and manage content through a simple admin panel.\n\n## Live Links\n\nProduction website:\n\n```text\nhttps://cox-elementary-pta.onrender.com/\n```\n\nAdmin panel:\n\n```text\nhttps://cox-elementary-pta.onrender.com/admin/\n```\n\nRender dashboard:\n\n```text\nhttps://dashboard.render.com/\n```\n\nGitHub repo:\n\n```text\nhttps://github.com/ItMeansBigMountain/cox-elementary-pta\n```\n\n## How the Infrastructure Works\n\n```text\nAI / developer updates code\n        \u2193\nGitHub stores the code\n        \u2193\nRender watches GitHub main branch\n        \u2193\nRender builds and deploys the Django website\n        \u2193\nWebsite runs online with a Django Admin panel\n        \u2193\nClient updates weekly content through /admin/\n```\n\nPlain English version:\n\n1. Code changes are made on a computer or with AI assistance.\n2. The code is pushed to GitHub.\n3. Render automatically sees the GitHub update.\n4. Render rebuilds and redeploys the website.\n5. The public website updates after a few minutes.\n6. The admin panel remains the place for client content updates.\n\n## Accounts / Services Needed\n\nTo fully operate the site, the project needs:\n\n- **GitHub account** \u2014 stores the website code and triggers deployments.\n- **Render account** \u2014 runs the live Django website and database.\n- **Stripe account** \u2014 used later for fundraising/payment links.\n- **Domain registrar account** \u2014 used later when attaching the custom domain.\n\n## Current Deployment Setup\n\nThe production site is a Django app hosted on Render.\n\nRender runs:\n\n- the Python/Django web app\n- the production database ";
function App() {
  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">HeRmEz live project review</p>
      <h1>Cox Elementary Pta</h1>
      <p className="lede">Live review shell for cox-elementary-pta.</p>
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

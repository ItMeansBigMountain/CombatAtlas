
import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
const summary = "## README.md\n# CombatAtlas - Martial Arts Drills Database\n\n## Overview\nCombatAtlas is a Django REST Framework application designed to serve as a comprehensive database for martial arts drills. The application organizes martial arts content into a hierarchical structure: Martial Arts -> Categories -> Drill Exercises.\n\n## Project Structure\n- **combatAtlas_Backend**: Django backend application\n  - **combatAtlas_Backend**: Main Django project configuration\n  - **core**: Django app containing models, views, and serializers\n- **combatAtlas_Frontend**: Frontend application (currently empty)\n\n## Core Models\n\n### MartialArt\n- `name`: CharField (max_length=100, unique=True)\n- `sport_type`: TextField\n- `description`: TextField\n- `image`: ImageField (optional)\n- `created_at`: DateTimeField (auto_now_add)\n\n### DrillCategory\n- `name`: CharField (max_length=100)\n- `martial_art`: ForeignKey to MartialArt\n- `description`: TextField\n- `image`: ImageField (optional)\n- `created_at`: DateTimeField (auto_now_add)\n\n### DrillExercise\n- `name`: CharField (max_length=100)\n- `difficulty_level`: CharField (max_length=50)\n- `drill_type`: CharField (max_length=100)\n- `category`: ForeignKey to DrillCategory\n- `description`: TextField\n- `image`: ImageField (optional)\n- `video_url`: URLField (optional)\n- `created_at`: DateTimeField (auto_now_add)\n\n## API Endpoints\nBased on the views.py file, the following API endpoints are implemented:\n\n### MartialArtViewSet\n- Standard CRUD operations for MartialArt\n- Custom action: `categories` (GET /martial-arts/{id}/categories/) - returns categories for a specific martial art\n\n### DrillCategoryViewSet\n- Standard CRUD operations for DrillCategory\n- Custom action: `drills` (GET /drill-categories/{id}/drills/) - returns drills for a specific category\n\n### DrillExerciseViewSet\n- Sta";
function App() {
  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">HeRmEz live project review</p>
      <h1>Combatatlas</h1>
      <p className="lede">Live review shell for CombatAtlas.</p>
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

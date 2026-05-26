import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ArrowLeft, ExternalLink, PlayCircle, Search } from 'lucide-react';
import { martialArts, searchAll, getArtProfile, getDrillMedia } from './data/combatData.js';
import './styles.css';

function App() {
  const [query, setQuery] = useState('');
  const [selectedArtId, setSelectedArtId] = useState(null);
  const [selectedDrill, setSelectedDrill] = useState(null);

  const search = useMemo(() => searchAll(query), [query]);
  const selectedArt = useMemo(() => selectedArtId ? getArtProfile(selectedArtId) : null, [selectedArtId]);
  const visibleArts = query ? search.arts : martialArts;
  const visibleDrills = query ? search.drills : [];

  function chooseArt(id) {
    setSelectedArtId(id);
    setSelectedDrill(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function goHome() {
    setSelectedArtId(null);
    setSelectedDrill(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  return <main>
    <header className="topbar">
      <button className="brand" onClick={goHome}>CombatAtlas</button>
      {selectedArt && <button className="back" onClick={goHome}><ArrowLeft size={17}/> All arts</button>}
    </header>

    <section className="hero-minimal">
      <p className="kicker">Find your next training session</p>
      <h1>Martial arts drills, kept simple.</h1>
      <label className="searchbar">
        <Search size={22}/>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search martial arts or drills"
          aria-label="Search martial arts or drills"
        />
      </label>
    </section>

    {selectedDrill ? <DrillView drill={selectedDrill} onBack={() => setSelectedDrill(null)} /> :
      selectedArt ? <ArtView art={selectedArt} onOpenDrill={setSelectedDrill} /> :
      <HomeView arts={visibleArts} drills={visibleDrills} hasQuery={Boolean(query.trim())} onChooseArt={chooseArt} onOpenDrill={setSelectedDrill} />}
  </main>;
}

function HomeView({ arts, drills, hasQuery, onChooseArt, onOpenDrill }) {
  return <>
    {hasQuery && <section className="search-results">
      <div className="section-title">
        <h2>Search results</h2>
        <p>{arts.length} martial arts · {drills.length} drills</p>
      </div>
      {drills.length > 0 && <div className="drill-strip">
        {drills.slice(0, 8).map((drill) => <DrillCard key={drill.id} drill={drill} onClick={() => onOpenDrill(drill)} />)}
      </div>}
    </section>}

    <section className="section-title">
      <h2>{hasQuery ? 'Martial arts' : 'Choose a martial art'}</h2>
      <p>{hasQuery ? 'Pick an art or open a matching drill.' : 'Start with the art, then open any drill inside it.'}</p>
    </section>

    <section className="art-grid">
      {arts.map((art) => <button key={art.id} className="art-card" onClick={() => onChooseArt(art.id)}>
        <img src={art.imageUrl} alt={art.imageAlt} loading="lazy" />
        <span>{art.name}</span>
      </button>)}
      {hasQuery && arts.length === 0 && drills.length === 0 && <p className="empty">No matches yet. Try “boxing”, “armbar”, “footwork”, or “kick”.</p>}
    </section>
  </>;
}

function ArtView({ art, onOpenDrill }) {
  return <section className="art-page">
    <div className="art-hero">
      <img src={art.imageUrl} alt={art.imageAlt} />
      <div>
        <p className="kicker">{art.origin}</p>
        <h2>{art.name}</h2>
        <p>{art.description}</p>
      </div>
    </div>

    <div className="section-title compact">
      <h2>Drills</h2>
      <p>{art.drills.length} options</p>
    </div>

    <div className="drill-grid">
      {art.drills.slice(0, 36).map((drill) => <DrillCard key={drill.id} drill={drill} onClick={() => onOpenDrill(drill)} />)}
    </div>
  </section>;
}

function DrillCard({ drill, onClick }) {
  const media = getDrillMedia(drill);
  return <button className="drill-card" onClick={onClick}>
    <img src={media.imageUrl} alt={media.imageAlt} loading="lazy" />
    <span>{drill.title}</span>
    <small>{drill.difficulty} · {drill.contactLevel}</small>
  </button>;
}

function DrillView({ drill, onBack }) {
  const media = getDrillMedia(drill);
  return <article className="drill-view">
    <button className="back inline" onClick={onBack}><ArrowLeft size={17}/> Back to drills</button>
    <img className="drill-photo" src={media.imageUrl} alt={media.imageAlt} />
    <div className="drill-copy">
      <p className="kicker">{drill.difficulty} · {drill.contactLevel}</p>
      <h2>{drill.title}</h2>
      <p>{drill.summary}</p>
      <a className="video-link" href={media.youtubeUrl} target="_blank" rel="noreferrer"><PlayCircle size={19}/> Watch a demonstration <ExternalLink size={15}/></a>
      <h3>How to practice</h3>
      <ol>{drill.instructions.slice(0, 4).map((step, index) => <li key={index}>{step}</li>)}</ol>
      <h3>Keep in mind</h3>
      <ul>{drill.coachingCues.slice(0, 3).map((cue, index) => <li key={index}>{cue}</li>)}</ul>
    </div>
  </article>;
}

createRoot(document.getElementById('root')).render(<App />);

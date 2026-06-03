import React from 'react';
import { createRoot } from 'react-dom/client';
import { TrendingUp, Radio, Mic2, Image as ImageIcon, Film, CheckCircle2, ArrowRight, Zap, DollarSign } from 'lucide-react';
import './styles.css';

const trendSources = [
  { name: 'Reddit RSS', cost: '$0', signal: 'viral social chatter', examples: ['r/popular', 'r/news', 'niche subs'] },
  { name: 'Hacker News', cost: '$0', signal: 'tech/AI spikes', examples: ['front page', 'high-points stories'] },
  { name: 'Google Trends RSS', cost: '$0', signal: 'search demand', examples: ['daily rising queries'] },
  { name: 'GDELT', cost: '$0', signal: 'global news events', examples: ['news themes', 'tone shifts'] },
];

const pipeline = [
  { icon: TrendingUp, title: 'Trend Watch', text: 'The VPS scans free feeds and APIs, then scores topics by velocity, controversy, audience fit, and source density.' },
  { icon: Radio, title: 'Angle Selection', text: 'Hermes turns a hot topic into a repeatable channel angle: hook, context, why it matters, hidden angle, takeaway.' },
  { icon: Mic2, title: 'Script + Voice', text: 'Original commentary is generated from sources, then converted to voiceover with free Edge/Piper-style TTS.' },
  { icon: ImageIcon, title: 'Visual Pack', text: 'Low-cost visuals: kinetic captions, diagrams, public images, and optional AI images only when they add value.' },
  { icon: Film, title: 'Render + Upload Kit', text: 'ffmpeg renders the MP4 and Hermes packages title options, description, tags, pinned comment, and thumbnail copy.' },
];

const backlog = [
  'Automate daily trend shortlist in Discord',
  'Generate scripts from selected trend briefs',
  'Build TTS voiceover and timestamped scene plan',
  'Render first faceless explainer MVP',
  'Add YouTube OAuth private upload later',
];

function App() {
  return (
    <main>
      <section className="hero">
        <div className="badge"><Zap size={16}/> VPS Automation Project</div>
        <h1>Faceless YouTube Channel</h1>
        <p className="lead">A cheap/free trend-to-video engine: catch what the internet is talking about, turn it into original faceless scripts, generate voiceover + visuals, then render upload-ready videos.</p>
        <div className="heroActions">
          <a href="#pipeline" className="button primary">See pipeline <ArrowRight size={18}/></a>
          <a href="#costs" className="button secondary">Cost strategy</a>
        </div>
      </section>

      <section className="stats">
        <div><strong>$0</strong><span>core trend feeds</span></div>
        <div><strong>24/7</strong><span>VPS monitoring</span></div>
        <div><strong>1 cmd</strong><span>future render flow</span></div>
      </section>

      <section id="sources" className="panel">
        <div className="sectionHeader">
          <h2>Free trend radar</h2>
          <p>We avoid paid social-listening tools first. The goal is enough signal to make one solid video at a time.</p>
        </div>
        <div className="grid cards">
          {trendSources.map((source) => (
            <article className="card" key={source.name}>
              <div className="cardTop"><h3>{source.name}</h3><span>{source.cost}</span></div>
              <p>{source.signal}</p>
              <ul>{source.examples.map((e) => <li key={e}>{e}</li>)}</ul>
            </article>
          ))}
        </div>
      </section>

      <section id="pipeline" className="panel darkPanel">
        <div className="sectionHeader">
          <h2>Content generation pipeline</h2>
          <p>Built for the VPS: less manual work, no desktop tools, no paid APIs unless the result justifies it.</p>
        </div>
        <div className="pipeline">
          {pipeline.map((step, idx) => {
            const Icon = step.icon;
            return <article className="step" key={step.title}>
              <div className="stepIcon"><Icon size={22}/></div>
              <div>
                <span>0{idx + 1}</span>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </div>
            </article>
          })}
        </div>
      </section>

      <section id="costs" className="split">
        <div className="panel costPanel">
          <DollarSign size={28}/>
          <h2>Cheap/free by default</h2>
          <p>Use RSS, HN, GDELT, Google Trends, Edge/Piper TTS, ffmpeg, and static/motion text visuals. Higgsfield or premium image/video tools stay optional.</p>
        </div>
        <div className="panel">
          <h2>Next build queue</h2>
          <ul className="checklist">
            {backlog.map((item) => <li key={item}><CheckCircle2 size={18}/>{item}</li>)}
          </ul>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);

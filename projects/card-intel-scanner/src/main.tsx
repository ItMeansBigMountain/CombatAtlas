import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { createWorker } from 'tesseract.js';
import './styles.css';

type CardMarket = {
  averageSellPrice?: number;
  lowPrice?: number;
  trendPrice?: number;
  suggestedPrice?: number;
  reverseHoloSell?: number;
  reverseHoloTrend?: number;
};

type TcgPlayerPrice = {
  low?: number;
  mid?: number;
  high?: number;
  market?: number;
  directLow?: number;
};

type PokemonCard = {
  id: string;
  name: string;
  number?: string;
  rarity?: string;
  set?: { name: string; series?: string; printedTotal?: number; releaseDate?: string };
  images?: { small?: string; large?: string };
  tcgplayer?: { url?: string; prices?: Record<string, TcgPlayerPrice> };
  cardmarket?: { url?: string; prices?: CardMarket };
};

type SourceRow = {
  source: string;
  metric: string;
  value: number | null;
  url?: string;
};

const API = 'https://api.pokemontcg.io/v2/cards';

function money(value: number | null | undefined) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}

function cleanOcr(text: string) {
  return text
    .replace(/[^a-zA-Z0-9\s'’.-]/g, ' ')
    .split(/\s+/)
    .filter((word) => word.length > 2)
    .slice(0, 8)
    .join(' ')
    .trim();
}

function priceRows(card: PokemonCard): SourceRow[] {
  const rows: SourceRow[] = [];
  const tcg = card.tcgplayer?.prices || {};
  for (const [variant, prices] of Object.entries(tcg)) {
    rows.push({ source: 'TCGplayer', metric: `${variant} market`, value: prices.market ?? prices.mid ?? null, url: card.tcgplayer?.url });
    rows.push({ source: 'TCGplayer', metric: `${variant} low`, value: prices.low ?? null, url: card.tcgplayer?.url });
  }
  const cm = card.cardmarket?.prices;
  if (cm) {
    rows.push({ source: 'Cardmarket', metric: 'trend', value: cm.trendPrice ?? null, url: card.cardmarket?.url });
    rows.push({ source: 'Cardmarket', metric: 'avg sell', value: cm.averageSellPrice ?? null, url: card.cardmarket?.url });
    rows.push({ source: 'Cardmarket', metric: 'low', value: cm.lowPrice ?? null, url: card.cardmarket?.url });
  }
  rows.push({
    source: 'eBay',
    metric: 'sold comps search',
    value: null,
    url: `https://www.ebay.com/sch/i.html?_nkw=${encodeURIComponent(`${card.name} ${card.set?.name || ''} ${card.number || ''} pokemon card`)}&LH_Sold=1&LH_Complete=1`
  });
  return rows;
}

function median(values: number[]) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function App() {
  const [query, setQuery] = useState('Charizard');
  const [cards, setCards] = useState<PokemonCard[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [loading, setLoading] = useState(false);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrText, setOcrText] = useState('');
  const [error, setError] = useState('');

  const selected = useMemo(() => cards.find((card) => card.id === selectedId) || cards[0], [cards, selectedId]);
  const rows = selected ? priceRows(selected) : [];
  const estimate = median(rows.map((row) => row.value).filter((value): value is number => typeof value === 'number'));

  async function searchCards(searchTerm = query) {
    const term = searchTerm.trim();
    if (!term) return;
    setLoading(true);
    setError('');
    try {
      const q = `name:${JSON.stringify(`*${term}*`)}`;
      const url = `${API}?q=${encodeURIComponent(q)}&pageSize=12&orderBy=-set.releaseDate`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Pokémon TCG API returned ${response.status}`);
      const data = await response.json();
      setCards(data.data || []);
      setSelectedId(data.data?.[0]?.id || '');
      if (!data.data?.length) setError('No card match. Try the exact card name or set number.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  }

  async function scanImage(file: File) {
    setOcrLoading(true);
    setError('');
    setOcrText('');
    try {
      const worker = await createWorker('eng');
      const result = await worker.recognize(file);
      await worker.terminate();
      const raw = result.data.text || '';
      const cleaned = cleanOcr(raw);
      setOcrText(raw.trim());
      if (cleaned) {
        setQuery(cleaned);
        await searchCards(cleaned);
      } else {
        setError('Scan did not find readable card text. Type the card name manually.');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Image scan failed');
    } finally {
      setOcrLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero panel">
        <div>
          <p className="eyebrow">card intel / price recon</p>
          <h1>Card Intel Scanner</h1>
          <p className="lede">
            Scan or search a Pokémon card, match it against the Pokémon TCG database, then compare price signals from TCGplayer, Cardmarket, and eBay sold comps.
          </p>
        </div>
        <div className="mission-box">
          <strong>MVP rule</strong>
          <span>No accounts. No inventory lock-in. Fast comps first.</span>
        </div>
      </section>

      <section className="grid">
        <article className="panel controls">
          <p className="eyebrow">01 / scan</p>
          <h2>Identify the card</h2>
          <label className="dropzone">
            <input type="file" accept="image/*" capture="environment" onChange={(event) => event.target.files?.[0] && scanImage(event.target.files[0])} />
            <span>{ocrLoading ? 'Scanning image…' : 'Upload / camera scan'}</span>
            <small>OCR grabs visible card text. Manual correction stays available.</small>
          </label>

          <label className="field">
            <span>Card name or OCR result</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && searchCards()} placeholder="Charizard, Pikachu, Umbreon VMAX…" />
          </label>
          <button disabled={loading || ocrLoading} onClick={() => searchCards()}>{loading ? 'Searching…' : 'Search prices'}</button>
          {error && <p className="error">{error}</p>}
          {ocrText && <details><summary>OCR raw text</summary><pre>{ocrText}</pre></details>}

          <div className="matches">
            <h3>Matches</h3>
            {cards.length === 0 ? <p className="muted">Search to load possible card matches.</p> : cards.map((card) => (
              <button className={`match ${selected?.id === card.id ? 'active' : ''}`} key={card.id} onClick={() => setSelectedId(card.id)}>
                <span>{card.name}</span>
                <small>{card.set?.name} #{card.number} · {card.rarity || 'unknown rarity'}</small>
              </button>
            ))}
          </div>
        </article>

        <article className="panel results">
          <p className="eyebrow">02 / aggregate</p>
          {!selected ? (
            <div className="empty">No card selected.</div>
          ) : (
            <>
              <div className="card-head">
                {selected.images?.small && <img src={selected.images.small} alt={selected.name} />}
                <div>
                  <h2>{selected.name}</h2>
                  <p>{selected.set?.name} · #{selected.number} · {selected.rarity || 'rarity unknown'}</p>
                  <div className="estimate">
                    <span>blended signal</span>
                    <strong>{money(estimate)}</strong>
                  </div>
                </div>
              </div>

              <div className="price-table">
                {rows.map((row, index) => (
                  <a className="price-row" href={row.url} target="_blank" rel="noreferrer" key={`${row.source}-${row.metric}-${index}`}>
                    <span>{row.source}</span>
                    <em>{row.metric}</em>
                    <strong>{money(row.value)}</strong>
                  </a>
                ))}
              </div>

              <div className="operator-note">
                <strong>Read:</strong> TCGplayer market is the US liquidity signal. Cardmarket is EU demand/trend. eBay sold comps validate reality for condition, grading, and hype spikes.
              </div>
            </>
          )}
        </article>
      </section>

      <section className="panel disclaimer">
        <strong>Source note:</strong> This MVP uses the public Pokémon TCG API for card metadata, TCGplayer, and Cardmarket pricing where available, plus an eBay sold-comps search link. It is unofficial and not affiliated with Pokémon, Nintendo, TCGplayer, Cardmarket, or eBay.
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);

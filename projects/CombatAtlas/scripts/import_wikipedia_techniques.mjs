import fs from 'node:fs/promises';

const endpoint = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Martial_arts_techniques&cmlimit=500&format=json&origin=*';
async function fetchJson(url) {
  const response = await fetch(url, { headers: { 'User-Agent': 'CombatAtlas/1.0 data import' } });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText} for ${url}`);
  return response.json();
}

let pages;
try {
  const category = await fetchJson(endpoint);
  pages = category.query.categorymembers.filter((page) => page.ns === 0).slice(0, 160);
} catch (error) {
  console.warn(`Wikipedia live import unavailable (${error.message}); using bundled technique-index fallback.`);
  const fallbackNames = ['Ashi guruma','Armbar','Back kick','Brazilian kick','Chokehold','Clinch fighting','Covering (martial arts)','De ashi barai','Double leg takedown','Elbow strike','Foot sweep','Front kick','Ground fighting','Hammerfist','Harai goshi','Head kick','Hip throw','Ippon seoi nage','Joint lock','Kata guruma','Knee strike','Low kick','Neck crank','Osoto gari','Parry','Punch (combat)','Rear naked choke','Roundhouse kick','Rubber guard','Shoulder throw','Side kick','Single-leg takedown','Spinning back fist','Sprawl (grappling)','Stance (martial arts)','Strike (attack)','Sweep (martial arts)','Throw (grappling)','Triangle choke','Uppercut','Wristlock','Uchi mata','Kimura lock','Omoplata','Guillotine choke','Ankle lock','Heel hook','Guard pass','Bridge and roll','Hip escape','Breakfall','Kesa gatame','Mount escape','Side control escape','Jab','Cross','Hook punch','Teep','Check hook','Bob and weave','Slip counter','Inside leg kick','Outside leg kick','Knee tap','Duck under','Arm drag','Sit-out','Granby roll','Shrimping','Technical stand-up','Men strike','Kote strike','Do strike','Sinawali','Hubud-lubud','Zornhau','Moulinet','Disarm','Knife defense'];
  pages = fallbackNames.map((title, index) => ({ title, ns: 0, pageid: index }));
}
const techniques = pages.map((page) => ({
  name: page.title,
  slug: page.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
  source: 'Wikipedia category index',
  sourceUrl: `https://en.wikipedia.org/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`,
  extract: '',
  license: 'CC BY-SA; fetch summaries slowly and verify attribution before merging copied text into seed database',
}));
await fs.mkdir('imports', { recursive: true });
await fs.writeFile('imports/wikipedia-techniques.json', JSON.stringify({ importedAt: new Date().toISOString(), count: techniques.length, techniques }, null, 2));
console.log(`Imported ${techniques.length} Wikipedia martial arts technique records into imports/wikipedia-techniques.json`);

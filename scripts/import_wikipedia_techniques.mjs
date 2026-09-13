import fs from 'node:fs/promises';
import path from 'node:path';

import { buildAttribution, mergeRecords, normalizeWikipedia } from './lib/lawful-ingestion.mjs';

const endpoint = 'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Martial_arts_techniques&cmlimit=500&format=json&origin=*';
const args = new Map(process.argv.slice(2).map((value, index, all) => value.startsWith('--') ? [value, all[index + 1]] : null).filter(Boolean));
const outputPath = args.get('--output') ?? 'imports/wikipedia-techniques-normalized.json';
const inputPath = args.get('--input');
const retrievedAtUtc = args.get('--retrieved-at') ?? new Date().toISOString();
async function fetchJson(url) {
  const response = await fetch(url, { headers: { 'User-Agent': 'CombatAtlas/1.0 data import' } });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText} for ${url}`);
  return response.json();
}

let pages;
if (inputPath) {
  const input = JSON.parse(await fs.readFile(inputPath, 'utf8'));
  pages = input.records ?? input;
} else try {
  const category = await fetchJson(endpoint);
  pages = category.query.categorymembers.filter((page) => page.ns === 0).slice(0, 160);
} catch (error) {
  console.warn(`Wikipedia live import unavailable (${error.message}); using bundled API snapshot with real page IDs.`);
  const fallback = JSON.parse(await fs.readFile('imports/research/wikipedia-martial-arts-techniques.json', 'utf8'));
  pages = fallback.records;
}
async function existingRecords() {
  try { return JSON.parse(await fs.readFile(outputPath, 'utf8')).records ?? []; }
  catch (error) { if (error.code === 'ENOENT') return []; throw error; }
}

const normalized = normalizeWikipedia(pages, retrievedAtUtc);
const records = mergeRecords(await existingRecords(), normalized);
const document = { schemaVersion: 1, source: 'Wikipedia category index', generatedAtUtc: retrievedAtUtc, count: records.length, records };
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, `${JSON.stringify(document, null, 2)}\n`);
let attributionRecords = records;
try {
  attributionRecords = attributionRecords.concat(JSON.parse(await fs.readFile('imports/bjjdata-normalized.json', 'utf8')).records ?? []);
} catch (error) { if (error.code !== 'ENOENT') throw error; }
await fs.writeFile('imports/ATTRIBUTION.md', buildAttribution(attributionRecords));
console.log(`Imported ${normalized.length} Wikipedia records; ${records.length} deduplicated records in ${outputPath}`);

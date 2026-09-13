import fs from 'node:fs/promises';
import path from 'node:path';

import { buildAttribution, mergeRecords, normalizeBjjData } from './lib/lawful-ingestion.mjs';

const DATASET_URL = 'https://ubershmekel.github.io/bjjdata/data.json';
const args = new Map(process.argv.slice(2).map((value, index, all) => value.startsWith('--') ? [value, all[index + 1]] : null).filter(Boolean));
const outputPath = args.get('--output') ?? 'imports/bjjdata-normalized.json';
const inputPath = args.get('--input');
const retrievedAtUtc = args.get('--retrieved-at') ?? new Date().toISOString();

async function loadInput() {
  if (inputPath) {
    const input = JSON.parse(await fs.readFile(inputPath, 'utf8'));
    return input.records ?? input;
  }
  const response = await fetch(DATASET_URL, { headers: { 'User-Agent': 'CombatAtlas/1.0 lawful-data-import (https://github.com/ItMeansBigMountain/HeRmEz)' } });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText} for ${DATASET_URL}`);
  return response.json();
}

async function existingRecords() {
  try { return JSON.parse(await fs.readFile(outputPath, 'utf8')).records ?? []; }
  catch (error) { if (error.code === 'ENOENT') return []; throw error; }
}

const normalized = normalizeBjjData(await loadInput(), retrievedAtUtc);
const records = mergeRecords(await existingRecords(), normalized);
const document = { schemaVersion: 1, source: 'bjjdata', generatedAtUtc: retrievedAtUtc, count: records.length, records };
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, `${JSON.stringify(document, null, 2)}\n`);
let attributionRecords = records;
try {
  attributionRecords = attributionRecords.concat(JSON.parse(await fs.readFile('imports/wikipedia-techniques-normalized.json', 'utf8')).records ?? []);
} catch (error) { if (error.code !== 'ENOENT') throw error; }
await fs.writeFile('imports/ATTRIBUTION.md', buildAttribution(attributionRecords));
console.log(`Imported ${normalized.length} bjjdata clips; ${records.length} deduplicated records in ${outputPath}`);

import { martialArts, drills, searchAll, getArtProfile, getDrillMedia } from '../src/data/combatData.js';
import fs from 'node:fs';

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
}

const ui = fs.readFileSync(new URL('../src/main.jsx', import.meta.url), 'utf8');

assert(typeof searchAll === 'function', 'exports universal searchAll helper');
assert(typeof getDrillMedia === 'function', 'exports drill media helper');
assert(searchAll('boxing').arts.some((art) => art.id === 'boxing'), 'universal search finds martial arts');
assert(searchAll('armbar').drills.length > 0, 'universal search finds drills');
assert(martialArts.every((art) => art.imageUrl && art.imageAlt), 'every martial art has a customer-facing image');
assert(drills.every((drill) => getDrillMedia(drill).imageUrl && getDrillMedia(drill).imageAlt), 'every drill resolves to an image');
assert(!decodeURIComponent(getDrillMedia(drills[0]).imageUrl).includes('<text'), 'generated illustrations do not embed text that can clip');
assert(drills.every((drill) => getDrillMedia(drill).youtubeUrl?.startsWith('https://www.youtube.com/results?search_query=')), 'every drill resolves to a YouTube demonstration search link');
assert(getArtProfile('bjj').drills.length > 0, 'selected art exposes drills');
assert(!/API|Vercel|seed|developer|KeyRound|Database|externalSources/i.test(ui), 'customer UI contains no developer-specific panels or copy');
assert(/placeholder="Search martial arts or drills/i.test(ui), 'landing page centers a universal search bar');
console.log('PASS: minimalist customer experience checks');

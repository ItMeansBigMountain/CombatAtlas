import { martialArts, drills, searchDrills, getArtProfile } from '../src/data/combatData.js';

function assert(condition, message) {
  if (!condition) {
    console.error(`FAIL: ${message}`);
    process.exit(1);
  }
}

assert(martialArts.length >= 20, 'ships at least 20 martial arts profiles');
assert(drills.length >= 500, 'ships at least 500 searchable drills');
assert(new Set(drills.map((d) => d.id)).size === drills.length, 'all drill ids are unique');
assert(drills.every((d) => d.instructions?.length >= 4), 'every drill has step-by-step instructions');
assert(drills.every((d) => d.safetyNotes?.length >= 2), 'every drill has safety notes');
assert(searchDrills({ query: 'armbar', difficulty: 'beginner' }).length > 0, 'search finds beginner armbar drills');
assert(searchDrills({ martialArt: 'muay-thai', category: 'striking' }).length >= 20, 'Muay Thai striking exploration is populated');
assert(searchDrills({ equipment: 'none', contactLevel: 'solo' }).length >= 20, 'no-equipment solo filter is populated');
assert(getArtProfile('bjj').drills.length >= 25, 'BJJ profile has enough drills to explore');
assert(getArtProfile('arnis-kali-eskrima').drills.some((d) => d.primaryCategory === 'weapons'), 'Kali profile includes weapon drills');
console.log(`PASS: ${martialArts.length} arts, ${drills.length} drills`);

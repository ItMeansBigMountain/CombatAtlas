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
assert(searchDrills({ martialArt: 'muay-thai', category: 'striking' }).some((d) => d.title === 'Teep to Low Kick'), 'Muay Thai striking search returns its curated drill');
assert(searchDrills().every((d) => d.id.startsWith('named-')), 'search only publishes curated named drills');
assert(getArtProfile('bjj').drills.length === 3, 'BJJ profile exposes its three curated guides');
assert(getArtProfile('arnis-kali-eskrima').drills.some((d) => d.primaryCategory === 'weapons'), 'Kali profile includes weapon drills');
for (const artId of ['kendo', 'fencing', 'hema', 'bjj', 'arnis-kali-eskrima']) {
  assert(
    getArtProfile(artId).drills.every((drill) => drill.martialArts.includes(artId)),
    `${artId} profile only presents drills authored for that art`,
  );
}
console.log(`PASS: ${martialArts.length} arts, ${drills.length} drills`);

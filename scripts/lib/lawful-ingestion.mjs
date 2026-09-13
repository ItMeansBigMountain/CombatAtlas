const ALLOWED_LICENSES = new Set(['MIT', 'CC0', 'public domain', 'CC BY 4.0', 'CC BY-SA 4.0']);
const CONTEXT_TAGS = new Set([
  'tournament', 'gi', 'no-gi', 'top', 'bottom', 'back', 'mount', 'guard', 'open-weight',
  'light-weight', 'middle-weight', 'medium-heavy-weight', 'heavy-weight', 'super-heavy-weight',
  'ultra-heavy-weight', 'rooster-weight', 'feather-weight', 'light-feather-weight', 'adult', 'male', 'female',
]);

function slug(value) {
  return String(value).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function assertTimestamp(value) {
  if (!value || Number.isNaN(Date.parse(value)) || new Date(value).toISOString() !== value) {
    throw new Error(`retrievedAtUtc must be an ISO-8601 UTC timestamp: ${value}`);
  }
}

export function normalizeBjjData(input, retrievedAtUtc) {
  assertTimestamp(retrievedAtUtc);
  const entries = Array.isArray(input) ? input : input?.entries;
  if (!Array.isArray(entries)) throw new Error('bjjdata input must contain an entries array');
  const records = entries.flatMap((entry) => (entry.clips ?? []).map((clip) => {
    const start = String(clip.start ?? '');
    const end = String(clip.end ?? '');
    const sourceRecordId = `bjjdata:${entry.id}:${start}-${end}`;
    const record = {
      schemaVersion: 1,
      recordType: 'technique-evidence',
      sourceRecordId,
      name: entry.title,
      slug: slug(sourceRecordId),
      techniqueFacets: [...new Set((clip.tags ?? []).map(slug).filter((tag) => tag && !CONTEXT_TAGS.has(tag)))].sort(),
      contextTags: [...new Set((clip.tags ?? []).map(slug).filter((tag) => CONTEXT_TAGS.has(tag)))].sort(),
      eventDate: entry.date ?? null,
      participants: Array.isArray(entry.who) ? entry.who : [],
      clip: { start, end },
      source: 'bjjdata',
      sourceUrl: entry.link,
      repositoryUrl: 'https://github.com/ubershmekel/bjjdata',
      license: 'MIT',
      attribution: 'bjjdata contributors; linked YouTube media remains owned and hosted by its respective rights holder.',
      retrievedAtUtc,
      firstSeenAtUtc: retrievedAtUtc,
      provenance: {
        datasetUrl: 'https://ubershmekel.github.io/bjjdata/data.json',
        upstreamEntryId: entry.id,
        contentPolicy: 'metadata-and-links-only',
      },
    };
    const errors = validateRecord(record);
    if (record.techniqueFacets.length === 0) errors.push('techniqueFacets must contain at least one technique tag');
    if (!entry.id || !start || !end) errors.push('sourceRecordId requires entry id and clip timestamps');
    if (errors.length) throw new Error(`${sourceRecordId}: ${errors.join('; ')}`);
    return record;
  }));
  return records;
}

export function normalizeWikipedia(pages, retrievedAtUtc) {
  assertTimestamp(retrievedAtUtc);
  if (!Array.isArray(pages)) throw new Error('Wikipedia input must be an array');
  return pages.filter((page) => page.ns === 0).map((page) => {
    if (!Number.isInteger(page.pageid) || page.pageid <= 0 || !String(page.title ?? '').trim()) {
      throw new Error('Wikipedia sourceRecordId requires a positive pageid and name');
    }
    const record = {
    schemaVersion: 1,
    recordType: 'technique-evidence',
    sourceRecordId: `wikipedia:${page.pageid}`,
    name: page.title,
    slug: slug(page.title),
    source: 'Wikipedia category index',
    sourceUrl: `https://en.wikipedia.org/wiki/${encodeURIComponent(page.title.replaceAll(' ', '_'))}`,
    license: 'CC BY-SA 4.0',
    attribution: `Wikipedia contributors, “${page.title}”, retrieved via the MediaWiki Action API.`,
    retrievedAtUtc,
    firstSeenAtUtc: retrievedAtUtc,
    provenance: {
      pageid: page.pageid,
      category: 'Category:Martial arts techniques',
      apiUrl: 'https://en.wikipedia.org/w/api.php',
      contentPolicy: 'names-and-identifiers-only',
    },
    };
    const errors = validateRecord(record);
    if (errors.length) throw new Error(`${record.sourceRecordId}: ${errors.join('; ')}`);
    return record;
  });
}

export function validateRecord(record) {
  const errors = [];
  for (const field of ['schemaVersion', 'recordType', 'sourceRecordId', 'name', 'source', 'sourceUrl', 'license', 'retrievedAtUtc', 'firstSeenAtUtc', 'attribution', 'provenance']) {
    if (record?.[field] === undefined || record?.[field] === null || record?.[field] === '') errors.push(`${field} is required`);
  }
  try { new URL(record?.sourceUrl); } catch { errors.push('sourceUrl must be an absolute URL'); }
  if (!ALLOWED_LICENSES.has(record?.license)) errors.push(`license is not allowed: ${record?.license}`);
  for (const field of ['retrievedAtUtc', 'firstSeenAtUtc']) {
    try { assertTimestamp(record?.[field]); } catch (error) { errors.push(error.message); }
  }
  if (record?.instructions || record?.extract || record?.description || record?.articleText) {
    errors.push('instructional text or copied prose is prohibited in source records');
  }
  if (record?.provenance?.contentPolicy === undefined) errors.push('provenance.contentPolicy is required');
  return [...new Set(errors)];
}

export function mergeRecords(existing, incoming) {
  const byId = new Map();
  for (const record of [...existing, ...incoming]) {
    const errors = validateRecord(record);
    if (errors.length) throw new Error(`${record?.sourceRecordId ?? 'unknown record'}: ${errors.join('; ')}`);
    const previous = byId.get(record.sourceRecordId);
    const latest = previous && previous.retrievedAtUtc > record.retrievedAtUtc ? previous : record;
    const earliestFirstSeen = previous && previous.firstSeenAtUtc < record.firstSeenAtUtc
      ? previous.firstSeenAtUtc
      : record.firstSeenAtUtc;
    byId.set(record.sourceRecordId, {
      ...latest,
      firstSeenAtUtc: earliestFirstSeen,
    });
  }
  return [...byId.values()].sort((a, b) => a.sourceRecordId.localeCompare(b.sourceRecordId));
}

export function buildAttribution(records) {
  const groups = new Map();
  for (const record of records) {
    const key = `${record.source}\u0000${record.license}\u0000${record.repositoryUrl ?? record.provenance?.apiUrl ?? record.provenance?.datasetUrl ?? record.sourceUrl}`;
    if (!groups.has(key)) groups.set(key, { source: record.source, license: record.license, url: key.split('\u0000')[2], count: 0 });
    groups.get(key).count += 1;
  }
  const lines = [...groups.values()].sort((a, b) => a.source.localeCompare(b.source)).map(
    ({ source, license, url, count }) => `- ${source} — ${license} — ${count} record${count === 1 ? '' : 's'} — ${url}`,
  );
  return `# CombatAtlas data attribution\n\nGenerated from normalized provenance records. Linked videos/media are not copied or redistributed.\n\n${lines.join('\n')}\n`;
}

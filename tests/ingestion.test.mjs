import assert from 'node:assert/strict';
import test from 'node:test';

import {
  buildAttribution,
  mergeRecords,
  normalizeBjjData,
  normalizeWikipedia,
  validateRecord,
} from '../scripts/lib/lawful-ingestion.mjs';

const retrievedAtUtc = '2026-09-10T00:00:00.000Z';

test('normalizes bjjdata clips without copying media or prose', () => {
  const input = {
    entries: [{
      id: 'match-1',
      title: 'Competitor A vs Competitor B',
      link: 'https://www.youtube.com/watch?v=abc123',
      date: '2025',
      who: ['Competitor A', 'Competitor B'],
      clips: [{ start: '1:02', end: '1:18', tags: ['gi', 'armbar', 'joint-lock'] }],
    }],
  };
  const records = normalizeBjjData(input, retrievedAtUtc);
  assert.equal(records.length, 1);
  assert.deepEqual(records[0].techniqueFacets, ['armbar', 'joint-lock']);
  assert.equal(records[0].sourceRecordId, 'bjjdata:match-1:1:02-1:18');
  assert.equal(records[0].license, 'MIT');
  assert.equal(records[0].provenance.contentPolicy, 'metadata-and-links-only');
  assert.equal('instructions' in records[0], false);
  assert.equal('media' in records[0], false);
});

test('normalizes Wikipedia names and identifiers without article text', () => {
  const records = normalizeWikipedia([{ pageid: 123, ns: 0, title: 'Ashi guruma' }], retrievedAtUtc);
  assert.equal(records.length, 1);
  assert.equal(records[0].sourceRecordId, 'wikipedia:123');
  assert.equal(records[0].name, 'Ashi guruma');
  assert.equal(records[0].license, 'CC BY-SA 4.0');
  assert.match(records[0].attribution, /Wikipedia contributors/);
  assert.equal('extract' in records[0], false);
});

test('schema rejects missing, malformed, and prohibited provenance', () => {
  const valid = normalizeWikipedia([{ pageid: 123, ns: 0, title: 'Ashi guruma' }], retrievedAtUtc)[0];
  assert.deepEqual(validateRecord(valid), []);
  assert.match(validateRecord({ ...valid, sourceUrl: '' }).join('\n'), /sourceUrl/);
  assert.match(validateRecord({ ...valid, retrievedAtUtc: 'today' }).join('\n'), /retrievedAtUtc/);
  assert.match(validateRecord({ ...valid, license: 'CC BY-NC-SA 4.0' }).join('\n'), /license/);
  assert.match(validateRecord({ ...valid, instructions: ['copied text'] }).join('\n'), /instructional text/);
});

test('deduplication preserves additional provenance and update-safe merge preserves firstSeenAtUtc', () => {
  const first = normalizeWikipedia([{ pageid: 123, ns: 0, title: 'Ashi guruma' }], retrievedAtUtc)[0];
  const updated = { ...first, retrievedAtUtc: '2026-09-11T00:00:00.000Z', name: 'Ashi-guruma' };
  const merged = mergeRecords([first], [updated, updated]);
  assert.equal(merged.length, 1);
  assert.equal(merged[0].name, 'Ashi-guruma');
  assert.equal(merged[0].firstSeenAtUtc, retrievedAtUtc);
  assert.equal(merged[0].retrievedAtUtc, '2026-09-11T00:00:00.000Z');
});

test('update-safe merge rejects stale overwrite regardless of input ordering', () => {
  const oldest = normalizeWikipedia([{ pageid: 123, ns: 0, title: 'Old title' }], retrievedAtUtc)[0];
  const newest = { ...oldest, name: 'Current title', retrievedAtUtc: '2026-09-12T00:00:00.000Z' };
  const merged = mergeRecords([newest], [oldest]);
  assert.equal(merged.length, 1);
  assert.equal(merged[0].name, 'Current title');
  assert.equal(merged[0].firstSeenAtUtc, retrievedAtUtc);
  assert.equal(merged[0].retrievedAtUtc, '2026-09-12T00:00:00.000Z');
});

test('normalizers reject incomplete upstream records before writing output', () => {
  assert.throws(
    () => normalizeBjjData({ entries: [{ id: '', title: 'Missing identity', link: '', clips: [{ start: '', end: '', tags: [] }] }] }, retrievedAtUtc),
    /sourceRecordId|sourceUrl|techniqueFacets/,
  );
  assert.throws(
    () => normalizeWikipedia([{ pageid: null, ns: 0, title: '' }], retrievedAtUtc),
    /sourceRecordId|name/,
  );
});

test('attribution output is deterministic and includes every source', () => {
  const records = [
    normalizeWikipedia([{ pageid: 123, ns: 0, title: 'Ashi guruma' }], retrievedAtUtc)[0],
    ...normalizeBjjData({ entries: [{ id: 'm', title: 'A v B', link: 'https://www.youtube.com/watch?v=x', clips: [{ start: '0:01', end: '0:02', tags: ['armbar'] }] }] }, retrievedAtUtc),
  ];
  const output = buildAttribution(records);
  assert.match(output, /bjjdata/);
  assert.match(output, /Wikipedia category index/);
  assert.match(output, /MIT/);
  assert.match(output, /CC BY-SA 4.0/);
});

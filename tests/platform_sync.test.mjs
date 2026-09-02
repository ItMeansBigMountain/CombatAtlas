import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const mirroredFiles = [
  'src/data/combatData.js',
  'src/data/themeMedia.js',
];

test('Expo and Vite consume identical catalog and media modules', async () => {
  for (const sourcePath of mirroredFiles) {
    const mobilePath = `mobile/${sourcePath}`;
    const [webSource, mobileSource] = await Promise.all([
      readFile(sourcePath, 'utf8'),
      readFile(mobilePath, 'utf8'),
    ]);

    assert.equal(
      mobileSource,
      webSource,
      `${mobilePath} drifted from ${sourcePath}; update both copies together`,
    );
  }
});

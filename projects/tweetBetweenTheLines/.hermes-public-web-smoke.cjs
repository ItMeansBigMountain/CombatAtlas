const { chromium } = require('playwright');
const assert = require('node:assert/strict');

const url = process.argv[2];
if (!url) throw new Error('usage: node smoke.cjs <url>');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
  page.on('pageerror', (err) => pageErrors.push(err.message));

  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await assertVisible(page, 'tweetBetweenTheLines · runnable web MVP');
  await assertVisible(page, 'Analyze a synthetic fixture');
  await assertVisible(page, 'no upload occurs');

  await page.getByRole('button', { name: 'Use synthetic demo' }).click();
  await assertVisible(page, 'events analyzed locally');
  await assertVisible(page, 'Not a diagnosis or complete profile');
  await assertVisible(page, 'evidence rows');
  await assertVisible(page, 'imported source labels');

  await page.getByRole('button', { name: 'Inspect derivation' }).first().click();
  await assertVisible(page, 'How “');
  await assertVisible(page, 'No generative model or diagnosis');
  await assertVisible(page, 'Limitations');
  await assertVisible(page, 'Source coverage');
  await assertVisible(page, 'Evidence');

  await page.getByRole('button', { name: 'Mark inaccurate' }).first().click();
  await assertVisible(page, 'Correction saved separately from source evidence');
  await page.getByRole('tab', { name: 'control' }).click();
  await assertVisible(page, '1 correction(s)');

  const downloadPromise = page.waitForEvent('download', { timeout: 10000 });
  await page.getByRole('button', { name: 'Download complete JSON export' }).click();
  const download = await downloadPromise;
  assert.equal(download.suggestedFilename(), 'tweet-between-the-lines-export.json');
  await assertVisible(page, 'Export downloaded as JSON.');

  page.once('dialog', (dialog) => dialog.accept());
  await page.getByRole('button', { name: 'Delete browser-session data' }).click();
  await assertVisible(page, 'Browser-session data deleted');
  await page.getByRole('tab', { name: 'data' }).click();
  await assertVisible(page, 'Loaded data');
  await assertVisible(page, 'None.');

  assert.deepEqual(consoleErrors, []);
  assert.deepEqual(pageErrors, []);
  await browser.close();
  console.log(JSON.stringify({ ok: true, url, consoleErrors: consoleErrors.length, pageErrors: pageErrors.length }));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});

async function assertVisible(page, text) {
  await page.getByText(text, { exact: false }).first().waitFor({ state: 'visible', timeout: 15000 });
}

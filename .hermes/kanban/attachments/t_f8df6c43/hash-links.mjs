import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const errors = [];
page.on('console', (message) => {
  if (message.type() === 'error') errors.push(message.text());
});
page.on('pageerror', (error) => errors.push(error.message));

for (const id of ['pipeline', 'costs']) {
  await page.goto(`http://127.0.0.1:4173/#${id}`);
  await page.waitForFunction((sectionId) => {
    const element = document.getElementById(sectionId);
    const bounds = element?.getBoundingClientRect();
    return window.scrollY > 0 && bounds && bounds.top < window.innerHeight && bounds.bottom > 0;
  }, id);
  assert.equal(await page.evaluate(() => window.location.hash), `#${id}`);
}

await page.goto('http://127.0.0.1:4173/');
await page.locator('a[href="#costs"]').click();
await page.waitForFunction(() => {
  const element = document.getElementById('costs');
  const bounds = element?.getBoundingClientRect();
  return window.location.hash === '#costs' && window.scrollY > 0 && bounds && bounds.top < window.innerHeight && bounds.bottom > 0;
});

assert.deepEqual(errors, []);
await browser.close();
console.log('hash deep links and CTA scrolling passed with no console errors');

import { resolve } from 'node:path';
import { chromium } from 'playwright';

async function capture() {
  const browser = await chromium.launch({ headless: true });

  // Desktop - Clean Icons
  const page1 = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page1.goto('https://combatatlas-flame.vercel.app/', { waitUntil: 'networkidle', timeout: 30000 });
  await page1.screenshot({ path: resolve('preview-evidence/prod-desktop-clean.png'), fullPage: true });
  await page1.close();

  // Desktop - Real Photography
  const page2 = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page2.goto('https://combatatlas-flame.vercel.app/', { waitUntil: 'networkidle', timeout: 30000 });
  await page2.click('button[role="radio"]:has-text("Photos")');
  await page2.waitForTimeout(500);
  await page2.screenshot({ path: resolve('preview-evidence/prod-desktop-photos.png'), fullPage: true });
  await page2.close();

  // iPhone-width - Real Photography
  const page3 = await browser.newPage({
    viewport: { width: 390, height: 844, deviceScaleFactor: 3 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  await page3.goto('https://combatatlas-flame.vercel.app/', { waitUntil: 'networkidle', timeout: 30000 });
  await page3.click('button[role="radio"]:has-text("Photos")');
  await page3.waitForTimeout(500);
  await page3.screenshot({ path: resolve('preview-evidence/prod-iphone-photos.png'), fullPage: true });
  await page3.close();

  await browser.close();
  console.log('Screenshots captured');
}

capture().catch(console.error);

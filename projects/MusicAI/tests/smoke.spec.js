const { test, expect } = require('@playwright/test');

test('homepage is YouTube-first and roadmap providers are parked', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: /Your YouTube music taste/i })).toBeVisible();
  await expect(page.getByRole('link', { name: /Connect YouTube/i })).toBeVisible();
  await expect(page.getByText(/Spotify.*Future connector|Future connector: blocked/i)).toBeVisible();
  await expect(page.getByText(/SoundCloud.*Future connector|paid SoundCloud API access/i)).toBeVisible();
});

test('health reports durable Postgres storage and configured core providers locally', async ({ request }) => {
  const response = await request.get('/healthz');
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body.ok).toBe(true);
  expect(body.token_storage.backend).toBe('postgres');
  expect(body.token_storage.durable).toBe(true);
  expect(body.token_storage.encrypted).toBe(true);
  expect(body.providers.google_youtube).toBe(true);
  expect(body.providers.watson).toBe(true);
});

test('Watson text analyzer API returns a real Watson result for normal song text', async ({ request }) => {
  const response = await request.post('/api/analyze-text', {
    data: { text: 'I love this hopeful cinematic song full of bright energy and joy.' },
  });
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body.ok).toBe(true);
  expect(body.warning).toBeFalsy();
  expect(body.analysis.source).toBe('watson_nlu');
  expect(body.analysis.sentiment).toBeTruthy();
  expect(body.analysis.overall_emotion).toBeTruthy();
});

test('text analyzer page validates empty input and renders analysis for pasted lyrics', async ({ page }) => {
  await page.goto('/analyze-text');
  await expect(page.getByRole('heading', { name: /Watson lyric/i })).toBeVisible();
  await page.locator('textarea[name="text"]').fill('');
  await page.getByRole('button', { name: /Analyze with Watson/i }).click();
  await expect(page.getByText(/Paste lyrics or a song description first/i)).toBeVisible();

  await page.locator('textarea[name="text"]').fill('Dark nights turn into bright mornings, I feel hope and energy rising.');
  await page.getByRole('button', { name: /Analyze with Watson/i }).click();
  await expect(page.locator('pre')).toContainText('overall_emotion');
});

test('YouTube connect route redirects to Google OAuth with YouTube scopes', async ({ request }) => {
  const response = await request.get('/providers/youtube_music/connect', { maxRedirects: 0 });
  expect(response.status()).toBe(302);
  const location = response.headers()['location'];
  expect(location).toContain('accounts.google.com/o/oauth2/v2/auth');
  const url = new URL(location);
  expect(url.searchParams.get('scope')).toContain('youtube.readonly');
  expect(url.searchParams.get('scope')).toContain('youtube.force-ssl');
  expect(url.searchParams.get('redirect_uri')).toContain('/providers/youtube_music/callback');
});

test('playlist analysis route is protected until YouTube is connected', async ({ request }) => {
  const response = await request.get('/youtube/playlist/PL_TEST/analysis', { maxRedirects: 0 });
  expect([302, 303]).toContain(response.status());
  expect(response.headers()['location']).toBe('/');
});

test('single song analyzer accepts a song name and shows cached analysis UI', async ({ page, request }) => {
  const api = await request.post('/api/analyze-song', { data: { query: 'Kendrick Lamar - DNA' } });
  expect(api.status()).toBe(200);
  const json = await api.json();
  expect(json.ok).toBe(true);
  expect(`${json.result.title} ${json.result.artist || json.result.channel}`).toContain('Kendrick');
  const emotionValues = Object.values(json.result.analysis.overall_emotion || {});
  expect(emotionValues.some((value) => Number(value) > 0)).toBeTruthy();
  await page.goto('/analyze-song');
  await page.getByPlaceholder(/youtu\.be|Kendrick/i).fill('Kendrick Lamar - DNA');
  await page.getByRole('button', { name: 'Analyze song' }).click();
  await expect(page.getByRole('heading', { name: /DNA\.?/ })).toBeVisible();
  await expect(page.getByText(/Emotion profile/i)).toBeVisible();
});

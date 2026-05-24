const { defineConfig } = require('@playwright/test');

const PORT = process.env.PORT || '5001';

module.exports = defineConfig({
  testDir: './tests',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: 'retain-on-failure',
  },
  webServer: {
    command: `bash -lc 'set -a; [ -f .env.local ] && . ./.env.local; set +a; . .venv/bin/activate; PORT=${PORT} flask --app musicAI:application run --host 127.0.0.1 --port ${PORT}'`,
    url: `http://127.0.0.1:${PORT}/healthz`,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});

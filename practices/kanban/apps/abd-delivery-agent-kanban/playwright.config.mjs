import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from '@playwright/test';

const repoRoot = path.dirname(fileURLToPath(import.meta.url));
const planningRoot = path.join(
  repoRoot,
  'tests/e2e/data/pawplace-mini/docs/planning',
);

export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: '**/*.spec.{ts,mjs}',
  timeout: 60_000,
  retries: 0,
  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
  },
  webServer: [
    {
      command: 'npx tsx packages/app-server/index.ts',
      url: 'http://127.0.0.1:3001/health',
      reuseExistingServer: true,
      env: { PORT: '3001' },
    },
    {
      command: 'npx vite packages/app-client --host 127.0.0.1 --port 3000',
      url: 'http://127.0.0.1:3000',
      reuseExistingServer: true,
      env: { VITE_PLANNING_ROOT: planningRoot },
    },
  ],
});

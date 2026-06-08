import { defineConfig } from '@playwright/test';
import path from 'path';

const planningRoot = path.join(__dirname, 'tests/e2e/data/pawplace-stubs/docs/planning');

export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: '**/*_e2e.spec.ts',
  timeout: 60_000,
  retries: 0,
  workers: 1,
  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
  },
  webServer: [
    {
      command: 'npx tsx packages/app-server/index.ts',
      url: 'http://127.0.0.1:3001/health',
      reuseExistingServer: !process.env.CI,
      env: { PORT: '3001', PLANNING_ROOT: planningRoot },
    },
    {
      command: 'npx vite packages/app-client --host 127.0.0.1 --port 3000',
      url: 'http://127.0.0.1:3000',
      reuseExistingServer: !process.env.CI,
    },
  ],
});

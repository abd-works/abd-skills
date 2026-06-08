import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from '@playwright/test';

const repoRoot = path.dirname(fileURLToPath(import.meta.url));

export function planningRootFor(fixture) {
  return path.join(repoRoot, 'tests/e2e/data', fixture, 'docs/planning');
}

/** @param {'pawplace-stubs' | 'pawplace-mini'} fixture */
export function defineFixtureConfig(fixture) {
  const planningRoot = planningRootFor(fixture);

  return defineConfig({
    testDir: 'tests/e2e',
    testMatch: '**/*.spec.{ts,mjs}',
    timeout: 60_000,
    retries: 0,
    projects: [
      {
        name: fixture,
        metadata: { fixture, planningRoot },
      },
    ],
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
        env: { VITE_PLANNING_ROOT: planningRoot },
      },
    ],
  });
}

export const DEFAULT_E2E_FIXTURE = 'pawplace-stubs';

export function defaultPlanningRoot() {
  return planningRootFor(DEFAULT_E2E_FIXTURE);
}

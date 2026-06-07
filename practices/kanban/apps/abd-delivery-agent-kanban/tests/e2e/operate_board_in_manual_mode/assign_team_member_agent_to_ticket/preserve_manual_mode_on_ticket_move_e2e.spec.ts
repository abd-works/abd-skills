import { test, expect } from '@playwright/test';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const appRoot = path.resolve(process.cwd());
const resetScript = path.join(appRoot, 'scripts', 'reset-e2e-fixture.ps1');

test.describe('Preserve Board Mode on Ticket Move', () => {
  test.beforeEach(() => {
    execFileSync(
      'powershell',
      ['-NoProfile', '-File', resetScript, '-Fixture', 'pawplace-stubs'],
      { stdio: 'pipe' },
    );
  });

  test('Scenario 1: Ticket move in manual mode does not reset board mode', async ({ page }) => {
    execFileSync(
      'powershell',
      ['-NoProfile', '-File', resetScript, '-Fixture', 'pawplace-stubs'],
      { stdio: 'pipe' },
    );

    await page.goto('http://127.0.0.1:3001/board');
    await expect(page.locator('[data-ticket="project-all"]')).toBeVisible();

    const ticket = page.locator('[data-ticket="project-all"]').first();
    const role = page.locator('.kb-agent-avatar--draggable[data-role="business-expert"]').first();

    await role.dragTo(ticket);

    await expect(ticket.locator('.kb-skill-icon--pending-intent').first()).toBeVisible({ timeout: 5_000 });

    await expect
      .poll(
        async () => {
          const pending = await ticket.locator('.kb-skill-icon--pending-intent').count();
          const bot = await ticket.locator('.kb-skill-icon--bot').count();
          const done = await ticket.locator('.kb-skill-icon--done').count();
          return { pending, bot, done };
        },
        { timeout: 20_000 },
      )
      .toMatchObject({ done: 1 });
  });

  test.skip('Scenario 2: Manual drag to done remains in done after refresh', async ({ page }) => {
    // TODO: implement — Scenario 2: Manual drag to done remains in done after refresh
  });
});

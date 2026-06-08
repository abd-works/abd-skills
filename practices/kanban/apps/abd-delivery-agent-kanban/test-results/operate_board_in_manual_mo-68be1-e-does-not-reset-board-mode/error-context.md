# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: operate_board_in_manual_mode\assign_team_member_agent_to_ticket\preserve_manual_mode_on_ticket_move_e2e.spec.ts >> Preserve Board Mode on Ticket Move >> Scenario 1: Ticket move in manual mode does not reset board mode
- Location: tests\e2e\operate_board_in_manual_mode\assign_team_member_agent_to_ticket\preserve_manual_mode_on_ticket_move_e2e.spec.ts:17:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[data-ticket="project-all"]')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('[data-ticket="project-all"]')

```

```yaml
- text: Cannot GET /board
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import path from 'node:path';
  3  | import { execFileSync } from 'node:child_process';
  4  | 
  5  | const appRoot = path.resolve(process.cwd());
  6  | const resetScript = path.join(appRoot, 'scripts', 'reset-e2e-fixture.ps1');
  7  | 
  8  | test.describe('Preserve Board Mode on Ticket Move', () => {
  9  |   test.beforeEach(() => {
  10 |     execFileSync(
  11 |       'powershell',
  12 |       ['-NoProfile', '-File', resetScript, '-Fixture', 'pawplace-stubs'],
  13 |       { stdio: 'pipe' },
  14 |     );
  15 |   });
  16 | 
  17 |   test('Scenario 1: Ticket move in manual mode does not reset board mode', async ({ page }) => {
  18 |     execFileSync(
  19 |       'powershell',
  20 |       ['-NoProfile', '-File', resetScript, '-Fixture', 'pawplace-stubs'],
  21 |       { stdio: 'pipe' },
  22 |     );
  23 | 
  24 |     await page.goto('http://127.0.0.1:3001/board');
> 25 |     await expect(page.locator('[data-ticket="project-all"]')).toBeVisible();
     |                                                               ^ Error: expect(locator).toBeVisible() failed
  26 | 
  27 |     const ticket = page.locator('[data-ticket="project-all"]').first();
  28 |     const role = page.locator('.kb-agent-avatar--draggable[data-role="business-expert"]').first();
  29 | 
  30 |     await role.dragTo(ticket);
  31 | 
  32 |     await expect(ticket.locator('.kb-skill-icon--pending-intent').first()).toBeVisible({ timeout: 5_000 });
  33 | 
  34 |     await expect
  35 |       .poll(
  36 |         async () => {
  37 |           const pending = await ticket.locator('.kb-skill-icon--pending-intent').count();
  38 |           const bot = await ticket.locator('.kb-skill-icon--bot').count();
  39 |           const done = await ticket.locator('.kb-skill-icon--done').count();
  40 |           return { pending, bot, done };
  41 |         },
  42 |         { timeout: 20_000 },
  43 |       )
  44 |       .toMatchObject({ done: 1 });
  45 |   });
  46 | 
  47 |   test.skip('Scenario 2: Manual drag to done remains in done after refresh', async ({ page }) => {
  48 |     // TODO: implement — Scenario 2: Manual drag to done remains in done after refresh
  49 |   });
  50 | });
  51 | 
```
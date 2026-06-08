# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visualize_delivery_board\display_ticket_cards\show_active_skill_and_agent_on_ticket_e2e.spec.ts >> Show Active Skill and Agent on Ticket >> Scenario 4: Reviewing agent replaces executor
- Location: tests\e2e\visualize_delivery_board\display_ticket_cards\show_active_skill_and_agent_on_ticket_e2e.spec.ts:130:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:3000/board
Call log:
  - navigating to "http://127.0.0.1:3000/board", waiting until "load"

```

# Test source

```ts
  1   | import path from 'node:path';
  2   | import { execFileSync } from 'node:child_process';
  3   | import { readFile, writeFile, mkdir } from 'node:fs/promises';
  4   | import { expect, type Page, type Locator } from '@playwright/test';
  5   | 
  6   | type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };
  7   | 
  8   | const APP_ROOT = path.resolve(process.cwd());
  9   | const RESET_SCRIPT = path.join(APP_ROOT, 'scripts', 'reset-e2e-fixture.ps1');
  10  | const DATA_ROOT = path.join(APP_ROOT, 'tests', 'e2e', 'data', 'pawplace-stubs', 'docs', 'planning', 'kanban');
  11  | 
  12  | export const BOARD_JSON_PATH = path.join(DATA_ROOT, 'board.json');
  13  | export const KANBAN_JSON_PATH = path.join(DATA_ROOT, 'kanban.json');
  14  | export const ACTION_STATE_PATH = path.join(DATA_ROOT, 'action-state.json');
  15  | 
  16  | export async function readJsonFile<T extends JsonValue>(filePath: string): Promise<T> {
  17  |   const raw = await readFile(filePath, 'utf8');
  18  |   return JSON.parse(raw) as T;
  19  | }
  20  | 
  21  | export async function writeJsonFile(filePath: string, value: JsonValue): Promise<void> {
  22  |   await writeFile(filePath, JSON.stringify(value, null, 2), 'utf8');
  23  | }
  24  | 
  25  | export async function updateJsonFile<T extends JsonValue>(
  26  |   filePath: string,
  27  |   updater: (value: T) => T,
  28  | ): Promise<void> {
  29  |   const current = await readJsonFile<T>(filePath);
  30  |   const next = updater(current);
  31  |   await writeJsonFile(filePath, next);
  32  | }
  33  | 
  34  | export function resetPawPlaceStubsFixture(): void {
  35  |   const maxAttempts = 5;
  36  |   for (let attempt = 1; attempt <= maxAttempts; attempt++) {
  37  |     try {
  38  |       execFileSync('powershell', ['-NoProfile', '-File', RESET_SCRIPT, '-Fixture', 'pawplace-stubs'], {
  39  |         stdio: 'pipe',
  40  |       });
  41  |       return;
  42  |     } catch (error) {
  43  |       if (attempt === maxAttempts) throw error;
  44  |       execFileSync('powershell', ['-NoProfile', '-Command', 'Start-Sleep -Milliseconds 250'], {
  45  |         stdio: 'pipe',
  46  |       });
  47  |     }
  48  |   }
  49  | }
  50  | 
  51  | export async function clearLocalPlanningRootOverride(page: Page): Promise<void> {
  52  |   await page.addInitScript(() => {
  53  |     window.localStorage.removeItem('planningRootOverride');
  54  |     window.localStorage.removeItem('planningRoot');
  55  |   });
  56  | }
  57  | 
  58  | export async function goToBoard(page: Page): Promise<void> {
  59  |   await clearLocalPlanningRootOverride(page);
> 60  |   await page.goto('/board');
      |              ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:3000/board
  61  |   await expect(page.getByRole('heading', { name: /Kanban Board/i })).toBeVisible();
  62  | }
  63  | 
  64  | export function stageColumn(page: Page, stageId: string): Locator {
  65  |   return page.locator(`.kb-stage-group[data-stage="${stageId}"]`);
  66  | }
  67  | 
  68  | export function stageInProgressColumn(page: Page, stageId: string): Locator {
  69  |   return stageColumn(page, stageId).locator('.kb-sub-col--ip');
  70  | }
  71  | 
  72  | export function stageDoneColumn(page: Page, stageId: string): Locator {
  73  |   return stageColumn(page, stageId).locator('.kb-sub-col--done');
  74  | }
  75  | 
  76  | export function backlogColumn(page: Page): Locator {
  77  |   return page.locator('[data-end-col="backlog"]');
  78  | }
  79  | 
  80  | export function ticketCard(page: Page, ticketId: string): Locator {
  81  |   return page.locator(`[data-ticket="${ticketId}"]`).first();
  82  | }
  83  | 
  84  | export async function expectTicketInStageInProgress(
  85  |   page: Page,
  86  |   ticketId: string,
  87  |   stageId: string,
  88  | ): Promise<void> {
  89  |   await expect(stageInProgressColumn(page, stageId).locator(`[data-ticket="${ticketId}"]`)).toBeVisible();
  90  | }
  91  | 
  92  | export async function expectTicketInStageDone(
  93  |   page: Page,
  94  |   ticketId: string,
  95  |   stageId: string,
  96  | ): Promise<void> {
  97  |   await expect(stageDoneColumn(page, stageId).locator(`[data-ticket="${ticketId}"]`)).toBeVisible();
  98  | }
  99  | 
  100 | export async function expectTicketNotInGlobalBacklog(page: Page, ticketId: string): Promise<void> {
  101 |   await expect(backlogColumn(page).locator(`[data-ticket="${ticketId}"]`)).toHaveCount(0);
  102 | }
  103 | 
  104 | export async function waitForUiRefresh(page: Page): Promise<void> {
  105 |   await page.waitForTimeout(3_200);
  106 | }
  107 | 
  108 | export async function ensurePlanningDirectoryExists(): Promise<void> {
  109 |   await mkdir(DATA_ROOT, { recursive: true });
  110 | }
  111 | 
  112 | export async function ensureDirectoryExists(dirPath: string): Promise<void> {
  113 |   await mkdir(dirPath, { recursive: true });
  114 | }
  115 | 
```
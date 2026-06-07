import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { expect, type Page, type Locator } from '@playwright/test';

type JsonValue = null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

const APP_ROOT = path.resolve(process.cwd());
const RESET_SCRIPT = path.join(APP_ROOT, 'scripts', 'reset-e2e-fixture.ps1');
const DATA_ROOT = path.join(APP_ROOT, 'tests', 'e2e', 'data', 'pawplace-stubs', 'docs', 'planning', 'kanban');

export const BOARD_JSON_PATH = path.join(DATA_ROOT, 'board.json');
export const KANBAN_JSON_PATH = path.join(DATA_ROOT, 'kanban.json');
export const ACTION_STATE_PATH = path.join(DATA_ROOT, 'action-state.json');

export async function readJsonFile<T extends JsonValue>(filePath: string): Promise<T> {
  const raw = await readFile(filePath, 'utf8');
  return JSON.parse(raw) as T;
}

export async function writeJsonFile(filePath: string, value: JsonValue): Promise<void> {
  await writeFile(filePath, JSON.stringify(value, null, 2), 'utf8');
}

export async function updateJsonFile<T extends JsonValue>(
  filePath: string,
  updater: (value: T) => T,
): Promise<void> {
  const current = await readJsonFile<T>(filePath);
  const next = updater(current);
  await writeJsonFile(filePath, next);
}

export function resetPawPlaceStubsFixture(): void {
  const maxAttempts = 5;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      execFileSync('powershell', ['-NoProfile', '-File', RESET_SCRIPT, '-Fixture', 'pawplace-stubs'], {
        stdio: 'pipe',
      });
      return;
    } catch (error) {
      if (attempt === maxAttempts) throw error;
      execFileSync('powershell', ['-NoProfile', '-Command', 'Start-Sleep -Milliseconds 250'], {
        stdio: 'pipe',
      });
    }
  }
}

export async function clearLocalPlanningRootOverride(page: Page): Promise<void> {
  await page.addInitScript(() => {
    window.localStorage.removeItem('planningRootOverride');
    window.localStorage.removeItem('planningRoot');
  });
}

export async function goToBoard(page: Page): Promise<void> {
  await clearLocalPlanningRootOverride(page);
  await page.goto('/board');
  await expect(page.getByRole('heading', { name: /Kanban Board/i })).toBeVisible();
}

export function stageColumn(page: Page, stageId: string): Locator {
  return page.locator(`.kb-stage-group[data-stage="${stageId}"]`);
}

export function stageInProgressColumn(page: Page, stageId: string): Locator {
  return stageColumn(page, stageId).locator('.kb-sub-col--ip');
}

export function stageDoneColumn(page: Page, stageId: string): Locator {
  return stageColumn(page, stageId).locator('.kb-sub-col--done');
}

export function backlogColumn(page: Page): Locator {
  return page.locator('[data-end-col="backlog"]');
}

export function ticketCard(page: Page, ticketId: string): Locator {
  return page.locator(`[data-ticket="${ticketId}"]`).first();
}

export async function expectTicketInStageInProgress(
  page: Page,
  ticketId: string,
  stageId: string,
): Promise<void> {
  await expect(stageInProgressColumn(page, stageId).locator(`[data-ticket="${ticketId}"]`)).toBeVisible();
}

export async function expectTicketInStageDone(
  page: Page,
  ticketId: string,
  stageId: string,
): Promise<void> {
  await expect(stageDoneColumn(page, stageId).locator(`[data-ticket="${ticketId}"]`)).toBeVisible();
}

export async function expectTicketNotInGlobalBacklog(page: Page, ticketId: string): Promise<void> {
  await expect(backlogColumn(page).locator(`[data-ticket="${ticketId}"]`)).toHaveCount(0);
}

export async function waitForUiRefresh(page: Page): Promise<void> {
  await page.waitForTimeout(3_200);
}

export async function ensurePlanningDirectoryExists(): Promise<void> {
  await mkdir(DATA_ROOT, { recursive: true });
}

export async function ensureDirectoryExists(dirPath: string): Promise<void> {
  await mkdir(dirPath, { recursive: true });
}

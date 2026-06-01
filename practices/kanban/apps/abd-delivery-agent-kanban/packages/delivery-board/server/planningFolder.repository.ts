import { promises as fs } from 'node:fs';
import {
  resolvePlanningPaths,
  type PlanningPaths,
  type BoardMode,
  type ActionIntent,
} from '@deliveryforge/delivery-board-shared';

export interface PlanningFolderRepositoryInterface {
  readText(filePath: string): Promise<string>;
  readJson(filePath: string): Promise<unknown>;
  writeJson(filePath: string, data: unknown): Promise<void>;
  planningRootExists(planningRoot: string): Promise<boolean>;
  boardExists(boardFile: string): Promise<boolean>;
  resolvePaths(planningRoot: string): PlanningPaths;
  writeBoardMode(boardFile: string, mode: BoardMode): Promise<void>;
  readActionIntents(actionStateFile: string): Promise<ActionIntent[]>;
  writeActionIntent(actionStateFile: string, intent: ActionIntent): Promise<void>;
}

export class PlanningFolderRepository implements PlanningFolderRepositoryInterface {
  resolvePaths(planningRoot: string): PlanningPaths {
    return resolvePlanningPaths(planningRoot);
  }

  async readText(filePath: string): Promise<string> {
    return fs.readFile(filePath, 'utf8');
  }

  async readJson(filePath: string): Promise<unknown> {
    const raw = await this.readText(filePath);
    return JSON.parse(raw) as unknown;
  }

  async writeJson(filePath: string, data: unknown): Promise<void> {
    await fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8');
  }

  async planningRootExists(planningRoot: string): Promise<boolean> {
    try {
      await fs.access(planningRoot);
      return true;
    } catch {
      return false;
    }
  }

  async boardExists(boardFile: string): Promise<boolean> {
    try {
      await fs.access(boardFile);
      return true;
    } catch {
      return false;
    }
  }

  async writeBoardMode(boardFile: string, mode: BoardMode): Promise<void> {
    const raw = await this.readJson(boardFile) as Record<string, unknown>;
    raw.board_mode = mode;
    await this.writeJson(boardFile, raw);
  }

  async readActionIntents(actionStateFile: string): Promise<ActionIntent[]> {
    try {
      const state = (await this.readJson(actionStateFile)) as { intents?: ActionIntent[] };
      return Array.isArray(state.intents) ? state.intents : [];
    } catch {
      return [];
    }
  }

  async writeActionIntent(actionStateFile: string, intent: ActionIntent): Promise<void> {
    let state: { intents: ActionIntent[] };
    try {
      state = (await this.readJson(actionStateFile)) as { intents: ActionIntent[] };
      if (!Array.isArray(state.intents)) state = { intents: [] };
    } catch {
      state = { intents: [] };
    }
    state.intents.push(intent);
    await this.writeJson(actionStateFile, state);
  }
}

import { promises as fs } from 'node:fs';
import { resolvePlanningPaths, type PlanningPaths } from '@deliveryforge/delivery-board-shared';

export interface PlanningFolderRepositoryInterface {
  readText(filePath: string): Promise<string>;
  readJson(filePath: string): Promise<unknown>;
  writeJson(filePath: string, data: unknown): Promise<void>;
  planningRootExists(planningRoot: string): Promise<boolean>;
  boardExists(boardFile: string): Promise<boolean>;
  resolvePaths(planningRoot: string): PlanningPaths;
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
}

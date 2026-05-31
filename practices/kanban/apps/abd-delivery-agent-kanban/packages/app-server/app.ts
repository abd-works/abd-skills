import express from 'express';
import cors from 'cors';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  createKanbanBoardRouter,
  KanbanBoardService,
  PlanningFolderRepository,
  WarRoomWatcher,
} from '@deliveryforge/delivery-board-server';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '../../..');

function loadDefaultPlanningRoot(): string {
  try {
    const configPath = path.join(repoRoot, 'config.default.json');
    const raw = JSON.parse(readFileSync(configPath, 'utf8')) as { planningRoot?: string };
    return raw.planningRoot ?? '';
  } catch {
    return '';
  }
}

export function createApp(): express.Application {
  const app = express();
  app.use(cors());
  app.use(express.json());

  const service = new KanbanBoardService(new PlanningFolderRepository());
  const watcher = new WarRoomWatcher(service);

  const defaultRoot = loadDefaultPlanningRoot();
  if (defaultRoot) {
    void service.setPlanningRoot(defaultRoot);
    watcher.watch(defaultRoot);
  }

  const originalSet = service.setPlanningRoot.bind(service);
  service.setPlanningRoot = async (root: string) => {
    await originalSet(root);
    watcher.watch(root);
  };

  app.use(createKanbanBoardRouter(service));
  return app;
}

export { KanbanBoardService, PlanningFolderRepository };

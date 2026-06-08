import express from 'express';
import cors from 'cors';
import { createKanbanBoardRouter } from './KanbanBoardRoutes';
import { PlanningFolderRepository } from '@deliveryforge/kanban-server';

export function createApp(): express.Application {
  const app = express();
  app.use(cors());
  app.use(express.json());

  const repo = new PlanningFolderRepository();
  app.use(createKanbanBoardRouter(repo));
  return app;
}

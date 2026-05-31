import type { KanbanBoard, KanbanBoardSnapshot } from './kanbanBoard';
import {
  STAGE_ORDER,
  buildColumnViews,
  buildArchivedViews,
  parseKanbanBoard,
  boardEtag,
} from './kanbanBoard';
import {
  buildStageSkillRails,
  activeStagesFromConfig,
  resolveTeamFromConfig,
  type KanbanConfiguration,
} from './parseSystemOfWork';

export class KanbanBoardLoader {
  /**
   * Compose pollable snapshot from board.json + kanban.json.
   * No plan markdown, no checklist, no slot files — the v2 model is self-describing.
   */
  static fromSources(
    planningRoot: string,
    boardJson: unknown,
    kanbanConfig: KanbanConfiguration,
  ): KanbanBoardSnapshot {
    const board = parseKanbanBoard(boardJson);
    const defName = board.stage_configuration ?? undefined;
    const stageSkillRails = buildStageSkillRails(kanbanConfig, defName);
    const activeStages = activeStagesFromConfig(kanbanConfig, defName);

    const stageFlow = activeStages.length > 0
      ? activeStages
      : STAGE_ORDER.filter((s) => s !== 'context');

    const boardTitle = deriveBoardTitle(board);

    return {
      planningRoot,
      boardTitle,
      syncedAt: board.synced_at ?? null,
      stageFlow,
      board,
      columnViews: buildColumnViews(board),
      archivedTickets: buildArchivedViews(board),
      stageSkillRails,
      polledAt: new Date().toISOString(),
      etag: boardEtag(board),
      team: resolveTeamFromConfig(kanbanConfig, defName, board.team),
      heartbeats: {},
      heartbeatSlots: {},
    };
  }
}

function deriveBoardTitle(board: KanbanBoard): string {
  const allTickets = [...board.backlog, ...board.active, ...board.done, ...board.archived];
  if (allTickets.length === 0) return 'Kanban Board';
  const topLevel = allTickets.find((t) => t.lineage.length > 0);
  return topLevel?.lineage[0] ?? 'Kanban Board';
}

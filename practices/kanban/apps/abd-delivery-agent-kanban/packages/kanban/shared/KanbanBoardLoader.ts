import { Stage } from './Stage';
import type { StageId } from './Stage';
import { KanbanBoard, parseKanbanBoard } from './KanbanBoard';
import type { KanbanBoardSnapshot, KanbanConfiguration } from './KanbanBoard';

export class KanbanBoardLoader {
  static fromSources(
    planningRoot: string,
    boardJson: unknown,
    kanbanConfig: KanbanConfiguration,
  ): KanbanBoardSnapshot {
    const board = new KanbanBoard(parseKanbanBoard(boardJson));
    const defName = board.stageConfiguration;
    const stageSkillRails = KanbanBoard.buildSkillRails(kanbanConfig, defName);
    const activeStages = KanbanBoard.activeStages(kanbanConfig, defName);

    const stageFlow = activeStages.length > 0
      ? activeStages
      : Stage.ORDER.filter((s: StageId) => s !== 'context');

    return {
      planningRoot,
      boardTitle: board.title(),
      syncedAt: board.syncedAt,
      stageFlow,
      board_mode: board.boardMode,
      board,
      columnViews: board.columnViews(),
      archivedTickets: board.archivedTickets(),
      stageSkillRails,
      polledAt: new Date().toISOString(),
      etag: board.etag(),
      team: KanbanBoard.resolveTeam(kanbanConfig, defName, board.team),
      pendingIntents: [],
    };
  }
}

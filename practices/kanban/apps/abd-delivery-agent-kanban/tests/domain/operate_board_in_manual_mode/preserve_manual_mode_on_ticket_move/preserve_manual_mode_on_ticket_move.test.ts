/**
 * Preserve Manual Mode on Ticket Move
 *
 * Epic:     Operate Board in Manual Mode
 * Sub-epic: Preserve Manual Mode on Ticket Move
 *
 * Story: Moving a ticket must not reset board mode to automatic.
 */
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { describe, it, expect } from 'vitest';
import { KanbanBoard, PlanningFolderRepository } from '@deliveryforge/kanban-server';
import { StageBucketLayout } from '@deliveryforge/kanban-shared';

type JsonObject = Record<string, unknown>;

async function given_planning_root_with_board_files(prefix: string): Promise<string> {
  const root = await mkdtemp(path.join(os.tmpdir(), prefix));
  await mkdir(path.join(root, 'kanban'), { recursive: true });
  return root.replace(/\\/g, '/');
}

async function given_kanban_config(planningRoot: string): Promise<void> {
  const config = {
    schema: 'abd-kanban-board/v1',
    definitions: {
      test: {
        stages: [
          { name: 'shaping', scope: 'all', stage_work_required: [] },
          { name: 'discovery', scope: 'increment', stage_work_required: [] },
          { name: 'exploration', scope: 'increment', stage_work_required: [] },
          { name: 'specification', scope: 'sprint', stage_work_required: [] },
          { name: 'engineering', scope: 'sprint', stage_work_required: [] },
        ],
      },
    },
  } satisfies JsonObject;

  await writeFile(
    path.join(planningRoot, 'kanban', 'kanban.json'),
    JSON.stringify(config, null, 2),
    'utf8',
  );
}

async function given_kanban_config_with_shaping_required_skill(planningRoot: string): Promise<void> {
  const config = {
    schema: 'abd-kanban-board/v1',
    definitions: {
      test: {
        stages: [
          {
            name: 'shaping',
            scope: 'all',
            stage_work_required: [{ skill: 'abd-story-mapping', role: 'product-owner' }],
          },
          { name: 'discovery', scope: 'increment', stage_work_required: [] },
          { name: 'exploration', scope: 'increment', stage_work_required: [] },
          { name: 'specification', scope: 'sprint', stage_work_required: [] },
          { name: 'engineering', scope: 'sprint', stage_work_required: [] },
        ],
      },
    },
  } satisfies JsonObject;

  await writeFile(
    path.join(planningRoot, 'kanban', 'kanban.json'),
    JSON.stringify(config, null, 2),
    'utf8',
  );
}

async function given_board_in_automatic_mode(planningRoot: string): Promise<void> {
  const board = {
    schema: 'abd-delivery-kanban/v2',
    stage_configuration: 'test',
    board_mode: 'automatic',
    backlog: [],
    active: [
      {
        ticket_id: 'project-all',
        lineage: ['PawPlace'],
        scope_level: 'all',
        stage: 'shaping',
        priority: 1,
        skill_progress: {},
        entered_stage: '2026-06-05T22:00:00.000Z',
        completed_stage: null,
        scatter_from: null,
        scatter_to: [],
        notes: '',
        stage_history: [],
      },
    ],
    done: [],
    archived: [],
    team: {
      'product-owner': 1,
      'business-expert': 1,
      'ux-designer': 1,
      engineer: 1,
    },
  } satisfies JsonObject;

  await writeFile(path.join(planningRoot, 'kanban', 'board.json'), JSON.stringify(board, null, 2), 'utf8');
}

describe('Preserve Board Mode on Ticket Move', () => {
  it('keeps manual mode after move even when in-memory board instance is stale', async () => {
    const planningRoot = await given_planning_root_with_board_files('kanban-mode-persist-');
    const repo = new PlanningFolderRepository();

    try {
      await given_kanban_config(planningRoot);
      await given_board_in_automatic_mode(planningRoot);

      const board = await KanbanBoard.load(planningRoot, repo);
      const paths = KanbanBoard.resolvePlanningPaths(planningRoot);

      // Simulates a mode toggle done after the board singleton was created.
      await repo.writeBoardMode(paths.boardFile, 'manual');

      const snapshot = await board.moveToStageAndPersist(
        'project-all',
        'discovery',
        planningRoot,
        'in_progress',
      );
      const onDiskBoard = await repo.readJson(paths.boardFile) as { board_mode: string; active: Array<{ stage: string }> };

      expect(snapshot.board_mode).toBe('manual');
      expect(onDiskBoard.board_mode).toBe('manual');
      expect(onDiskBoard.active[0]?.stage).toBe('discovery');
    } finally {
      await rm(planningRoot, { recursive: true, force: true });
    }
  });

  it('keeps ticket in stage done after manual drop into done sub-column', async () => {
    const planningRoot = await given_planning_root_with_board_files('kanban-stage-done-');
    const repo = new PlanningFolderRepository();

    try {
      await given_kanban_config_with_shaping_required_skill(planningRoot);
      await given_board_in_automatic_mode(planningRoot);

      const board = await KanbanBoard.load(planningRoot, repo);
      const paths = KanbanBoard.resolvePlanningPaths(planningRoot);
      await repo.writeBoardMode(paths.boardFile, 'manual');

      const snapshot = await board.moveToStageAndPersist(
        'project-all',
        'shaping',
        planningRoot,
        'stage_done',
      );
      const buckets = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      ).buildStageBuckets();
      const shapingBucket = buckets.get('shaping');

      expect(shapingBucket?.done.some((t) => t.ticketId === 'project-all')).toBe(true);
      expect(shapingBucket?.ip.some((t) => t.ticketId === 'project-all')).toBe(false);
    } finally {
      await rm(planningRoot, { recursive: true, force: true });
    }
  });

  it('changes etag when active ticket skill state transitions with same skill key count', async () => {
    const planningRoot = await given_planning_root_with_board_files('kanban-etag-skill-state-');
    const repo = new PlanningFolderRepository();

    try {
      await given_kanban_config(planningRoot);
      await given_board_in_automatic_mode(planningRoot);

      const board = await KanbanBoard.load(planningRoot, repo);
      const paths = KanbanBoard.resolvePlanningPaths(planningRoot);

      const before = await board.loadSnapshot(planningRoot);

      const raw = await repo.readJson(paths.boardFile) as {
        active: Array<{
          ticket_id: string;
          skill_progress?: Record<string, {
            execution_status: 'not_started' | 'in_progress' | 'done';
            review_status?: 'in_progress' | 'done' | 'failed' | null;
          }>;
        }>;
      };

      const ticket = raw.active.find((t) => t.ticket_id === 'project-all');
      if (!ticket) throw new Error('fixture ticket missing');
      ticket.skill_progress = {
        'abd-story-mapping': {
          execution_status: 'in_progress',
          review_status: null,
        },
      };
      await repo.writeJson(paths.boardFile, raw);

      const inProgress = await board.loadSnapshot(planningRoot);
      expect(inProgress.etag).not.toBe(before.etag);

      const raw2 = await repo.readJson(paths.boardFile) as typeof raw;
      const ticket2 = raw2.active.find((t) => t.ticket_id === 'project-all');
      if (!ticket2) throw new Error('fixture ticket missing');
      ticket2.skill_progress = {
        'abd-story-mapping': {
          execution_status: 'done',
          review_status: 'in_progress',
        },
      };
      await repo.writeJson(paths.boardFile, raw2);

      const review = await board.loadSnapshot(planningRoot);
      expect(review.etag).not.toBe(inProgress.etag);
    } finally {
      await rm(planningRoot, { recursive: true, force: true });
    }
  });
});

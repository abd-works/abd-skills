import path from 'node:path';
import { readdir } from 'node:fs/promises';
import type {
  AgentRole,
  HeartbeatAges,
  HeartbeatSlots,
  KanbanBoardSnapshot,
  Team,
} from '@deliveryforge/delivery-board-shared';
import {
  AGENT_ROLES,
  DEFAULT_TEAM,
  KanbanBoardLoader,
  buildHeartbeatSlots,
  resolveTeamFromConfig,
  type KanbanConfiguration,
} from '@deliveryforge/delivery-board-shared';
import type { PlanningFolderRepository } from './planningFolder.repository';

export class KanbanBoardService {
  private cachedRoot: string | null = null;
  private lastSnapshot: KanbanBoardSnapshot | null = null;

  constructor(private readonly repo: PlanningFolderRepository) {}

  async setPlanningRoot(planningRoot: string): Promise<void> {
    this.cachedRoot = planningRoot;
    this.lastSnapshot = null;
  }

  getPlanningRoot(): string | null {
    return this.cachedRoot;
  }

  invalidateSnapshotCache(): void {
    this.lastSnapshot = null;
  }

  async loadSnapshot(planningRoot?: string): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');

    const paths = this.repo.resolvePaths(root);
    const exists = await this.repo.planningRootExists(paths.planningRoot);
    if (!exists) {
      throw new Error(`Planning folder not found: ${paths.planningRoot}`);
    }

    const hasBoard = await this.repo.boardExists(paths.boardFile);
    if (!hasBoard) {
      throw new Error(
        `board.json missing at ${paths.boardFile}. Initialize with kanban-lead setup.`,
      );
    }

    const [rawBoardJson, rawKanbanConfig] = await Promise.all([
      this.repo.readJson(paths.boardFile),
      this.repo.readJson(paths.kanbanFile),
    ]);

    const kanbanConfig = rawKanbanConfig as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(root, rawBoardJson, kanbanConfig);

    const { heartbeats, heartbeatSlots } = await this.loadHeartbeats(paths.kanbanDir);
    snapshot.heartbeats = heartbeats;
    snapshot.heartbeatSlots = heartbeatSlots;

    this.cachedRoot = root;
    this.lastSnapshot = snapshot;
    return snapshot;
  }

  private async loadHeartbeats(
    kanbanDir: string,
  ): Promise<{ heartbeats: HeartbeatAges; heartbeatSlots: HeartbeatSlots }> {
    let fileNames: string[] = [];
    try {
      const entries = await readdir(kanbanDir);
      fileNames = entries.filter(
        (name) => name.startsWith('heartbeat-') && name.endsWith('.json'),
      );
    } catch {
      fileNames = [];
    }

    const files = await Promise.all(
      fileNames.map(async (fileName) => {
        const filePath = path.join(kanbanDir, fileName);
        try {
          const raw = (await this.repo.readJson(filePath)) as {
            ts?: string;
            status?: string;
          };
          return { fileName, raw };
        } catch {
          return { fileName, raw: {} };
        }
      }),
    );

    const heartbeatSlots = buildHeartbeatSlots(files);
    const heartbeats: HeartbeatAges = {};
    for (const role of [...AGENT_ROLES, 'kanban-lead'] as const) {
      heartbeats[role] = heartbeatSlots[role]?.[0]?.ageSeconds ?? null;
    }
    return { heartbeats, heartbeatSlots };
  }

  async updateTeam(
    role: AgentRole,
    delta: number,
    planningRoot?: string,
  ): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');

    const paths = this.repo.resolvePaths(root);

    const [rawBoard, rawKanbanConfig] = await Promise.all([
      this.repo.readJson(paths.boardFile),
      this.repo.readJson(paths.kanbanFile),
    ]);

    const board = rawBoard as Record<string, unknown>;
    const kanbanConfig = rawKanbanConfig as KanbanConfiguration;
    const defName = (board.stage_configuration as string | undefined) ?? undefined;

    const team = resolveTeamFromConfig(
      kanbanConfig,
      defName,
      board.team as Team,
    );
    const currentCount = team[role] ?? DEFAULT_TEAM[role];
    const next = Math.max(0, currentCount + delta);
    team[role] = next;

    board.team = team;
    await this.repo.writeJson(paths.boardFile, board);

    const resolvedDefName =
      defName ?? Object.keys(kanbanConfig.definitions)[0] ?? '';
    if (resolvedDefName && kanbanConfig.definitions[resolvedDefName]) {
      kanbanConfig.definitions[resolvedDefName].team = { ...team };
      await this.repo.writeJson(paths.kanbanFile, kanbanConfig);
    }

    this.lastSnapshot = null;
    return this.loadSnapshot(root);
  }

  lastEtag(): string | null {
    return this.lastSnapshot?.etag ?? null;
  }
}

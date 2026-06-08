import {
  KanbanBoard as DomainKanbanBoard,
  KanbanBoardLoader,
  parseKanbanBoard,
  type KanbanBoardData,
  type KanbanBoardSnapshot,
  type KanbanConfiguration,
  type StageId,
  type AgentRole,
  type ActionIntent,
  type MoveTicketOptions,
} from '@deliveryforge/kanban-shared';
import { TeamMembership } from './TeamMembership';
import { Ticket } from './Ticket';
import type { PlanningFolderRepository } from './PlanningFolderRepository';

/**
 * Server-side KanbanBoard — extends the shared domain aggregate with
 * persistence (filesystem I/O) and scatter-child resolution from planning
 * artifacts.
 *
 * Every read goes to disk. There is no snapshot cache and no file watcher.
 * The domain objects own all state; the server just reads and writes JSON.
 */
export class KanbanBoard extends DomainKanbanBoard {
  private cachedRoot: string | null = null;

  constructor(
    data: KanbanBoardData,
    private readonly repo: PlanningFolderRepository,
  ) {
    super(data);
  }

  // ── Factory ───────────────────────────────────────────────────────

  static async load(
    planningRoot: string,
    repo: PlanningFolderRepository,
  ): Promise<KanbanBoard> {
    const paths = DomainKanbanBoard.resolvePlanningPaths(planningRoot);

    const exists = await repo.planningRootExists(paths.planningRoot);
    if (!exists) throw new Error(`Planning folder not found: ${paths.planningRoot}`);

    const hasBoard = await repo.boardExists(paths.boardFile);
    if (!hasBoard) {
      throw new Error(
        `board.json missing at ${paths.boardFile}. Initialize with kanban-lead setup.`,
      );
    }

    const rawBoard = await repo.readJson(paths.boardFile);
    const boardData = parseKanbanBoard(rawBoard);
    const board = new KanbanBoard(boardData, repo);
    board.cachedRoot = planningRoot;
    return board;
  }

  // ── Persist ───────────────────────────────────────────────────────

  async persist(planningRoot?: string): Promise<void> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');
    const paths = DomainKanbanBoard.resolvePlanningPaths(root);
    await this.repo.writeJson(paths.boardFile, this.toJSON());
  }

  private async loadFreshBoard(root: string): Promise<KanbanBoard> {
    return KanbanBoard.load(root, this.repo);
  }

  // ── Snapshot — always reads all files fresh from disk ─────────────

  async loadSnapshot(planningRoot?: string): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');
    this.cachedRoot = root;

    const paths = DomainKanbanBoard.resolvePlanningPaths(root);

    const rawBoard = await this.repo.readJson(paths.boardFile);
    const boardData = parseKanbanBoard(rawBoard);

    const rawKanbanConfig = await this.repo.readJson(paths.kanbanFile);
    const kanbanConfig = rawKanbanConfig as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(root, boardData, kanbanConfig);

    const pendingIntents = await this.repo.readActionIntents(paths.actionStateFile);
    snapshot.pendingIntents = pendingIntents;
    DomainKanbanBoard.applyPendingIntents(snapshot);
    snapshot.etag = snapshot.board.etag(pendingIntents.length);

    return snapshot;
  }

  // ── Move ticket ───────────────────────────────────────────────────

  async moveToStageAndPersist(
    ticketId: string,
    targetStage: StageId | null,
    planningRoot?: string,
    placement: 'in_progress' | 'stage_done' = 'in_progress',
  ): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');

    const freshBoard = await this.loadFreshBoard(root);
    const paths = DomainKanbanBoard.resolvePlanningPaths(root);
    const rawKanban = await this.repo.readJson(paths.kanbanFile);
    const kanbanConfig = rawKanban as KanbanConfiguration;
    const defName = freshBoard.stageConfiguration;

    let updated: DomainKanbanBoard;
    if (targetStage === null) {
      updated = freshBoard.resumeInProgress(ticketId);
    } else {
      const ticket = freshBoard.findRawTicket(ticketId);
      let childrenSpec: ReturnType<typeof Ticket.tryResolveScatterChildren> | undefined;
      if (ticket) {
        const boundary = freshBoard.scatterBoundaryOnPath(
          kanbanConfig, defName,
          ticket.scope_level,
          ticket.stage as StageId,
          targetStage,
        );
        if (boundary) {
          const engagementRoot = DomainKanbanBoard.engagementWorkspaceFromPlanningRoot(root);
          childrenSpec =
            Ticket.tryResolveScatterChildren(engagementRoot, ticketId, {
              childScope: boundary.childScope,
              ticketScopeLevel: ticket.scope_level,
            }) ?? undefined;
        }
      }
      updated = freshBoard.moveToStage(ticketId, targetStage, kanbanConfig, defName, {
        childrenSpec,
        advanceWithoutScatter: true,
        placement: placement === 'stage_done' ? 'stage_done' : 'in_progress',
      } as MoveTicketOptions);
    }

    await this.repo.writeJson(paths.boardFile, updated.toJSON());
    return this.loadSnapshot(root);
  }

  // ── Team update ───────────────────────────────────────────────────

  async updateTeamAndPersist(
    role: AgentRole,
    delta: number,
    planningRoot?: string,
  ): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');

    const freshBoard = await this.loadFreshBoard(root);
    const paths = DomainKanbanBoard.resolvePlanningPaths(root);
    const rawKanbanConfig = await this.repo.readJson(paths.kanbanFile);
    const kanbanConfig = rawKanbanConfig as KanbanConfiguration;
    const defName = freshBoard.stageConfiguration;

    const membership = TeamMembership.fromConfig(kanbanConfig, defName, freshBoard.team)
      .adjust(role, delta);

    await membership.persistToBoard(paths.boardFile, this.repo);

    const resolvedDefName = defName ?? Object.keys(kanbanConfig.definitions)[0] ?? '';
    if (resolvedDefName) {
      await membership.persistToConfig(paths.kanbanFile, kanbanConfig, resolvedDefName, this.repo);
    }

    return this.loadSnapshot(root);
  }

  // ── Board mode toggle ─────────────────────────────────────────────

  async toggleModeAndPersist(planningRoot?: string): Promise<KanbanBoardSnapshot> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');

    const freshBoard = await this.loadFreshBoard(root);
    const paths = DomainKanbanBoard.resolvePlanningPaths(root);
    const nextMode = freshBoard.boardMode === 'automatic' ? 'manual' : 'automatic';
    await this.repo.writeBoardMode(paths.boardFile, nextMode);

    return this.loadSnapshot(root);
  }

  // ── Action intents ────────────────────────────────────────────────

  async writeActionIntent(
    intent: ActionIntent,
    planningRoot?: string,
  ): Promise<void> {
    const root = planningRoot ?? this.cachedRoot;
    if (!root) throw new Error('Planning root not configured');
    const paths = DomainKanbanBoard.resolvePlanningPaths(root);
    await this.repo.writeActionIntent(paths.actionStateFile, intent);
  }

  // ── Planning root ─────────────────────────────────────────────────

  getPlanningRoot(): string | null {
    return this.cachedRoot;
  }

  setPlanningRoot(planningRoot: string): void {
    this.cachedRoot = planningRoot;
  }
}

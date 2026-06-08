import { Ticket } from './Ticket';
import { SkillCatalog } from './SkillCatalog';
import type { KanbanColumn, KanbanColumnView } from './Ticket';
import type { RawTicket } from './Ticket.schema';
import type { Team } from './TeamMembership.schema';
import { AGENT_ROLES, DEFAULT_TEAM } from './TeamMembership';
import type { SkillProgress } from './SkillProgress.schema';
import type { StageId, StageSkillRail } from './Stage';
import { Stage } from './Stage';// ── Kanban configuration types (owned by KanbanBoard per domain model) ────────────────

export interface StageWorkRequiredEntry {
  skill: string;
  role: string;
  optional?: boolean;
  run_when?: string;
}

export interface StageDefinition {
  name: string;
  scope: string;
  optional?: boolean;
  skills?: StageWorkRequiredEntry[];
  stage_work_required?: StageWorkRequiredEntry[];
}

export interface KanbanConfigurationDefinition {
  label?: string;
  team?: Partial<Record<import('./TeamMembership').AgentRole, number>>;
  stages: StageDefinition[];
}

export interface KanbanConfiguration {
  schema: string;
  definitions: Record<string, KanbanConfigurationDefinition>;
}

export { KanbanBoardSchema, parseKanbanBoard } from './KanbanBoard.schema';
export type { KanbanBoardData } from './KanbanBoard.schema';
import type { KanbanBoardData } from './KanbanBoard.schema';

// ── Constants & types ────────────────────────────────────────────────────

export const KANBAN_COLUMNS: readonly KanbanColumn[] = [
  'backlog', 'active', 'done', 'archived',
];

export const KANBAN_COLUMN_LABELS: Record<KanbanColumn, string> = {
  backlog: 'Backlog', active: 'Active', done: 'Done', archived: 'Archived',
};

export type BoardMode = 'automatic' | 'manual';

export interface ActionIntent {
  ticket_id: string;
  skill: string;
  agent_role: string;
  created_at: string;
}

export const SCOPE_LEVEL_LABELS: Record<string, string> = {
  project: 'Project', all: 'Project', partition: 'Partition',
  increment: 'Increment', sprint: 'Sprint',
};

export type MoveTicketPlacement = 'in_progress' | 'stage_done';

export type ScatterChildSpec = { id: string; name: string; priority: number };

export type MoveTicketOptions = {
  childrenSpec?: ScatterChildSpec[];
  placement?: MoveTicketPlacement;
  advanceWithoutScatter?: boolean;
};

export interface AgentSessionInfo {
  state: 'running' | 'completed' | 'failed';
  messageCount: number;
  lastActivitySec: number;
  finalMessage?: string;
  errorDetail?: string;
}

export interface KanbanBoardSnapshot {
  planningRoot: string;
  boardTitle: string;
  syncedAt: string | null;
  stageFlow: StageId[];
  board_mode: BoardMode;
  board: KanbanBoard;
  columnViews: KanbanColumnView[];
  archivedTickets: Ticket[];
  stageSkillRails: StageSkillRail[];
  polledAt: string;
  etag: string;
  team: NonNullable<Team>;
  pendingIntents: ActionIntent[];
  agentSessions?: Record<string, AgentSessionInfo>;
}

export interface PlanningPaths {
  planningRoot: string;
  kanbanDir: string;
  boardFile: string;
  kanbanFile: string;
  metricsLogFile: string;
  strategyFile: string;
  manifestFile: string;
  actionStateFile: string;
}

// ── Scope ranking ────────────────────────────────────────────────────────

const SCOPE_RANK: Record<string, number> = {
  all: 0, project: 1, partition: 2, increment: 3, sprint: 4, story: 5,
};

function scopeRank(scope: string): number {
  return SCOPE_RANK[scope] ?? 99;
}

// ── RawTicket mutation helpers (operate on mutable copies during moves) ──

function getStageDef(
  stages: StageDefinition[],
  name: string,
): StageDefinition | undefined {
  return stages.find((s: StageDefinition) => s.name === name);
}

function requiredSteps(
  stageDef: StageDefinition | undefined,
): StageWorkRequiredEntry[] {
  if (!stageDef) return [];
  const steps = stageDef.stage_work_required ?? stageDef.skills ?? [];
  return steps.filter((s: StageWorkRequiredEntry) => !s.optional);
}

function isSkillDone(sp: SkillProgress | undefined): boolean {
  return sp?.execution_status === 'done' && sp?.review_status === 'done';
}

function skippedSkillProgress(role: string): SkillProgress {
  const now = new Date().toISOString();
  return {
    execution_status: 'done', review_status: 'done',
    agent: role, reviewer: role,
    start: now, end: now, review_start: now, review_end: now,
  };
}

function completeRequiredSkills(
  ticket: RawTicket,
  stageDef: StageDefinition | undefined,
): void {
  for (const step of requiredSteps(stageDef)) {
    if (isSkillDone(ticket.skill_progress[step.skill])) continue;
    ticket.skill_progress[step.skill] = skippedSkillProgress(step.role);
  }
}

function recordAdvance(
  ticket: RawTicket,
  completedStageName: string,
  nextStageName: string,
  skipped = true,
): void {
  const now = new Date().toISOString();
  if (ticket.stage && ticket.entered_stage) {
    ticket.stage_history = [
      ...(ticket.stage_history ?? []),
      { stage: completedStageName, entered: ticket.entered_stage, completed: now, skipped },
    ];
  }
  ticket.stage = nextStageName;
  ticket.skill_progress = {};
  ticket.entered_stage = now;
  ticket.completed_stage = null;
}

function advanceRawTicket(
  ticket: RawTicket,
  targetStage: StageId,
  stages: StageDefinition[],
): void {
  const fromIdx = Stage.indexOf(ticket.stage as StageId);
  const toIdx = Stage.indexOf(targetStage);
  if (fromIdx < 0 || toIdx < 0 || toIdx <= fromIdx) return;
  completeRequiredSkills(ticket, getStageDef(stages, ticket.stage as StageId));
  for (let i = fromIdx + 1; i <= toIdx; i++) {
    recordAdvance(ticket, Stage.ORDER[i - 1]!, Stage.ORDER[i]!);
    if (i < toIdx) completeRequiredSkills(ticket, getStageDef(stages, Stage.ORDER[i]!));
  }
}

function applyPlacement(
  ticket: RawTicket,
  placement: MoveTicketPlacement,
): RawTicket {
  if (placement === 'stage_done') {
    const out: RawTicket = {
      ...ticket,
      skill_progress: { ...ticket.skill_progress },
      completed_stage: new Date().toISOString(),
    };
    delete out.hold_in_progress;
    return out;
  }
  return { ...ticket, hold_in_progress: true };
}

/**
 * domain model: Kanban Board — aggregate root.
 *       Ordered stages, active stage flow, team configuration, tickets in flow.
 *       Invariant: every ticket occupies exactly one column at any given time.
 *
 * Instance wraps KanbanBoardData. Operations return new KanbanBoard instances
 * (immutable aggregate style). Serialise with toJSON().
 */
export class KanbanBoard {
  protected readonly data: KanbanBoardData;

  constructor(data: KanbanBoardData) {
    this.data = data;
  }

  // ── Factory ────────────────────────────────────────────────────────

  static parse(raw: unknown): KanbanBoard {
    const { parseKanbanBoard: parse } = require('./KanbanBoard.schema') as {
      parseKanbanBoard: (r: unknown) => KanbanBoardData;
    };
    return new KanbanBoard(parse(raw));
  }

  // ── Accessors ──────────────────────────────────────────────────────

  get stageConfiguration(): string | undefined {
    return this.data.stage_configuration ?? undefined;
  }

  get boardMode(): BoardMode {
    return this.data.board_mode;
  }

  get syncedAt(): string | null {
    return this.data.synced_at ?? null;
  }

  get team(): Team {
    return this.data.team;
  }

  // ── Column views (read model derived from aggregate state) ─────────

  columnViews(): KanbanColumnView[] {
    return KANBAN_COLUMNS
      .filter((id: KanbanColumn) => id !== 'archived')
      .map((id: KanbanColumn) => {
        let tickets: Ticket[];
        switch (id) {
          case 'backlog':
            tickets = this.data.backlog.map((t: RawTicket) => new Ticket(t, 'backlog'));
            break;
          case 'active':
            tickets = this.data.active.map((t: RawTicket) => new Ticket(t, 'active'));
            break;
          case 'done':
            tickets = this.data.done.map((t: RawTicket) => new Ticket(t, 'done'));
            break;
          default:
            tickets = [];
        }
        return { id, label: KANBAN_COLUMN_LABELS[id], tickets };
      });
  }

  archivedTickets(): Ticket[] {
    return this.data.archived.map((t: RawTicket) => new Ticket(t, 'archived'));
  }

  // ── Etag ───────────────────────────────────────────────────────────

  etag(pendingIntentCount = 0): string {
    const activeSig = this.data.active
      .map((t: RawTicket) =>
        `${t.ticket_id}:${t.stage}:${KanbanBoard.skillProgressSignature(t)}`,
      )
      .join('|');
    return [
      this.data.synced_at ?? 'none',
      this.data.board_mode ?? 'automatic',
      this.data.backlog.length,
      activeSig,
      this.data.done.length,
      this.data.archived.length,
      `pi${pendingIntentCount}`,
    ].join(':');
  }

  private static skillProgressSignature(ticket: RawTicket): string {
    return Object.entries(ticket.skill_progress ?? {})
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([skillId, progress]) => {
        const execution = progress?.execution_status ?? 'not_started';
        const review = progress?.review_status ?? 'none';
        const agent = progress?.agent ?? 'none';
        const reviewer = progress?.reviewer ?? 'none';
        return `${skillId}:${execution}:${review}:${agent}:${reviewer}`;
      })
      .join(',');
  }

  // ── Board title ────────────────────────────────────────────────────

  title(): string {
    const all = [
      ...this.data.backlog, ...this.data.active,
      ...this.data.done, ...this.data.archived,
    ];
    if (all.length === 0) return 'Kanban Board';
    const topLevel = all.find((t: RawTicket) => t.lineage.length > 0);
    return topLevel?.lineage[0] ?? 'Kanban Board';
  }

  // ── Resume ticket ─────────────────────────────────────────────────

  resumeInProgress(ticketId: string): KanbanBoard {
    const done = [...this.data.done];
    const archived = [...this.data.archived];
    let active = [...this.data.active];
    const backlog = [...this.data.backlog];

    const pull = (list: RawTicket[]): RawTicket | undefined => {
      const idx = list.findIndex((t: RawTicket) => t.ticket_id === ticketId);
      if (idx < 0) return undefined;
      return list.splice(idx, 1)[0];
    };

    let ticket = pull(done) ?? pull(archived) ?? pull(backlog);
    if (!ticket) {
      const existing = active.find((t: RawTicket) => t.ticket_id === ticketId);
      if (!existing) throw new Error(`Ticket not found: ${ticketId}`);
      ticket = existing;
    }
    active = active.filter((t: RawTicket) => t.ticket_id !== ticketId);
    active.push({ ...ticket, hold_in_progress: true });

    return new KanbanBoard({ ...this.data, active, done, archived, backlog });
  }

  // ── Scatter boundary detection ────────────────────────────────────

  scatterBoundaryOnPath(
    config: KanbanConfiguration,
    definitionName: string | null | undefined,
    ticketScopeLevel: string,
    fromStage: StageId,
    toStage: StageId,
  ): { boundaryStage: StageId; childStage: StageId; childScope: string } | null {
    const { stages } = this.resolveDefinition(config, definitionName);
    const fromIdx = Stage.indexOf(fromStage);
    const toIdx = Stage.indexOf(toStage);
    if (fromIdx < 0 || toIdx < 0) return null;
    const ticketRank = scopeRank(ticketScopeLevel);

    for (let i = fromIdx; i < toIdx; i++) {
      const curName = Stage.ORDER[i]! as StageId;
      const nextName = Stage.ORDER[i + 1]! as StageId;
      const curDef = getStageDef(stages, curName);
      const nextDef = getStageDef(stages, nextName);
      if (!curDef || !nextDef) continue;
      if (
        scopeRank(nextDef.scope) > scopeRank(curDef.scope) &&
        ticketRank <= scopeRank(curDef.scope)
      ) {
        return { boundaryStage: curName, childStage: nextName, childScope: nextDef.scope };
      }
    }
    return null;
  }

  // ── Scatter and advance ───────────────────────────────────────────

  scatterAndAdvance(
    parent: RawTicket,
    targetStage: StageId,
    childrenSpec: ScatterChildSpec[],
    config: KanbanConfiguration,
    definitionName: string | null | undefined,
    placement: MoveTicketPlacement = 'in_progress',
  ): KanbanBoard {
    const { stages } = this.resolveDefinition(config, definitionName);
    const boundary = this.scatterBoundaryOnPath(
      config, definitionName, parent.scope_level,
      parent.stage as StageId, targetStage,
    );
    if (!boundary) {
      throw new Error(
        'scatterAndAdvance called without a scatter boundary on this path',
      );
    }

    const existingIds = this.existingTicketIds();
    const collisions = childrenSpec
      .filter((c: ScatterChildSpec) => existingIds.has(c.id))
      .map((c: ScatterChildSpec) => c.id);
    if (collisions.length > 0) {
      throw new Error(
        `Scatter from ${parent.ticket_id} would create duplicate IDs: ${collisions.join(', ')}`,
      );
    }
    if (parent.scatter_to && parent.scatter_to.length > 0) {
      throw new Error(
        `Ticket ${parent.ticket_id} already scattered into ${parent.scatter_to.join(', ')}. ` +
        'Drag an increment ticket instead.',
      );
    }

    const workingParent: RawTicket = {
      ...parent,
      skill_progress: { ...parent.skill_progress },
      stage_history: [...(parent.stage_history ?? [])],
    };
    completeRequiredSkills(workingParent, getStageDef(stages, boundary.boundaryStage));

    const now = new Date().toISOString();
    workingParent.completed_stage = now;
    workingParent.scatter_to = childrenSpec.map((c: ScatterChildSpec) => c.id);
    if (workingParent.stage && workingParent.entered_stage) {
      workingParent.stage_history = [
        ...(workingParent.stage_history ?? []),
        { stage: workingParent.stage, entered: workingParent.entered_stage, completed: now },
      ];
    }

    const children: RawTicket[] = childrenSpec.map((spec: ScatterChildSpec) => ({
      ticket_id: spec.id,
      lineage: [...parent.lineage, spec.name],
      scope_level: boundary.childScope,
      stage: boundary.childStage,
      priority: spec.priority,
      entered_stage: now,
      completed_stage: null,
      stage_history: [],
      scatter_from: parent.ticket_id,
      scatter_to: [],
      skill_progress: {},
      notes: '',
    }));

    for (const child of children) {
      if (Stage.indexOf(targetStage) > Stage.indexOf(boundary.childStage)) {
        advanceRawTicket(child, targetStage, stages);
      }
      if (placement === 'stage_done') {
        completeRequiredSkills(child, getStageDef(stages, targetStage));
        delete child.hold_in_progress;
      } else {
        child.hold_in_progress = true;
      }
    }

    const active = this.data.active.filter(
      (t: RawTicket) => t.ticket_id !== parent.ticket_id,
    );
    active.push(...children);
    return new KanbanBoard({
      ...this.data,
      active,
      archived: [...this.data.archived, workingParent],
    });
  }

  // ── Move ticket to stage ──────────────────────────────────────────

  moveToStage(
    ticketId: string,
    targetStage: StageId,
    config: KanbanConfiguration,
    definitionName?: string | null,
    options?: MoveTicketOptions,
  ): KanbanBoard {
    const { stages } = this.resolveDefinition(config, definitionName);
    const { remaining, ticket } = this.extractTicket(ticketId);

    const currentStage = Stage.normalize(ticket.stage);
    if (!currentStage) throw new Error(`Ticket ${ticketId} has no stage`);
    const fromIdx = Stage.indexOf(currentStage);
    const toIdx = Stage.indexOf(targetStage);
    if (fromIdx < 0 || toIdx < 0) {
      throw new Error(`Invalid stage: ${ticket.stage} → ${targetStage}`);
    }

    const placement = options?.placement ?? 'in_progress';

    if (toIdx < fromIdx) {
      return this.applyBackwardMove(remaining, ticket, targetStage, placement);
    }

    if (toIdx === fromIdx) {
      const active = remaining.active.filter(
        (t: RawTicket) => t.ticket_id !== ticketId,
      );
      active.push(applyPlacement(ticket, placement));
      return new KanbanBoard({ ...remaining, active });
    }

    const boundary = this.scatterBoundaryOnPath(
      config, definitionName, ticket.scope_level, currentStage, targetStage,
    );
    const alreadyScattered = (ticket.scatter_to?.length ?? 0) > 0;
    if (boundary && !alreadyScattered) {
      if (options?.childrenSpec?.length) {
        const intermediate = new KanbanBoard(remaining);
        return intermediate.scatterAndAdvance(
          ticket, targetStage, options.childrenSpec,
          config, definitionName, placement,
        );
      }
      if (!options?.advanceWithoutScatter) {
        throw new Error(
          `Cannot move to ${targetStage}: ticket must scatter after ` +
          `${boundary.boundaryStage} (${boundary.childScope} at ${boundary.childStage}). ` +
          'Thin-slicing children are required.',
        );
      }
    }

    const working: RawTicket = {
      ...ticket,
      skill_progress: { ...ticket.skill_progress },
      stage_history: [...(ticket.stage_history ?? [])],
    };
    completeRequiredSkills(working, getStageDef(stages, currentStage));
    for (let i = fromIdx + 1; i <= toIdx; i++) {
      recordAdvance(working, Stage.ORDER[i - 1]!, Stage.ORDER[i]!);
      if (i < toIdx) {
        completeRequiredSkills(working, getStageDef(stages, Stage.ORDER[i]!));
      }
    }

    const active = remaining.active.filter(
      (t: RawTicket) => t.ticket_id !== ticketId,
    );
    active.push(applyPlacement(working, placement));
    return new KanbanBoard({ ...remaining, active });
  }

  // ── Find ticket ───────────────────────────────────────────────────

  findRawTicket(ticketId: string): RawTicket | undefined {
    return [
      ...this.data.active, ...this.data.backlog,
      ...this.data.done, ...this.data.archived,
    ].find((t: RawTicket) => t.ticket_id === ticketId);
  }

  // ── Pending intents (operates on Snapshot, stays static) ──────────

  static applyPendingIntents(snapshot: KanbanBoardSnapshot): void {
    const intentsByTicket = new Map<string, Set<string>>();
    for (const intent of snapshot.pendingIntents) {
      let skills = intentsByTicket.get(intent.ticket_id);
      if (!skills) {
        skills = new Set();
        intentsByTicket.set(intent.ticket_id, skills);
      }
      skills.add(intent.skill);
    }
    if (intentsByTicket.size === 0) return;

    const allTickets = [
      ...snapshot.columnViews.flatMap((c: KanbanColumnView) => c.tickets),
      ...snapshot.archivedTickets,
    ];
    for (const ticket of allTickets) {
      const skills = intentsByTicket.get(ticket.ticketId);
      if (!skills) continue;
      const doneSet = new Set(ticket.doneSkillIds);
      const executingSet = new Set(ticket.executingSkillIds);
      const reviewingSet = new Set(ticket.reviewingSkillIds);
      ticket.pendingIntentSkillIds = [...skills].filter(
        (skillId: string) =>
          !doneSet.has(skillId) && !executingSet.has(skillId) &&
          !reviewingSet.has(skillId) &&
          ticket.activeSkillId !== skillId && ticket.reviewSkillId !== skillId,
      );
    }
  }

  // ── Planning paths ────────────────────────────────────────────────

  static resolvePlanningPaths(planningRoot: string): PlanningPaths {
    const root = planningRoot.replace(/\\/g, '/').replace(/\/$/, '');
    const kanbanDir = `${root}/kanban`;
    return {
      planningRoot: root, kanbanDir,
      boardFile: `${kanbanDir}/board.json`,
      kanbanFile: `${kanbanDir}/kanban.json`,
      metricsLogFile: `${kanbanDir}/metrics-log.jsonl`,
      strategyFile: `${kanbanDir}/strategy.md`,
      manifestFile: `${kanbanDir}/manifest.md`,
      actionStateFile: `${kanbanDir}/action-state.json`,
    };
  }

  static engagementWorkspaceFromPlanningRoot(planningRoot: string): string {
    const root = planningRoot.replace(/\\/g, '/').replace(/\/$/, '');
    if (root.endsWith('/docs/planning/delivery-war-room')) {
      return root.slice(0, -'/docs/planning/delivery-war-room'.length);
    }
    if (root.endsWith('/docs/planning')) {
      return root.slice(0, -'/docs/planning'.length);
    }
    return root;
  }

  // ── Serialisation ─────────────────────────────────────────────────

  toJSON(): KanbanBoardData {
    return this.data;
  }

  // ── Private helpers ───────────────────────────────────────────────

  private resolveDefinition(
    config: KanbanConfiguration,
    definitionName: string | null | undefined,
  ): { stages: StageDefinition[] } {
    const defName = definitionName ?? Object.keys(config.definitions)[0] ?? '';
    const def = config.definitions[defName];
    if (!def) throw new Error(`Unknown stage configuration: ${defName}`);
    return { stages: def.stages };
  }

  // ── Stage configuration — static helpers (formerly SystemOfWork) ───

  private static resolveDefName(
    config: KanbanConfiguration,
    definitionName?: string | null,
  ): string {
    return definitionName ?? Object.keys(config.definitions)[0] ?? '';
  }

  private static stepsToSkillRails(steps: StageWorkRequiredEntry[]): StageSkillRail['skills'] {
    return steps
      .filter((s: StageWorkRequiredEntry) => !s.optional)
      .map((s: StageWorkRequiredEntry) => ({
        skillId: s.skill,
        label: SkillCatalog.label(s.skill),
        family: SkillCatalog.familyFor(s.skill),
        role: s.role,
      }));
  }

  /** Build stage skill rails from the kanban config definition. */
  static buildSkillRails(
    config: KanbanConfiguration,
    definitionName?: string | null,
  ): StageSkillRail[] {
    const defName = KanbanBoard.resolveDefName(config, definitionName);
    const def = config.definitions[defName];
    if (!def) return Stage.ORDER.map((stage) => ({ stage, skills: [] }));

    const stageMap = new Map<string, StageDefinition>();
    for (const stageDef of def.stages) stageMap.set(stageDef.name, stageDef);

    return Stage.ORDER.map((stage) => {
      const stageDef = stageMap.get(stage);
      const steps = stageDef?.stage_work_required ?? stageDef?.skills ?? [];
      return { stage, skills: steps.length ? KanbanBoard.stepsToSkillRails(steps) : [] };
    });
  }

  /** Resolve effective team: definition defaults merged with board overrides. */
  static resolveTeam(
    config: KanbanConfiguration,
    definitionName?: string | null,
    boardTeam?: import('./TeamMembership').Team,
  ): NonNullable<import('./TeamMembership').Team> {
    const defName = KanbanBoard.resolveDefName(config, definitionName);
    const defTeam = config.definitions[defName]?.team ?? {};
    const merged = { ...DEFAULT_TEAM, ...defTeam, ...boardTeam } as NonNullable<import('./TeamMembership').Team>;
    for (const role of AGENT_ROLES) merged[role] = merged[role] ?? DEFAULT_TEAM[role];
    return merged;
  }

  /** Active stages (those with at least one required skill) for a definition. */
  static activeStages(
    config: KanbanConfiguration,
    definitionName?: string | null,
  ): import('./Stage').StageId[] {
    const defName = KanbanBoard.resolveDefName(config, definitionName);
    const def = config.definitions[defName];
    if (!def) return [];
    const activeNames = new Set(
      def.stages
        .filter((s: StageDefinition) =>
          (s.stage_work_required ?? s.skills ?? []).some((step: StageWorkRequiredEntry) => !step.optional),
        )
        .map((s: StageDefinition) => s.name),
    );
    return Stage.ORDER.filter((s) => activeNames.has(s));
  }

  private extractTicket(ticketId: string): {
    remaining: KanbanBoardData;
    ticket: RawTicket;
  } {
    const done = [...this.data.done];
    const archived = [...this.data.archived];
    let active = [...this.data.active];
    const backlog = [...this.data.backlog];

    const pull = (list: RawTicket[]): RawTicket | undefined => {
      const idx = list.findIndex((t: RawTicket) => t.ticket_id === ticketId);
      if (idx < 0) return undefined;
      return list.splice(idx, 1)[0];
    };

    let ticket = pull(done) ?? pull(archived) ?? pull(backlog);
    if (!ticket) {
      const existing = active.find((t: RawTicket) => t.ticket_id === ticketId);
      if (!existing) throw new Error(`Ticket not found: ${ticketId}`);
      ticket = { ...existing };
      active = active.filter((t: RawTicket) => t.ticket_id !== ticketId);
    }
    return {
      remaining: { ...this.data, active, done, archived, backlog },
      ticket,
    };
  }

  private existingTicketIds(): Set<string> {
    const ids = new Set<string>();
    for (const t of [
      ...this.data.active, ...this.data.backlog,
      ...this.data.done, ...this.data.archived,
    ]) {
      ids.add(t.ticket_id);
    }
    return ids;
  }

  private applyBackwardMove(
    remaining: KanbanBoardData,
    ticket: RawTicket,
    targetStage: StageId,
    placement: MoveTicketPlacement,
  ): KanbanBoard {
    if (ticket.scatter_to && ticket.scatter_to.length > 0) {
      throw new Error(
        `Cannot move ${ticket.ticket_id} backward: scatter parent. ` +
        'Drag an increment ticket instead.',
      );
    }
    const now = new Date().toISOString();
    const active = remaining.active.filter(
      (t: RawTicket) => t.ticket_id !== ticket.ticket_id,
    );
    const working: RawTicket = {
      ...ticket,
      stage: targetStage,
      entered_stage: now,
      completed_stage: null,
      skill_progress: {},
      stage_history: [...(ticket.stage_history ?? [])],
    };
    if (placement === 'stage_done') {
      working.completed_stage = now;
      delete working.hold_in_progress;
    } else {
      working.hold_in_progress = true;
    }
    active.push(working);
    return new KanbanBoard({ ...remaining, active });
  }
}

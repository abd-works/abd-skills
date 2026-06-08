import type { RawTicket } from './Ticket.schema';
import type { StageId, StageSkill, StageSubColumn } from './Stage';
import { Stage } from './Stage';
import type { AgentRole, Team } from './TeamMembership';
import { AGENT_ROLES, normalizeDeliveryRole } from './TeamMembership';
import { SkillProgressMap } from './SkillProgressMap';

export type KanbanColumn = 'backlog' | 'active' | 'done' | 'archived';

/**
 * domain model: Ticket — unique identifier, lineage, scope level, priority, notes,
 *               stage timestamps, board position, skill progress entries.
 * domain model: Board Position — in-progress or done sub-state, current stage
 *                        (derived from skill progress).
 */
export class Ticket {
  readonly ticketId: string;
  readonly lineage: string[];
  readonly scopeLevel: string;
  readonly stage: StageId | null;
  readonly column: KanbanColumn;
  readonly priority: number;
  readonly notes: string;
  readonly enteredStage: string | null;
  readonly completedStage: string | null;
  readonly scatterFrom: string | null;
  readonly scatterTo: string[];
  readonly holdInProgress: boolean;
  readonly skillProgress: SkillProgressMap;

  pendingIntentSkillIds: string[] = [];

  private readonly raw: RawTicket;

  constructor(ticket: RawTicket, column: KanbanColumn) {
    this.raw = ticket;
    this.ticketId = ticket.ticket_id;
    this.lineage = ticket.lineage;
    this.scopeLevel = ticket.scope_level;
    this.stage = Stage.normalize(ticket.stage);
    this.column = column;
    this.priority = ticket.priority;
    this.notes = ticket.notes;
    this.enteredStage = ticket.entered_stage ?? null;
    this.completedStage = ticket.completed_stage ?? null;
    this.scatterFrom = ticket.scatter_from ?? null;
    this.scatterTo = ticket.scatter_to ?? [];
    this.holdInProgress = ticket.hold_in_progress === true;
    this.skillProgress = new SkillProgressMap(ticket.skill_progress);
  }

  get activeSkillId(): string | null {
    return this.skillProgress.firstExecuting()?.skillId ?? null;
  }

  get activeAgent(): string | null {
    return this.skillProgress.firstExecuting()?.agent ?? null;
  }

  get executingSkillIds(): string[] {
    return this.skillProgress.executingSkillIds();
  }

  get reviewSkillId(): string | null {
    return this.skillProgress.firstReviewing()?.skillId ?? null;
  }

  get reviewAgent(): string | null {
    return this.skillProgress.firstReviewing()?.agent ?? null;
  }

  get reviewingSkillIds(): string[] {
    return this.skillProgress.reviewingSkillIds();
  }

  get awaitingReviewSkillId(): string | null {
    return this.skillProgress.firstAwaitingReview()?.skillId ?? null;
  }

  get awaitingReviewAgent(): AgentRole | null {
    const agent = this.skillProgress.firstAwaitingReview()?.agent ?? null;
    return agent ? normalizeDeliveryRole(agent) : null;
  }

  get awaitingReviewSkillIds(): string[] {
    return this.skillProgress.awaitingReviewSkillIds();
  }

  get isReviewing(): boolean {
    return this.reviewingSkillIds.length > 0;
  }

  get doneSkillIds(): string[] {
    return this.skillProgress.doneSkillIds();
  }

  get failedReviewSkillIds(): string[] {
    return this.skillProgress.failedReviewSkillIds();
  }

  get displayLabel(): string {
    if (this.lineage.length === 0) return this.ticketId;
    return this.lineage[this.lineage.length - 1];
  }

  get chipLabel(): string {
    const id = this.ticketId;
    if (id.length <= 8) return id;
    const match = id.match(/(\d+)$/);
    if (match) return `#${match[1]}`;
    return id.slice(0, 8);
  }

  isScatterParent(): boolean {
    return this.column === 'archived' && this.scatterTo.length > 0;
  }

  isAwaitingScatter(stageSkillIds: string[]): boolean {
    if (this.scatterTo.length > 0) return false;
    if (this.column === 'archived') return false;
    if (!this.isStageSkillsComplete(stageSkillIds)) return false;
    return (
      this.scopeLevel === 'partition' ||
      this.scopeLevel === 'project' ||
      this.scopeLevel === 'all'
    );
  }

  isStageSkillsComplete(stageSkillIds: string[]): boolean {
    if (stageSkillIds.length === 0) return false;
    const doneSet = new Set(this.doneSkillIds);
    return stageSkillIds.every((id: string) => doneSet.has(id));
  }

  hasSkillProgress(): boolean {
    return (
      this.doneSkillIds.length > 0 ||
      this.executingSkillIds.length > 0 ||
      this.activeSkillId !== null ||
      this.reviewSkillId !== null
    );
  }

  resolveArchivedStageDone(): StageId | null {
    if (!this.stage || this.column !== 'archived') return null;
    if (this.scatterTo.length > 0) return this.stage;
    if (this.completedStage) return this.stage;
    return null;
  }

  stageSkillsForColumn(
    columnStage: StageId,
    skillsByStage: Map<StageId, StageSkill[]>,
  ): StageSkill[] {
    if (this.isScatterParent() && this.stage && this.stage !== columnStage) {
      return skillsByStage.get(this.stage) ?? [];
    }
    return skillsByStage.get(columnStage) ?? [];
  }

  workingAgent(): AgentRole | null {
    if (this.reviewSkillId && this.reviewAgent) {
      return normalizeDeliveryRole(this.reviewAgent);
    }
    if (this.activeSkillId && this.activeAgent) {
      return normalizeDeliveryRole(this.activeAgent);
    }
    if (this.awaitingReviewSkillId && this.awaitingReviewAgent) {
      return this.awaitingReviewAgent;
    }
    return null;
  }

  hasLiveAgentWork(): boolean {
    return this.workingAgent() !== null;
  }

  canExpand(stageSkillIds: string[], stageSubColumn?: StageSubColumn): boolean {
    if (stageSkillIds.length === 0 || !this.stage) return false;
    if (stageSubColumn === 'feeds-next') return true;
    if (this.column === 'backlog') return false;
    if (this.column === 'active') return true;
    if (this.column === 'archived' || this.column === 'done') return this.hasSkillProgress();
    return false;
  }

  private nextIncompleteSkill(stageSkillIds: string[]): string | null {
    const doneSet = new Set(this.doneSkillIds);
    return stageSkillIds.find((id: string) => !doneSet.has(id)) ?? null;
  }

  focusSkillId(stageSkillIds: string[], stageSubColumn?: StageSubColumn): string | null {
    if (this.reviewSkillId) return this.reviewSkillId;
    if (this.activeSkillId) return this.activeSkillId;
    if (this.awaitingReviewSkillId) return this.awaitingReviewSkillId;
    if (
      stageSubColumn === 'ip' ||
      stageSubColumn === 'feeds-next' ||
      (stageSubColumn === 'done' && this.holdInProgress)
    ) {
      return this.nextIncompleteSkill(stageSkillIds);
    }
    return null;
  }

  displayFocusSkillId(
    stageSkills: StageSkill[],
    stageSubColumn: StageSubColumn | undefined,
    activeStagePeers: Ticket[],
    team: NonNullable<Team>,
  ): string | null {
    const skillIds = stageSkills.map((s: StageSkill) => s.skillId);
    const focus = this.focusSkillId(skillIds, stageSubColumn);
    if (!focus) return null;

    if (stageSubColumn === 'feeds-next') {
      return this.activeSkillId || this.reviewSkillId ? focus : null;
    }

    if (this.activeSkillId || this.reviewSkillId || this.awaitingReviewSkillId) {
      return focus;
    }

    const focusSkill = stageSkills.find((s: StageSkill) => s.skillId === focus);
    if (!focusSkill) return focus;

    const role = focusSkill.role as AgentRole;
    if (!AGENT_ROLES.includes(role)) return focus;

    const capacity = team[role] ?? 1;
    const contenders = activeStagePeers
      .filter((t: Ticket) => t.stage === this.stage)
      .filter((t: Ticket) => t.column === 'active' || t.column === 'backlog')
      .filter((t: Ticket) => {
        const peerSub: StageSubColumn = t.column === 'backlog' ? 'feeds-next' : 'ip';
        const peerFocus = t.focusSkillId(skillIds, peerSub);
        if (!peerFocus && !t.activeSkillId && !t.reviewSkillId && !t.awaitingReviewSkillId) {
          return false;
        }
        if (t.activeSkillId || t.reviewSkillId || t.awaitingReviewSkillId) {
          const liveId = t.reviewSkillId ?? t.activeSkillId ?? t.awaitingReviewSkillId!;
          const liveSkill = stageSkills.find((s: StageSkill) => s.skillId === liveId);
          return liveSkill?.role === role;
        }
        const peerSkill = stageSkills.find((s: StageSkill) => s.skillId === peerFocus);
        return peerSkill?.role === role;
      })
      .sort((a: Ticket, b: Ticket) => a.priority - b.priority);

    const rank = contenders.findIndex((t: Ticket) => t.ticketId === this.ticketId);
    if (rank < 0 || rank >= capacity) return null;
    return focus;
  }

  scopeCssClass(): string {
    switch (this.scopeLevel) {
      case 'project':
      case 'all':
        return 'kb-ticket--scope-project';
      case 'partition':
        return 'kb-ticket--scope-partition';
      case 'increment':
        return 'kb-ticket--scope-increment';
      default:
        return 'kb-ticket--scope-sprint';
    }
  }

  /**
   * True when a running agent session matches the role responsible for one of this
   * ticket's pending-intent skills. Used to promote the pending-intent icon to a
   * live bot icon when the Cursor SDK session is active but has not yet written
   * execution_status: 'in_progress' to skill_progress.
   */
  showsAgentRunning(activeRoles: Set<string>, stageSkills: StageSkill[]): boolean {
    if (this.pendingIntentSkillIds.length === 0) return false;
    const pendingSet = new Set(this.pendingIntentSkillIds);
    return stageSkills.some((s) => pendingSet.has(s.skillId) && activeRoles.has(s.role));
  }

  showsLiveSkillIcon(stageSubColumn?: StageSubColumn): boolean {
    const hasLiveWork = Boolean(
      this.activeSkillId ||
        this.reviewSkillId ||
        this.awaitingReviewSkillId ||
        this.executingSkillIds.length > 0 ||
        this.reviewingSkillIds.length > 0,
    );
    if (!hasLiveWork) return false;
    if (stageSubColumn !== 'ip' && !(stageSubColumn === 'done' && this.holdInProgress)) {
      return false;
    }
    return true;
  }

  skillRowDisplayState(skillId: string, focusSkill: string | null): SkillRowDisplayState {
    const doneSet = new Set(this.doneSkillIds);
    const isDone = doneSet.has(skillId);
    const executingSet = new Set(this.executingSkillIds);
    const isExecuting = executingSet.has(skillId) || this.activeSkillId === skillId;
    const reviewingSet = new Set(this.reviewingSkillIds);
    const awaitingReviewSet = new Set(this.awaitingReviewSkillIds);
    const isUnderReview = reviewingSet.has(skillId) || this.reviewSkillId === skillId;
    const isAwaitingReview =
      awaitingReviewSet.has(skillId) || this.awaitingReviewSkillId === skillId;
    const isFocus = focusSkill === skillId && !isDone;
    const isFailedReview = this.failedReviewSkillIds.includes(skillId);
    const isPendingIntent = this.pendingIntentSkillIds.includes(skillId);
    const showBot = !isDone && isExecuting && !isUnderReview;
    const showMagnify = (isUnderReview || isAwaitingReview) && !isFailedReview;
    const showRework = isFailedReview && !isDone;
    const showPendingIntent = isPendingIntent && !isDone && !isExecuting && !isUnderReview;
    return {
      isDone, isExecuting, isUnderReview, isPendingIntent, isFocus,
      showBot, showMagnify, showRework, showPendingIntent,
    };
  }

  static countRoleEngagement(columnViews: KanbanColumnView[]): Record<AgentRole, number> {
    const counts: Record<AgentRole, number> = {
      'product-owner': 0, 'business-expert': 0, 'ux-designer': 0, engineer: 0,
    };
    for (const col of columnViews) {
      if (col.id !== 'active' && col.id !== 'backlog') continue;
      for (const ticket of col.tickets) {
        const liveAgent = ticket.workingAgent();
        if (liveAgent) counts[liveAgent]++;
      }
    }
    return counts;
  }

  static ticketsAtStage(columnViews: KanbanColumnView[], stageId: StageId): Ticket[] {
    const active = columnViews.find((c: KanbanColumnView) => c.id === 'active')?.tickets ?? [];
    const backlog = columnViews.find((c: KanbanColumnView) => c.id === 'backlog')?.tickets ?? [];
    return [...active, ...backlog].filter((t: Ticket) => t.stage === stageId);
  }

  toRaw(): RawTicket {
    return this.raw;
  }

  // ─── Test Factories ───────────────────────────────────────────────────────

  static createActive(
    ticketId: string,
    stage: string,
    skill: string,
    role: string,
  ): Ticket {
    return new Ticket(
      {
        ticket_id: ticketId,
        lineage: [],
        scope_level: 'sprint',
        stage,
        priority: 1,
        notes: '',
        skill_progress: { [skill]: { execution_status: 'in_progress', agent: role } },
        scatter_to: [],
      },
      'active',
    );
  }

  static createWithAllSkillsDoneExcept(
    ticketId: string,
    stage: string,
    skill: string,
    role: string,
  ): Ticket {
    return new Ticket(
      {
        ticket_id: ticketId,
        lineage: [],
        scope_level: 'sprint',
        stage,
        priority: 1,
        notes: '',
        skill_progress: {
          'abd-prior-skill': {
            execution_status: 'done',
            review_status: 'done',
            agent: role,
            reviewer: role,
          },
          [skill]: { execution_status: 'in_progress', agent: role },
        },
        scatter_to: [],
      },
      'active',
    );
  }
}

export interface KanbanColumnView {
  id: KanbanColumn;
  label: string;
  tickets: Ticket[];
}

export interface SkillRowDisplayState {
  isDone: boolean;
  isExecuting: boolean;
  isUnderReview: boolean;
  isPendingIntent: boolean;
  isFocus: boolean;
  showBot: boolean;
  showMagnify: boolean;
  showRework: boolean;
  showPendingIntent: boolean;
}

import { z } from 'zod';

// ─── Kanban columns ───────────────────────────────────────────────────────────
// Ticket position is determined by which board array it lives in.
// The UI derives finer-grained visual state (executing/reviewing) from progress.

export const KANBAN_COLUMNS = ['backlog', 'active', 'done', 'archived'] as const;
export type KanbanColumn = (typeof KANBAN_COLUMNS)[number];

export const KANBAN_COLUMN_LABELS: Record<KanbanColumn, string> = {
  backlog: 'Backlog',
  active: 'Active',
  done: 'Done',
  archived: 'Archived',
};

// ─── Stages ───────────────────────────────────────────────────────────────────

export type StageId =
  | 'context'
  | 'shaping'
  | 'discovery'
  | 'exploration'
  | 'specification'
  | 'engineering';

export const STAGE_ORDER: StageId[] = [
  'context',
  'shaping',
  'discovery',
  'exploration',
  'specification',
  'engineering',
];

export const STAGE_LABELS: Record<StageId, string> = {
  context: 'Context',
  shaping: 'Shaping',
  discovery: 'Discovery',
  exploration: 'Exploration',
  specification: 'Specification',
  engineering: 'Engineering',
};

export function normalizeStage(raw: string): StageId | null {
  const key = raw.toLowerCase().trim();
  if (STAGE_ORDER.includes(key as StageId)) return key as StageId;
  return null;
}

// ─── Skill families ───────────────────────────────────────────────────────────

export type SkillFamily =
  | 'domain-driven-design'
  | 'user-experience-design'
  | 'story-driven-delivery'
  | 'architecture-centric-engineering'
  | 'delivery'
  | 'idea-shaping'
  | 'context-to-memory';

// ─── Skill progress (per-skill on a ticket) ──────────────────────────────────

export const SkillProgressSchema = z.object({
  execution_status: z
    .preprocess(
      (v) => (v === 'pending' ? 'not_started' : v),
      z.enum(['not_started', 'in_progress', 'done']),
    )
    .default('not_started'),
  agent: z.string().nullable().optional(),
  start: z.string().nullable().optional(),
  end: z.string().nullable().optional(),
  review_status: z
    .enum(['not_started', 'in_progress', 'done', 'failed'])
    .nullable()
    .optional()
    .transform((v) => (v === 'not_started' ? null : v)),
  reviewer: z.string().nullable().optional(),
  review_start: z.string().nullable().optional(),
  review_end: z.string().nullable().optional(),
});

export type SkillProgress = z.infer<typeof SkillProgressSchema>;

// ─── Ticket ───────────────────────────────────────────────────────────────────

export const TicketSchema = z.object({
  ticket_id: z.string(),
  lineage: z.array(z.string()).default([]),
  scope_level: z.string().default('all'),
  stage: z.string(),
  priority: z.number().default(1),
  skill_progress: z.record(SkillProgressSchema).default({}),
  entered_stage: z.string().nullable().optional(),
  completed_stage: z.string().nullable().optional(),
  scatter_from: z.string().nullable().optional(),
  scatter_to: z.array(z.string()).default([]),
  notes: z.string().default(''),
});

export type Ticket = z.infer<typeof TicketSchema>;

// ─── Team (pair counts per agent role) ────────────────────────────────────────

export const TeamSchema = z.object({
  'product-owner': z.number().int().min(0).default(1),
  'business-expert': z.number().int().min(0).default(1),
  'ux-designer': z.number().int().min(0).default(1),
  engineer: z.number().int().min(0).default(1),
}).optional();

export type Team = z.infer<typeof TeamSchema>;

export const DEFAULT_TEAM: NonNullable<Team> = {
  'product-owner': 1,
  'business-expert': 1,
  'ux-designer': 1,
  engineer: 1,
};

export const AGENT_ROLES = ['product-owner', 'business-expert', 'ux-designer', 'engineer'] as const;
export type AgentRole = (typeof AGENT_ROLES)[number];

/** Map board agent ids (incl. legacy *-reviewer) to pool roles. */
export function normalizeDeliveryRole(agent: string | null | undefined): AgentRole | null {
  if (!agent) return null;
  if (AGENT_ROLES.includes(agent as AgentRole)) return agent as AgentRole;
  const reviewerMatch = agent.match(/^(.+)-reviewer$/);
  if (reviewerMatch && AGENT_ROLES.includes(reviewerMatch[1] as AgentRole)) {
    return reviewerMatch[1] as AgentRole;
  }
  return null;
}

// ─── Board ────────────────────────────────────────────────────────────────────

export const KanbanBoardSchema = z.object({
  schema: z.literal('abd-delivery-kanban/v2'),
  synced_at: z.string().nullable().optional(),
  stage_configuration: z.string().nullable().optional(),
  backlog: z.array(TicketSchema).default([]),
  active: z.array(TicketSchema).default([]),
  done: z.array(TicketSchema).default([]),
  archived: z.array(TicketSchema).default([]),
  team: TeamSchema,
});

export type KanbanBoard = z.infer<typeof KanbanBoardSchema>;

export function parseKanbanBoard(raw: unknown): KanbanBoard {
  return KanbanBoardSchema.parse(raw);
}

// ─── Stage skill rail (from system of work) ──────────────────────────────────

export interface StageSkill {
  skillId: string;
  label: string;
  family: SkillFamily;
  role: string;
}

export interface StageSkillRail {
  stage: StageId;
  skills: StageSkill[];
}

// ─── Ticket view (UI enrichment) ─────────────────────────────────────────────

export interface TicketView {
  ticketId: string;
  lineage: string[];
  scopeLevel: string;
  stage: StageId | null;
  column: KanbanColumn;
  priority: number;
  /** The skill currently being executed (status: in_progress) */
  activeSkillId: string | null;
  activeAgent: string | null;
  /** The skill currently under review (review_status: in_progress) */
  reviewSkillId: string | null;
  reviewAgent: string | null;
  /** Execution done, review not complete, review not yet in progress */
  awaitingReviewSkillId: string | null;
  awaitingReviewAgent: AgentRole | null;
  isReviewing: boolean;
  /** All skill IDs with status: done (for the expanded skill list) */
  doneSkillIds: string[];
  enteredStage: string | null;
  completedStage: string | null;
  scatterFrom: string | null;
  scatterTo: string[];
  notes: string;
  /** Display label derived from lineage */
  displayLabel: string;
  /** Short chip label (e.g. ticket_id abbreviation) */
  chipLabel: string;
}

/** Per-stage sub-columns: in progress, done (includes next-stage backlog in prev stage done). */
export interface StageBucket {
  ip: TicketView[];
  done: TicketView[];
  /** board.backlog tickets whose target stage follows this one — shown in this stage's Done. */
  feedsNext: TicketView[];
}

export type StageSubColumn = 'ip' | 'done' | 'feeds-next';

export function previousStage(stage: StageId): StageId | null {
  const idx = STAGE_ORDER.indexOf(stage);
  if (idx <= 0) return null;
  return STAGE_ORDER[idx - 1]!;
}

/** Active plus staged-backlog tickets sharing a target stage (for WIP focus). */
export function ticketsAtStage(
  columnViews: KanbanColumnView[],
  stageId: StageId,
): TicketView[] {
  const active = columnViews.find((c) => c.id === 'active')?.tickets ?? [];
  const backlog = columnViews.find((c) => c.id === 'backlog')?.tickets ?? [];
  return [...active, ...backlog].filter((t) => t.stage === stageId);
}

/** True when a skill is actively executing or under review with an assigned agent. */
export function ticketHasLiveAgentWork(ticket: TicketView): boolean {
  return resolveWorkingAgent(ticket) !== null;
}

function peerFocusSubColumn(ticket: TicketView): StageSubColumn {
  if (ticket.column === 'backlog') return 'feeds-next';
  if (ticket.column === 'active' && !ticketHasLiveAgentWork(ticket)) return 'feeds-next';
  return 'ip';
}

function nextIncompleteSkill(
  ticket: TicketView,
  stageSkillIds: string[],
): string | null {
  const doneSet = new Set(ticket.doneSkillIds);
  return stageSkillIds.find((id) => !doneSet.has(id)) ?? null;
}

export function hasSkillProgress(ticket: TicketView): boolean {
  return (
    ticket.doneSkillIds.length > 0 ||
    ticket.activeSkillId !== null ||
    ticket.reviewSkillId !== null
  );
}

/** Expand skill list for in-flight, awaiting-pickup, and completed stage work. */
export function ticketCanExpand(
  ticket: TicketView,
  stageSkillIds: string[],
  stageSubColumn?: StageSubColumn,
): boolean {
  if (stageSkillIds.length === 0 || !ticket.stage) return false;
  if (stageSubColumn === 'feeds-next') return true;
  if (ticket.column === 'backlog') return false;
  if (ticket.column === 'active') return true;
  if (ticket.column === 'archived') return hasSkillProgress(ticket);
  if (ticket.column === 'done') return hasSkillProgress(ticket);
  return false;
}

/**
 * The skill the board highlights on a ticket: under review, executing, or — when
 * the ticket is active in In Progress with idle gaps — the next incomplete stage skill.
 */
export function resolveFocusSkillId(
  ticket: TicketView,
  stageSkillIds: string[],
  stageSubColumn?: StageSubColumn,
): string | null {
  if (ticket.reviewSkillId) return ticket.reviewSkillId;
  if (ticket.activeSkillId) return ticket.activeSkillId;
  if (ticket.awaitingReviewSkillId) return ticket.awaitingReviewSkillId;
  if (stageSubColumn === 'ip' || stageSubColumn === 'feeds-next') {
    return nextIncompleteSkill(ticket, stageSkillIds);
  }
  return null;
}

/** Agent role with live board work: executing, reviewing, or awaiting review. */
export function resolveWorkingAgent(ticket: TicketView): AgentRole | null {
  if (ticket.reviewSkillId && ticket.reviewAgent) {
    return normalizeDeliveryRole(ticket.reviewAgent);
  }
  if (ticket.activeSkillId && ticket.activeAgent) {
    return normalizeDeliveryRole(ticket.activeAgent);
  }
  if (ticket.awaitingReviewSkillId && ticket.awaitingReviewAgent) {
    return ticket.awaitingReviewAgent;
  }
  return null;
}

/**
 * Focus skill for display, respecting per-role WIP from team capacity.
 * Live execution/review always shows; idle "next skill" focus is limited to capacity.
 */
export function resolveDisplayFocusSkillId(
  ticket: TicketView,
  stageSkills: StageSkill[],
  stageSubColumn: StageSubColumn | undefined,
  activeStagePeers: TicketView[],
  team: NonNullable<Team>,
): string | null {
  const skillIds = stageSkills.map((s) => s.skillId);
  const focus = resolveFocusSkillId(ticket, skillIds, stageSubColumn);
  if (!focus) return null;

  // Queued tickets (feeds-next) never show collapsed-card focus — expand only.
  if (stageSubColumn === 'feeds-next') {
    return ticket.activeSkillId || ticket.reviewSkillId ? focus : null;
  }

  if (ticket.activeSkillId || ticket.reviewSkillId || ticket.awaitingReviewSkillId) {
    return focus;
  }

  const focusSkill = stageSkills.find((s) => s.skillId === focus);
  if (!focusSkill) return focus;

  const role = focusSkill.role as AgentRole;
  if (!AGENT_ROLES.includes(role)) return focus;

  const capacity = team[role] ?? 1;
  const contenders = activeStagePeers
    .filter((t) => t.stage === ticket.stage)
    .filter((t) => t.column === 'active' || t.column === 'backlog')
    .filter((t) => {
      const peerSub = peerFocusSubColumn(t);
      const peerFocus = resolveFocusSkillId(t, skillIds, peerSub);
      if (!peerFocus && !t.activeSkillId && !t.reviewSkillId && !t.awaitingReviewSkillId) {
        return false;
      }
      if (t.activeSkillId || t.reviewSkillId || t.awaitingReviewSkillId) {
        const liveId = t.reviewSkillId ?? t.activeSkillId ?? t.awaitingReviewSkillId!;
        const liveSkill = stageSkills.find((s) => s.skillId === liveId);
        return liveSkill?.role === role;
      }
      const peerSkill = stageSkills.find((s) => s.skillId === peerFocus);
      return peerSkill?.role === role;
    })
    .sort((a, b) => a.priority - b.priority);

  const rank = contenders.findIndex((t) => t.ticketId === ticket.ticketId);
  if (rank < 0 || rank >= capacity) return null;
  return focus;
}

export interface SkillRowDisplayState {
  isDone: boolean;
  isExecuting: boolean;
  isUnderReview: boolean;
  isFocus: boolean;
  showBot: boolean;
  showMagnify: boolean;
}

/** Per-row icon and styling flags for the expanded skill list on a ticket card. */
export function skillRowDisplayState(
  skillId: string,
  ticket: TicketView,
  focusSkillId: string | null,
): SkillRowDisplayState {
  const doneSet = new Set(ticket.doneSkillIds);
  const isDone = doneSet.has(skillId);
  const isExecuting = ticket.activeSkillId === skillId;
  const isUnderReview = ticket.reviewSkillId === skillId;
  const isAwaitingReview = ticket.awaitingReviewSkillId === skillId;
  const isFocus = focusSkillId === skillId && !isDone;
  // Bot icon = live execution only (pool uses the same rule via resolveWorkingAgent).
  const showBot = !isDone && isExecuting && !isUnderReview;
  const showMagnify = isUnderReview || isAwaitingReview;
  return { isDone, isExecuting, isUnderReview, isFocus, showBot, showMagnify };
}

/** Whether the collapsed ticket card should show the skill icon (bot / magnify). No avatars on tickets — pool only. */
export function ticketShowsLiveSkillIcon(
  ticket: TicketView,
  focusSkillId: string | null,
  stageSubColumn?: StageSubColumn,
): boolean {
  if (focusSkillId === null || stageSubColumn !== 'ip') return false;
  return Boolean(ticket.activeSkillId || ticket.reviewSkillId);
}

export const HEARTBEAT_STALE_SECS = 120;

/**
 * Count live agent engagements per role — only skills actively executing or under review.
 * Queued tickets (backlog or active without a live agent) do not consume pool WIP slots.
 */
export function countRoleEngagement(
  columnViews: KanbanColumnView[],
  _stageSkillRails: StageSkillRail[],
  _team: NonNullable<Team>,
): Record<AgentRole, number> {
  const counts: Record<AgentRole, number> = {
    'product-owner': 0,
    'business-expert': 0,
    'ux-designer': 0,
    engineer: 0,
  };

  for (const col of columnViews) {
    if (col.id !== 'active' && col.id !== 'backlog') continue;
    for (const ticket of col.tickets) {
      const liveAgent = resolveWorkingAgent(ticket);
      if (liveAgent) counts[liveAgent]++;
    }
  }

  return counts;
}

/** Pool avatar liveness: board engagement, or heartbeat status working (not ready). */
export function resolvePoolAvatarState(
  slotIndex: number,
  engagedCount: number,
  heartbeatAge: number | null,
  stalenessSecs = HEARTBEAT_STALE_SECS,
  heartbeatStatus: string | null = null,
): 'idle' | 'working' | 'inactive' {
  if (slotIndex < engagedCount) return 'working';
  const effectiveAge =
    heartbeatAge !== null && heartbeatAge >= 0 ? heartbeatAge : null;
  const heartbeatFresh =
    effectiveAge !== null && effectiveAge < stalenessSecs;
  if (heartbeatFresh && heartbeatStatus === 'working') {
    return 'working';
  }
  if (heartbeatFresh || effectiveAge === null) return 'idle';
  return 'inactive';
}

export interface HeartbeatSlot {
  ageSeconds: number | null;
  status: string | null;
}

/** Per-instance heartbeats for multi-slot roles (e.g. heartbeat-business-expert-be2.json). */
export type HeartbeatSlots = Partial<
  Record<AgentRole | 'kanban-lead', HeartbeatSlot[]>
>;

export function parseHeartbeatFileName(
  fileName: string,
): { role: AgentRole | 'kanban-lead'; slotKey: string } | null {
  if (!fileName.startsWith('heartbeat-') || !fileName.endsWith('.json')) {
    return null;
  }
  const body = fileName.slice('heartbeat-'.length, -'.json'.length);
  const roles: Array<AgentRole | 'kanban-lead'> = [...AGENT_ROLES, 'kanban-lead'];
  for (const role of roles) {
    if (body === role) return { role, slotKey: '' };
    const prefix = `${role}-`;
    if (body.startsWith(prefix)) {
      return { role, slotKey: body.slice(prefix.length) };
    }
  }
  return null;
}

export function buildHeartbeatSlots(
  files: Array<{ fileName: string; raw: { ts?: string; status?: string } }>,
  nowMs = Date.now(),
): HeartbeatSlots {
  const byRole = new Map<
    string,
    Array<{ slotKey: string; ageSeconds: number | null; status: string | null }>
  >();

  for (const { fileName, raw } of files) {
    const parsed = parseHeartbeatFileName(fileName);
    if (!parsed) continue;
    let ageSeconds: number | null = null;
    if (raw?.ts) {
      const parsed = Math.floor((nowMs - new Date(raw.ts).getTime()) / 1000);
      // Future/skewed timestamps must not read as "fresh" (negative age).
      ageSeconds = parsed >= 0 ? parsed : null;
    }
    const list = byRole.get(parsed.role) ?? [];
    list.push({
      slotKey: parsed.slotKey,
      ageSeconds,
      status: raw.status ?? null,
    });
    byRole.set(parsed.role, list);
  }

  const result: HeartbeatSlots = {};
  for (const [role, slots] of byRole) {
    slots.sort((a, b) => {
      if (a.slotKey === '') return -1;
      if (b.slotKey === '') return 1;
      return a.slotKey.localeCompare(b.slotKey);
    });
    result[role as AgentRole | 'kanban-lead'] = slots.map((s) => ({
      ageSeconds: s.ageSeconds,
      status: s.status,
    }));
  }
  return result;
}

export interface KanbanColumnView {
  id: KanbanColumn;
  label: string;
  tickets: TicketView[];
}

// ─── Heartbeats ───────────────────────────────────────────────────────────────

export type HeartbeatAges = Partial<Record<AgentRole | 'kanban-lead', number | null>>;

// ─── Snapshot ─────────────────────────────────────────────────────────────────

export interface KanbanBoardSnapshot {
  planningRoot: string;
  boardTitle: string;
  syncedAt: string | null;
  stageFlow: StageId[];
  board: KanbanBoard;
  columnViews: KanbanColumnView[];
  archivedTickets: TicketView[];
  stageSkillRails: StageSkillRail[];
  polledAt: string;
  etag: string;
  team: NonNullable<Team>;
  heartbeats: HeartbeatAges;
  heartbeatSlots: HeartbeatSlots;
}

// ─── Planning paths ───────────────────────────────────────────────────────────

export interface PlanningPaths {
  planningRoot: string;
  kanbanDir: string;
  boardFile: string;
  kanbanFile: string;
  metricsLogFile: string;
  strategyFile: string;
  manifestFile: string;
}

export function resolvePlanningPaths(planningRoot: string): PlanningPaths {
  const root = planningRoot.replace(/\\/g, '/').replace(/\/$/, '');
  const kanbanDir = `${root}/kanban`;
  return {
    planningRoot: root,
    kanbanDir,
    boardFile: `${kanbanDir}/board.json`,
    kanbanFile: `${kanbanDir}/kanban.json`,
    metricsLogFile: `${kanbanDir}/metrics-log.jsonl`,
    strategyFile: `${kanbanDir}/strategy.md`,
    manifestFile: `${kanbanDir}/manifest.md`,
  };
}

// ─── View builders ────────────────────────────────────────────────────────────

function ticketDisplayLabel(ticket: Ticket): string {
  if (ticket.lineage.length === 0) return ticket.ticket_id;
  return ticket.lineage[ticket.lineage.length - 1];
}

function ticketChipLabel(ticket: Ticket): string {
  const id = ticket.ticket_id;
  if (id.length <= 8) return id;
  const match = id.match(/(\d+)$/);
  if (match) return `#${match[1]}`;
  return id.slice(0, 8);
}

/** CSS class for ticket card tint by scope_level (all = project, increment, sprint). */
export function scopeLevelCssClass(scopeLevel: string): string {
  switch (scopeLevel) {
    case 'all':
      return 'kb-ticket--scope-all';
    case 'increment':
      return 'kb-ticket--scope-increment';
    case 'sprint':
      return 'kb-ticket--scope-sprint';
    default:
      return 'kb-ticket--scope-sprint';
  }
}

/** A skill is complete only when both execution and review are done (work-queue gate). */
export function isSkillComplete(sp: SkillProgress): boolean {
  return sp.execution_status === 'done' && sp.review_status === 'done';
}

function deriveActiveSkill(skillProgress: Record<string, SkillProgress>): {
  activeSkillId: string | null;
  activeAgent: string | null;
  reviewSkillId: string | null;
  reviewAgent: string | null;
  awaitingReviewSkillId: string | null;
  awaitingReviewAgent: AgentRole | null;
  doneSkillIds: string[];
} {
  let activeSkillId: string | null = null;
  let activeAgent: string | null = null;
  let reviewSkillId: string | null = null;
  let reviewAgent: string | null = null;
  let awaitingReviewSkillId: string | null = null;
  let awaitingReviewAgent: AgentRole | null = null;
  const doneSkillIds: string[] = [];

  for (const [skillId, sp] of Object.entries(skillProgress)) {
    if (sp.execution_status === 'in_progress' && !activeSkillId) {
      activeSkillId = skillId;
      activeAgent = sp.agent ?? null;
    }
    if (sp.review_status === 'in_progress' && !reviewSkillId) {
      reviewSkillId = skillId;
      reviewAgent = sp.reviewer ?? sp.agent ?? null;
    }
    if (
      sp.execution_status === 'done' &&
      sp.review_status !== 'done' &&
      sp.review_status !== 'in_progress' &&
      !awaitingReviewSkillId
    ) {
      awaitingReviewSkillId = skillId;
      awaitingReviewAgent = normalizeDeliveryRole(sp.reviewer ?? sp.agent ?? null);
    }
    if (isSkillComplete(sp)) {
      doneSkillIds.push(skillId);
    }
  }

  return {
    activeSkillId,
    activeAgent,
    reviewSkillId,
    reviewAgent,
    awaitingReviewSkillId,
    awaitingReviewAgent,
    doneSkillIds,
  };
}

function toTicketView(ticket: Ticket, column: KanbanColumn): TicketView {
  const {
    activeSkillId,
    activeAgent,
    reviewSkillId,
    reviewAgent,
    awaitingReviewSkillId,
    awaitingReviewAgent,
    doneSkillIds,
  } = deriveActiveSkill(ticket.skill_progress);

  return {
    ticketId: ticket.ticket_id,
    lineage: ticket.lineage,
    scopeLevel: ticket.scope_level,
    stage: normalizeStage(ticket.stage),
    column,
    priority: ticket.priority,
    activeSkillId,
    activeAgent,
    reviewSkillId,
    reviewAgent,
    awaitingReviewSkillId,
    awaitingReviewAgent,
    isReviewing: reviewSkillId !== null,
    doneSkillIds,
    enteredStage: ticket.entered_stage ?? null,
    completedStage: ticket.completed_stage ?? null,
    scatterFrom: ticket.scatter_from ?? null,
    scatterTo: ticket.scatter_to ?? [],
    notes: ticket.notes,
    displayLabel: ticketDisplayLabel(ticket),
    chipLabel: ticketChipLabel(ticket),
  };
}

export function buildColumnViews(board: KanbanBoard): KanbanColumnView[] {
  return KANBAN_COLUMNS
    .filter((id) => id !== 'archived')
    .map((id) => {
      let tickets: TicketView[];
      switch (id) {
        case 'backlog':
          tickets = board.backlog.map((t) => toTicketView(t, 'backlog'));
          break;
        case 'active':
          tickets = board.active.map((t) => toTicketView(t, 'active'));
          break;
        case 'done':
          tickets = board.done.map((t) => toTicketView(t, 'done'));
          break;
        default:
          tickets = [];
      }
      return { id, label: KANBAN_COLUMN_LABELS[id], tickets };
    });
}

export function buildArchivedViews(board: KanbanBoard): TicketView[] {
  return board.archived.map((t) => toTicketView(t, 'archived'));
}

/** True when every skill on the stage rail is complete (execution + review). */
export function isStageSkillsComplete(
  ticket: TicketView,
  stageSkillIds: string[],
): boolean {
  if (stageSkillIds.length === 0) return false;
  const doneSet = new Set(ticket.doneSkillIds);
  return stageSkillIds.every((id) => doneSet.has(id));
}

/** Which stage's Done column should show an archived ticket, if any. */
export function resolveArchivedStageDone(ticket: TicketView): StageId | null {
  if (!ticket.stage || ticket.column !== 'archived') return null;
  if (ticket.scatterTo.length > 0) return ticket.stage;
  if (ticket.completedStage) return ticket.stage;
  return null;
}

/** Archived ticket that scattered into child tickets. */
export function isScatterParent(ticket: TicketView): boolean {
  return ticket.column === 'archived' && ticket.scatterTo.length > 0;
}

/**
 * Skill rail for a ticket in a stage column. Scatter parents relocated to a
 * child’s stage column keep their own stage’s skills (e.g. exploration UL/AC/UX
 * on an increment parent sitting in specification Done).
 */
export function stageSkillsForTicket(
  ticket: TicketView,
  columnStage: StageId,
  skillsByStage: Map<StageId, StageSkill[]>,
): StageSkill[] {
  if (
    isScatterParent(ticket) &&
    ticket.stage &&
    ticket.stage !== columnStage
  ) {
    return skillsByStage.get(ticket.stage) ?? [];
  }
  return skillsByStage.get(columnStage) ?? [];
}

type StageBucketKey = 'ip' | 'done' | 'feedsNext';

function removeTicketFromBuckets(
  buckets: Map<StageId, StageBucket>,
  ticketId: string,
): { stage: StageId; key: StageBucketKey; ticket: TicketView } | null {
  for (const [stage, bucket] of buckets) {
    for (const key of ['ip', 'done', 'feedsNext'] as const) {
      const idx = bucket[key].findIndex((t) => t.ticketId === ticketId);
      if (idx >= 0) {
        const [ticket] = bucket[key].splice(idx, 1);
        return { stage, key, ticket };
      }
    }
  }
  return null;
}

const SUB_COLUMN_TRAILING_RANK: Record<StageBucketKey, number> = {
  ip: 0,
  feedsNext: 1,
  done: 2,
};

/** Narrower scope scatter parents relocate before wider (increment before project). */
function scatterParentRelocateOrder(ticket: TicketView): number {
  switch (ticket.scopeLevel) {
    case 'sprint':
      return 0;
    case 'increment':
      return 1;
    case 'all':
      return 2;
    default:
      return 1;
  }
}

function relocateOneScatterParent(
  buckets: Map<StageId, StageBucket>,
  parent: TicketView,
): boolean {
  const childIds = new Set(parent.scatterTo);
  const located: Array<{
    stage: StageId;
    key: StageBucketKey;
    ticket: TicketView;
    stageIdx: number;
  }> = [];

  for (const [stage, bucket] of buckets) {
    const stageIdx = STAGE_ORDER.indexOf(stage);
    for (const key of ['ip', 'done', 'feedsNext'] as const) {
      for (const ticket of bucket[key]) {
        if (childIds.has(ticket.ticketId)) {
          located.push({ stage, key, ticket, stageIdx });
        }
      }
    }
  }

  if (located.length === 0) return false;

  located.sort((a, b) => {
    if (a.stageIdx !== b.stageIdx) return a.stageIdx - b.stageIdx;
    const rankA = SUB_COLUMN_TRAILING_RANK[a.key];
    const rankB = SUB_COLUMN_TRAILING_RANK[b.key];
    if (rankA !== rankB) return rankA - rankB;
    return a.ticket.priority - b.ticket.priority;
  });

  const { stage, key } = located[0]!;
  const removed = removeTicketFromBuckets(buckets, parent.ticketId);
  if (!removed) return false;

  const targetList = buckets.get(stage)![key];
  const ownChildIndices = targetList
    .map((t, i) => (childIds.has(t.ticketId) ? i : -1))
    .filter((i) => i >= 0);
  const insertAt = ownChildIndices.length > 0 ? Math.min(...ownChildIndices) : 0;
  targetList.splice(insertAt, 0, removed.ticket);
  return true;
}

/**
 * Move scatter parents to the bucket of their **trailing** (lagging) child; parent
 * inserted on top of that child in the list. Trailing = earliest stage, then least
 * progressed sub-column (IP before queued before done), then lowest priority.
 *
 * Runs multiple passes so project-level parents follow increments after those
 * increments relocate beside their sprint children.
 */
export function relocateScatterParents(
  buckets: Map<StageId, StageBucket>,
  archivedTickets: TicketView[],
): void {
  const parents = archivedTickets
    .filter(isScatterParent)
    .sort(
      (a, b) =>
        scatterParentRelocateOrder(a) - scatterParentRelocateOrder(b) ||
        a.priority - b.priority,
    );
  const maxPasses = Math.max(parents.length, 1);
  for (let pass = 0; pass < maxPasses; pass++) {
    let anyMoved = false;
    for (const parent of parents) {
      if (relocateOneScatterParent(buckets, parent)) anyMoved = true;
    }
    if (!anyMoved) break;
  }
}

function emptyStageBuckets(): Map<StageId, StageBucket> {
  const buckets = new Map<StageId, StageBucket>();
  for (const stage of STAGE_ORDER) {
    buckets.set(stage, { ip: [], done: [], feedsNext: [] });
  }
  return buckets;
}

/**
 * Map board arrays into per-stage in-progress / done sub-columns.
 * - board.backlog tickets with a stage → previous stage Done (feeds next stage).
 * - board.active tickets without a live agent → **same stage** Done feeds-next (queued in stage, not IP).
 */
export function buildStageBuckets(
  columnViews: KanbanColumnView[],
  archivedTickets: TicketView[],
  stageSkillRails: StageSkillRail[],
): Map<StageId, StageBucket> {
  const buckets = emptyStageBuckets();
  const skillsByStage = new Map(
    stageSkillRails.map((r) => [r.stage, r.skills.map((s) => s.skillId)]),
  );

  for (const col of columnViews) {
    if (col.id === 'archived') continue;
    for (const ticket of col.tickets) {
      if (!ticket.stage) continue;

      if (col.id === 'backlog') {
        const prev = previousStage(ticket.stage);
        if (prev) buckets.get(prev)?.feedsNext.push(ticket);
        continue;
      }

      const bucket = buckets.get(ticket.stage);
      if (!bucket) continue;
      const skillIds = skillsByStage.get(ticket.stage) ?? [];

      if (col.id === 'done') {
        bucket.done.push(ticket);
      } else if (col.id === 'active') {
        if (isStageSkillsComplete(ticket, skillIds)) {
          bucket.done.push(ticket);
        } else if (ticketHasLiveAgentWork(ticket)) {
          bucket.ip.push(ticket);
        } else {
          bucket.feedsNext.push(ticket);
        }
      }
    }
  }

  for (const bucket of buckets.values()) {
    bucket.feedsNext.sort((a, b) => a.priority - b.priority);
  }

  for (const ticket of archivedTickets) {
    const stage = resolveArchivedStageDone(ticket);
    if (stage) buckets.get(stage)?.done.push(ticket);
  }

  relocateScatterParents(buckets, archivedTickets);

  return buckets;
}

/** Global Backlog column — tickets not yet assigned to a delivery stage. */
export function buildGlobalBacklogTickets(columnViews: KanbanColumnView[]): TicketView[] {
  const backlogCol = columnViews.find((c) => c.id === 'backlog');
  if (!backlogCol) return [];
  return backlogCol.tickets.filter((t) => !t.stage);
}

/** Archived tickets not already shown in a stage column (done, feeds-next, or IP). */
export function buildArchivedColumnTickets(
  archivedTickets: TicketView[],
  stageBuckets: Map<StageId, StageBucket>,
): TicketView[] {
  const shownOnBoard = new Set<string>();
  for (const bucket of stageBuckets.values()) {
    for (const t of bucket.done) shownOnBoard.add(t.ticketId);
    for (const t of bucket.feedsNext) shownOnBoard.add(t.ticketId);
    for (const t of bucket.ip) shownOnBoard.add(t.ticketId);
  }
  return archivedTickets.filter((t) => !shownOnBoard.has(t.ticketId));
}

export function boardEtag(board: KanbanBoard): string {
  const activeSig = board.active
    .map((t) => `${t.ticket_id}:${t.stage}:${Object.keys(t.skill_progress).length}`)
    .join('|');
  return `${board.synced_at ?? 'none'}:${board.backlog.length}:${activeSig}:${board.done.length}:${board.archived.length}`;
}

// ─── Agent Domain ─────────────────────────────────────────────────────────────
export { SDK_SESSION_STALE_SECS } from './AgentLiveness';
export type { BootstrapPrompt } from './BootstrapPrompt';
export type { AgentStartResult, AgentStopResult, ActionIntentResult } from './AgentLifecycleResult';
export { SkillProgress } from './SkillProgress';
export type { SkillExecutionStatus } from './SkillProgress';

// ─── Domain Entities ─────────────────────────────────────────────────────────
export { Ticket } from './Ticket';
export type { KanbanColumn, KanbanColumnView, SkillRowDisplayState } from './Ticket';
export { TicketSchema, type RawTicket } from './Ticket.schema';

export { SkillProgressEntry } from './SkillProgressEntry';
export { SkillProgressMap } from './SkillProgressMap';
export { SkillProgressSchema, type SkillProgress } from './SkillProgress.schema';

export { TeamMembership, AGENT_ROLES, DEFAULT_TEAM, normalizeDeliveryRole } from './TeamMembership';
export { TeamSchema } from './TeamMembership';
export type { AgentRole, Team } from './TeamMembership';

// ─── Domain Collections ──────────────────────────────────────────────────────
export { StageBucketLayout } from './StageBucketLayout';

// ─── Stage ───────────────────────────────────────────────────────────────────
export { Stage } from './Stage';
export type {
  StageId, SkillFamily, StageSkill, StageSkillRail,
  StageBucket, StageSubColumn, KanbanEndColumn,
} from './Stage';

// ─── Skill Catalog ───────────────────────────────────────────────────────────
export { SkillCatalog } from './SkillCatalog';

// ─── Kanban Board (aggregate) ────────────────────────────────────────────────
export {
  KanbanBoard,
  KanbanBoardSchema,
  parseKanbanBoard,
  KANBAN_COLUMNS,
  KANBAN_COLUMN_LABELS,
  SCOPE_LEVEL_LABELS,
} from './KanbanBoard';
export type {
  KanbanBoardData,
  KanbanBoardSnapshot,
  AgentSessionInfo,
  PlanningPaths,
  BoardMode,
  ActionIntent,
  MoveTicketPlacement,
  ScatterChildSpec,
  MoveTicketOptions,
  KanbanConfiguration,
  KanbanConfigurationDefinition,
  StageDefinition,
  StageDefinition as StageDef,
  StageWorkRequiredEntry,
} from './KanbanBoard';

export { KanbanBoardLoader } from './KanbanBoardLoader';

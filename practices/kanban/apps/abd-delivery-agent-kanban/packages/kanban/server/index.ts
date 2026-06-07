// ─── Agent Domain ─────────────────────────────────────────────────────────────
export { AgentDefinition, type ResolvedSkills } from './AgentDefinition';
export { AgentSession, type AgentSessionOptions, type SessionStatusReport } from './AgentSession';
export { AgentOutputStream, type AgentOutputEvent } from './AgentOutputStream';
export { KanbanLead, type KanbanLeadOptions, type HandleSkillCompletionResult } from './KanbanLead';
export { TeamMember, type SlotType } from './TeamMember';

// ─── Kanban Domain ────────────────────────────────────────────────────────────
export { KanbanBoard } from './KanbanBoard';
export { Ticket, type ScatterChildSpec, type ScatterResolveContext } from './Ticket';
export { Stage } from './Stage';
export { SkillCatalog, type DiscoveredSkill } from './SkillCatalog';
export { StageBucketLayout } from './StageBucketLayout';
export { TeamMembership } from './TeamMembership';
export {
  PlanningFolderRepository,
  type PlanningFolderRepositoryInterface,
} from './PlanningFolderRepository';

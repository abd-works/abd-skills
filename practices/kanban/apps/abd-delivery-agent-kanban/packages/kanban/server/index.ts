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

// ─── Migrated Python Domain Layer ─────────────────────────────────────────────
export {
  resolveWarRoomDir,
  loadBoard,
  saveBoard,
  loadKanbanConfig,
  parseKanbanBoards,
  resolveKb,
  loadTeam,
  appendMetricsLog,
  nowIso,
  type WrTicket,
  type WrBoard,
  type WrSkillProgress,
  type WrKanbanBoard,
  type WrKanbanConfig,
  type WrKanbanConfigEntry,
  type WrStageDef,
  type WrSkillDef,
  type WrStageHistoryEntry,
} from './WarRoomService';

export {
  heartbeatPath,
  writeHeartbeat,
  readHeartbeatAge,
  countLiveAgents,
  countWorkingAgents,
  hasFreshHeartbeatWithStatus,
  registerExecutorSpawn,
  readRegisteredSpawnEpoch,
  heartbeatMatchesRegisteredSpawn,
  purgeUnregisteredHeartbeats,
} from './HeartbeatService';

export {
  loadActionIntents,
  removeActionIntentEntry,
  findFirstIntentForRole,
  countIntentsByRole,
  actionStateFileExists,
  type ActionIntentEntry,
} from './ActionStateService';

export {
  isStageComplete,
  nextEligibleSkill,
  advanceToNextStage,
  needsScatter,
  scatterIntoChildren,
  findTicketInBoard,
  saveTicketInBoard,
  listEligiblePulls,
  sortBacklog,
  ticketsNeedingScatter,
} from './KanbanDomainOps';

export {
  pullSkill,
  claimSkillOnBoard,
  completeSkillOnBoard,
  signalReady,
  claimNextIntent,
  findInProgressClaim,
  applySkillFixture,
  type AgentOperationResult,
} from './TeamMemberDomainService';

export { LeadScanService, type LeadScanReport, type SpawnPrompt } from './LeadScanService';

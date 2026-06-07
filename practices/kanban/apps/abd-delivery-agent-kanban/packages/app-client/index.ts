// ── Domain extensions ─────────────────────────────────────────────
export {
  Ticket,
  TICKET_DRAG_ID,
  TICKET_DRAG_STAGE,
  type LeadScanResult,
  type TicketDragPayload,
  type TicketDropPlacement,
  type TicketDropTarget,
  type TicketStageDropHandler,
} from '@deliveryforge/kanban-client';
export { Heartbeat, ROLE_LABELS, ROLE_FULL } from '@deliveryforge/kanban-client';
export { KanbanBoard } from '@deliveryforge/kanban-client';
export { StageBucketLayout } from '@deliveryforge/kanban-client';
export { Stage } from '@deliveryforge/kanban-client';
export { SkillCatalog } from '@deliveryforge/kanban-client';

// ── React components ──────────────────────────────────────────────
export { KanbanBoardView, type KanbanBoardViewProps } from './KanbanBoardView';
export { TicketView } from './TicketView';
export { StageInProgressView } from './StageInProgressView';
export { StageDoneView } from './StageDoneView';
export { StageGroupView } from './StageGroupView';
export { KanbanEndColumnView } from './KanbanEndColumnView';
export { TeamMemberView } from './TeamMemberView';
export { TeamRoleView } from './TeamRoleView';
export { TeamView } from './TeamView';
export {
  ChatbotIcon,
  MagnifyIcon,
  DoneIcon,
  ReworkIcon,
  PendingIntentIcon,
} from './icons';

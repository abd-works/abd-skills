import { type MutableRefObject } from 'react';
import { StageInProgressView } from './StageInProgressView';
import { StageDoneView } from './StageDoneView';
import { Ticket } from '@deliveryforge/kanban-client';
import { Stage, SkillCatalog } from '@deliveryforge/kanban-shared';
import type {
  AgentSessionInfo,
  BoardMode,
  KanbanBoardSnapshot,
  StageId,
  StageSkill,
  StageBucket,
} from '@deliveryforge/kanban-shared';
import type { TicketDragPayload, TicketStageDropHandler } from '@deliveryforge/kanban-client';

export function StageGroupView({
  stage,
  bucket,
  skills,
  skillsByStage,
  peersByTargetStage,
  team,
  boardMode,
  agentSessions,
  onResumeTicket,
  draggingTicketRef,
  draggingTicketId,
  draggingTicket,
  onTicketDrop,
  onTicketDragStart,
  onTicketDragEnd,
}: {
  stage: StageId;
  bucket: StageBucket;
  skills: StageSkill[];
  skillsByStage: Map<StageId, StageSkill[]>;
  peersByTargetStage: Map<StageId, Ticket[]>;
  team: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  agentSessions?: Record<string, AgentSessionInfo>;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: 'in_progress' | 'stage_done') => void;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  draggingTicketId?: string | null;
  draggingTicket?: TicketDragPayload | null;
  onTicketDrop?: TicketStageDropHandler;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
}) {
  const ipTickets = bucket.ip as Ticket[];
  const activeStagePeers = [...ipTickets];

  return (
    <div
      className={'kb-stage-group kb-stage-group--' + stage}
      data-stage={stage}
    >
      <div className="kb-stage-group-header">
        {Stage.LABELS[stage]}
      </div>
      <div className="kb-stage-sub-cols">
        <StageInProgressView
          label="In Progress"
          subColId="ip"
          tickets={ipTickets}
          stageSkills={skills}
          activeStagePeers={activeStagePeers}
          team={team}
          boardMode={boardMode}
          agentSessions={agentSessions}
          onResumeTicket={onResumeTicket}
          columnStage={stage}
          draggingTicketRef={draggingTicketRef}
          draggingTicketId={draggingTicketId}
          draggingTicket={draggingTicket}
          onTicketDrop={onTicketDrop}
          onTicketDragStart={onTicketDragStart}
          onTicketDragEnd={onTicketDragEnd}
        />
        <StageDoneView
          columnStage={stage}
          doneTickets={bucket.done as Ticket[]}
          feedsNextTickets={bucket.feedsNext as Ticket[]}
          stageSkills={skills}
          skillsByStage={skillsByStage}
          peersByTargetStage={peersByTargetStage}
          team={team}
          boardMode={boardMode}
          onResumeTicket={onResumeTicket}
          onTicketDragStart={onTicketDragStart}
          onTicketDragEnd={onTicketDragEnd}
          draggingTicketRef={draggingTicketRef}
          draggingTicketId={draggingTicketId}
          draggingTicket={draggingTicket}
          onTicketDrop={onTicketDrop}
        />
      </div>
      {skills.length > 0 && (
        <div className="kb-stage-skills">
          {skills.map((s) => (
            <span
              key={s.skillId}
              className={'kb-skill-chip ' + SkillCatalog.familyCssClass(s.family)}
              title={s.label}
            >
              {s.label}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

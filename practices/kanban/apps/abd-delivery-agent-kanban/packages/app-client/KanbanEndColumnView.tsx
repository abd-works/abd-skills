import { type MutableRefObject } from 'react';
import { TicketView } from './TicketView';
import { Ticket } from '@deliveryforge/kanban-client';
import type { BoardMode, StageId, StageSkill, KanbanEndColumn } from '@deliveryforge/kanban-shared';
import type { TicketDragPayload } from '@deliveryforge/kanban-client';

export function KanbanEndColumnView({
  heading,
  colId,
  tickets,
  skillsByStage,
  boardMode,
  draggingTicketRef,
}: {
  heading: string;
  colId: KanbanEndColumn;
  tickets: Ticket[];
  skillsByStage: Map<StageId, StageSkill[]>;
  boardMode?: BoardMode;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
}) {
  return (
    <div className={'kb-end-col kb-end-col--' + colId} data-end-col={colId}>
      <div className="kb-stage-head">
        <span className="kb-stage-label">{heading}</span>
        {tickets.length > 0 ? (
          <span className="kb-col-count">{tickets.length}</span>
        ) : null}
      </div>
      <div className="kb-sub-col-tickets">
        {tickets.map((t) => {
          const stageSkills = t.stage ? skillsByStage.get(t.stage) ?? [] : [];
          return (
            <TicketView
              key={t.ticketId}
              ticket={t}
              stageSkills={stageSkills}
              stageSubColumn={colId === 'backlog' ? 'ip' : 'done'}
              activeStagePeers={[]}
              boardMode={boardMode}
              draggingTicketRef={draggingTicketRef}
            />
          );
        })}
      </div>
    </div>
  );
}

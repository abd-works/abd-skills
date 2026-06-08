import { useState, useRef, useEffect, type MutableRefObject } from 'react';
import { TicketView } from './TicketView';
import { Ticket } from '@deliveryforge/kanban-client';
import type { BoardMode, StageId, StageSkill, KanbanBoardSnapshot } from '@deliveryforge/kanban-shared';
import type { TicketDragPayload, TicketStageDropHandler } from '@deliveryforge/kanban-client';

export function StageDoneView({
  columnStage,
  doneTickets,
  feedsNextTickets,
  stageSkills,
  skillsByStage,
  peersByTargetStage,
  team,
  boardMode,
  onResumeTicket,
  onTicketDragStart,
  onTicketDragEnd,
  draggingTicketRef,
  draggingTicketId,
  draggingTicket,
  onTicketDrop,
}: {
  columnStage: StageId;
  doneTickets: Ticket[];
  feedsNextTickets: Ticket[];
  stageSkills: StageSkill[];
  skillsByStage: Map<StageId, StageSkill[]>;
  peersByTargetStage: Map<StageId, Ticket[]>;
  team: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: 'in_progress' | 'stage_done') => void;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  draggingTicketId?: string | null;
  draggingTicket?: TicketDragPayload | null;
  onTicketDrop?: TicketStageDropHandler;
}) {
  const isManual = boardMode === 'manual';
  const acceptsTicketDrop = isManual && !!onTicketDrop;
  const [ticketDropHighlight, setTicketDropHighlight] = useState(false);
  const ticketDragCounterRef = useRef(0);

  useEffect(() => {
    if (!draggingTicket) {
      setTicketDropHighlight(false);
      ticketDragCounterRef.current = 0;
    }
  }, [draggingTicket]);

  function isLeavingColumn(e: React.DragEvent): boolean {
    const related = e.relatedTarget;
    return !(related instanceof Node && e.currentTarget.contains(related));
  }

  function allowTicketDrop(e: React.DragEvent) {
    if (!acceptsTicketDrop) return;
    if (!Ticket.isTicketStageDrag(e.dataTransfer, draggingTicketRef.current?.id)) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }

  function enterDropZone(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    if (!Ticket.isTicketStageDrag(e.dataTransfer, draggingTicketRef.current?.id)) return;
    e.preventDefault();
    ticketDragCounterRef.current++;
    setTicketDropHighlight(true);
  }

  function leaveDropZone(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    ticketDragCounterRef.current--;
    if (ticketDragCounterRef.current <= 0) {
      ticketDragCounterRef.current = 0;
      setTicketDropHighlight(false);
    }
  }

  function commitTicketDrop(e: React.DragEvent) {
    if (!acceptsTicketDrop || !onTicketDrop) return;
    e.preventDefault();
    e.stopPropagation();
    ticketDragCounterRef.current = 0;
    setTicketDropHighlight(false);
    const ticketId =
      Ticket.readTicketIdFromDataTransfer(e.dataTransfer) ||
      draggingTicketRef.current?.id;
    if (!ticketId) return;
    onTicketDrop(ticketId, columnStage, 'stage_done');
  }

  const dropZoneHandlers = acceptsTicketDrop
    ? {
        onDragOver: allowTicketDrop,
        onDragEnter: enterDropZone,
        onDragLeave: leaveDropZone,
        onDrop: commitTicketDrop,
      }
    : {};

  const hasTickets = doneTickets.length + feedsNextTickets.length > 0;
  return (
    <div
      className={
        'kb-sub-col kb-sub-col--done' + (ticketDropHighlight ? ' kb-sub-col--drop-target' : '')
      }
      {...dropZoneHandlers}
    >
      <div className="kb-sub-col-head">
        <span>Done</span>
        {hasTickets ? (
          <span className="kb-col-count">{doneTickets.length + feedsNextTickets.length}</span>
        ) : null}
      </div>
      <div
        className={
          'kb-sub-col-tickets' + (ticketDropHighlight ? ' kb-sub-col-tickets--drop-target' : '')
        }
      >
        {doneTickets.length > 0 && (
          <div className="kb-done-section">
            <div className="kb-done-section-label">
              Complete
              <span className="kb-col-count">{doneTickets.length}</span>
            </div>
            {doneTickets.map((t) => (
              <TicketView
                key={t.ticketId}
                ticket={t}
                stageSkills={t.stageSkillsForColumn(columnStage, skillsByStage)}
                stageSubColumn="done"
                activeStagePeers={[]}
                team={team}
                boardMode={boardMode}
                onResumeTicket={onResumeTicket}
                onTicketDragStart={onTicketDragStart}
                onTicketDragEnd={onTicketDragEnd}
                draggingTicketRef={draggingTicketRef}
                isDraggingSource={draggingTicketId === t.ticketId}
                stageMoveDragActive={!!draggingTicket}
              />
            ))}
          </div>
        )}
        {feedsNextTickets.length > 0 && (
          <div className="kb-done-section kb-done-section--queued">
            <div className="kb-done-section-label">
              Queued
              <span className="kb-col-count">{feedsNextTickets.length}</span>
            </div>
            {feedsNextTickets.map((t) => {
              const targetSkills = t.stage ? skillsByStage.get(t.stage) ?? [] : [];
              return (
                <TicketView
                  key={t.ticketId}
                  ticket={t}
                  stageSkills={targetSkills}
                  stageSubColumn="feeds-next"
                  activeStagePeers={t.stage ? peersByTargetStage.get(t.stage) ?? [] : []}
                  team={team}
                  boardMode={boardMode}
                  onTicketDragStart={onTicketDragStart}
                  onTicketDragEnd={onTicketDragEnd}
                  draggingTicketRef={draggingTicketRef}
                  isDraggingSource={draggingTicketId === t.ticketId}
                  stageMoveDragActive={!!draggingTicket}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

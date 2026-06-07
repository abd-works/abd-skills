import { useState, useRef, useEffect, type MutableRefObject } from 'react';
import { TicketView } from './TicketView';
import { Ticket } from '@deliveryforge/kanban-client';
import type { BoardMode, StageId, StageSkill, StageSubColumn, KanbanBoardSnapshot } from '@deliveryforge/kanban-shared';
import type { TicketDragPayload, TicketStageDropHandler } from '@deliveryforge/kanban-client';

export function StageInProgressView({
  label,
  subColId,
  tickets,
  stageSkills = [],
  activeStagePeers = [],
  team,
  boardMode,
  onResumeTicket,
  columnStage,
  draggingTicketRef,
  draggingTicketId,
  draggingTicket,
  onTicketDrop,
  onTicketDragStart,
  onTicketDragEnd,
}: {
  label: string;
  subColId: StageSubColumn;
  tickets: Ticket[];
  stageSkills?: StageSkill[];
  activeStagePeers?: Ticket[];
  team?: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: 'in_progress' | 'stage_done') => void;
  columnStage: StageId;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  draggingTicketId?: string | null;
  draggingTicket?: TicketDragPayload | null;
  onTicketDrop?: TicketStageDropHandler;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
}) {
  const [ticketDropHighlight, setTicketDropHighlight] = useState(false);
  const [dropRejectMsg, setDropRejectMsg] = useState<string | null>(null);
  const ticketDragCounterRef = useRef(0);
  const isManual = boardMode === 'manual';
  const acceptsTicketDrop = isManual && subColId === 'ip' && !!onTicketDrop;

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
    setDropRejectMsg(null);
    ticketDragCounterRef.current++;
    setTicketDropHighlight(true);
  }

  function leaveDropZone(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    ticketDragCounterRef.current--;
    if (ticketDragCounterRef.current <= 0) {
      ticketDragCounterRef.current = 0;
      setTicketDropHighlight(false);
      setDropRejectMsg(null);
    }
  }

  function commitTicketDrop(e: React.DragEvent) {
    if (!acceptsTicketDrop || !onTicketDrop) return;
    e.preventDefault();
    e.stopPropagation();
    ticketDragCounterRef.current = 0;
    setTicketDropHighlight(false);
    setDropRejectMsg(null);
    const ticketId =
      Ticket.readTicketIdFromDataTransfer(e.dataTransfer) ||
      draggingTicketRef.current?.id;
    if (!ticketId) return;
    onTicketDrop(ticketId, columnStage, 'in_progress');
  }

  const dropZoneHandlers = acceptsTicketDrop
    ? {
        onDragOver: allowTicketDrop,
        onDragEnter: enterDropZone,
        onDragLeave: leaveDropZone,
        onDrop: commitTicketDrop,
      }
    : {};

  return (
    <div
      className={
        'kb-sub-col kb-sub-col--' +
        subColId +
        (ticketDropHighlight && subColId === 'ip' ? ' kb-sub-col--drop-target' : '')
      }
      {...dropZoneHandlers}
    >
      <div className="kb-sub-col-head">
        <span>{label}</span>
        {tickets.length > 0 ? <span className="kb-col-count">{tickets.length}</span> : null}
      </div>
      {dropRejectMsg && subColId === 'ip' ? (
        <div className="kb-sub-col-drop-hint">{dropRejectMsg}</div>
      ) : null}
      <div
        className={
          'kb-sub-col-tickets' + (ticketDropHighlight ? ' kb-sub-col-tickets--drop-target' : '')
        }
      >
        {tickets.map((t) => (
          <TicketView
            key={t.ticketId}
            ticket={t}
            stageSkills={stageSkills}
            stageSubColumn={subColId}
            activeStagePeers={activeStagePeers}
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
    </div>
  );
}

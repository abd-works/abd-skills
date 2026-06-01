import { useCallback, useEffect, useMemo, useRef, useState, type MutableRefObject } from 'react';
import { useFlipTicketAnimations } from './useFlipTicketAnimations';
import { LiveSkillIcon } from './LiveSkillIcon';
import {
  toggleBoardMode,
  postActionIntent,
  postMoveTicketToStage,
  type MoveTicketPlacement,
} from './deliveryBoard.api';
import type { TicketDragPayload, TicketStageDropHandler } from './ticketStageDrag';
import type {
  AgentRole,
  BoardMode,
  KanbanBoardSnapshot,
  KanbanColumnView,
  TicketView,
  StageId,
  StageSkill,
} from '@deliveryforge/delivery-board-shared';
import {
  AGENT_ROLES,
  STAGE_LABELS,
  STAGE_ORDER,
  familyCssClass,
  skillFamilyFor,
  buildStageBuckets,
  buildGlobalBacklogTickets,
  buildArchivedColumnTickets,
  ticketsAtStage,
  ticketCanExpand,
  resolveFocusSkillId,
  resolveDisplayFocusSkillId,
  countRoleEngagement,
  resolvePoolAvatarState,
  HEARTBEAT_STALE_SECS,
  HEARTBEAT_STALE_LEAD_SECS,
  skillRowDisplayState,
  ticketShowsLiveSkillIcon,
  isScatterParent,
  isStageSkillsComplete,
  scopeLevelCssClass,
  stageSkillsForTicket,
  type StageBucket,
  type StageSubColumn,
  type SkillRowDisplayState,
} from '@deliveryforge/delivery-board-shared';

// ---- Icons ----

function ChatbotIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--bot ' + colorClass}
      viewBox="0 0 20 20"
      width="13"
      height="13"
      aria-label="In progress"
    >
      <rect x="2" y="4" width="16" height="11" rx="2.5" fill="currentColor" fillOpacity="0.2" stroke="currentColor" strokeWidth="1.5" />
      <path d="M5 15 L4 18 L8 15" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
      <line x1="10" y1="4" x2="10" y2="2" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <circle cx="10" cy="1.5" r="0.9" fill="currentColor" />
      <circle cx="7" cy="9" r="1.2" fill="currentColor" />
      <circle cx="13" cy="9" r="1.2" fill="currentColor" />
      <path d="M7.5 12 Q10 13.5 12.5 12" stroke="currentColor" strokeWidth="1" fill="none" strokeLinecap="round" />
    </svg>
  );
}

function MagnifyIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--review ' + colorClass}
      viewBox="0 0 20 20"
      width="13"
      height="13"
      aria-label="In review"
    >
      <circle cx="8" cy="8" r="5" fill="none" stroke="currentColor" strokeWidth="1.6" />
      <line x1="12" y1="12" x2="17" y2="17" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

function DoneIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--done ' + colorClass}
      viewBox="0 0 14 14"
      width="11"
      height="11"
      aria-label="Done"
    >
      <polyline points="2,7 5.5,11 12,3" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function ReworkIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--rework ' + colorClass}
      viewBox="0 0 16 16"
      width="14"
      height="14"
      aria-label="Rework needed"
    >
      <path d="M2 8a6 6 0 0 1 10.3-4.2l-1.8 1.8H15V1.1l-1.7 1.7A8 8 0 0 0 0 8h2zm12 0a6 6 0 0 1-10.3 4.2l1.8-1.8H1v4.5l1.7-1.7A8 8 0 0 0 16 8h-2z" fill="currentColor" />
    </svg>
  );
}

function PendingIntentIcon({ colorClass }: { colorClass: string }) {
  return (
    <svg
      className={'kb-skill-icon kb-skill-icon--pending-intent ' + colorClass}
      viewBox="0 0 16 16"
      width="13"
      height="13"
      aria-label="Intent queued"
    >
      <path d="M8 14V4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      <path d="M4 7l4-4 4 4" stroke="currentColor" strokeWidth="1.8" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <line x1="3" y1="2" x2="13" y2="2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

// ---- Ticket stage drag (manual cross-column moves) ----

const TICKET_DRAG_ID = 'application/ticket-id';
const TICKET_DRAG_STAGE = 'application/ticket-stage';

function isActiveTicketDrag(
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>,
): boolean {
  return draggingTicketRef.current !== null;
}

function isTicketStageDrag(
  dt: DataTransfer,
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>,
): boolean {
  if (isActiveTicketDrag(draggingTicketRef)) return true;
  return Array.from(dt.types).some((t) => t === TICKET_DRAG_ID || t === 'text/plain');
}

function readTicketIdFromDataTransfer(
  dt: DataTransfer,
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>,
): string {
  const id = dt.getData(TICKET_DRAG_ID);
  if (id) return id;
  const plain = dt.getData('text/plain');
  if (plain.startsWith('ticket:')) return plain.slice('ticket:'.length);
  return draggingTicketRef.current?.id ?? '';
}

// ---- Ticket card ----

function ticketStatusClass(ticket: TicketView): string {
  if (isScatterParent(ticket)) return 'kb-ticket--scatter-parent';
  if (ticket.notes.toLowerCase().includes('blocked')) return 'kb-ticket--blocked';
  return '';
}

function TicketCard({
  ticket,
  stageSkills = [],
  stageSubColumn,
  activeStagePeers = [],
  team,
  boardMode = 'automatic',
  planningRoot,
  onTicketDragStart,
  onTicketDragEnd,
  draggingTicketRef,
  isDraggingSource = false,
  stageMoveDragActive = false,
}: {
  ticket: TicketView;
  stageSkills?: StageSkill[];
  stageSubColumn?: StageSubColumn;
  activeStagePeers?: TicketView[];
  team?: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  planningRoot?: string;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: MoveTicketPlacement) => void;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  isDraggingSource?: boolean;
  /** Another ticket is being dragged for cross-stage move — disable agent drop on this card. */
  stageMoveDragActive?: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const [dropHighlight, setDropHighlight] = useState(false);
  const [pendingAssignment, setPendingAssignment] = useState(false);
  const [rejectionMsg, setRejectionMsg] = useState<string | null>(null);
  const dragCounterRef = useRef(0);

  const isReviewing = ticket.isReviewing;

  const stageSkillIds = stageSkills.map((s) => s.skillId);
  const focusSkillId =
    team && stageSkills.length > 0
      ? resolveDisplayFocusSkillId(
          ticket,
          stageSkills,
          stageSubColumn,
          activeStagePeers,
          team,
        )
      : resolveFocusSkillId(ticket, stageSkillIds, stageSubColumn);
  const primaryFamClass = focusSkillId ? familyCssClass(skillFamilyFor(focusSkillId)) : null;
  const showLiveSkillIcon = ticketShowsLiveSkillIcon(ticket, focusSkillId, stageSubColumn);

  const canExpand = ticketCanExpand(ticket, stageSkillIds, stageSubColumn);

  const isManual = boardMode === 'manual';
  const isDraggableForStageMove =
    isManual &&
    (stageSubColumn === 'ip' ||
      stageSubColumn === 'done' ||
      stageSubColumn === 'feeds-next');

  function findNextEligibleSkill(agentRole?: string): string | null {
    const doneSet = new Set(ticket.doneSkillIds);
    const pendingSet = new Set(ticket.pendingIntentSkillIds ?? []);
    const executingSet = new Set(ticket.executingSkillIds ?? []);
    for (const s of stageSkills) {
      if (agentRole && s.role !== agentRole) continue;
      if (doneSet.has(s.skillId)) continue;
      if (executingSet.has(s.skillId)) continue;
      if ((ticket.reviewingSkillIds ?? []).includes(s.skillId)) continue;
      if (ticket.reviewSkillId === s.skillId) continue;
      if (pendingSet.has(s.skillId)) continue;
      return s.skillId;
    }
    return null;
  }

  function handleDragOver(e: React.DragEvent) {
    if (!isManual) return;
    if (isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  }

  function handleDragEnter(e: React.DragEvent) {
    if (!isManual) return;
    if (isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    dragCounterRef.current++;
    setDropHighlight(true);
  }

  function handleDragLeave() {
    if (!isManual) return;
    dragCounterRef.current--;
    if (dragCounterRef.current <= 0) {
      dragCounterRef.current = 0;
      setDropHighlight(false);
    }
  }

  function handleDrop(e: React.DragEvent) {
    if (!isManual) return;
    if (
      isTicketStageDrag(e.dataTransfer, draggingTicketRef) ||
      readTicketIdFromDataTransfer(e.dataTransfer, draggingTicketRef)
    ) {
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current = 0;
    setDropHighlight(false);

    const agentRole = e.dataTransfer.getData('application/agent-role');
    if (!agentRole) {
      setRejectionMsg('Drop failed — no agent role');
      setTimeout(() => setRejectionMsg(null), 3000);
      return;
    }

    const skillId = findNextEligibleSkill(agentRole);
    if (skillId && planningRoot) {
      setPendingAssignment(true);
      void postActionIntent(planningRoot, ticket.ticketId, skillId, agentRole)
        .then((payload) => {
          if (payload.lead_scan?.must_spawn) {
            setRejectionMsg(
              'Delegated on board — start or resume Kanban Lead agent to spawn executors (ticks alone do not spawn).',
            );
            setTimeout(() => setRejectionMsg(null), 8000);
          }
        })
        .catch(() => {
          setRejectionMsg('API error — intent not saved');
          setTimeout(() => setRejectionMsg(null), 3000);
        });
      setTimeout(() => setPendingAssignment(false), 2500);
    } else {
      setRejectionMsg(skillId ? 'Missing planning root' : 'No eligible skills remain');
      setTimeout(() => setRejectionMsg(null), 3000);
    }
  }

  const isInProgressActive =
    stageSubColumn === 'ip' &&
    ((ticket.executingSkillIds?.length ?? 0) > 0 ||
      ticket.activeSkillId !== null ||
      (ticket.reviewingSkillIds?.length ?? 0) > 0 ||
      ticket.reviewSkillId !== null);

  function handleTicketDragStart(e: React.DragEvent) {
    if (!isDraggableForStageMove) return;
    const stage = ticket.stage;
    if (!stage) return;
    e.stopPropagation();
    e.dataTransfer.setData(TICKET_DRAG_ID, ticket.ticketId);
    e.dataTransfer.setData(TICKET_DRAG_STAGE, stage);
    e.dataTransfer.setData('text/plain', `ticket:${ticket.ticketId}`);
    e.dataTransfer.effectAllowed = 'move';
    onTicketDragStart?.(ticket.ticketId, stage);
  }

  function handleTicketDragEnd() {
    onTicketDragEnd?.();
  }

  return (
    <div
      className={
        'kb-ticket ' +
        scopeLevelCssClass(ticket.scopeLevel) +
        ' ' +
        ticketStatusClass(ticket) +
        (stageSubColumn === 'feeds-next' ? ' kb-ticket--feeds-next' : '') +
        (dropHighlight ? ' kb-ticket--drop-target' : '') +
        (pendingAssignment ? ' kb-ticket--pending-assignment' : '') +
        (isInProgressActive ? ' kb-ticket--in-progress-active' : '') +
        (isDraggableForStageMove ? ' kb-ticket--draggable-ticket' : '') +
        (isDraggingSource ? ' kb-ticket--stage-drag-source' : '')
      }
      data-ticket={ticket.ticketId}
      data-scope={ticket.scopeLevel}
      title={
        isDraggableForStageMove
          ? ticket.lineage.join(' > ') +
            ' — drag to another stage (In Progress or Done) to move or skip ahead'
          : ticket.lineage.join(' > ')
      }
      draggable={isDraggableForStageMove}
      onDragStart={isDraggableForStageMove ? handleTicketDragStart : undefined}
      onDragEnd={isDraggableForStageMove ? handleTicketDragEnd : undefined}
      onDragOver={isManual && !stageMoveDragActive ? handleDragOver : undefined}
      onDragEnter={isManual && !stageMoveDragActive ? handleDragEnter : undefined}
      onDragLeave={isManual && !stageMoveDragActive ? handleDragLeave : undefined}
      onDrop={isManual && !stageMoveDragActive ? handleDrop : undefined}
    >
      {rejectionMsg && <div className="kb-drop-rejection">{rejectionMsg}</div>}
      <div className="kb-ticket-chip">
        {ticket.chipLabel}
        {isReviewing && (
          <span className="kb-status-dot kb-status-dot--review" title="In review" />
        )}
        {canExpand && (
          <button
            type="button"
            className="kb-ticket-expand-btn"
            draggable={false}
            onMouseDown={(ev) => ev.stopPropagation()}
            onClick={() => setExpanded((e) => !e)}
            aria-label={expanded ? 'Collapse skills' : 'Expand skills'}
            title={expanded ? 'Collapse skills' : 'Show skill progress'}
          >
            {expanded ? '\u2212' : '+'}
          </button>
        )}
      </div>
      <div className="kb-ticket-label">{ticket.displayLabel}</div>
      {stageSubColumn === 'ip' ? (
        <div className="kb-ticket-meta">
          <LiveSkillIcon
            visible={showLiveSkillIcon}
            mode={
              isReviewing || (ticket.awaitingReviewSkillId !== null && !ticket.activeSkillId)
                ? 'magnify'
                : 'bot'
            }
            BotIcon={ChatbotIcon}
            MagnifyIcon={MagnifyIcon}
            colorClass={primaryFamClass ?? ''}
          />
        </div>
      ) : null}
      {expanded && canExpand && (
        <div className="kb-ticket-skills-expand">
          {stageSkills.map((s) => {
            const row = skillRowDisplayState(s.skillId, ticket, focusSkillId);
            const fc = familyCssClass(s.family);
            return (
              <div
                key={s.skillId}
                className={[
                  'kb-ticket-skill-row',
                  fc,
                  row.isDone ? 'is-done' : '',
                  row.isExecuting || row.isUnderReview || row.isFocus ? 'is-active' : '',
                  !row.isDone && !row.isExecuting && !row.isUnderReview && !row.isFocus
                    ? 'is-pending'
                    : '',
                ].filter(Boolean).join(' ')}
              >
                <span className="kb-ticket-skill-label">{s.label}</span>
                <span className="kb-ticket-skill-icons">
                  {row.showRework && <ReworkIcon colorClass={fc} />}
                  {row.isDone && !row.showRework && <DoneIcon colorClass={fc} />}
                  {row.showPendingIntent && <PendingIntentIcon colorClass={fc} />}
                  {row.showBot && (
                    <span className="kb-live-skill-icon kb-live-skill-icon--working kb-live-skill-icon--inline">
                      <ChatbotIcon colorClass={fc} />
                    </span>
                  )}
                  {row.showMagnify && <MagnifyIcon colorClass={fc} />}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ---- Sub-column ----

function SubColumn({
  label,
  subColId,
  tickets,
  stageSkills = [],
  activeStagePeers = [],
  team,
  boardMode,
  planningRoot,
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
  tickets: TicketView[];
  stageSkills?: StageSkill[];
  activeStagePeers?: TicketView[];
  team?: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  planningRoot?: string;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: MoveTicketPlacement) => void;
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

  function handleTicketDragOver(e: React.DragEvent) {
    if (!acceptsTicketDrop) return;
    if (!isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }

  function handleTicketDragEnter(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    if (!isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    setDropRejectMsg(null);
    ticketDragCounterRef.current++;
    setTicketDropHighlight(true);
  }

  function handleTicketDragLeave(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    ticketDragCounterRef.current--;
    if (ticketDragCounterRef.current <= 0) {
      ticketDragCounterRef.current = 0;
      setTicketDropHighlight(false);
      setDropRejectMsg(null);
    }
  }

  function handleTicketDrop(e: React.DragEvent) {
    if (!acceptsTicketDrop || !onTicketDrop) return;
    e.preventDefault();
    e.stopPropagation();
    ticketDragCounterRef.current = 0;
    setTicketDropHighlight(false);
    setDropRejectMsg(null);
    const ticketId =
      readTicketIdFromDataTransfer(e.dataTransfer, draggingTicketRef) ||
      draggingTicketRef.current?.id;
    if (!ticketId) return;
    onTicketDrop(ticketId, columnStage, 'in_progress');
  }

  const dropZoneHandlers = acceptsTicketDrop
    ? {
        onDragOver: handleTicketDragOver,
        onDragEnter: handleTicketDragEnter,
        onDragLeave: handleTicketDragLeave,
        onDrop: handleTicketDrop,
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
          <TicketCard
            key={t.ticketId}
            ticket={t}
            stageSkills={stageSkills}
            stageSubColumn={subColId}
            activeStagePeers={activeStagePeers}
            team={team}
            boardMode={boardMode}
            planningRoot={planningRoot}
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

// ---- Done sub-column (stage complete + next-stage backlog) ----

function DoneSubColumn({
  columnStage,
  doneTickets,
  feedsNextTickets,
  stageSkills,
  skillsByStage,
  peersByTargetStage,
  team,
  boardMode,
  planningRoot,
  onResumeTicket,
  onTicketDragStart,
  onTicketDragEnd,
  draggingTicketRef,
  draggingTicketId,
  draggingTicket,
  onTicketDrop,
}: {
  columnStage: StageId;
  doneTickets: TicketView[];
  feedsNextTickets: TicketView[];
  stageSkills: StageSkill[];
  skillsByStage: Map<StageId, StageSkill[]>;
  peersByTargetStage: Map<StageId, TicketView[]>;
  team: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  planningRoot?: string;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: MoveTicketPlacement) => void;
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

  function handleTicketDragOver(e: React.DragEvent) {
    if (!acceptsTicketDrop) return;
    if (!isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }

  function handleTicketDragEnter(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    if (!isTicketStageDrag(e.dataTransfer, draggingTicketRef)) return;
    e.preventDefault();
    ticketDragCounterRef.current++;
    setTicketDropHighlight(true);
  }

  function handleTicketDragLeave(e: React.DragEvent) {
    if (!acceptsTicketDrop || !isLeavingColumn(e)) return;
    ticketDragCounterRef.current--;
    if (ticketDragCounterRef.current <= 0) {
      ticketDragCounterRef.current = 0;
      setTicketDropHighlight(false);
    }
  }

  function handleTicketDrop(e: React.DragEvent) {
    if (!acceptsTicketDrop || !onTicketDrop) return;
    e.preventDefault();
    e.stopPropagation();
    ticketDragCounterRef.current = 0;
    setTicketDropHighlight(false);
    const ticketId =
      readTicketIdFromDataTransfer(e.dataTransfer, draggingTicketRef) ||
      draggingTicketRef.current?.id;
    if (!ticketId) return;
    onTicketDrop(ticketId, columnStage, 'stage_done');
  }

  const dropZoneHandlers = acceptsTicketDrop
    ? {
        onDragOver: handleTicketDragOver,
        onDragEnter: handleTicketDragEnter,
        onDragLeave: handleTicketDragLeave,
        onDrop: handleTicketDrop,
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
              <TicketCard
                key={t.ticketId}
                ticket={t}
                stageSkills={stageSkillsForTicket(t, columnStage, skillsByStage)}
                stageSubColumn="done"
                activeStagePeers={[]}
                team={team}
                boardMode={boardMode}
                planningRoot={planningRoot}
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
                <TicketCard
                  key={t.ticketId}
                  ticket={t}
                  stageSkills={targetSkills}
                  stageSubColumn="feeds-next"
                  activeStagePeers={t.stage ? peersByTargetStage.get(t.stage) ?? [] : []}
                  team={team}
                  boardMode={boardMode}
                  planningRoot={planningRoot}
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

// ---- Stage group ----

function StageGroup({
  stage,
  bucket,
  skills,
  skillsByStage,
  peersByTargetStage,
  team,
  boardMode,
  planningRoot,
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
  peersByTargetStage: Map<StageId, TicketView[]>;
  team: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  planningRoot?: string;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: MoveTicketPlacement) => void;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  draggingTicketId?: string | null;
  draggingTicket?: TicketDragPayload | null;
  onTicketDrop?: TicketStageDropHandler;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
}) {
  const hasWork = bucket.ip.length + bucket.done.length + bucket.feedsNext.length > 0;
  return (
    <div
      className={'kb-stage-group ' + (hasWork ? 'kb-stage-group--active' : '')}
      data-stage={stage}
    >
      <div className="kb-stage-group-header">
        {STAGE_LABELS[stage]}
      </div>
      <div className="kb-stage-sub-cols">
        <SubColumn
          label="In Progress"
          subColId="ip"
          tickets={bucket.ip}
          stageSkills={skills}
          activeStagePeers={peersByTargetStage.get(stage) ?? []}
          team={team}
          boardMode={boardMode}
          planningRoot={planningRoot}
          onResumeTicket={onResumeTicket}
          columnStage={stage}
          draggingTicketRef={draggingTicketRef}
          draggingTicketId={draggingTicketId}
          draggingTicket={draggingTicket}
          onTicketDrop={onTicketDrop}
          onTicketDragStart={onTicketDragStart}
          onTicketDragEnd={onTicketDragEnd}
        />
        <DoneSubColumn
          columnStage={stage}
          doneTickets={bucket.done}
          feedsNextTickets={bucket.feedsNext}
          stageSkills={skills}
          skillsByStage={skillsByStage}
          peersByTargetStage={peersByTargetStage}
          team={team}
          boardMode={boardMode}
          planningRoot={planningRoot}
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
          {skills.map((sk) => (
            <span key={sk.skillId} className={'kb-skill-chip ' + familyCssClass(skillFamilyFor(sk.skillId))}>
              {sk.label}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

// ---- End columns ----

function EndColumn({
  heading,
  colId,
  tickets,
  skillsByStage,
  boardMode,
  planningRoot,
  draggingTicketRef,
}: {
  heading: string;
  colId: string;
  tickets: TicketView[];
  skillsByStage?: Map<StageId, StageSkill[]>;
  boardMode?: BoardMode;
  planningRoot?: string;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
}) {
  return (
    <div className="kb-end-col" data-col={colId}>
      <div className="kb-end-col-header">{heading}</div>
      <div className="kb-end-col-tickets">
        {tickets.map((t) => {
          const skills = t.stage && skillsByStage ? skillsByStage.get(t.stage) ?? [] : [];
          return (
            <TicketCard
              key={t.ticketId}
              ticket={t}
              stageSkills={skills}
              boardMode={boardMode}
              planningRoot={planningRoot}
              draggingTicketRef={draggingTicketRef}
            />
          );
        })}
      </div>
    </div>
  );
}

// ---- Agent pool ----

const ROLE_LABELS: Record<AgentRole, string> = {
  'product-owner': 'PO',
  'business-expert': 'BE',
  'ux-designer': 'UX',
  engineer: 'ENG',
};

const ROLE_FULL: Record<AgentRole, string> = {
  'product-owner': 'Product Owner',
  'business-expert': 'Business Expert',
  'ux-designer': 'UX Designer',
  engineer: 'Engineer',
};

function formatAge(seconds: number | null): string {
  if (seconds === null) return '';
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m ago`;
}

function AgentAvatar({
  role,
  state,
  index,
  note,
  ageSeconds,
  size = 'md',
  boardMode,
}: {
  role: AgentRole | 'kanban-lead';
  state: 'idle' | 'working' | 'inactive';
  index: number;
  note?: string | null;
  ageSeconds?: number | null;
  size?: 'sm' | 'md';
  boardMode?: BoardMode;
}) {
  const label = role === 'kanban-lead' ? 'KL' : ROLE_LABELS[role as AgentRole];
  const fullName = role === 'kanban-lead' ? 'Kanban Lead' : ROLE_FULL[role as AgentRole];
  const stateLabel = state === 'inactive' ? 'no thread' : state;
  const agePart = ageSeconds != null ? ` (${formatAge(ageSeconds)})` : '';
  const notePart = note ? `\n${note}` : '';
  const tip = fullName + (role !== 'kanban-lead' ? ' #' + (index + 1) : '') + ' \u2014 ' + stateLabel + agePart + notePart;
  const isDraggable = boardMode === 'manual' && role !== 'kanban-lead';

  function handleDragStart(e: React.DragEvent) {
    e.dataTransfer.setData('application/agent-role', role);
    e.dataTransfer.effectAllowed = 'copy';
  }

  return (
    <div
      className={
        'kb-agent-avatar kb-agent-avatar--' + size + ' kb-agent-avatar--' + state +
        (isDraggable ? ' kb-agent-avatar--draggable' : '')
      }
      data-role={role}
      title={tip}
      draggable={isDraggable}
      onDragStart={isDraggable ? handleDragStart : undefined}
    >
      <span className="kb-agent-initial">{label}</span>
    </div>
  );
}

async function postTeamAdjust(
  planningRoot: string,
  role: AgentRole,
  delta: number,
): Promise<KanbanBoardSnapshot | null> {
  const res = await fetch('/api/board/team', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ planningRoot, role, delta }),
  });
  if (!res.ok) return null;
  return res.json() as Promise<KanbanBoardSnapshot>;
}

function AgentPoolGroup({
  role,
  total,
  engagedCount,
  slotHeartbeats,
  spawnNeeded,
  planningRoot,
  onUpdate,
  boardMode,
}: {
  role: AgentRole;
  total: number;
  engagedCount: number;
  slotHeartbeats: Array<{ ageSeconds: number | null; status: string | null; note?: string | null }>;
  spawnNeeded?: number;
  planningRoot: string;
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  boardMode?: BoardMode;
}) {
  async function adjust(delta: number) {
    const next = await postTeamAdjust(planningRoot, role, delta);
    if (next) onUpdate?.(next);
  }

  const slots = Math.max(total, 1);

  return (
    <div className="kb-pool-group" data-role={role}>
      <div className="kb-pool-group-label">
        {ROLE_FULL[role]}
        {spawnNeeded ? <span className="kb-spawn-badge" title={`${spawnNeeded} agent(s) need spawning`}>{spawnNeeded}</span> : null}
      </div>
      <div className="kb-pool-group-row">
        {Array.from({ length: slots }, (_, i) => {
          const slot = slotHeartbeats[i];
          const st =
            total === 0
              ? 'inactive'
              : resolvePoolAvatarState(
                  i,
                  engagedCount,
                  slot?.ageSeconds ?? null,
                  HEARTBEAT_STALE_SECS,
                  slot?.status ?? null,
                );
          return (
            <AgentAvatar
              key={i}
              role={role}
              state={st}
              index={i}
              note={slot?.note}
              ageSeconds={slot?.ageSeconds}
              size="sm"
              boardMode={boardMode}
            />
          );
        })}
        <div className="kb-pool-controls">
          <button className="kb-pool-btn" onClick={() => void adjust(1)} title={'Add ' + ROLE_FULL[role]}>+</button>
          <button className="kb-pool-btn" onClick={() => void adjust(-1)} title={'Remove ' + ROLE_FULL[role]} disabled={total === 0}>&minus;</button>
        </div>
      </div>
    </div>
  );
}

function AgentPoolBar({
  team,
  columnViews,
  stageSkillRails,
  heartbeats,
  heartbeatSlots,
  planningRoot,
  onUpdate,
  boardMode,
}: {
  team: KanbanBoardSnapshot['team'];
  columnViews: KanbanBoardSnapshot['columnViews'];
  stageSkillRails: KanbanBoardSnapshot['stageSkillRails'];
  heartbeats: KanbanBoardSnapshot['heartbeats'];
  heartbeatSlots: KanbanBoardSnapshot['heartbeatSlots'];
  planningRoot: string;
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  boardMode?: BoardMode;
}) {
  const engagedCounts = useMemo(
    () => countRoleEngagement(columnViews, stageSkillRails, team!),
    [columnViews, stageSkillRails, team],
  );

  const klSlot = heartbeatSlots?.['kanban-lead']?.[0];
  const klAge = klSlot?.ageSeconds ?? heartbeats?.['kanban-lead'] ?? null;
  const klStatus = klSlot?.status ?? null;
  const klNote = klSlot?.note ?? null;
  const klState = resolvePoolAvatarState(0, 0, klAge, HEARTBEAT_STALE_LEAD_SECS, klStatus);
  const [klScanning, setKlScanning] = useState(false);
  const [lastScanResult, setLastScanResult] = useState<{ spawns?: Array<{ role: string; instance: number }>; actions?: string[] } | null>(null);

  async function wakeLeadScan() {
    if (klScanning) return;
    setKlScanning(true);
    try {
      const res = await fetch('/api/board/lead-scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ planningRoot }),
      });
      if (res.ok) {
        const result = await res.json();
        setLastScanResult(result);
      }
    } finally {
      setKlScanning(false);
    }
  }

  const spawnsByRole: Partial<Record<AgentRole, number>> = {};
  if (lastScanResult?.spawns) {
    for (const s of lastScanResult.spawns) {
      const r = s.role as AgentRole;
      spawnsByRole[r] = (spawnsByRole[r] ?? 0) + 1;
    }
  }

  return (
    <div className="kb-pool-bar">
      <div className="kb-pool-group kb-pool-group--lead" data-role="kanban-lead">
        <div className="kb-pool-group-label">Kanban Lead</div>
        <div className="kb-pool-group-row">
          <div
            className={'kb-lead-wake' + (klScanning ? ' kb-lead-wake--scanning' : '')}
            onClick={() => void wakeLeadScan()}
            title={klState === 'inactive' ? 'Click to wake lead scan' : undefined}
            style={{ cursor: klState === 'inactive' || klState === 'idle' ? 'pointer' : 'default' }}
          >
            <AgentAvatar
              role="kanban-lead"
              state={klScanning ? 'working' : klState}
              index={0}
              note={klScanning ? 'Running scan...' : klNote}
              ageSeconds={klScanning ? null : klAge}
              size="sm"
            />
          </div>
        </div>
      </div>

      <div className="kb-pool-divider" />
      <span className="kb-pool-bar-label">Agent Pool</span>

      {AGENT_ROLES.map((role) => {
        const pairCount = team[role] ?? 1;
        return (
          <AgentPoolGroup
            key={role}
            role={role}
            total={pairCount}
            engagedCount={engagedCounts[role]}
            slotHeartbeats={heartbeatSlots?.[role] ?? []}
            spawnNeeded={spawnsByRole[role]}
            planningRoot={planningRoot}
            onUpdate={onUpdate}
            boardMode={boardMode}
          />
        );
      })}
    </div>
  );
}

// ---- Board ----

export interface DeliveryKanbanBoardProps {
  snapshot: KanbanBoardSnapshot;
  onTeamUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  onModeToggle?: (snapshot: KanbanBoardSnapshot) => void;
}

export function DeliveryKanbanBoard({
  snapshot,
  onTeamUpdate,
  onModeToggle,
}: DeliveryKanbanBoardProps) {
  const boardScrollRef = useRef<HTMLDivElement>(null);
  const draggingTicketRef = useRef<TicketDragPayload | null>(null);
  const ticketDropCommittedRef = useRef(false);
  const [draggingTicket, setDraggingTicket] = useState<TicketDragPayload | null>(null);
  /** Applied one frame after dragstart so pointer-events:none does not cancel the drag. */
  const [ticketDragPassThrough, setTicketDragPassThrough] = useState(false);
  const snapshotKey = snapshot.etag + ':' + snapshot.polledAt;
  useFlipTicketAnimations(boardScrollRef, snapshotKey);

  const boardMode: BoardMode = snapshot.board_mode ?? 'automatic';

  const handleMoveTicket = useCallback(
    async (
      ticketId: string,
      targetStage: StageId,
      placement: MoveTicketPlacement = 'in_progress',
    ) => {
      try {
        const next = await postMoveTicketToStage(
          snapshot.planningRoot,
          ticketId,
          targetStage,
          placement,
        );
        onTeamUpdate?.(next);
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Move failed';
        window.alert(msg);
      }
    },
    [snapshot.planningRoot, onTeamUpdate],
  );

  const handleTicketDragStart = useCallback((ticketId: string, stage: StageId) => {
    const payload = { id: ticketId, stage };
    draggingTicketRef.current = payload;
    ticketDropCommittedRef.current = false;
    setDraggingTicket(payload);
    requestAnimationFrame(() => setTicketDragPassThrough(true));
  }, []);

  const endTicketDrag = useCallback(() => {
    draggingTicketRef.current = null;
    setDraggingTicket(null);
    setTicketDragPassThrough(false);
  }, []);

  const handleTicketDragEnd = useCallback(() => {
    // Drop fires before dragend on the source; defer cleanup so drop can read draggingTicketRef.
    requestAnimationFrame(() => {
      if (!ticketDropCommittedRef.current) {
        endTicketDrag();
      }
    });
  }, [endTicketDrag]);

  // Recover if dragend on the card does not run (e.g. pointer-events glitch).
  useEffect(() => {
    const onWindowDragEnd = () => {
      if (!draggingTicketRef.current) return;
      requestAnimationFrame(() => {
        if (!ticketDropCommittedRef.current) {
          endTicketDrag();
        }
      });
    };
    window.addEventListener('dragend', onWindowDragEnd);
    return () => window.removeEventListener('dragend', onWindowDragEnd);
  }, [endTicketDrag]);

  const handleTicketDrop = useCallback<TicketStageDropHandler>(
    (ticketId, targetStage, placement) => {
      if (ticketDropCommittedRef.current) return;
      const payload = draggingTicketRef.current;
      if (!payload) return;

      ticketDropCommittedRef.current = true;
      void handleMoveTicket(ticketId, targetStage, placement).finally(() => {
        ticketDropCommittedRef.current = false;
        endTicketDrag();
      });
    },
    [handleMoveTicket, endTicketDrag],
  );

  const handleTicketDropRef = useRef(handleTicketDrop);
  handleTicketDropRef.current = handleTicketDrop;

  // Native capture drop: React synthetic onDrop is unreliable in Chromium for HTML5 DnD.
  useEffect(() => {
    const root = boardScrollRef.current;
    if (!root || boardMode !== 'manual') return;

    const allowTicketDragOver = (e: DragEvent) => {
      if (!draggingTicketRef.current) return;
      const hit = e.target instanceof HTMLElement ? e.target : null;
      if (!hit?.closest('.kb-sub-col--ip, .kb-sub-col--done')) return;
      e.preventDefault();
      if (e.dataTransfer) e.dataTransfer.dropEffect = 'move';
    };

    const commitTicketDrop = (e: DragEvent) => {
      if (!draggingTicketRef.current || ticketDropCommittedRef.current) return;
      const hit = e.target instanceof HTMLElement ? e.target : null;
      if (!hit) return;

      const stageEl = hit.closest('[data-stage]');
      const stageAttr = stageEl?.getAttribute('data-stage');
      if (!stageAttr || !STAGE_ORDER.includes(stageAttr as StageId)) return;

      const ipCol = hit.closest('.kb-sub-col--ip');
      const doneCol = hit.closest('.kb-sub-col--done');
      if (!ipCol && !doneCol) return;

      e.preventDefault();
      e.stopPropagation();

      const placement: MoveTicketPlacement = doneCol && !ipCol ? 'stage_done' : 'in_progress';
      const ticketId =
        readTicketIdFromDataTransfer(e.dataTransfer, draggingTicketRef) ||
        draggingTicketRef.current.id;
      handleTicketDropRef.current(ticketId, stageAttr as StageId, placement);
    };

    const commitFromPointer = (hit: HTMLElement | null) => {
      if (!draggingTicketRef.current || ticketDropCommittedRef.current || !hit) return false;
      const stageEl = hit.closest('[data-stage]');
      const stageAttr = stageEl?.getAttribute('data-stage');
      if (!stageAttr || !STAGE_ORDER.includes(stageAttr as StageId)) return false;
      const ipCol = hit.closest('.kb-sub-col--ip');
      const doneCol = hit.closest('.kb-sub-col--done');
      if (!ipCol && !doneCol) return false;
      const placement: MoveTicketPlacement = doneCol && !ipCol ? 'stage_done' : 'in_progress';
      const ticketId = draggingTicketRef.current.id;
      handleTicketDropRef.current(ticketId, stageAttr as StageId, placement);
      return true;
    };

    const onMouseUp = (e: MouseEvent) => {
      const hit = e.target instanceof HTMLElement ? e.target : null;
      commitFromPointer(hit);
    };

    root.addEventListener('dragover', allowTicketDragOver);
    root.addEventListener('drop', commitTicketDrop, true);
    root.addEventListener('mouseup', onMouseUp, true);
    return () => {
      root.removeEventListener('dragover', allowTicketDragOver);
      root.removeEventListener('drop', commitTicketDrop, true);
      root.removeEventListener('mouseup', onMouseUp, true);
    };
  }, [boardMode]);

  const handleModeToggle = useCallback(async () => {
    try {
      const next = await toggleBoardMode(snapshot.planningRoot);
      onModeToggle?.(next);
    } catch {
      // Server toggle failed; next poll will reconcile
    }
  }, [snapshot.planningRoot, onModeToggle]);

  const stageBuckets = useMemo(
    () => buildStageBuckets(snapshot.columnViews, snapshot.archivedTickets, snapshot.stageSkillRails),
    [snapshot.columnViews, snapshot.archivedTickets, snapshot.stageSkillRails],
  );

  const skillsByStage = useMemo(() => {
    const m = new Map<StageId, StageSkill[]>();
    for (const rail of snapshot.stageSkillRails) m.set(rail.stage, rail.skills);
    return m;
  }, [snapshot.stageSkillRails]);

  const visibleStages = useMemo(
    () => snapshot.stageFlow.length > 0 ? snapshot.stageFlow : STAGE_ORDER.filter((s) => s !== 'context'),
    [snapshot.stageFlow],
  );

  const backlogTickets = useMemo(
    () => buildGlobalBacklogTickets(snapshot.columnViews),
    [snapshot.columnViews],
  );

  const archivedColumnTickets = useMemo(
    () => buildArchivedColumnTickets(snapshot.archivedTickets, stageBuckets),
    [snapshot.archivedTickets, stageBuckets],
  );

  const peersByTargetStage = useMemo(() => {
    const m = new Map<StageId, TicketView[]>();
    for (const stage of visibleStages) {
      m.set(stage, ticketsAtStage(snapshot.columnViews, stage));
    }
    return m;
  }, [snapshot.columnViews, visibleStages]);

  return (
    <div
      className={
        'kb-board-outer' + (ticketDragPassThrough ? ' kb-board-outer--ticket-drag' : '')
      }
    >
      <AgentPoolBar
        team={snapshot.team}
        columnViews={snapshot.columnViews}
        stageSkillRails={snapshot.stageSkillRails}
        heartbeats={snapshot.heartbeats}
        heartbeatSlots={snapshot.heartbeatSlots ?? {}}
        planningRoot={snapshot.planningRoot}
        onUpdate={onTeamUpdate}
        boardMode={boardMode}
      />
      <div className="kbd-board-mode-bar">
        <div className="abd-slide-mode-toggle kbd-board-mode-toggle" role="group" aria-label="Board mode">
          <button
            type="button"
            className={'abd-slide-mode-btn ' + (boardMode === 'automatic' ? 'is-active' : '')}
            onClick={() => void handleModeToggle()}
          >
            Auto
          </button>
          <button
            type="button"
            className={'abd-slide-mode-btn ' + (boardMode === 'manual' ? 'is-active' : '')}
            onClick={() => void handleModeToggle()}
          >
            Manual
          </button>
        </div>
      </div>
      <div className="kb-board-scroll" ref={boardScrollRef}>
        <EndColumn
          heading="Backlog"
          colId="backlog"
          tickets={backlogTickets}
          skillsByStage={skillsByStage}
          boardMode={boardMode}
          planningRoot={snapshot.planningRoot}
          draggingTicketRef={draggingTicketRef}
        />

        {visibleStages.map((stage) => (
          <StageGroup
            key={stage}
            stage={stage}
            bucket={stageBuckets.get(stage) ?? { ip: [], done: [], feedsNext: [] }}
            skills={skillsByStage.get(stage) ?? []}
            skillsByStage={skillsByStage}
            peersByTargetStage={peersByTargetStage}
            team={snapshot.team}
            boardMode={boardMode}
            planningRoot={snapshot.planningRoot}
            onResumeTicket={boardMode === 'manual' ? handleMoveTicket : undefined}
            draggingTicketRef={draggingTicketRef}
            draggingTicketId={draggingTicket?.id ?? null}
            draggingTicket={draggingTicket}
            onTicketDrop={boardMode === 'manual' ? handleTicketDrop : undefined}
            onTicketDragStart={handleTicketDragStart}
            onTicketDragEnd={handleTicketDragEnd}
          />
        ))}

        {archivedColumnTickets.length > 0 ? (
          <EndColumn
            heading="Archived"
            colId="archived"
            tickets={archivedColumnTickets}
            skillsByStage={skillsByStage}
            boardMode={boardMode}
            planningRoot={snapshot.planningRoot}
            draggingTicketRef={draggingTicketRef}
          />
        ) : null}
      </div>
      <div className="kanban-legend-row">
        <div className="kanban-legend-heading">Ticket scope</div>
        <div className="kanban-legend-cards">
          {(
            [
              ['project', 'Project'],
              ['partition', 'Partition'],
              ['increment', 'Increment'],
              ['sprint', 'Sprint'],
            ] as const
          ).map(([key, label]) => (
            <span key={key} className="kanban-legend-chip">
              <span className={'kanban-legend-swatch kanban-legend-swatch--' + key} />
              {label}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

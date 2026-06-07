import { useEffect, useState, useRef, type MutableRefObject } from 'react';
import { LiveSkillIconView } from './LiveSkillIconView';
import { ChatbotIcon, DoneIcon, ReworkIcon, PendingIntentIcon } from './icons';
import { Ticket, TICKET_DRAG_ID } from '@deliveryforge/kanban-client';
import { SkillCatalog } from '@deliveryforge/kanban-shared';
import type {
  AgentRole,
  BoardMode,
  KanbanBoardSnapshot,
  StageId,
  StageSkill,
  StageSubColumn,
} from '@deliveryforge/kanban-shared';
import type { TicketDragPayload } from '@deliveryforge/kanban-client';

export function TicketView({
  ticket,
  stageSkills = [],
  stageSubColumn,
  activeStagePeers = [],
  team,
  boardMode = 'automatic',
  onTicketDragStart,
  onTicketDragEnd,
  draggingTicketRef,
  isDraggingSource = false,
  stageMoveDragActive = false,
}: {
  ticket: Ticket;
  stageSkills?: StageSkill[];
  stageSubColumn?: StageSubColumn;
  activeStagePeers?: Ticket[];
  team?: KanbanBoardSnapshot['team'];
  boardMode?: BoardMode;
  onResumeTicket?: (ticketId: string, targetStage: StageId, placement?: 'in_progress' | 'stage_done') => void;
  onTicketDragStart?: (ticketId: string, stage: StageId) => void;
  onTicketDragEnd?: () => void;
  draggingTicketRef: MutableRefObject<TicketDragPayload | null>;
  isDraggingSource?: boolean;
  stageMoveDragActive?: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const [dropHighlight, setDropHighlight] = useState(false);
  const [rejectionMsg, setRejectionMsg] = useState<string | null>(null);
  const [optimisticIncoming, setOptimisticIncoming] = useState(false);
  const [optimisticDone, setOptimisticDone] = useState(false);
  const [recentDropSkillId, setRecentDropSkillId] = useState<string | null>(null);
  const dragCounterRef = useRef(0);
  const incomingTimerRef = useRef<number | null>(null);
  const doneTimerRef = useRef<number | null>(null);

  const isReviewing = ticket.isReviewing;
  const stageSkillIds = stageSkills.map((s) => s.skillId);
  const focusSkillId =
    team && stageSkills.length > 0
      ? ticket.displayFocusSkillId(stageSkills, stageSubColumn, activeStagePeers, team)
      : ticket.focusSkillId(stageSkillIds, stageSubColumn);
  const primaryFamClass = focusSkillId
    ? SkillCatalog.familyCssClass(SkillCatalog.familyFor(focusSkillId))
    : null;
  const familyClassForSkill = (skillId: string | null): string =>
    skillId ? SkillCatalog.familyCssClass(SkillCatalog.familyFor(skillId)) : '';

  const showLiveSkillIcon = ticket.showsLiveSkillIcon(stageSubColumn);
  const canExpand = ticket.canExpand(stageSkillIds, stageSubColumn);
  const isManual = boardMode === 'manual';
  const isDraggable = ticket.isDraggableForStageMove(boardMode, stageSubColumn);
  const isInProgressActive = ticket.isInProgressActive(stageSubColumn ?? 'ip');
  const hasIncomingVisual = optimisticIncoming;
  const doneSkillSignature = ticket.doneSkillIds.join('|');
  const hasPendingIntent = ticket.pendingIntentSkillIds.length > 0;
  const hasReviewSignal =
    ticket.reviewSkillId !== null ||
    ticket.reviewingSkillIds.length > 0 ||
    ticket.awaitingReviewSkillId !== null;
  const activeSkillForIcon =
    ticket.activeSkillId ?? (ticket.executingSkillIds.length > 0 ? ticket.executingSkillIds[0]! : null);
  const reviewSkillForIcon =
    ticket.reviewSkillId ??
    (ticket.reviewingSkillIds.length > 0 ? ticket.reviewingSkillIds[0]! : null) ??
    ticket.awaitingReviewSkillId;
  const pendingSkillForIcon =
    recentDropSkillId ??
    (ticket.pendingIntentSkillIds.length > 0 ? ticket.pendingIntentSkillIds[0]! : null) ??
    focusSkillId;

  useEffect(() => {
    if (!recentDropSkillId) return;
    if (!ticket.doneSkillIds.includes(recentDropSkillId)) return;

    setOptimisticIncoming(false);
    setOptimisticDone(true);
    if (doneTimerRef.current !== null) {
      window.clearTimeout(doneTimerRef.current);
    }
    doneTimerRef.current = window.setTimeout(() => {
      setOptimisticDone(false);
      setRecentDropSkillId(null);
      doneTimerRef.current = null;
    }, 2200);
  }, [recentDropSkillId, doneSkillSignature]);

  useEffect(() => {
    return () => {
      if (incomingTimerRef.current !== null) {
        window.clearTimeout(incomingTimerRef.current);
      }
      if (doneTimerRef.current !== null) {
        window.clearTimeout(doneTimerRef.current);
      }
    };
  }, []);

  function allowDrop(e: React.DragEvent) {
    if (!isManual) return;
    if (Ticket.isTicketStageDrag(e.dataTransfer, draggingTicketRef.current?.id)) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  }

  function enterDrop(e: React.DragEvent) {
    if (!isManual) return;
    if (Ticket.isTicketStageDrag(e.dataTransfer, draggingTicketRef.current?.id)) return;
    e.preventDefault();
    dragCounterRef.current++;
    setDropHighlight(true);
  }

  function leaveDrop() {
    if (!isManual) return;
    dragCounterRef.current--;
    if (dragCounterRef.current <= 0) {
      dragCounterRef.current = 0;
      setDropHighlight(false);
    }
  }

  function commitDrop(e: React.DragEvent) {
    if (!isManual) return;
    if (Ticket.hasExplicitTicketDragData(e.dataTransfer)) {
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    dragCounterRef.current = 0;
    setDropHighlight(false);

    const agentRole = Ticket.readAgentRoleFromDataTransfer(e.dataTransfer);
    if (!agentRole) {
      setRejectionMsg('Drop failed — no agent role');
      setTimeout(() => setRejectionMsg(null), 3000);
      return;
    }

    const skillId = ticket.findNextEligibleSkill(stageSkills, agentRole);
    if (skillId) {
      setOptimisticIncoming(true);
      if (incomingTimerRef.current !== null) {
        window.clearTimeout(incomingTimerRef.current);
      }
      incomingTimerRef.current = window.setTimeout(() => {
        setOptimisticIncoming(false);
        incomingTimerRef.current = null;
      }, 1600);
      setRecentDropSkillId(skillId);
      setOptimisticDone(false);
      void Ticket.postActionIntent(ticket.ticketId, skillId, agentRole)
        .then(() => {})
        .catch(() => {
          setOptimisticIncoming(false);
          setRecentDropSkillId(null);
          setOptimisticDone(false);
          setRejectionMsg('API error — intent not saved');
          setTimeout(() => setRejectionMsg(null), 3000);
        });
    } else {
      setRejectionMsg(skillId ? 'Missing planning root' : 'No eligible skills remain');
      setTimeout(() => setRejectionMsg(null), 3000);
    }
  }

  function startDrag(e: React.DragEvent) {
    if (!isDraggable) return;
    e.stopPropagation();
    ticket.setDragData(e.dataTransfer);
    onTicketDragStart?.(ticket.ticketId, ticket.stage as StageId);
  }

  function finishDrag() {
    onTicketDragEnd?.();
  }

  return (
    <div
      className={[
        'kb-ticket',
        ticket.scopeCssClass(),
        ticket.statusCssClass(),
        stageSubColumn === 'feeds-next' ? 'kb-ticket--feeds-next' : '',
        dropHighlight ? 'kb-ticket--drop-target' : '',
        isInProgressActive ? 'kb-ticket--in-progress-active' : '',
        isDraggable ? 'kb-ticket--draggable-ticket' : '',
        isDraggingSource ? 'kb-ticket--stage-drag-source' : '',
      ].filter(Boolean).join(' ')}
      data-ticket={ticket.ticketId}
      data-scope={ticket.scopeLevel}
      title={
        isDraggable
          ? ticket.lineage.join(' > ') + ' — drag to another stage to move or skip ahead'
          : ticket.lineage.join(' > ')
      }
      draggable={isDraggable}
      onDragStart={isDraggable ? startDrag : undefined}
      onDragEnd={isDraggable ? finishDrag : undefined}
      onDragOver={isManual && !stageMoveDragActive ? allowDrop : undefined}
      onDragEnter={isManual && !stageMoveDragActive ? enterDrop : undefined}
      onDragLeave={isManual && !stageMoveDragActive ? leaveDrop : undefined}
      onDrop={isManual && !stageMoveDragActive ? commitDrop : undefined}
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
          {hasIncomingVisual ? (
            <span className="kb-ticket-agent-icon">
              <PendingIntentIcon colorClass={familyClassForSkill(pendingSkillForIcon)} />
            </span>
          ) : optimisticDone ? (
            <span className="kb-ticket-agent-icon">
              <DoneIcon colorClass={familyClassForSkill(recentDropSkillId)} />
            </span>
          ) : hasReviewSignal ? (
            <span className="kb-ticket-agent-icon">
              <DoneIcon colorClass={familyClassForSkill(reviewSkillForIcon)} />
            </span>
          ) : showLiveSkillIcon ? (
            <LiveSkillIconView
              visible
              mode="bot"
              BotIcon={ChatbotIcon}
              MagnifyIcon={DoneIcon}
              colorClass={familyClassForSkill(activeSkillForIcon)}
            />
          ) : hasPendingIntent ? (
            <span className="kb-ticket-agent-icon">
              <PendingIntentIcon colorClass={familyClassForSkill(pendingSkillForIcon)} />
            </span>
          ) : null}
        </div>
      ) : null}
      {expanded && canExpand && (
        <div className="kb-ticket-skills-expand">
          {stageSkills.map((s) => {
            const row = ticket.skillRowDisplayState(s.skillId, focusSkillId);
            const fc = SkillCatalog.familyCssClass(s.family);
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
                  {row.showMagnify && <DoneIcon colorClass={fc} />}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

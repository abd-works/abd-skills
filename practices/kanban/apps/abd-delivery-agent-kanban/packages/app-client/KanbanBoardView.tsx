import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { KanbanBoard } from '@deliveryforge/kanban-client';
import { Ticket, type TicketDragPayload, type TicketStageDropHandler, type TicketDropPlacement } from '@deliveryforge/kanban-client';
import type {
  AgentRole,
  BoardMode,
  KanbanBoardSnapshot,
  StageId,
  StageSkill,
} from '@deliveryforge/kanban-shared';
import { Stage } from '@deliveryforge/kanban-shared';
import { StageBucketLayout } from '@deliveryforge/kanban-client';
import { TeamView } from './TeamView';
import { StageGroupView } from './StageGroupView';
import { KanbanEndColumnView } from './KanbanEndColumnView';
import { AgentStreamPanel } from './AgentStreamPanel';

export interface KanbanBoardViewProps {
  snapshot: KanbanBoardSnapshot;
  onTeamUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  onModeToggle?: (snapshot: KanbanBoardSnapshot) => void;
}

export function KanbanBoardView({
  snapshot,
  onTeamUpdate,
  onModeToggle,
}: KanbanBoardViewProps) {
  const boardScrollRef = useRef<HTMLDivElement>(null);
  const draggingTicketRef = useRef<TicketDragPayload | null>(null);
  const ticketDropCommittedRef = useRef(false);
  const [draggingTicket, setDraggingTicket] = useState<TicketDragPayload | null>(null);
  const [ticketDragPassThrough, setTicketDragPassThrough] = useState(false);
  const [openStreamPanels, setOpenStreamPanels] = useState<AgentRole[]>([]);
  const snapshotKey = snapshot.etag + ':' + snapshot.polledAt;
  KanbanBoard.useFlipAnimations(boardScrollRef, snapshotKey);

  const boardMode: BoardMode = snapshot.board_mode ?? 'automatic';

  // ── Ticket move ───────────────────────────────────────────────────

  const handleMoveTicket = useCallback(
    async (
      ticketId: string,
      targetStage: StageId,
      placement: TicketDropPlacement = 'in_progress',
    ) => {
      try {
        const raw = await Ticket.moveToStage(
          ticketId,
          targetStage,
          placement,
        );
        onTeamUpdate?.(KanbanBoard.fromSnapshot(raw));
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Move failed';
        window.alert(msg);
      }
    },
    [onTeamUpdate],
  );

  // ── Ticket drag coordination ──────────────────────────────────────

  const startTicketDrag = useCallback((ticketId: string, stage: StageId) => {
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

  const finishTicketDrag = useCallback(() => {
    requestAnimationFrame(() => {
      if (!ticketDropCommittedRef.current) {
        endTicketDrag();
      }
    });
  }, [endTicketDrag]);

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

  const commitTicketDrop = useCallback<TicketStageDropHandler>(
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

  const ticketDropRef = useRef(commitTicketDrop);
  ticketDropRef.current = commitTicketDrop;

  // Native capture drop — React synthetic onDrop is unreliable in Chromium for HTML5 DnD.
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
      const dropTarget = Ticket.resolveDropTarget(hit);
      if (!dropTarget) return;
      e.preventDefault();
      e.stopPropagation();
      const ticketId =
        (e.dataTransfer
          ? Ticket.readTicketIdFromDataTransfer(e.dataTransfer, draggingTicketRef.current?.id)
          : null) || draggingTicketRef.current.id;
      ticketDropRef.current(ticketId, dropTarget.stage, dropTarget.placement);
    };

    const commitFromPointer = (hit: HTMLElement | null) => {
      if (!draggingTicketRef.current || ticketDropCommittedRef.current || !hit) return false;
      const dropTarget = Ticket.resolveDropTarget(hit);
      if (!dropTarget) return false;
      ticketDropRef.current(draggingTicketRef.current.id, dropTarget.stage, dropTarget.placement);
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

  // ── Mode toggle ───────────────────────────────────────────────────

  const handleToggleMode = useCallback(async () => {
    try {
      const next = await KanbanBoard.toggleMode();
      onModeToggle?.(next);
    } catch {
      // Server toggle failed; next poll will reconcile
    }
  }, [onModeToggle]);

  const handleAvatarClick = useCallback((role: AgentRole) => {
    setOpenStreamPanels((prev) =>
      prev.includes(role) ? prev.filter((r) => r !== role) : [...prev, role],
    );
  }, []);

  // ── Layout derivations ────────────────────────────────────────────

  const stageLayout = useMemo(
    () => StageBucketLayout.build(snapshot.columnViews, snapshot.archivedTickets, snapshot.stageSkillRails),
    [snapshot.columnViews, snapshot.archivedTickets, snapshot.stageSkillRails],
  );

  const stageBuckets = useMemo(() => stageLayout.buildStageBuckets(), [stageLayout]);

  const skillsByStage = useMemo(() => {
    const m = new Map<StageId, StageSkill[]>();
    for (const rail of snapshot.stageSkillRails) m.set(rail.stage, rail.skills);
    return m;
  }, [snapshot.stageSkillRails]);

  const visibleStages = useMemo(
    () =>
      snapshot.stageFlow.length > 0
        ? snapshot.stageFlow
        : Stage.ORDER.filter((s: StageId) => s !== 'context'),
    [snapshot.stageFlow],
  );

  const backlogTickets = useMemo(
    () => StageBucketLayout.globalBacklogTickets(snapshot.columnViews) as Ticket[],
    [snapshot.columnViews],
  );

  const archivedColumnTickets = useMemo(
    () => stageLayout.archivedColumnTickets(snapshot.archivedTickets) as Ticket[],
    [stageLayout, snapshot.archivedTickets],
  );

  const peersByTargetStage = useMemo(() => {
    const m = new Map<StageId, Ticket[]>();
    for (const stage of visibleStages) {
      m.set(stage, Ticket.ticketsAtStage(snapshot.columnViews, stage) as Ticket[]);
    }
    return m;
  }, [snapshot.columnViews, visibleStages]);

  // ── Render ────────────────────────────────────────────────────────

  return (
    <div
      className={
        'kb-board-outer' + (ticketDragPassThrough ? ' kb-board-outer--ticket-drag' : '')
      }
    >
      <TeamView
        team={snapshot.team}
        columnViews={snapshot.columnViews}
        stageSkillRails={snapshot.stageSkillRails}
        agentSessions={snapshot.agentSessions}
        onUpdate={onTeamUpdate}
        boardMode={boardMode}
        onAvatarClick={handleAvatarClick}
      />
      <div className="kbd-board-mode-bar">
        <div className="abd-slide-mode-toggle kbd-board-mode-toggle" role="group" aria-label="Board mode">
          <button
            type="button"
            className={'abd-slide-mode-btn ' + (boardMode === 'automatic' ? 'is-active' : '')}
            onClick={() => void handleToggleMode()}
          >
            Auto
          </button>
          <button
            type="button"
            className={'abd-slide-mode-btn ' + (boardMode === 'manual' ? 'is-active' : '')}
            onClick={() => void handleToggleMode()}
          >
            Manual
          </button>
        </div>
      </div>
      <div className="kb-board-scroll" ref={boardScrollRef}>
        <KanbanEndColumnView
          heading="Backlog"
          colId="backlog"
          tickets={backlogTickets}
          skillsByStage={skillsByStage}
          boardMode={boardMode}
          draggingTicketRef={draggingTicketRef}
        />

        {visibleStages.map((stage: StageId) => (
          <StageGroupView
            key={stage}
            stage={stage}
            bucket={stageBuckets.get(stage) ?? { ip: [], done: [], feedsNext: [] }}
            skills={skillsByStage.get(stage) ?? []}
            skillsByStage={skillsByStage}
            peersByTargetStage={peersByTargetStage}
            team={snapshot.team}
            boardMode={boardMode}
            onResumeTicket={boardMode === 'manual' ? handleMoveTicket : undefined}
            draggingTicketRef={draggingTicketRef}
            draggingTicketId={draggingTicket?.id ?? null}
            draggingTicket={draggingTicket}
            onTicketDrop={boardMode === 'manual' ? commitTicketDrop : undefined}
            onTicketDragStart={startTicketDrag}
            onTicketDragEnd={finishTicketDrag}
          />
        ))}

        {archivedColumnTickets.length > 0 ? (
          <KanbanEndColumnView
            heading="Archived"
            colId="archived"
            tickets={archivedColumnTickets}
            skillsByStage={skillsByStage}
            boardMode={boardMode}
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

      {openStreamPanels.length > 0 && (
        <div className="kb-stream-panels-row">
          {openStreamPanels.map((role) => (
            <AgentStreamPanel
              key={role}
              role={role}
              onClose={() => setOpenStreamPanels((prev) => prev.filter((r) => r !== role))}
            />
          ))}
        </div>
      )}
    </div>
  );
}

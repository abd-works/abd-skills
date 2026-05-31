import { useMemo, useState } from 'react';
import type {
  AgentRole,
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

function DoneIcon() {
  return (
    <svg
      className="kb-skill-icon kb-skill-icon--done"
      viewBox="0 0 14 14"
      width="11"
      height="11"
      aria-label="Done"
    >
      <polyline points="2,7 5.5,11 12,3" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

// ---- Ticket card ----

function ticketStatusClass(ticket: TicketView): string {
  if (isScatterParent(ticket)) return 'kb-ticket--scatter-parent';
  if (ticket.notes.toLowerCase().includes('blocked')) return 'kb-ticket--blocked';
  return '';
}

function TicketCard({
  ticket,
  moved,
  stageSkills = [],
  stageSubColumn,
  activeStagePeers = [],
  team,
}: {
  ticket: TicketView;
  moved?: boolean;
  stageSkills?: StageSkill[];
  stageSubColumn?: StageSubColumn;
  activeStagePeers?: TicketView[];
  team?: KanbanBoardSnapshot['team'];
}) {
  const [expanded, setExpanded] = useState(false);

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
  const showSkillMeta = stageSubColumn === 'ip' && showLiveSkillIcon;

  const canExpand = ticketCanExpand(ticket, stageSkillIds, stageSubColumn);

  return (
    <div
      className={
        'kb-ticket ' +
        scopeLevelCssClass(ticket.scopeLevel) +
        ' ' +
        (moved ? 'kb-ticket--moving ' : '') +
        ticketStatusClass(ticket) +
        (stageSubColumn === 'feeds-next' ? ' kb-ticket--feeds-next' : '')
      }
      data-ticket={ticket.ticketId}
      data-scope={ticket.scopeLevel}
      title={ticket.lineage.join(' > ')}
    >
      <div className="kb-ticket-chip">
        {ticket.chipLabel}
        {isReviewing && (
          <span className="kb-status-dot kb-status-dot--review" title="In review" />
        )}
        {canExpand && (
          <button
            className="kb-ticket-expand-btn"
            onClick={() => setExpanded((e) => !e)}
            aria-label={expanded ? 'Collapse skills' : 'Expand skills'}
            title={expanded ? 'Collapse skills' : 'Show skill progress'}
          >
            {expanded ? '\u2212' : '+'}
          </button>
        )}
      </div>
      <div className="kb-ticket-label">{ticket.displayLabel}</div>
      {showSkillMeta ? (
        <div className="kb-ticket-meta">
          <span className="kb-ticket-agent-icon">
            {isReviewing || ticket.awaitingReviewSkillId !== null
              ? <MagnifyIcon colorClass={primaryFamClass!} />
              : <ChatbotIcon colorClass={primaryFamClass!} />}
          </span>
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
                {row.isDone && <DoneIcon />}
                <span className="kb-ticket-skill-label">{s.label}</span>
                {row.showBot && <ChatbotIcon colorClass={fc} />}
                {row.showMagnify && <MagnifyIcon colorClass={fc} />}
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
  movedTickets,
  stageSkills = [],
  activeStagePeers = [],
  team,
}: {
  label: string;
  subColId: StageSubColumn;
  tickets: TicketView[];
  movedTickets: Set<string>;
  stageSkills?: StageSkill[];
  activeStagePeers?: TicketView[];
  team?: KanbanBoardSnapshot['team'];
}) {
  return (
    <div className={'kb-sub-col kb-sub-col--' + subColId}>
      <div className="kb-sub-col-head">
        <span>{label}</span>
        {tickets.length > 0 ? <span className="kb-col-count">{tickets.length}</span> : null}
      </div>
      <div className="kb-sub-col-tickets">
        {tickets.map((t) => (
          <TicketCard
            key={t.ticketId}
            ticket={t}
            moved={movedTickets.has('ticket-' + t.ticketId)}
            stageSkills={stageSkills}
            stageSubColumn={subColId}
            activeStagePeers={activeStagePeers}
            team={team}
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
  movedTickets,
  peersByTargetStage,
  team,
}: {
  columnStage: StageId;
  doneTickets: TicketView[];
  feedsNextTickets: TicketView[];
  stageSkills: StageSkill[];
  skillsByStage: Map<StageId, StageSkill[]>;
  movedTickets: Set<string>;
  peersByTargetStage: Map<StageId, TicketView[]>;
  team: KanbanBoardSnapshot['team'];
}) {
  const hasTickets = doneTickets.length + feedsNextTickets.length > 0;
  return (
    <div className="kb-sub-col kb-sub-col--done">
      <div className="kb-sub-col-head">
        <span>Done</span>
        {hasTickets ? (
          <span className="kb-col-count">{doneTickets.length + feedsNextTickets.length}</span>
        ) : null}
      </div>
      <div className="kb-sub-col-tickets">
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
                moved={movedTickets.has('ticket-' + t.ticketId)}
                stageSkills={stageSkillsForTicket(t, columnStage, skillsByStage)}
                stageSubColumn="done"
                activeStagePeers={[]}
                team={team}
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
                  moved={movedTickets.has('ticket-' + t.ticketId)}
                  stageSkills={targetSkills}
                  stageSubColumn="feeds-next"
                  activeStagePeers={t.stage ? peersByTargetStage.get(t.stage) ?? [] : []}
                  team={team}
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
  movedTickets,
  peersByTargetStage,
  team,
}: {
  stage: StageId;
  bucket: StageBucket;
  skills: StageSkill[];
  skillsByStage: Map<StageId, StageSkill[]>;
  movedTickets: Set<string>;
  peersByTargetStage: Map<StageId, TicketView[]>;
  team: KanbanBoardSnapshot['team'];
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
          movedTickets={movedTickets}
          stageSkills={skills}
          activeStagePeers={peersByTargetStage.get(stage) ?? []}
          team={team}
        />
        <DoneSubColumn
          columnStage={stage}
          doneTickets={bucket.done}
          feedsNextTickets={bucket.feedsNext}
          stageSkills={skills}
          skillsByStage={skillsByStage}
          movedTickets={movedTickets}
          peersByTargetStage={peersByTargetStage}
          team={team}
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
}: {
  heading: string;
  colId: string;
  tickets: TicketView[];
}) {
  return (
    <div className="kb-end-col" data-col={colId}>
      <div className="kb-end-col-header">{heading}</div>
      <div className="kb-end-col-tickets">
        {tickets.map((t) => (
          <TicketCard key={t.ticketId} ticket={t} />
        ))}
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

function AgentAvatar({
  role,
  state,
  index,
  size = 'md',
}: {
  role: AgentRole | 'kanban-lead';
  state: 'idle' | 'working' | 'inactive';
  index: number;
  size?: 'sm' | 'md';
}) {
  const label = role === 'kanban-lead' ? 'KL' : ROLE_LABELS[role as AgentRole];
  const fullName = role === 'kanban-lead' ? 'Kanban Lead' : ROLE_FULL[role as AgentRole];
  const stateLabel = state === 'inactive' ? 'no thread' : state;
  return (
    <div
      className={'kb-agent-avatar kb-agent-avatar--' + size + ' kb-agent-avatar--' + state}
      data-role={role}
      title={fullName + (role !== 'kanban-lead' ? ' #' + (index + 1) : '') + ' \u2014 ' + stateLabel}
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
  planningRoot,
  onUpdate,
}: {
  role: AgentRole;
  total: number;
  engagedCount: number;
  slotHeartbeats: Array<{ ageSeconds: number | null; status: string | null }>;
  planningRoot: string;
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
}) {
  async function adjust(delta: number) {
    const next = await postTeamAdjust(planningRoot, role, delta);
    if (next) onUpdate?.(next);
  }

  const slots = Math.max(total, 1);

  return (
    <div className="kb-pool-group" data-role={role}>
      <div className="kb-pool-group-label">{ROLE_FULL[role]}</div>
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
            <AgentAvatar key={i} role={role} state={st} index={i} size="sm" />
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
}: {
  team: KanbanBoardSnapshot['team'];
  columnViews: KanbanBoardSnapshot['columnViews'];
  stageSkillRails: KanbanBoardSnapshot['stageSkillRails'];
  heartbeats: KanbanBoardSnapshot['heartbeats'];
  heartbeatSlots: KanbanBoardSnapshot['heartbeatSlots'];
  planningRoot: string;
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
}) {
  const engagedCounts = useMemo(
    () => countRoleEngagement(columnViews, stageSkillRails, team!),
    [columnViews, stageSkillRails, team],
  );

  const klAge = heartbeats?.['kanban-lead'] ?? null;
  const klAlive =
    klAge !== null && klAge < HEARTBEAT_STALE_SECS;

  return (
    <div className="kb-pool-bar">
      <div className="kb-pool-group kb-pool-group--lead" data-role="kanban-lead">
        <div className="kb-pool-group-label">Kanban Lead</div>
        <div className="kb-pool-group-row">
          <AgentAvatar
            role="kanban-lead"
            state={klAlive || klAge === null ? 'idle' : 'inactive'}
            index={0}
            size="sm"
          />
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
            planningRoot={planningRoot}
            onUpdate={onUpdate}
          />
        );
      })}
    </div>
  );
}

// ---- Board ----

export interface DeliveryKanbanBoardProps {
  snapshot: KanbanBoardSnapshot;
  movedTickets?: Set<string>;
  onTeamUpdate?: (snapshot: KanbanBoardSnapshot) => void;
}

export function DeliveryKanbanBoard({
  snapshot,
  movedTickets = new Set(),
  onTeamUpdate,
}: DeliveryKanbanBoardProps) {
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
    <div className="kb-board-outer">
      <AgentPoolBar
        team={snapshot.team}
        columnViews={snapshot.columnViews}
        stageSkillRails={snapshot.stageSkillRails}
        heartbeats={snapshot.heartbeats}
        heartbeatSlots={snapshot.heartbeatSlots ?? {}}
        planningRoot={snapshot.planningRoot}
        onUpdate={onTeamUpdate}
      />
      <div className="kb-board-scroll">
        <EndColumn heading="Backlog" colId="backlog" tickets={backlogTickets} />

        {visibleStages.map((stage) => (
          <StageGroup
            key={stage}
            stage={stage}
            bucket={stageBuckets.get(stage) ?? { ip: [], done: [], feedsNext: [] }}
            skills={skillsByStage.get(stage) ?? []}
            skillsByStage={skillsByStage}
            movedTickets={movedTickets}
            peersByTargetStage={peersByTargetStage}
            team={snapshot.team}
          />
        ))}

        {archivedColumnTickets.length > 0 ? (
          <EndColumn heading="Archived" colId="archived" tickets={archivedColumnTickets} />
        ) : null}
      </div>
    </div>
  );
}

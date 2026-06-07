import { TeamMemberView } from './TeamMemberView';
import { Heartbeat, ROLE_FULL } from '@deliveryforge/kanban-client';
import type { AgentRole, BoardMode, KanbanBoardSnapshot, AgentSessionInfo } from '@deliveryforge/kanban-shared';

function resolveSlotState(
  slotIndex: number,
  engagedCount: number,
  session: AgentSessionInfo | undefined,
): 'idle' | 'working' | 'inactive' {
  if (slotIndex < engagedCount) return 'working';
  if (!session) return 'idle';
  if (session.state === 'running') return 'working';
  if (session.state === 'completed' || session.state === 'failed') return 'inactive';
  return 'idle';
}

export function TeamRoleView({
  role,
  total,
  engagedCount,
  agentSession,
  spawnNeeded,
  onUpdate,
  boardMode,
  onAvatarClick,
}: {
  role: AgentRole;
  total: number;
  engagedCount: number;
  agentSession?: AgentSessionInfo;
  spawnNeeded?: number;
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  boardMode?: BoardMode;
  onAvatarClick?: (role: AgentRole) => void;
}) {
  async function adjust(delta: number) {
    const next = await Heartbeat.adjustTeam(role, delta);
    if (next) onUpdate?.(next);
  }

  const slots = Math.max(total, 1);
  const note = agentSession?.finalMessage ?? agentSession?.errorDetail ?? null;

  return (
    <div className="kb-pool-group" data-role={role}>
      <div className="kb-pool-group-label">
        {ROLE_FULL[role]}
        {spawnNeeded ? (
          <span className="kb-spawn-badge" title={`${spawnNeeded} agent(s) need spawning`}>
            {spawnNeeded}
          </span>
        ) : null}
      </div>
      <div className="kb-pool-group-row">
        {Array.from({ length: slots }, (_, i) => {
          const state = total === 0
            ? 'inactive'
            : resolveSlotState(i, engagedCount, i === 0 ? agentSession : undefined);
          return (
            <TeamMemberView
              key={i}
              role={role}
              state={state}
              index={i}
              lastActivitySec={i === 0 ? (agentSession?.lastActivitySec ?? null) : null}
              note={i === 0 ? note : null}
              size="sm"
              boardMode={boardMode}
              onAvatarClick={onAvatarClick}
            />
          );
        })}
        <div className="kb-pool-controls">
          <button
            className="kb-pool-btn"
            onClick={() => void adjust(1)}
            title={'Add ' + ROLE_FULL[role]}
          >
            +
          </button>
          <button
            className="kb-pool-btn"
            onClick={() => void adjust(-1)}
            title={'Remove ' + ROLE_FULL[role]}
            disabled={total === 0}
          >
            &minus;
          </button>
        </div>
      </div>
    </div>
  );
}

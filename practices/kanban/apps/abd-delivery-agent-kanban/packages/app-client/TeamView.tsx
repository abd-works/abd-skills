import { useMemo, useState } from 'react';
import { TeamMemberView } from './TeamMemberView';
import { TeamRoleView } from './TeamRoleView';
import { Heartbeat } from '@deliveryforge/kanban-client';
import { Ticket } from '@deliveryforge/kanban-client';
import { AGENT_ROLES } from '@deliveryforge/kanban-shared';
import type { AgentRole, BoardMode, KanbanBoardSnapshot } from '@deliveryforge/kanban-shared';

export function TeamView({
  team,
  columnViews,
  stageSkillRails,
  agentSessions,
  onUpdate,
  boardMode,
  onAvatarClick,
}: {
  team: KanbanBoardSnapshot['team'];
  columnViews: KanbanBoardSnapshot['columnViews'];
  stageSkillRails: KanbanBoardSnapshot['stageSkillRails'];
  agentSessions?: KanbanBoardSnapshot['agentSessions'];
  onUpdate?: (snapshot: KanbanBoardSnapshot) => void;
  boardMode?: BoardMode;
  onAvatarClick?: (role: AgentRole) => void;
}) {
  const engagedCounts = useMemo(
    () => Ticket.countRoleEngagement(columnViews),
    [columnViews],
  );

  const klSession = agentSessions?.['kanban-lead'];
  const klState = klSession
    ? klSession.state === 'running' ? 'working' : 'inactive'
    : 'idle';

  const [klScanning, setKlScanning] = useState(false);
  const [lastScanResult, setLastScanResult] = useState<{
    spawns?: Array<{ role: string; instance: number }>;
    actions?: string[];
  } | null>(null);

  async function wakeLeadScan() {
    if (klScanning) return;
    setKlScanning(true);
    try {
      const result = await Heartbeat.leadScan();
      if (result) setLastScanResult(result);
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
            <TeamMemberView
              role="kanban-lead"
              state={klScanning ? 'working' : klState}
              index={0}
              note={klScanning ? 'Running scan...' : (klSession?.finalMessage ?? klSession?.errorDetail ?? null)}
              lastActivitySec={klScanning ? null : (klSession?.lastActivitySec ?? null)}
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
          <TeamRoleView
            key={role}
            role={role}
            total={pairCount}
            engagedCount={engagedCounts[role]}
            agentSession={agentSessions?.[role]}
            spawnNeeded={spawnsByRole[role]}
            onUpdate={onUpdate}
            boardMode={boardMode}
            onAvatarClick={onAvatarClick}
          />
        );
      })}
    </div>
  );
}

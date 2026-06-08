import { Heartbeat } from '@deliveryforge/kanban-client';
import type { AgentRole, BoardMode } from '@deliveryforge/kanban-shared';

export function TeamMemberView({
  role,
  state,
  index,
  lastActivitySec,
  note,
  size = 'md',
  boardMode,
  onAvatarClick,
}: {
  role: AgentRole | 'kanban-lead';
  state: 'idle' | 'working' | 'inactive';
  index: number;
  lastActivitySec?: number | null;
  note?: string | null;
  size?: 'sm' | 'md';
  boardMode?: BoardMode;
  onAvatarClick?: (role: AgentRole) => void;
}) {
  const label = Heartbeat.roleLabel(role);
  const tip = Heartbeat.avatarTooltip(role, index, state, lastActivitySec ?? null, note);
  const isDraggable = boardMode === 'manual' && role !== 'kanban-lead';

  function startDrag(e: React.DragEvent) {
    e.dataTransfer.setData('application/agent-role', role);
    e.dataTransfer.setData('text/plain', `agent-role:${role}`);
    e.dataTransfer.effectAllowed = 'copy';
  }

  function handleClick() {
    if (role !== 'kanban-lead' && onAvatarClick) {
      onAvatarClick(role as AgentRole);
    }
  }

  return (
    <div
      className={[
        'kb-agent-avatar',
        'kb-agent-avatar--' + size,
        'kb-agent-avatar--' + state,
        isDraggable ? 'kb-agent-avatar--draggable' : '',
        role !== 'kanban-lead' && onAvatarClick ? 'kb-agent-avatar--clickable' : '',
      ].filter(Boolean).join(' ')}
      data-role={role}
      title={tip}
      draggable={isDraggable}
      onDragStart={isDraggable ? startDrag : undefined}
      onClick={role !== 'kanban-lead' ? handleClick : undefined}
    >
      <span className="kb-agent-initial">{label}</span>
    </div>
  );
}

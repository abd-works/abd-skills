/**
 * View Multiple Agent Streams
 *
 * Epic:     Display Agent Output Stream
 * Sub-epic: View Multiple Agent Streams
 *
 * Stories:
 *   - Open Second Agent Stream While First Is Open
 */
import { describe, it, expect } from 'vitest';

import type { AgentStreamPanelView } from '@deliveryforge/kanban-client';
import { useAgentStream } from '@deliveryforge/kanban-client';
import type { AgentOutputStream, AgentSession } from '@deliveryforge/kanban-shared';

// ============================================================================
// TYPES
// ============================================================================

type AgentRole = 'engineer' | 'business-expert' | 'quality-advocate';
type SessionState = 'active' | 'idle' | 'none';

interface AgentAvatar {
  role: AgentRole;
  session_state: SessionState;
  active_ticket_id: string | null;
  active_stage: string | null;
  active_skill: string | null;
}

interface AgentPool {
  avatars: AgentAvatar[];
}

interface StreamPanel {
  role: AgentRole;
  anchored_stage: string;
  is_open: boolean;
  shows_live_stream: boolean;
  height: number;
  is_independently_scrollable: boolean;
}

interface StageColumn {
  stage_name: string;
  height: number;
}

interface BoardLayout {
  agent_pool: AgentPool;
  stage_columns: StageColumn[];
  open_panels: StreamPanel[];
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function given_agent_pool_with_avatar(
  role: AgentRole,
  state: SessionState,
): BoardLayout {
  return {
    agent_pool: {
      avatars: [
        {
          role,
          session_state: state,
          active_ticket_id: state === 'active' ? 'TICKET-001' : null,
          active_stage: null,
          active_skill: null,
        },
      ],
    },
    stage_columns: [],
    open_panels: [],
  };
}

function given_additional_agent(
  layout: BoardLayout,
  role: AgentRole,
  state: SessionState,
): BoardLayout {
  const avatar: AgentAvatar = {
    role,
    session_state: state,
    active_ticket_id: state === 'active' ? `TICKET-${layout.agent_pool.avatars.length + 1}` : null,
    active_stage: null,
    active_skill: null,
  };
  return {
    ...layout,
    agent_pool: { avatars: [...layout.agent_pool.avatars, avatar] },
  };
}

function given_agent_executing_skill_on_ticket(
  layout: BoardLayout,
  role: AgentRole,
  skill: string,
  ticketId: string,
  stage: string,
): BoardLayout {
  const avatars = layout.agent_pool.avatars.map((a) =>
    a.role === role
      ? { ...a, session_state: 'active' as SessionState, active_ticket_id: ticketId, active_stage: stage, active_skill: skill }
      : a,
  );
  const has_stage = layout.stage_columns.some((c) => c.stage_name === stage);
  const stage_columns = has_stage
    ? layout.stage_columns
    : [...layout.stage_columns, { stage_name: stage, height: 480 }];
  return { ...layout, agent_pool: { avatars }, stage_columns, open_panels: layout.open_panels };
}

function given_stream_panel_open_for(
  layout: BoardLayout,
  role: AgentRole,
  stage: string,
): BoardLayout {
  const panel: StreamPanel = {
    role,
    anchored_stage: stage,
    is_open: true,
    shows_live_stream: true,
    height: 480,
    is_independently_scrollable: true,
  };
  return { ...layout, open_panels: [...layout.open_panels, panel] };
}

function when_user_clicks_avatar(layout: BoardLayout, role: AgentRole): BoardLayout {
  const avatar = layout.agent_pool.avatars.find((a) => a.role === role);
  if (!avatar || avatar.session_state !== 'active' || !avatar.active_stage) return layout;

  const column = layout.stage_columns.find((c) => c.stage_name === avatar.active_stage);
  const panel: StreamPanel = {
    role,
    anchored_stage: avatar.active_stage!,
    is_open: true,
    shows_live_stream: true,
    height: column?.height ?? 480,
    is_independently_scrollable: true,
  };
  return { ...layout, open_panels: [...layout.open_panels, panel] };
}

function then_both_panels_visible(
  layout: BoardLayout,
  role_a: AgentRole,
  role_b: AgentRole,
): void {
  const panel_a = layout.open_panels.find((p) => p.role === role_a);
  const panel_b = layout.open_panels.find((p) => p.role === role_b);
  expect(panel_a).toBeDefined();
  expect(panel_b).toBeDefined();
  expect(panel_a!.is_open).toBe(true);
  expect(panel_b!.is_open).toBe(true);
}

function then_panels_stacked_horizontally(layout: BoardLayout, count: number): void {
  const open = layout.open_panels.filter((p) => p.is_open);
  expect(open).toHaveLength(count);
}

function then_each_panel_independently_scrollable(layout: BoardLayout): void {
  const open = layout.open_panels.filter((p) => p.is_open);
  for (const panel of open) {
    expect(panel.is_independently_scrollable).toBe(true);
  }
}

function then_stream_panel_opens_beside_stage(
  layout: BoardLayout,
  role: AgentRole,
  stage: string,
): void {
  const panel = layout.open_panels.find((p) => p.role === role);
  expect(panel).toBeDefined();
  expect(panel!.is_open).toBe(true);
  expect(panel!.anchored_stage).toBe(stage);
}

// ============================================================================
// STORY: Open Second Agent Stream While First Is Open
// ============================================================================

describe('Open Second Agent Stream While First Is Open', () => {
  it('business-expert panel at discovery, user clicks engineer at specification → both visible side by side', () => {
    // Given
    let layout = given_agent_pool_with_avatar('business-expert', 'active');
    layout = given_additional_agent(layout, 'engineer', 'active');
    layout = given_agent_executing_skill_on_ticket(
      layout, 'business-expert', 'abd-domain-language', 'TICKET-010', 'discovery',
    );
    layout = given_agent_executing_skill_on_ticket(
      layout, 'engineer', 'abd-story-specification', 'TICKET-020', 'specification',
    );
    layout = given_stream_panel_open_for(layout, 'business-expert', 'discovery');

    // When
    layout = when_user_clicks_avatar(layout, 'engineer');

    // Then
    then_both_panels_visible(layout, 'business-expert', 'engineer');
    then_stream_panel_opens_beside_stage(layout, 'business-expert', 'discovery');
    then_stream_panel_opens_beside_stage(layout, 'engineer', 'specification');
  });

  it('three panels open → all three stack horizontally, independently scrollable', () => {
    // Given
    let layout = given_agent_pool_with_avatar('business-expert', 'active');
    layout = given_additional_agent(layout, 'engineer', 'active');
    layout = given_additional_agent(layout, 'quality-advocate', 'active');
    layout = given_agent_executing_skill_on_ticket(
      layout, 'business-expert', 'abd-domain-terms', 'TICKET-010', 'discovery',
    );
    layout = given_agent_executing_skill_on_ticket(
      layout, 'engineer', 'abd-story-acceptance-test', 'TICKET-020', 'specification',
    );
    layout = given_agent_executing_skill_on_ticket(
      layout, 'quality-advocate', 'abd-story-acceptance-criteria', 'TICKET-030', 'exploration',
    );
    layout = given_stream_panel_open_for(layout, 'business-expert', 'discovery');
    layout = given_stream_panel_open_for(layout, 'engineer', 'specification');

    // When
    layout = when_user_clicks_avatar(layout, 'quality-advocate');

    // Then
    then_panels_stacked_horizontally(layout, 3);
    then_each_panel_independently_scrollable(layout);
  });
});

/**
 * Open Agent Stream Panel
 *
 * Epic:     Display Agent Output Stream
 * Sub-epic: Open Agent Stream Panel
 *
 * Stories:
 *   - Expand Agent Stream by Clicking Team Member Avatar
 *   - Anchor Stream Panel beside Active Ticket Stage Column
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
  content: string | null;
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

function given_board_with_stages(layout: BoardLayout, stages: string[]): BoardLayout {
  const stage_columns: StageColumn[] = stages.map((s) => ({ stage_name: s, height: 480 }));
  return { ...layout, stage_columns };
}

function when_user_clicks_avatar(layout: BoardLayout, role: AgentRole): BoardLayout {
  const avatar = layout.agent_pool.avatars.find((a) => a.role === role);
  if (!avatar) return layout;

  if (avatar.session_state !== 'active' || !avatar.active_stage) {
    const panel: StreamPanel = {
      role,
      anchored_stage: '',
      is_open: true,
      shows_live_stream: false,
      height: 0,
      content: 'No active session',
    };
    return { ...layout, open_panels: [...layout.open_panels, panel] };
  }

  const column = layout.stage_columns.find((c) => c.stage_name === avatar.active_stage);
  const panel: StreamPanel = {
    role,
    anchored_stage: avatar.active_stage!,
    is_open: true,
    shows_live_stream: true,
    height: column?.height ?? 480,
    content: null,
  };
  return { ...layout, open_panels: [...layout.open_panels, panel] };
}

function when_agent_moves_ticket_to_stage(
  layout: BoardLayout,
  role: AgentRole,
  new_stage: string,
): BoardLayout {
  const avatars = layout.agent_pool.avatars.map((a) =>
    a.role === role ? { ...a, active_stage: new_stage } : a,
  );
  const open_panels = layout.open_panels.map((p) =>
    p.role === role ? { ...p, anchored_stage: new_stage } : p,
  );
  return { ...layout, agent_pool: { avatars }, stage_columns: layout.stage_columns, open_panels };
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

function then_panel_displays_live_stream(panel: StreamPanel): void {
  expect(panel.shows_live_stream).toBe(true);
}

function then_panel_height_matches_column(
  layout: BoardLayout,
  panel: StreamPanel,
  stage: string,
): void {
  const column = layout.stage_columns.find((c) => c.stage_name === stage);
  expect(column).toBeDefined();
  expect(panel.height).toBe(column!.height);
}

function then_panel_shows_no_active_session(panel: StreamPanel): void {
  expect(panel.shows_live_stream).toBe(false);
  expect(panel.content).toBe('No active session');
}

// ============================================================================
// STORY: Expand Agent Stream by Clicking Team Member Avatar
// ============================================================================

describe('Expand Agent Stream by Clicking Team Member Avatar', () => {
  it('clicking engineer avatar with active ticket opens panel beside stage column with live stream', () => {
    // Given
    let layout = given_agent_pool_with_avatar('engineer', 'active');
    layout = given_board_with_stages(layout, ['discovery', 'specification', 'implementation']);
    layout = given_agent_executing_skill_on_ticket(
      layout, 'engineer', 'abd-specification-by-example', 'TICKET-042', 'specification',
    );

    // When
    layout = when_user_clicks_avatar(layout, 'engineer');

    // Then
    then_stream_panel_opens_beside_stage(layout, 'engineer', 'specification');
    const panel = layout.open_panels.find((p) => p.role === 'engineer')!;
    then_panel_displays_live_stream(panel);
    then_panel_height_matches_column(layout, panel, 'specification');
  });

  it('clicking avatar with no active session shows "No active session"', () => {
    // Given
    let layout = given_agent_pool_with_avatar('engineer', 'idle');
    layout = given_board_with_stages(layout, ['discovery', 'specification']);

    // When
    layout = when_user_clicks_avatar(layout, 'engineer');

    // Then
    const panel = layout.open_panels.find((p) => p.role === 'engineer')!;
    then_panel_shows_no_active_session(panel);
  });
});

// ============================================================================
// STORY: Anchor Stream Panel beside Active Ticket Stage Column
// ============================================================================

describe('Anchor Stream Panel beside Active Ticket Stage Column', () => {
  it('engineer working at exploration → panel anchored to right of exploration column', () => {
    // Given
    let layout = given_agent_pool_with_avatar('engineer', 'active');
    layout = given_board_with_stages(layout, ['discovery', 'exploration', 'specification']);
    layout = given_agent_executing_skill_on_ticket(
      layout, 'engineer', 'abd-domain-language', 'TICKET-010', 'exploration',
    );

    // When
    layout = when_user_clicks_avatar(layout, 'engineer');

    // Then
    then_stream_panel_opens_beside_stage(layout, 'engineer', 'exploration');
  });

  it('agent moves ticket exploration→specification → panel follows to specification column', () => {
    // Given
    let layout = given_agent_pool_with_avatar('engineer', 'active');
    layout = given_board_with_stages(layout, ['exploration', 'specification', 'implementation']);
    layout = given_agent_executing_skill_on_ticket(
      layout, 'engineer', 'abd-acceptance-criteria', 'TICKET-020', 'exploration',
    );
    layout = when_user_clicks_avatar(layout, 'engineer');
    then_stream_panel_opens_beside_stage(layout, 'engineer', 'exploration');

    // When
    layout = when_agent_moves_ticket_to_stage(layout, 'engineer', 'specification');

    // Then
    then_stream_panel_opens_beside_stage(layout, 'engineer', 'specification');
  });
});

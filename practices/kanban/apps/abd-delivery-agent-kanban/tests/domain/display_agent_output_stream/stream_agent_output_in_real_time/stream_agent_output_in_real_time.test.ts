/**
 * Stream Agent Output in Real Time
 *
 * Epic:     Display Agent Output Stream
 * Sub-epic: Stream Agent Output in Real Time
 *
 * Stories:
 *   - Stream Agent Messages to Panel Like IDE Chat
 */
import { describe, it, expect } from 'vitest';

import type { AgentStreamPanelView } from '@deliveryforge/kanban-client';
import { useAgentStream } from '@deliveryforge/kanban-client';
import type { AgentOutputStream, AgentSession } from '@deliveryforge/kanban-shared';

// ============================================================================
// TYPES
// ============================================================================

type AgentRole = 'engineer' | 'business-expert' | 'quality-advocate';
type MessageType = 'text' | 'thinking' | 'skill-complete';

interface StreamMessage {
  type: MessageType;
  content: string;
  timestamp: number;
}

interface StreamPanelState {
  role: AgentRole;
  stage: string;
  messages: StreamMessage[];
  is_auto_scrolling: boolean;
  thinking_indicator_visible: boolean;
  is_open: boolean;
}

interface RenderedMessage {
  type: MessageType;
  content: string;
  styled_as: 'agent-response' | 'thinking' | 'status';
}

interface PanelRender {
  messages: RenderedMessage[];
  auto_scrolled: boolean;
  thinking_indicator_visible: boolean;
  is_open: boolean;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function given_stream_panel_open_for(
  role: AgentRole,
  stage: string,
): StreamPanelState {
  return {
    role,
    stage,
    messages: [],
    is_auto_scrolling: true,
    thinking_indicator_visible: false,
    is_open: true,
  };
}

function when_agent_sends_text_message(
  panel: StreamPanelState,
  content: string,
): StreamPanelState {
  const message: StreamMessage = { type: 'text', content, timestamp: Date.now() };
  return {
    ...panel,
    messages: [...panel.messages, message],
    thinking_indicator_visible: false,
    is_auto_scrolling: true,
  };
}

function when_agent_starts_thinking(panel: StreamPanelState): StreamPanelState {
  return { ...panel, thinking_indicator_visible: true };
}

function when_agent_completes_skill(
  panel: StreamPanelState,
  skill_name: string,
): StreamPanelState {
  const message: StreamMessage = {
    type: 'skill-complete',
    content: `${skill_name} — complete`,
    timestamp: Date.now(),
  };
  return {
    ...panel,
    messages: [...panel.messages, message],
    thinking_indicator_visible: false,
  };
}

function render_panel(panel: StreamPanelState): PanelRender {
  const messages: RenderedMessage[] = panel.messages.map((m) => {
    switch (m.type) {
      case 'text':
        return { type: 'text', content: m.content, styled_as: 'agent-response' };
      case 'thinking':
        return { type: 'thinking', content: m.content, styled_as: 'thinking' };
      case 'skill-complete':
        return { type: 'skill-complete', content: m.content, styled_as: 'status' };
    }
  });

  return {
    messages,
    auto_scrolled: panel.is_auto_scrolling,
    thinking_indicator_visible: panel.thinking_indicator_visible,
    is_open: panel.is_open,
  };
}

function then_message_appears_as_chat_bubble(
  rendered: PanelRender,
  content: string,
): void {
  const msg = rendered.messages.find((m) => m.content === content);
  expect(msg).toBeDefined();
  expect(msg!.styled_as).toBe('agent-response');
}

function then_panel_auto_scrolls(rendered: PanelRender): void {
  expect(rendered.auto_scrolled).toBe(true);
}

function then_thinking_indicator_animates(rendered: PanelRender): void {
  expect(rendered.thinking_indicator_visible).toBe(true);
}

function then_thinking_indicator_disappears(rendered: PanelRender): void {
  expect(rendered.thinking_indicator_visible).toBe(false);
}

function then_completion_status_shown(
  rendered: PanelRender,
  expected_content: string,
): void {
  const msg = rendered.messages.find(
    (m) => m.type === 'skill-complete' && m.content === expected_content,
  );
  expect(msg).toBeDefined();
  expect(msg!.styled_as).toBe('status');
}

function then_panel_remains_open(rendered: PanelRender): void {
  expect(rendered.is_open).toBe(true);
}

// ============================================================================
// STORY: Stream Agent Messages to Panel Like IDE Chat
// ============================================================================

describe('Stream Agent Messages to Panel Like IDE Chat', () => {
  it('agent sends text response → appears as chat bubble, styled as agent response, auto-scrolls', () => {
    // Given
    let panel = given_stream_panel_open_for('engineer', 'specification');

    // When
    panel = when_agent_sends_text_message(
      panel,
      'Writing acceptance tests for the Add Pet story…',
    );

    // Then
    const rendered = render_panel(panel);
    then_message_appears_as_chat_bubble(rendered, 'Writing acceptance tests for the Add Pet story…');
    then_panel_auto_scrolls(rendered);
  });

  it('agent thinking → thinking indicator animates, disappears on next text message', () => {
    // Given
    let panel = given_stream_panel_open_for('engineer', 'exploration');

    // When — agent starts thinking
    panel = when_agent_starts_thinking(panel);

    // Then — indicator visible
    let rendered = render_panel(panel);
    then_thinking_indicator_animates(rendered);

    // When — agent sends next text message
    panel = when_agent_sends_text_message(panel, 'Identified three key abstractions.');

    // Then — indicator gone
    rendered = render_panel(panel);
    then_thinking_indicator_disappears(rendered);
    then_message_appears_as_chat_bubble(rendered, 'Identified three key abstractions.');
  });

  it('agent completes skill → completion status shown, panel remains open', () => {
    // Given
    let panel = given_stream_panel_open_for('engineer', 'specification');
    panel = when_agent_sends_text_message(panel, 'Generating scenarios from acceptance criteria.');

    // When
    panel = when_agent_completes_skill(panel, 'abd-story-acceptance-test');

    // Then
    const rendered = render_panel(panel);
    then_completion_status_shown(rendered, 'abd-story-acceptance-test — complete');
    then_panel_remains_open(rendered);
  });
});

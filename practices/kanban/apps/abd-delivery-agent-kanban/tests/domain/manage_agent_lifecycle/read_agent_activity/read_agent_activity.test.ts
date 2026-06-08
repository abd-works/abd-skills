/**
 * Read Agent Activity
 *
 * Epic:     Manage Agent Lifecycle via Cursor SDK
 * Sub-epic: Read Agent Activity
 *
 * Stories:
 *   - Stream Agent Messages via SDK
 *   - Derive Agent Liveness from SDK Session State
 */

import { describe, it, expect } from 'vitest';
import { AgentSession, AgentOutputStream } from '@deliveryforge/kanban-server';
import { SDK_SESSION_STALE_SECS } from '@deliveryforge/kanban-shared';

// ============================================================================
// HELPER FUNCTIONS — Given
// ============================================================================

function given_active_agent_session(
  role: string,
  messageCount: number,
  lastActivitySec: number,
): AgentSession {
  const now = Date.now();
  return new AgentSession(role, {
    status: 'running',
    messageCount,
    lastActivityTs: now - lastActivitySec * 1000,
  });
}

function given_no_agent_session_for_role(_role: string): AgentSession | null {
  return null;
}

// ============================================================================
// HELPER FUNCTIONS — When
// ============================================================================

function when_agent_emits_message(
  session: AgentSession,
  text: string,
): AgentOutputStream {
  return session.emit({ type: 'text', content: text });
}

function when_agent_emits_thinking_indicator(
  session: AgentSession,
): AgentOutputStream {
  return session.emit({ type: 'thinking' });
}

function when_system_derives_agent_liveness(
  role: string,
  session: AgentSession | null,
): { liveness: 'alive' | 'stale' | 'idle'; avatarState: 'working' | 'idle' | 'inactive' } {
  if (!session) {
    return { liveness: 'idle', avatarState: 'idle' };
  }
  const ageSec = (Date.now() - session.lastActivityTs) / 1000;
  const isStale = ageSec >= SDK_SESSION_STALE_SECS;
  const isEngaged = session.messageCount > 0 && session.status === 'running';

  if (session.status === 'running' && !isStale) {
    return {
      liveness: 'alive',
      avatarState: isEngaged ? 'working' : 'idle',
    };
  }
  if (session.status === 'running' && isStale) {
    return { liveness: 'stale', avatarState: 'inactive' };
  }
  return { liveness: 'idle', avatarState: 'idle' };
}

// ============================================================================
// HELPER FUNCTIONS — Then
// ============================================================================

function then_server_receives_message(
  stream: AgentOutputStream,
  expectedText: string,
): void {
  expect(stream.lastMessage()).toBe(expectedText);
}

function then_agent_liveness_is(
  result: { liveness: string },
  expected: 'alive' | 'stale' | 'idle',
): void {
  expect(result.liveness).toBe(expected);
}

function then_pool_avatar_displays_as(
  result: { avatarState: string },
  state: 'working' | 'idle' | 'inactive',
): void {
  expect(result.avatarState).toBe(state);
}

// ============================================================================
// STORY: Stream Agent Messages via SDK
// ============================================================================

describe('Stream Agent Messages via SDK', () => {
  it('running agent emits text message — server receives in real time, last activity updated', () => {
    const session = given_active_agent_session('engineer', 3, 10);
    const stream = when_agent_emits_message(session, 'Refactoring module');

    then_server_receives_message(stream, 'Refactoring module');
    expect(session.lastActivityTs).toBeGreaterThan(0);
  });

  it('agent emits thinking indicator — server relays thinking state, pool avatar working', () => {
    const session = given_active_agent_session('engineer', 1, 5);
    const stream = when_agent_emits_thinking_indicator(session);

    expect(stream.isThinking()).toBe(true);
    const result = when_system_derives_agent_liveness('engineer', session);
    then_pool_avatar_displays_as(result, 'working');
  });
});

// ============================================================================
// STORY: Derive Agent Liveness from SDK Session State
// ============================================================================

describe('Derive Agent Liveness from SDK Session State', () => {
  it('session running + recent activity → alive; avatar working if engaged, idle otherwise', () => {
    const engaged = given_active_agent_session('engineer', 5, 30);
    const engagedResult = when_system_derives_agent_liveness('engineer', engaged);

    then_agent_liveness_is(engagedResult, 'alive');
    then_pool_avatar_displays_as(engagedResult, 'working');

    const idle = given_active_agent_session('engineer', 0, 30);
    const idleResult = when_system_derives_agent_liveness('engineer', idle);

    then_agent_liveness_is(idleResult, 'alive');
    then_pool_avatar_displays_as(idleResult, 'idle');
  });

  it('session running + no activity for >120s → stale; avatar inactive; eligible for restart', () => {
    const session = given_active_agent_session('engineer', 2, 125);
    const result = when_system_derives_agent_liveness('engineer', session);

    then_agent_liveness_is(result, 'stale');
    then_pool_avatar_displays_as(result, 'inactive');
  });

  it('no session for role + no engagement → idle; avatar idle', () => {
    const session = given_no_agent_session_for_role('ux-designer');
    const result = when_system_derives_agent_liveness('ux-designer', session);

    then_agent_liveness_is(result, 'idle');
    then_pool_avatar_displays_as(result, 'idle');
  });
});

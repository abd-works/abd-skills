/**
 * Display Agent Pool
 *
 * Epic:     Manage Agent Pool
 * Sub-epic: Display Agent Pool
 *
 * Stories: Indicate Agent Liveness from SDK Session,
 *          Show Role Engagement in Agent Pool
 */
import { describe, it, expect } from 'vitest';
import type { AgentSessionInfo } from '@deliveryforge/kanban-shared';

// ── Agent avatar state from SDK session ──────────────────────────────────────

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

function makeSession(state: AgentSessionInfo['state']): AgentSessionInfo {
  return { state, messageCount: 1, lastActivitySec: 30 };
}

// ============================================================================
// STORY: Indicate Agent Liveness from SDK Session
// ============================================================================

describe('Indicate Agent Liveness from SDK Session', () => {
  it('agent alive — session running and no board engagement', () => {
    expect(resolveSlotState(0, 0, makeSession('running'))).toBe('working');
  });

  it('agent inactive — session completed', () => {
    expect(resolveSlotState(0, 0, makeSession('completed'))).toBe('inactive');
  });

  it('agent inactive — session failed', () => {
    expect(resolveSlotState(0, 0, makeSession('failed'))).toBe('inactive');
  });

  it('agent idle — no session and no engagement', () => {
    expect(resolveSlotState(0, 0, undefined)).toBe('idle');
  });
});

// ============================================================================
// STORY: Show Role Engagement in Agent Pool
// ============================================================================

describe('Show Role Engagement in Agent Pool', () => {
  it('engaged slot working without a session', () => {
    expect(resolveSlotState(0, 1, undefined)).toBe('working');
  });

  it('engaged slot working despite failed session', () => {
    expect(resolveSlotState(0, 1, makeSession('failed'))).toBe('working');
  });

  it('unengaged extra slot inactive when session finished', () => {
    expect(resolveSlotState(1, 1, makeSession('completed'))).toBe('inactive');
  });
});

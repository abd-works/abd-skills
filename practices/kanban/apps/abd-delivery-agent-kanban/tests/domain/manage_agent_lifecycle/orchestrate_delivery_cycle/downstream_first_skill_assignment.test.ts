/**
 * Downstream-First Skill Assignment
 *
 * The scan cycle should find the next eligible skill across ALL tickets
 * (backlog, active, done) — not just active. When multiple tickets need
 * the same team member, downstream stages are prioritized first.
 */
import { describe, it, expect } from 'vitest';
import {
  findNextEligible,
  findNextEligibleAcrossBoard,
} from '@deliveryforge/kanban-server/KanbanDomainOps';
import type { WrTicket, WrStageDef, WrKanbanBoard, WrBoard } from '@deliveryforge/kanban-server/WarRoomService';

// ── Minimal kanban config with two stages ────────────────────────────────────

const discoveryStage: WrStageDef = {
  name: 'discovery',
  scope: 'increment',
  stage_work_required: [
    { skill: 'abd-domain-terms', role: 'business-expert', optional: false },
    { skill: 'abd-story-mapping', role: 'product-owner', optional: false },
  ],
};

const explorationStage: WrStageDef = {
  name: 'exploration',
  scope: 'increment',
  stage_work_required: [
    { skill: 'abd-domain-language', role: 'business-expert', optional: false },
    { skill: 'abd-acceptance-criteria', role: 'product-owner', optional: false },
  ],
};

const engineeringStage: WrStageDef = {
  name: 'engineering',
  scope: 'sprint',
  stage_work_required: [
    { skill: 'abd-clean-code', role: 'engineer', optional: false },
  ],
};

const kb: WrKanbanBoard = {
  stages: [discoveryStage, explorationStage, engineeringStage],
  strategy: {} as any,
  team: { 'business-expert': 1, 'product-owner': 1, engineer: 1 },
};

// ── Helpers ──────────────────────────────────────────────────────────────────

function ticket(overrides: Partial<WrTicket> & { ticket_id: string; stage: string }): WrTicket {
  return {
    lineage: [],
    scope_level: 'increment',
    priority: 1,
    skill_progress: {},
    stage_history: [],
    scatter_to: [],
    notes: '',
    ...overrides,
  } as WrTicket;
}

// ── Tests ────────────────────────────────────────────────────────────────────

describe('Downstream-first skill assignment across all columns', () => {
  it('prefers a downstream active ticket over an upstream backlog ticket for the same role', () => {
    const backlogTicket = ticket({
      ticket_id: 'inc-2',
      stage: 'discovery',
      priority: 1,
      skill_progress: {},
    });

    const activeTicket = ticket({
      ticket_id: 'inc-1',
      stage: 'exploration',
      priority: 1,
      skill_progress: {},
    });

    // findNextEligible should pick the exploration ticket (downstream)
    // when both tickets are passed in
    const allTickets = [backlogTicket, activeTicket];
    const match = findNextEligible(kb, allTickets, 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-1');
    expect(match!.skill).toBe('abd-domain-language');
  });

  it('finds eligible skill on a backlog ticket when no active tickets need the role', () => {
    const backlogTicket = ticket({
      ticket_id: 'inc-2',
      stage: 'discovery',
      priority: 1,
      skill_progress: {},
    });

    // Only backlog ticket available — should still be found
    const match = findNextEligible(kb, [backlogTicket], 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-2');
    expect(match!.skill).toBe('abd-domain-terms');
  });

  it('finds next skill on a done-column ticket whose stage is not fully complete', () => {
    // Ticket in done column but still has work: first skill done, second not started
    const doneTicket = ticket({
      ticket_id: 'inc-1',
      stage: 'discovery',
      priority: 1,
      skill_progress: {
        'abd-domain-terms': {
          execution_status: 'done',
          review_status: 'done',
          agent: 'business-expert',
          reviewer: 'business-expert',
        },
      },
    });

    // Product owner should get abd-story-mapping (second skill in discovery)
    const match = findNextEligible(kb, [doneTicket], 'product-owner');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-1');
    expect(match!.skill).toBe('abd-story-mapping');
  });

  it('with multiple tickets at same stage, picks highest priority', () => {
    const lowPriority = ticket({
      ticket_id: 'inc-2',
      stage: 'exploration',
      priority: 2,
      skill_progress: {},
    });

    const highPriority = ticket({
      ticket_id: 'inc-1',
      stage: 'exploration',
      priority: 1,
      skill_progress: {},
    });

    const match = findNextEligible(kb, [lowPriority, highPriority], 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-1');
  });
});

describe('findNextEligibleAcrossBoard — scans all columns', () => {
  it('finds eligible skill on a backlog ticket when no active or done tickets need the role', () => {
    const board: WrBoard = {
      schema: 'abd-delivery-kanban/v2',
      backlog: [
        ticket({ ticket_id: 'inc-2', stage: 'discovery', priority: 1 }),
      ],
      active: [],
      done: [],
      archived: [],
    };

    const match = findNextEligibleAcrossBoard(kb, board, 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-2');
    expect(match!.skill).toBe('abd-domain-terms');
    expect(match!.source).toBe('backlog');
  });

  it('prefers downstream active ticket over upstream backlog ticket', () => {
    const board: WrBoard = {
      schema: 'abd-delivery-kanban/v2',
      backlog: [
        ticket({ ticket_id: 'inc-2', stage: 'discovery', priority: 1 }),
      ],
      active: [
        ticket({ ticket_id: 'inc-1', stage: 'exploration', priority: 1 }),
      ],
      done: [],
      archived: [],
    };

    const match = findNextEligibleAcrossBoard(kb, board, 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-1');
    expect(match!.skill).toBe('abd-domain-language');
    expect(match!.source).toBe('active');
  });

  it('skips done tickets where all skills for the role are complete', () => {
    const board: WrBoard = {
      schema: 'abd-delivery-kanban/v2',
      backlog: [
        ticket({ ticket_id: 'inc-2', stage: 'discovery', priority: 1 }),
      ],
      active: [],
      done: [
        ticket({
          ticket_id: 'inc-1',
          stage: 'discovery',
          priority: 1,
          skill_progress: {
            'abd-domain-terms': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'business-expert',
              reviewer: 'business-expert',
            },
          },
        }),
      ],
      archived: [],
    };

    const match = findNextEligibleAcrossBoard(kb, board, 'business-expert');
    expect(match).not.toBeNull();
    expect(match!.ticket.ticket_id).toBe('inc-2');
    expect(match!.source).toBe('backlog');
  });
});

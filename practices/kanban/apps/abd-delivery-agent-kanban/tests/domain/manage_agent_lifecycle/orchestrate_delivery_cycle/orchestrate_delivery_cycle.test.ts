/**
 * Orchestrate Delivery Cycle
 *
 * Epic:     Manage Agent Lifecycle
 * Sub-epic: Orchestrate Delivery Cycle
 *
 * Stories: Move Ticket to Stage,
 *          Resolve Scatter Children,
 *          Resume Ticket In Progress
 */
import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { describe, it, expect } from 'vitest';
import {
  KanbanBoard,
  Ticket,
  StageBucketLayout,
  parseKanbanBoard,
  type KanbanBoardData,
  type KanbanColumnView,
  type KanbanConfiguration,
  type RawTicket,
  type StageSkillRail,
  type StageSkill,
} from '@deliveryforge/kanban-shared';
import { Ticket as ServerTicket } from '@deliveryforge/kanban-server';

// Resolve from project root — test file lives 4 dirs deep under project root
const projectRoot = resolve(__dirname, '../../../..');
const seedRoot = join(projectRoot, 'tests/e2e/_seed/pawplace-mini');

const kanbanConfig = JSON.parse(
  readFileSync(join(seedRoot, 'docs/planning/kanban/kanban.json'), 'utf8'),
) as KanbanConfiguration;

// ============================================================================
// HELPERS — move_ticket_server
// ============================================================================

function applyMoveTicketToStage(
  data: KanbanBoardData, ticketId: string, targetStage: string,
  config: KanbanConfiguration, definitionName?: string | null,
  options?: Parameters<KanbanBoard['moveToStage']>[4],
): KanbanBoardData {
  return new KanbanBoard(data).moveToStage(ticketId, targetStage as any, config, definitionName, options).toJSON();
}

function scatterBoundaryOnPath(
  config: KanbanConfiguration, definitionName: string | null | undefined,
  ticketScopeLevel: string, fromStage: string, toStage: string,
) {
  const empty = parseKanbanBoard({
    schema: 'abd-delivery-kanban/v2', backlog: [], active: [], done: [], archived: [], board_mode: 'automatic',
  });
  return new KanbanBoard(empty).scatterBoundaryOnPath(config, definitionName, ticketScopeLevel, fromStage as any, toStage as any);
}

function scatterRequiredForJump(
  config: KanbanConfiguration, definitionName: string | null | undefined,
  ticketScopeLevel: string, fromStage: string, toStage: string,
): string | null {
  const boundary = scatterBoundaryOnPath(config, definitionName, ticketScopeLevel, fromStage, toStage);
  if (!boundary) return null;
  return `Scope boundary at ${boundary.boundaryStage} → ${boundary.childScope}`;
}

const pawplaceIncrements = [
  {
    id: 'project-all-inc-1-find-products-and-check-store-stock',
    name: 'Find products and check store stock',
    priority: 1,
  },
];

// ============================================================================
// HELPERS — resolve_scatter_children_server
// ============================================================================

const seedPlanning = join(projectRoot, 'tests/e2e/_seed/pawplace-mini/docs/planning');
const seedEngagement = KanbanBoard.engagementWorkspaceFromPlanningRoot(seedPlanning);
const sprintFixtureEngagement = join(projectRoot, 'tests/fixtures/pawplace-sprint-resolve');

const incParent = 'project-all-inc-1-find-products-and-check-store-stock';

// ============================================================================
// HELPERS — resume_ticket_server
// ============================================================================

const shapingSkills: StageSkillRail = {
  stage: 'shaping',
  skills: [
    { skillId: 'abd-impact-mapping', label: 'Impact', role: 'ux-designer', family: 'idea-shaping' },
    { skillId: 'abd-story-mapping', label: 'Story map', role: 'product-owner', family: 'story-driven-delivery' },
  ],
};

function boardWithProjectAllInDone(): KanbanBoardData {
  return parseKanbanBoard({
    schema: 'abd-delivery-kanban/v2',
    backlog: [],
    active: [],
    done: [
      {
        ticket_id: 'project-all',
        lineage: ['PawPlace'],
        scope_level: 'all',
        stage: 'shaping',
        priority: 1,
        skill_progress: {
          'abd-impact-mapping': {
            execution_status: 'done',
            review_status: 'done',
            agent: 'ux-designer',
            reviewer: 'ux-designer',
          },
          'abd-story-mapping': {
            execution_status: 'done',
            review_status: 'done',
            agent: 'product-owner',
            reviewer: 'product-owner',
          },
        },
      },
    ],
    archived: [],
  });
}

// ============================================================================
// STORY: Move Ticket to Stage (from move_ticket_server.test.ts)
// ============================================================================

describe('Validate Board Data Structure', () => {
  it('coerces legacy notes arrays to empty string', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 't1',
          lineage: [],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          notes: [],
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });
    expect(board.active[0]!.notes).toBe('');
  });
});

describe('Scatter Ticket at Scope Boundary', () => {
  it('scatters project-all shaping → discovery into increment children', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          skill_progress: {
            'abd-story-mapping': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'product-owner',
              reviewer: 'product-owner',
            },
          },
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    const updated = applyMoveTicketToStage(
      board,
      'project-all',
      'discovery',
      kanbanConfig,
      'pawplace-mini',
      { childrenSpec: pawplaceIncrements, placement: 'stage_done' },
    );

    const parent = updated.archived.find((t: RawTicket) => t.ticket_id === 'project-all');
    expect(parent?.scatter_to).toHaveLength(1);
    const children = updated.active.filter((t: RawTicket) => t.scatter_from === 'project-all');
    expect(children).toHaveLength(1);
    expect(children.every((c: RawTicket) => c.scope_level === 'increment')).toBe(true);
    expect(children.every((c: RawTicket) => c.stage === 'discovery')).toBe(true);
    expect(
      children.every((c: RawTicket) => c.skill_progress['abd-domain-terms']?.execution_status === 'done'),
    ).toBe(true);
    expect(updated.active.some((t: RawTicket) => t.ticket_id === 'project-all')).toBe(false);
  });

  it('moves active ticket to stage Done when dropped on same stage Done column', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 'inc-1',
          lineage: ['PawPlace', 'Inc 1'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          hold_in_progress: true,
          skill_progress: {
            'abd-domain-terms': {
              execution_status: 'in_progress',
              review_status: null,
              agent: 'business-expert',
            },
          },
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    const updated = applyMoveTicketToStage(
      board,
      'inc-1',
      'discovery',
      kanbanConfig,
      'pawplace-mini',
      { placement: 'stage_done' },
    );

    const t = updated.active.find((x: RawTicket) => x.ticket_id === 'inc-1')!;
    expect(t.hold_in_progress).toBeFalsy();
    expect(t.skill_progress['abd-domain-terms']?.execution_status).toBe('in_progress');
    expect(t.skill_progress['abd-domain-terms']?.review_status).toBeNull();
    expect(t.completed_stage).toBeTruthy();
  });

  it('archived scatter parent can move to same stage Done', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [],
      done: [],
      backlog: [],
      archived: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          scatter_to: ['1-product-catalog', '2-store-operations'],
          skill_progress: { 'abd-story-mapping': { execution_status: 'done', review_status: 'done' } },
        },
      ],
    });

    const updated = applyMoveTicketToStage(
      board,
      'project-all',
      'shaping',
      kanbanConfig,
      'pawplace-mini',
      { placement: 'stage_done' },
    );

    const t = updated.active.find((x: RawTicket) => x.ticket_id === 'project-all')!;
    expect(t.completed_stage).toBeTruthy();
    expect(updated.archived.some((x: RawTicket) => x.ticket_id === 'project-all')).toBe(false);
  });

  it('pulls queued backlog ticket into active when dropped on same stage In Progress', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [],
      done: [],
      archived: [],
      backlog: [
        {
          ticket_id: 'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
          lineage: ['PawPlace', 'Click-and-collect'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 2,
          scatter_from: 'project-all',
          scatter_to: [],
          skill_progress: {},
        },
      ],
    });

    const updated = applyMoveTicketToStage(
      board,
      'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
      'discovery',
      kanbanConfig,
      'pawplace-mini',
    );

    expect(
      updated.backlog.some(
        (t: RawTicket) => t.ticket_id === 'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
      ),
    ).toBe(false);
    const t = updated.active.find(
      (x: RawTicket) => x.ticket_id === 'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
    );
    expect(t?.stage).toBe('discovery');
    expect(t?.hold_in_progress).toBe(true);
  });

  it('advances increment ticket discovery → exploration and marks skipped skills done', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 'inc-1',
          lineage: ['PawPlace', 'Inc 1'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          entered_stage: '2026-01-01T00:00:00.000Z',
          skill_progress: {
            'abd-domain-terms': {
              execution_status: 'in_progress',
              review_status: null,
              agent: 'business-expert',
            },
          },
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    const updated = applyMoveTicketToStage(
      board,
      'inc-1',
      'exploration',
      kanbanConfig,
      'pawplace-mini',
    );
    const t = updated.active.find((x: RawTicket) => x.ticket_id === 'inc-1')!;
    expect(t.stage).toBe('exploration');
    expect(t.hold_in_progress).toBe(true);
    expect(t.skill_progress).toEqual({});
    expect(t.stage_history?.some((h: { stage: string; skipped?: boolean }) => h.stage === 'discovery' && h.skipped)).toBe(true);
  });
});

describe('Advance Ticket to Next Stage (Same Scope)', () => {
  it('moves exploration ticket back to discovery In Progress', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 'inc-1',
          lineage: ['PawPlace', 'Inc 1'],
          scope_level: 'increment',
          stage: 'exploration',
          priority: 1,
          hold_in_progress: true,
          skill_progress: { 'abd-acceptance-criteria': { execution_status: 'in_progress' } },
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    const updated = applyMoveTicketToStage(
      board,
      'inc-1',
      'discovery',
      kanbanConfig,
      'pawplace-mini',
    );

    const t = updated.active.find((x: RawTicket) => x.ticket_id === 'inc-1')!;
    expect(t.stage).toBe('discovery');
    expect(t.hold_in_progress).toBe(true);
    expect(t.skill_progress).toEqual({});
  });
});

describe('Scatter Ticket at Scope Boundary — boundary detection', () => {
  it('flags all → increment boundary for project scope ticket', () => {
    const boundary = scatterBoundaryOnPath(
      kanbanConfig,
      'pawplace-mini',
      'all',
      'shaping',
      'discovery',
    );
    expect(boundary?.boundaryStage).toBe('shaping');
    expect(boundary?.childStage).toBe('discovery');
    expect(boundary?.childScope).toBe('increment');
  });
});

describe('Advance Ticket to Next Stage (Same Scope) — advanceWithoutScatter', () => {
  it('advances increment to a later stage when advanceWithoutScatter is set (no sprint scatter)', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      board_mode: 'manual',
      active: [
        {
          ticket_id: 'project-all-inc-1-find-products-and-check-store-stock',
          lineage: ['PawPlace', 'Find products'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          scatter_from: 'project-all',
          scatter_to: [],
          skill_progress: {},
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    const updated = applyMoveTicketToStage(
      board,
      'project-all-inc-1-find-products-and-check-store-stock',
      'exploration',
      kanbanConfig,
      'pawplace-mini',
      { advanceWithoutScatter: true },
    );

    const t = updated.active.find(
      (x: RawTicket) => x.ticket_id === 'project-all-inc-1-find-products-and-check-store-stock',
    )!;
    expect(t.stage).toBe('exploration');
    expect(t.scope_level).toBe('increment');
    expect(updated.archived.length).toBe(0);
  });

  it('still requires children when advanceWithoutScatter is false', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      active: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          skill_progress: {},
        },
      ],
      done: [],
      archived: [],
      backlog: [],
    });

    expect(() =>
      applyMoveTicketToStage(board, 'project-all', 'discovery', kanbanConfig, 'pawplace-mini'),
    ).toThrow(/Thin-slicing children are required/);
  });
});

describe('Scatter Ticket at Scope Boundary — scope guard', () => {
  it('returns message when boundary exists', () => {
    const msg = scatterRequiredForJump(
      kanbanConfig,
      'pawplace-mini',
      'all',
      'shaping',
      'discovery',
    );
    expect(msg).toMatch(/shaping/);
  });
});

// ============================================================================
// FROM: resolve_scatter_children_server.test.ts
// ============================================================================

describe('Scatter Ticket at Scope Boundary — workspace resolution', () => {
  it('strips docs/planning from planning root', () => {
    expect(seedEngagement.replace(/\\/g, '/')).toMatch(/pawplace-mini$/);
    expect(seedEngagement).not.toContain('docs/planning');
  });
});

describe('Scatter Ticket at Scope Boundary — resolveScatterChildren', () => {
  it('reads discovery thin-slicing for project-all → increment only', () => {
    const children = ServerTicket.resolveScatterChildren(seedEngagement, 'project-all', {
      childScope: 'increment',
    });
    expect(children).toHaveLength(1);
    expect(children[0]!.id).toBe('project-all-inc-1-find-products-and-check-store-stock');
    expect(children[0]!.id).toMatch(/^project-all-inc-\d+-/);
  });

  it('does not re-parse thin-slicing when increment parent crosses to sprint', () => {
    expect(
      ServerTicket.tryResolveScatterChildren(seedEngagement, incParent, { childScope: 'sprint' }),
    ).toBeNull();
    expect(() =>
      ServerTicket.resolveScatterChildren(seedEngagement, incParent, { childScope: 'sprint' }),
    ).toThrow(/sprint-groupings/);
  });

  it('reads sprint-groupings for increment → sprint when file exists', () => {
    const children = ServerTicket.resolveScatterChildren(sprintFixtureEngagement, incParent, {
      childScope: 'sprint',
    });
    expect(children.map((c: { id: string }) => c.id)).toEqual([
      '1-find-products-and-check-store-stock-sprint-1',
      '1-find-products-and-check-store-stock-sprint-2',
    ]);
  });

  it('returns null from tryResolve when engagement root is wrong (planning path)', () => {
    expect(
      ServerTicket.tryResolveScatterChildren(seedPlanning, 'project-all', { childScope: 'increment' }),
    ).toBeNull();
  });
});

// ============================================================================
// FROM: resume_ticket_server.test.ts
// ============================================================================

describe('Promote Backlog Ticket on Skill Claim', () => {
  it('moves ticket from done bucket to active with hold_in_progress', () => {
    const updated = new KanbanBoard(boardWithProjectAllInDone()).resumeInProgress('project-all').toJSON();
    expect(updated.done).toHaveLength(0);
    expect(updated.active).toHaveLength(1);
    expect(updated.active[0]!.ticket_id).toBe('project-all');
    expect(updated.active[0]!.hold_in_progress).toBe(true);
  });

  it('pulls archived ticket back to active with hold_in_progress', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      backlog: [],
      active: [],
      done: [],
      archived: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          skill_progress: {},
        },
      ],
    });
    const updated = new KanbanBoard(board).resumeInProgress('project-all').toJSON();
    expect(updated.archived).toHaveLength(0);
    expect(updated.active[0]!.hold_in_progress).toBe(true);
  });
});

describe('Preserve Board Mode on Ticket Move', () => {
  it('shows active ticket with all skills done in IP when hold_in_progress', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      backlog: [],
      active: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          hold_in_progress: true,
          skill_progress: {
            'abd-impact-mapping': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'ux-designer',
              reviewer: 'ux-designer',
            },
            'abd-story-mapping': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'product-owner',
              reviewer: 'product-owner',
            },
          },
        },
      ],
      done: [],
      archived: [],
    });
    const columns = new KanbanBoard(board).columnViews();
    const views = columns.flatMap((c: KanbanColumnView) => c.tickets);
    const t = views.find((v: Ticket) => v.ticketId === 'project-all')!;
    const skillIds = shapingSkills.skills.map((s: StageSkill) => s.skillId);
    expect(t.isStageSkillsComplete(skillIds)).toBe(true);
    expect(t.holdInProgress).toBe(true);

    const buckets = StageBucketLayout.build(columns, [], [shapingSkills]).buildStageBuckets();
    const shaping = buckets.get('shaping')!;
    expect(shaping.ip.map((x: Ticket) => x.ticketId)).toContain('project-all');
    expect(shaping.done.map((x: Ticket) => x.ticketId)).not.toContain('project-all');
    expect(shaping.feedsNext.map((x: Ticket) => x.ticketId)).not.toContain('project-all');
  });

  it('hold_in_progress wins over awaiting-scatter queued placement for scope all', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      backlog: [],
      active: [
        {
          ticket_id: 'project-all',
          lineage: ['PawPlace'],
          scope_level: 'all',
          stage: 'shaping',
          priority: 1,
          hold_in_progress: true,
          skill_progress: {
            'abd-impact-mapping': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'ux-designer',
              reviewer: 'ux-designer',
            },
            'abd-story-mapping': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'product-owner',
              reviewer: 'product-owner',
            },
          },
        },
      ],
      done: [],
      archived: [],
    });
    const columns = new KanbanBoard(board).columnViews();
    const buckets = StageBucketLayout.build(columns, [], [shapingSkills]).buildStageBuckets();
    const shaping = buckets.get('shaping')!;
    expect(shaping.ip.map((x: Ticket) => x.ticketId)).toContain('project-all');
    expect(shaping.feedsNext.map((x: Ticket) => x.ticketId)).not.toContain('project-all');
  });
});

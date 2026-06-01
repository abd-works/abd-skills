import { readFileSync } from 'node:fs';

import { join } from 'node:path';

import { describe, it, expect } from 'vitest';

import {

  applyMoveTicketToStage,

  parseKanbanBoard,

  scatterBoundaryOnPath,

  scatterRequiredForJump,

  type KanbanBoard,

} from '@deliveryforge/delivery-board-shared';

import type { KanbanConfiguration } from '@deliveryforge/delivery-board-shared';



const seedRoot = join(__dirname, '../e2e/_seed/pawplace-mini');



const kanbanConfig = JSON.parse(

  readFileSync(join(seedRoot, 'docs/planning/kanban/kanban.json'), 'utf8'),

) as KanbanConfiguration;



const pawplaceIncrements = [
  {
    id: 'project-all-inc-1-find-products-and-check-store-stock',
    name: 'Find products and check store stock',
    priority: 1,
  },
];



describe('parseKanbanBoard notes', () => {
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

describe('applyMoveTicketToStage forward skip', () => {

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



    const parent = updated.archived.find((t) => t.ticket_id === 'project-all');

    expect(parent?.scatter_to).toHaveLength(1);

    const children = updated.active.filter((t) => t.scatter_from === 'project-all');

    expect(children).toHaveLength(1);

    expect(children.every((c) => c.scope_level === 'increment')).toBe(true);

    expect(children.every((c) => c.stage === 'discovery')).toBe(true);

    expect(

      children.every((c) => c.skill_progress['abd-domain-terms']?.execution_status === 'done'),

    ).toBe(true);

    expect(updated.active.some((t) => t.ticket_id === 'project-all')).toBe(false);

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

    const t = updated.active.find((x) => x.ticket_id === 'inc-1')!;
    expect(t.hold_in_progress).toBeFalsy();
    expect(t.skill_progress['abd-domain-terms']?.execution_status).toBe('in_progress');
    expect(t.skill_progress['abd-domain-terms']?.review_status).toBeNull();
    expect(t.completed_stage).toBeTruthy();
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
        (t) => t.ticket_id === 'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
      ),
    ).toBe(false);
    const t = updated.active.find(
      (x) => x.ticket_id === 'project-all-inc-2-click-and-collect-purchase-online-pick-up-in-store',
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

    const t = updated.active.find((x) => x.ticket_id === 'inc-1')!;

    expect(t.stage).toBe('exploration');

    expect(t.hold_in_progress).toBe(true);
    expect(t.skill_progress).toEqual({});
    expect(t.stage_history?.some((h) => h.stage === 'discovery' && h.skipped)).toBe(true);

  });

});



describe('applyMoveTicketToStage backward', () => {
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

    const t = updated.active.find((x) => x.ticket_id === 'inc-1')!;
    expect(t.stage).toBe('discovery');
    expect(t.hold_in_progress).toBe(true);
    expect(t.skill_progress).toEqual({});
  });
});

describe('scatterBoundaryOnPath', () => {

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



describe('manual advanceWithoutScatter', () => {
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
      (x) => x.ticket_id === 'project-all-inc-1-find-products-and-check-store-stock',
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

describe('scatterRequiredForJump', () => {

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


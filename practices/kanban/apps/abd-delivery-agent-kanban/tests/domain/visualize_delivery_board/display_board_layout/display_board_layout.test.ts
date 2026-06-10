/**
 * Display Board Layout
 *
 * Epic:     Visualize Delivery Board
 * Sub-epic: Display Board Layout
 */
import { describe, expect, it } from 'vitest';
import {
  KanbanBoardLoader,
  Ticket,
  StageBucketLayout,
  type KanbanConfiguration,
  type StageSkillRail,
  type StageSkill,
} from '@deliveryforge/kanban-shared';

// Inline kanban config — exploration and specification both include
// abd-architecture-specification so skill-rail assertions run without
// depending on any external planning folder.
const kanbanConfig: KanbanConfiguration = {
  schema: 'abd-kanban-board/v1',
  definitions: {
    'test-delivery': {
      label: 'Test delivery config',
      stages: [
        {
          name: 'shaping',
          scope: 'all',
          stage_work_required: [{ skill: 'abd-story-mapping', role: 'product-owner' }],
        },
        {
          name: 'discovery',
          scope: 'increment',
          stage_work_required: [{ skill: 'abd-domain-terms', role: 'business-expert' }],
        },
        {
          name: 'exploration',
          scope: 'increment',
          stage_work_required: [
            { skill: 'abd-story-acceptance-criteria', role: 'product-owner' },
            { skill: 'abd-architecture-specification', role: 'engineer' },
          ],
        },
        {
          name: 'specification',
          scope: 'sprint',
          stage_work_required: [
            { skill: 'abd-story-specification', role: 'product-owner' },
            { skill: 'abd-architecture-specification', role: 'engineer' },
          ],
        },
        {
          name: 'engineering',
          scope: 'sprint',
          stage_work_required: [{ skill: 'abd-clean-code', role: 'engineer' }],
        },
      ],
    },
  },
};

function backlogIncrement(id: string, priority: number, scatterFrom: string) {
  return {
    ticket_id: id,
    lineage: ['Project'],
    scope_level: 'increment',
    // stage is where the ticket will go next — drives feedsNext placement
    stage: 'exploration',
    priority,
    scatter_from: scatterFrom,
    scatter_to: [],
    skill_progress: {},
  };
}

// Board state:
//   parent-alpha scattered to 3 backlog increments + 1 active-exploration increment
//   parent-beta  scattered to 4 backlog increments
const boardJson = {
  schema: 'abd-delivery-kanban/v2',
  synced_at: '2026-01-01T00:00:00Z',
  stage_configuration: 'test-delivery',
  board_mode: 'manual',
  backlog: [
    backlogIncrement('alpha-1', 1, 'parent-alpha'),
    backlogIncrement('alpha-2', 2, 'parent-alpha'),
    backlogIncrement('alpha-3', 3, 'parent-alpha'),
    backlogIncrement('beta-1', 1, 'parent-beta'),
    backlogIncrement('beta-2', 2, 'parent-beta'),
    backlogIncrement('beta-3', 3, 'parent-beta'),
    backlogIncrement('beta-4', 4, 'parent-beta'),
  ],
  active: [
    {
      ticket_id: 'alpha-ip',
      lineage: ['Project'],
      scope_level: 'increment',
      stage: 'exploration',
      priority: 1,
      scatter_from: 'parent-alpha',
      scatter_to: [],
      skill_progress: {},
      completed_stage: null,
      hold_in_progress: false,
    },
  ],
  done: [],
  archived: [
    {
      ticket_id: 'parent-alpha',
      lineage: ['Project'],
      scope_level: 'increment',
      stage: 'discovery',
      priority: 1,
      scatter_from: null,
      scatter_to: ['alpha-1', 'alpha-2', 'alpha-3', 'alpha-ip'],
      skill_progress: {},
    },
    {
      ticket_id: 'parent-beta',
      lineage: ['Project'],
      scope_level: 'increment',
      stage: 'discovery',
      priority: 2,
      scatter_from: null,
      scatter_to: ['beta-1', 'beta-2', 'beta-3', 'beta-4'],
      skill_progress: {},
    },
  ],
  team: { 'product-owner': 1, 'business-expert': 1, 'ux-designer': 1, 'engineer': 1 },
};

describe('Organize Tickets into Stage Groups by Delivery Phase', () => {
  it('puts scattered increment tickets in the stage that feeds next once they are in backlog', () => {
    const snapshot = KanbanBoardLoader.fromSources('/test-planning', boardJson, kanbanConfig);
    const buckets = StageBucketLayout.build(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    ).buildStageBuckets();

    const discovery = buckets.get('discovery')!;

    // Backlog increments with stage:exploration → discovery.feedsNext.
    // alpha-ip is in active/exploration → exploration.ip.
    const alphaTickets = [
      ...discovery.feedsNext,
      ...(buckets.get('exploration')?.ip ?? []),
    ].filter((t: Ticket) => t.scopeLevel === 'increment' && t.scatterFrom === 'parent-alpha');
    expect(alphaTickets.length).toBe(4); // 3 backlog + 1 in-progress

    const betaTickets = discovery.feedsNext.filter(
      (t: Ticket) => t.scopeLevel === 'increment' && t.scatterFrom === 'parent-beta',
    );
    expect(betaTickets.length).toBe(4);

    const explorationRail = snapshot.stageSkillRails.find(
      (r: StageSkillRail) => r.stage === 'exploration',
    );
    expect(explorationRail?.skills.map((s: StageSkill) => s.skillId)).toContain(
      'abd-architecture-specification',
    );

    const specRail = snapshot.stageSkillRails.find(
      (r: StageSkillRail) => r.stage === 'specification',
    );
    expect(specRail?.skills.map((s: StageSkill) => s.skillId)).toContain(
      'abd-architecture-specification',
    );
  });

  it('puts exploration increments in Exploration IP when pulled active', () => {
    const snapshot = KanbanBoardLoader.fromSources('/test-planning', boardJson, kanbanConfig);
    const buckets = StageBucketLayout.build(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    ).buildStageBuckets();

    const exploration = buckets.get('exploration')!;
    expect(exploration.ip.length).toBeGreaterThanOrEqual(1);
    expect(exploration.ip.some((t: Ticket) => t.ticketId.startsWith('alpha-'))).toBe(true);
  });
});

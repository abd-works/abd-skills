import { describe, it, expect } from 'vitest';
import {
  KanbanBoard,
  buildColumnViews,
  isSkillComplete,
  parseKanbanBoard,
  StageBucketLayout,
  Ticket,
  type KanbanBoardData,
  type StageSkillRail,
} from '@deliveryforge/delivery-board-shared';

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

describe('resumeInProgress (KanbanBoard instance)', () => {
  it('moves ticket from done bucket to active with hold_in_progress', () => {
    const board = new KanbanBoard(boardWithProjectAllInDone());
    const updated = board.resumeInProgress('project-all').toJSON();
    expect(updated.done).toHaveLength(0);
    expect(updated.active).toHaveLength(1);
    expect(updated.active[0]!.ticket_id).toBe('project-all');
    expect(updated.active[0]!.hold_in_progress).toBe(true);
  });

  it('pulls archived ticket back to active with hold_in_progress', () => {
    const data = parseKanbanBoard({
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
    const board = new KanbanBoard(data);
    const updated = board.resumeInProgress('project-all').toJSON();
    expect(updated.archived).toHaveLength(0);
    expect(updated.active[0]!.hold_in_progress).toBe(true);
  });
});

function isStageSkillsComplete(ticket: Ticket, skillIds: string[]): boolean {
  return skillIds.every((id) => {
    const sp = ticket.raw.skill_progress[id];
    return sp ? isSkillComplete(sp) : false;
  });
}

describe('buildStageBuckets hold_in_progress', () => {
  it('shows active ticket with all skills done in IP when hold_in_progress', () => {
    const data = parseKanbanBoard({
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
    const columns = buildColumnViews(data);
    const views = columns.flatMap((c) => c.tickets);
    const t = views.find((v) => v.ticketId === 'project-all')!;
    const skillIds = shapingSkills.skills.map((s) => s.skillId);
    expect(isStageSkillsComplete(t, skillIds)).toBe(true);
    expect(t.holdInProgress).toBe(true);

    const buckets = StageBucketLayout.buildStageBuckets(columns, [], [shapingSkills]);
    const shaping = buckets.get('shaping')!;
    expect(shaping.ip.map((x) => x.ticketId)).toContain('project-all');
    expect(shaping.done.map((x) => x.ticketId)).not.toContain('project-all');
    expect(shaping.feedsNext.map((x) => x.ticketId)).not.toContain('project-all');
  });

  it('hold_in_progress wins over awaiting-scatter queued placement for scope all', () => {
    const data = parseKanbanBoard({
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
    const columns = buildColumnViews(data);
    const buckets = StageBucketLayout.buildStageBuckets(columns, [], [shapingSkills]);
    const shaping = buckets.get('shaping')!;
    expect(shaping.ip.map((x) => x.ticketId)).toContain('project-all');
    expect(shaping.feedsNext.map((x) => x.ticketId)).not.toContain('project-all');
  });
});

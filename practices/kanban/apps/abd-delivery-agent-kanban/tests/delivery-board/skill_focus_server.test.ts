/**
 * Skill focus and row indicator tests
 *
 * Stories: Show Focus Skill on In-Progress Ticket,
 *          Show Skill Execution and Completion Indicators
 */
import { describe, expect, it } from 'vitest';
import {
  resolveFocusSkillId,
  resolveDisplayFocusSkillId,
  resolveWorkingAgent,
  countRoleEngagement,
  resolvePoolAvatarState,
  HEARTBEAT_STALE_SECS,
  skillRowDisplayState,
  ticketShowsLiveSkillIcon,
  relocateScatterParents,
  isScatterParent,
  scopeLevelCssClass,
  parseKanbanBoard,
  SkillProgressSchema,
  STAGE_ORDER,
  type StageBucket,
  type StageId,
  type StageSkill,
  type TicketView,
} from '@deliveryforge/delivery-board-shared';

const SPEC_SKILLS = [
  'abd-class-responsibility-collaborator',
  'abd-specification-by-example',
  'abd-scenario-walkthrough',
];

const SPEC_STAGE_SKILLS: StageSkill[] = [
  {
    skillId: 'abd-class-responsibility-collaborator',
    label: 'CRC',
    family: 'domain-driven-design',
    role: 'business-expert',
  },
  {
    skillId: 'abd-specification-by-example',
    label: 'spec by example',
    family: 'story-driven-delivery',
    role: 'product-owner',
  },
  {
    skillId: 'abd-scenario-walkthrough',
    label: 'scenario walkthrough',
    family: 'domain-driven-design',
    role: 'business-expert',
  },
];

const PAWPLACE_TEAM = {
  'product-owner': 1,
  'business-expert': 2,
  'ux-designer': 1,
  engineer: 1,
};

function ticket(partial: Partial<TicketView> & Pick<TicketView, 'ticketId'>): TicketView {
  return {
    ticketId: partial.ticketId,
    lineage: partial.lineage ?? [partial.ticketId],
    scopeLevel: partial.scopeLevel ?? 'sprint',
    stage: partial.stage ?? 'specification',
    column: partial.column ?? 'active',
    priority: partial.priority ?? 1,
    activeSkillId: partial.activeSkillId ?? null,
    activeAgent: partial.activeAgent ?? null,
    executingSkillIds: partial.executingSkillIds ?? [],
    reviewSkillId: partial.reviewSkillId ?? null,
    reviewAgent: partial.reviewAgent ?? null,
    reviewingSkillIds: partial.reviewingSkillIds ?? [],
    awaitingReviewSkillId: partial.awaitingReviewSkillId ?? null,
    awaitingReviewAgent: partial.awaitingReviewAgent ?? null,
    awaitingReviewSkillIds: partial.awaitingReviewSkillIds ?? [],
    isReviewing: partial.isReviewing ?? false,
    doneSkillIds: partial.doneSkillIds ?? [],
    failedReviewSkillIds: partial.failedReviewSkillIds ?? [],
    enteredStage: partial.enteredStage ?? null,
    completedStage: partial.completedStage ?? null,
    scatterFrom: partial.scatterFrom ?? null,
    scatterTo: partial.scatterTo ?? [],
    notes: partial.notes ?? '',
    displayLabel: partial.displayLabel ?? partial.ticketId,
    chipLabel: partial.chipLabel ?? partial.ticketId,
    pendingIntentSkillIds: partial.pendingIntentSkillIds ?? [],
    holdInProgress: partial.holdInProgress ?? false,
  };
}

describe('resolveFocusSkillId', () => {
  it('returns review skill when review is in progress', () => {
    const t = ticket({
      ticketId: 't1',
      reviewSkillId: 'abd-specification-by-example',
      isReviewing: true,
    });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, 'ip')).toBe('abd-specification-by-example');
  });

  it('returns executing skill when execution is in progress', () => {
    const t = ticket({
      ticketId: 't2',
      activeSkillId: 'abd-specification-by-example',
      activeAgent: 'product-owner',
    });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, 'ip')).toBe('abd-specification-by-example');
  });

  it('returns next incomplete stage skill when active in In Progress between skills', () => {
    const t = ticket({
      ticketId: 'inc-8-sprint-2',
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, 'ip')).toBe('abd-specification-by-example');
  });

  it('returns null for global backlog tickets', () => {
    const t = ticket({ ticketId: 't3', column: 'backlog', stage: null });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, undefined)).toBeNull();
  });

  it('returns next skill for staged backlog shown in prev stage done', () => {
    const t = ticket({
      ticketId: 'inc-8-sprint-3',
      column: 'backlog',
      stage: 'specification',
      doneSkillIds: [],
    });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, 'feeds-next')).toBe(
      'abd-class-responsibility-collaborator',
    );
  });

  it('returns null when all stage skills are done in Done sub-column', () => {
    const t = ticket({
      ticketId: 't4',
      doneSkillIds: [...SPEC_SKILLS],
    });
    expect(resolveFocusSkillId(t, SPEC_SKILLS, 'done')).toBeNull();
  });
});

describe('resolveDisplayFocusSkillId', () => {
  it('limits idle PO focus to team capacity across active peers', () => {
    const sprint1 = ticket({
      ticketId: 'inc-8-sprint-1-reviews',
      priority: 1,
      doneSkillIds: [
        'abd-class-responsibility-collaborator',
        'abd-specification-by-example',
      ],
    });
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    const sprint9 = ticket({
      ticketId: 'inc-9-sprint-1-search',
      priority: 5,
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    const peers = [sprint1, sprint2, sprint9];

    expect(
      resolveDisplayFocusSkillId(sprint1, SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-scenario-walkthrough');
    expect(
      resolveDisplayFocusSkillId(sprint2, SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-specification-by-example');
    expect(
      resolveDisplayFocusSkillId(sprint9, SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBeNull();
  });

  it('always shows live execution focus regardless of WIP rank', () => {
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      activeSkillId: 'abd-specification-by-example',
      activeAgent: 'product-owner',
    });
    const sprint9 = ticket({
      ticketId: 'inc-9-sprint-1-search',
      priority: 5,
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    const peers = [sprint2, sprint9];

    expect(
      resolveDisplayFocusSkillId(sprint2, SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-specification-by-example');
  });
});

describe('resolvePoolAvatarState', () => {
  it('shows working for engaged slots even without heartbeat', () => {
    expect(resolvePoolAvatarState(0, 1, null)).toBe('working');
    expect(resolvePoolAvatarState(1, 1, null)).toBe('idle');
  });

  it('shows idle when no heartbeat and role not engaged', () => {
    expect(resolvePoolAvatarState(0, 0, null)).toBe('idle');
  });

  it('shows inactive only when heartbeat is stale and role not engaged', () => {
    expect(resolvePoolAvatarState(0, 0, 180)).toBe('inactive');
    expect(resolvePoolAvatarState(0, 1, 180)).toBe('working');
  });

  it('shows idle for ready agent instance (alive but not on a skill)', () => {
    expect(resolvePoolAvatarState(1, 1, 30, HEARTBEAT_STALE_SECS, 'ready')).toBe(
      'idle',
    );
    expect(resolvePoolAvatarState(1, 1, 180, HEARTBEAT_STALE_SECS, 'ready')).toBe(
      'inactive',
    );
  });

  it('shows idle when heartbeat timestamp is in the future (negative age)', () => {
    expect(resolvePoolAvatarState(0, 0, -5000, HEARTBEAT_STALE_SECS, 'ready')).toBe(
      'idle',
    );
  });

  it('shows working only when heartbeat status is working', () => {
    expect(resolvePoolAvatarState(0, 0, 30, HEARTBEAT_STALE_SECS, 'working')).toBe(
      'working',
    );
  });
});

describe('countRoleEngagement', () => {
  it('counts only live execution or review — not idle queued active tickets', () => {
    const sprint1 = ticket({
      ticketId: 'inc-8-sprint-1-reviews',
      priority: 1,
      doneSkillIds: [
        'abd-class-responsibility-collaborator',
        'abd-specification-by-example',
      ],
    });
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      activeSkillId: 'abd-class-responsibility-collaborator',
      activeAgent: 'business-expert',
    });
    const columnViews = [
      {
        id: 'active' as const,
        label: 'Active',
        tickets: [sprint1, sprint2],
      },
    ];
    const stageSkillRails = [
      { stage: 'specification' as const, skills: SPEC_STAGE_SKILLS },
    ];

    const counts = countRoleEngagement(columnViews, stageSkillRails, PAWPLACE_TEAM);
    expect(counts['business-expert']).toBe(1);
    expect(counts['product-owner']).toBe(0);
    expect(counts['ux-designer']).toBe(0);
    expect(counts.engineer).toBe(0);
  });
});

describe('skillRowDisplayState', () => {
  it('shows checkmark row only for completed skills', () => {
    const t = ticket({
      ticketId: 't5',
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    const done = skillRowDisplayState('abd-class-responsibility-collaborator', t, null);
    expect(done.isDone).toBe(true);
    expect(done.showBot).toBe(false);
    expect(done.showMagnify).toBe(false);
  });

  it('highlights focus skill without bot when queued next up', () => {
    const t = ticket({
      ticketId: 't6',
      doneSkillIds: ['abd-class-responsibility-collaborator'],
    });
    const focusId = resolveFocusSkillId(t, SPEC_SKILLS, 'ip')!;
    const next = skillRowDisplayState('abd-specification-by-example', t, focusId);
    expect(next.showBot).toBe(false);
    expect(next.showMagnify).toBe(false);
    expect(next.isFocus).toBe(true);
  });

  it('shows magnify when skill is in reviewingSkillIds', () => {
    const t = ticket({
      ticketId: 't7b',
      reviewingSkillIds: ['abd-specification-by-example'],
      isReviewing: true,
      reviewAgent: 'product-owner',
    });
    const row = skillRowDisplayState('abd-specification-by-example', t, null);
    expect(row.showMagnify).toBe(true);
    expect(row.showBot).toBe(false);
  });

  it('shows magnify on review skill only', () => {
    const t = ticket({
      ticketId: 't7',
      reviewSkillId: 'abd-specification-by-example',
      reviewingSkillIds: ['abd-specification-by-example'],
      isReviewing: true,
      reviewAgent: 'product-owner',
    });
    const focusId = resolveFocusSkillId(t, SPEC_SKILLS, 'ip')!;
    const review = skillRowDisplayState('abd-specification-by-example', t, focusId);
    const crc = skillRowDisplayState('abd-class-responsibility-collaborator', t, focusId);
    expect(review.showMagnify).toBe(true);
    expect(review.showBot).toBe(false);
    expect(crc.showBot).toBe(false);
    expect(crc.showMagnify).toBe(false);
  });
});

describe('resolveWorkingAgent', () => {
  it('returns agent only when execution is in progress', () => {
    const t = ticket({
      ticketId: 'w1',
      activeSkillId: 'abd-specification-by-example',
      activeAgent: 'product-owner',
    });
    expect(resolveWorkingAgent(t)).toBe('product-owner');
  });

  it('returns reviewer role when review is in progress (legacy *-reviewer id)', () => {
    const t = ticket({
      ticketId: 'w2b',
      reviewSkillId: 'abd-class-responsibility-collaborator',
      reviewAgent: 'business-expert-reviewer',
      isReviewing: true,
    });
    expect(resolveWorkingAgent(t)).toBe('business-expert');
  });

  it('returns reviewer only when review is in progress', () => {
    const t = ticket({
      ticketId: 'w2',
      reviewSkillId: 'abd-specification-by-example',
      reviewAgent: 'product-owner',
      isReviewing: true,
    });
    expect(resolveWorkingAgent(t)).toBe('product-owner');
  });

  it('returns null when focus skill is next up but no live work', () => {
    const t = ticket({
      ticketId: 'w3',
      doneSkillIds: ['abd-class-responsibility-collaborator'],
      activeAgent: null,
      reviewAgent: null,
    });
    expect(resolveWorkingAgent(t)).toBeNull();
  });

  it('returns null when execution done and only awaiting review', () => {
    const t = ticket({
      ticketId: 'w4',
      awaitingReviewSkillId: 'abd-specification-by-example',
      activeAgent: 'product-owner',
      reviewAgent: 'product-owner',
    });
    expect(resolveWorkingAgent(t)).toBeNull();
  });
});

describe('ticketShowsLiveSkillIcon', () => {
  it('hides icon on IP sub-column when no skill is actively executing or under review', () => {
    const t = ticket({
      ticketId: 't8',
      doneSkillIds: ['abd-class-responsibility-collaborator'],
      activeAgent: null,
      reviewAgent: null,
    });
    const focusId = resolveFocusSkillId(t, SPEC_SKILLS, 'ip');
    expect(ticketShowsLiveSkillIcon(t, focusId, 'ip')).toBe(false);
  });

  it('feeds-next backlog resolves focus but never shows icon on card face', () => {
    const t = ticket({
      ticketId: 't8b',
      column: 'backlog',
      stage: 'specification',
      doneSkillIds: [],
    });
    const focusId = resolveFocusSkillId(t, SPEC_SKILLS, 'feeds-next');
    expect(focusId).toBe('abd-class-responsibility-collaborator');
    expect(ticketShowsLiveSkillIcon(t, focusId, 'feeds-next')).toBe(false);
  });

  it('shows icon on active ticket while skill is executing', () => {
    const t = ticket({
      ticketId: 't8c',
      activeSkillId: 'abd-class-responsibility-collaborator',
      activeAgent: 'business-expert',
    });
    const focusId = resolveFocusSkillId(t, SPEC_SKILLS, 'ip');
    expect(ticketShowsLiveSkillIcon(t, focusId, 'ip')).toBe(true);
  });

  it('hides icon for non-active tickets without feeds-next', () => {
    const t = ticket({ ticketId: 't9', column: 'archived' });
    expect(ticketShowsLiveSkillIcon(t, 'abd-specification-by-example')).toBe(false);
  });
});

describe('relocateScatterParents', () => {
  it('moves scatter parent to top of column containing trailing child', () => {
    const parent = ticket({
      ticketId: 'inc-parent',
      column: 'archived',
      stage: 'exploration',
      scopeLevel: 'increment',
      scatterTo: ['child-a', 'child-b'],
    });
    const childA = ticket({
      ticketId: 'child-a',
      stage: 'engineering',
      scatterFrom: 'inc-parent',
      priority: 1,
    });
    const childB = ticket({
      ticketId: 'child-b',
      stage: 'engineering',
      scatterFrom: 'inc-parent',
      priority: 2,
    });

    const buckets = new Map<StageId, StageBucket>();
    for (const stage of STAGE_ORDER) {
      buckets.set(stage, { ip: [], done: [], feedsNext: [] });
    }
    buckets.get('exploration')!.done.push(parent);
    buckets.get('engineering')!.feedsNext.push(childA, childB);

    relocateScatterParents(buckets, [parent]);

    expect(buckets.get('exploration')!.done).toHaveLength(0);
    expect(buckets.get('engineering')!.feedsNext[0]!.ticketId).toBe('inc-parent');
    expect(isScatterParent(buckets.get('engineering')!.feedsNext[0]!)).toBe(true);
    expect(buckets.get('engineering')!.feedsNext.map((t) => t.ticketId)).toEqual([
      'inc-parent',
      'child-a',
      'child-b',
    ]);
  });

  it('project scatter parent stays with trailing increment (IP before done, on top)', () => {
    const parent = ticket({
      ticketId: 'project-all',
      column: 'archived',
      stage: 'discovery',
      scopeLevel: 'all',
      scatterTo: ['1-walk-in-driver', '2-click-and-collect'],
    });
    const childA = ticket({
      ticketId: '1-walk-in-driver',
      column: 'active',
      stage: 'exploration',
      scopeLevel: 'increment',
      scatterFrom: 'project-all',
      priority: 1,
      activeSkillId: 'abd-ux-mockup',
      activeAgent: 'ux-designer',
    });
    const childB = ticket({
      ticketId: '2-click-and-collect',
      column: 'active',
      stage: 'exploration',
      scopeLevel: 'increment',
      scatterFrom: 'project-all',
      priority: 2,
      doneSkillIds: ['abd-ubiquitous-language', 'abd-acceptance-criteria'],
    });

    const buckets = new Map<StageId, StageBucket>();
    for (const stage of STAGE_ORDER) {
      buckets.set(stage, { ip: [], done: [], feedsNext: [] });
    }
    buckets.get('discovery')!.done.push(parent);
    buckets.get('exploration')!.ip.push(childA);
    buckets.get('exploration')!.done.push(childB);

    relocateScatterParents(buckets, [parent]);

    expect(buckets.get('discovery')!.done).toHaveLength(0);
    expect(buckets.get('exploration')!.ip.map((t) => t.ticketId)).toEqual([
      'project-all',
      '1-walk-in-driver',
    ]);
    expect(buckets.get('exploration')!.done.map((t) => t.ticketId)).toEqual([
      '2-click-and-collect',
    ]);
  });

  it('project follows increments after they relocate beside sprint children', () => {
    const project = ticket({
      ticketId: 'project-all',
      column: 'archived',
      stage: 'discovery',
      scopeLevel: 'all',
      scatterTo: ['1-walk-in-driver', '2-click-and-collect'],
    });
    const walkIn = ticket({
      ticketId: '1-walk-in-driver',
      column: 'archived',
      stage: 'exploration',
      scopeLevel: 'increment',
      scatterTo: ['1-walk-in-driver-sprint-2'],
      priority: 1,
    });
    const clickCollect = ticket({
      ticketId: '2-click-and-collect',
      column: 'archived',
      stage: 'exploration',
      scopeLevel: 'increment',
      scatterTo: ['2-click-and-collect-sprint-2', '2-click-and-collect-sprint-3'],
      priority: 2,
    });
    const walkInSprint2 = ticket({
      ticketId: '1-walk-in-driver-sprint-2',
      stage: 'engineering',
      scatterFrom: '1-walk-in-driver',
      priority: 2,
      activeSkillId: 'abd-interface-design',
      activeAgent: 'ux-designer',
    });
    const ccSprint2 = ticket({
      ticketId: '2-click-and-collect-sprint-2',
      stage: 'specification',
      scatterFrom: '2-click-and-collect',
      priority: 2,
    });
    const ccSprint3 = ticket({
      ticketId: '2-click-and-collect-sprint-3',
      stage: 'specification',
      scatterFrom: '2-click-and-collect',
      priority: 3,
    });

    const buckets = new Map<StageId, StageBucket>();
    for (const stage of STAGE_ORDER) {
      buckets.set(stage, { ip: [], done: [], feedsNext: [] });
    }
    buckets.get('discovery')!.done.push(project);
    buckets.get('exploration')!.done.push(walkIn, clickCollect);
    buckets.get('engineering')!.ip.push(walkInSprint2);
    buckets.get('specification')!.feedsNext.push(ccSprint2, ccSprint3);

    relocateScatterParents(buckets, [project, walkIn, clickCollect]);

    expect(buckets.get('discovery')!.done).toHaveLength(0);
    expect(buckets.get('specification')!.feedsNext.map((t) => t.ticketId)).toEqual([
      'project-all',
      '2-click-and-collect',
      '2-click-and-collect-sprint-2',
      '2-click-and-collect-sprint-3',
    ]);
    expect(buckets.get('engineering')!.ip.map((t) => t.ticketId)).toEqual([
      '1-walk-in-driver',
      '1-walk-in-driver-sprint-2',
    ]);
  });
});

describe('scopeLevelCssClass', () => {
  it('maps scope_level to ticket CSS classes', () => {
    expect(scopeLevelCssClass('project')).toBe('kb-ticket--scope-project');
    expect(scopeLevelCssClass('all')).toBe('kb-ticket--scope-project');
    expect(scopeLevelCssClass('partition')).toBe('kb-ticket--scope-partition');
    expect(scopeLevelCssClass('increment')).toBe('kb-ticket--scope-increment');
    expect(scopeLevelCssClass('sprint')).toBe('kb-ticket--scope-sprint');
    expect(scopeLevelCssClass('unknown')).toBe('kb-ticket--scope-sprint');
  });
});

describe('SkillProgressSchema', () => {
  it('coerces execution_status pending to not_started', () => {
    const parsed = SkillProgressSchema.parse({ execution_status: 'pending' });
    expect(parsed.execution_status).toBe('not_started');
  });

  it('coerces review_status not_started to null', () => {
    const parsed = SkillProgressSchema.parse({
      execution_status: 'done',
      review_status: 'not_started',
    });
    expect(parsed.review_status).toBeNull();
  });

  it('parses board.json with legacy pending execution_status', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      backlog: [],
      active: [
        {
          ticket_id: 't1',
          stage: 'engineering',
          skill_progress: {
            'abd-interface-design': { execution_status: 'pending', agent: 'ux-designer' },
          },
        },
      ],
      done: [],
      archived: [],
      team: { engineer: 1 },
    });
    expect(
      board.active[0].skill_progress['abd-interface-design'].execution_status,
    ).toBe('not_started');
  });
});

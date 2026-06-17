/**
 * Inspect Skill Progress
 *
 * Epic:     Visualize Delivery Board
 * Sub-epic: Inspect Skill Progress
 */
import { describe, expect, it } from 'vitest';
import {
  Ticket,
  StageBucketLayout,
  parseKanbanBoard,
  SkillProgressSchema,
  type AgentSessionInfo,
  type KanbanColumn,
  type KanbanColumnView,
  type StageSkill,
  type StageSkillRail,
  type RawTicket,
  type SkillProgress,
} from '@deliveryforge/kanban-shared';

const SPEC_SKILLS = [
  'abd-domain-model',
  'abd-story-specification',
  'abd-domain-walk',
];

const SPEC_STAGE_SKILLS: StageSkill[] = [
  {
    skillId: 'abd-domain-model',
    label: 'domain model',
    family: 'domain-driven-design',
    role: 'business-expert',
  },
  {
    skillId: 'abd-story-specification',
    label: 'spec by example',
    family: 'story-driven-delivery',
    role: 'product-owner',
  },
  {
    skillId: 'abd-domain-walk',
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

type TicketInput = {
  ticketId: string;
  lineage?: string[];
  scopeLevel?: string;
  stage?: string | null;
  column?: KanbanColumn;
  priority?: number;
  doneSkillIds?: string[];
  activeSkillId?: string | null;
  activeAgent?: string | null;
  executingSkillIds?: string[];
  reviewSkillId?: string | null;
  reviewAgent?: string | null;
  reviewingSkillIds?: string[];
  awaitingReviewSkillId?: string | null;
  failedReviewSkillIds?: string[];
  pendingIntentSkillIds?: string[];
  enteredStage?: string | null;
  completedStage?: string | null;
  scatterFrom?: string | null;
  scatterTo?: string[];
  notes?: string;
  holdInProgress?: boolean;
};

function buildSkillProgress(input: TicketInput): Record<string, SkillProgress> {
  const sp: Record<string, SkillProgress> = {};

  for (const id of input.doneSkillIds ?? []) {
    sp[id] = { execution_status: 'done', review_status: 'done' };
  }

  const executing = new Set(input.executingSkillIds ?? []);
  if (input.activeSkillId) executing.add(input.activeSkillId);
  for (const id of executing) {
    sp[id] = { execution_status: 'in_progress', agent: input.activeAgent };
  }

  const reviewing = new Set(input.reviewingSkillIds ?? []);
  if (input.reviewSkillId) reviewing.add(input.reviewSkillId);
  for (const id of reviewing) {
    sp[id] = {
      execution_status: 'done',
      review_status: 'in_progress',
      agent: input.reviewAgent,
      reviewer: input.reviewAgent,
    };
  }

  const awaiting = new Set<string>();
  if (input.awaitingReviewSkillId) awaiting.add(input.awaitingReviewSkillId);
  for (const id of awaiting) {
    if (!sp[id]) sp[id] = { execution_status: 'done' };
  }

  for (const id of input.failedReviewSkillIds ?? []) {
    if (!sp[id]) sp[id] = { execution_status: 'done', review_status: 'failed' };
    else sp[id] = { ...sp[id], review_status: 'failed' };
  }

  return sp;
}

function ticket(input: TicketInput): Ticket {
  const raw: RawTicket = {
    ticket_id: input.ticketId,
    lineage: input.lineage ?? [input.ticketId],
    scope_level: input.scopeLevel ?? 'sprint',
    stage: input.stage === null ? '_none' : input.stage ?? 'specification',
    priority: input.priority ?? 1,
    skill_progress: buildSkillProgress(input),
    entered_stage: input.enteredStage ?? null,
    completed_stage: input.completedStage ?? null,
    scatter_from: input.scatterFrom ?? null,
    scatter_to: input.scatterTo ?? [],
    notes: input.notes ?? '',
    stage_history: [],
    hold_in_progress: input.holdInProgress,
  };
  const entity = new Ticket(raw, input.column ?? 'active');
  if (input.pendingIntentSkillIds) {
    entity.pendingIntentSkillIds = input.pendingIntentSkillIds;
  }
  return entity;
}

describe('resolveFocusSkillId', () => {
  it('returns review skill when review is in progress', () => {
    const t = ticket({
      ticketId: 't1',
      reviewSkillId: 'abd-story-specification',
      reviewAgent: 'product-owner',
    });
    expect(t.focusSkillId(SPEC_SKILLS, 'ip')).toBe('abd-story-specification');
  });

  it('returns executing skill when execution is in progress', () => {
    const t = ticket({
      ticketId: 't2',
      activeSkillId: 'abd-story-specification',
      activeAgent: 'product-owner',
    });
    expect(t.focusSkillId(SPEC_SKILLS, 'ip')).toBe('abd-story-specification');
  });

  it('returns next incomplete stage skill when active in In Progress between skills', () => {
    const t = ticket({
      ticketId: 'inc-8-sprint-2',
      doneSkillIds: ['abd-domain-model'],
    });
    expect(t.focusSkillId(SPEC_SKILLS, 'ip')).toBe('abd-story-specification');
  });

  it('returns null for global backlog tickets', () => {
    const t = ticket({ ticketId: 't3', column: 'backlog', stage: null });
    expect(t.focusSkillId(SPEC_SKILLS, undefined)).toBeNull();
  });

  it('returns next skill for staged backlog shown in prev stage done', () => {
    const t = ticket({
      ticketId: 'inc-8-sprint-3',
      column: 'backlog',
      stage: 'specification',
      doneSkillIds: [],
    });
    expect(t.focusSkillId(SPEC_SKILLS, 'feeds-next')).toBe(
      'abd-domain-model',
    );
  });

  it('returns null when all stage skills are done in Done sub-column', () => {
    const t = ticket({
      ticketId: 't4',
      doneSkillIds: [...SPEC_SKILLS],
    });
    expect(t.focusSkillId(SPEC_SKILLS, 'done')).toBeNull();
  });
});

describe('resolveDisplayFocusSkillId', () => {
  it('limits idle PO focus to team capacity across active peers', () => {
    const sprint1 = ticket({
      ticketId: 'inc-8-sprint-1-reviews',
      priority: 1,
      doneSkillIds: [
        'abd-domain-model',
        'abd-story-specification',
      ],
    });
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      doneSkillIds: ['abd-domain-model'],
    });
    const sprint9 = ticket({
      ticketId: 'inc-9-sprint-1-search',
      priority: 5,
      doneSkillIds: ['abd-domain-model'],
    });
    const peers = [sprint1, sprint2, sprint9];

    expect(
      sprint1.displayFocusSkillId(SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-domain-walk');
    expect(
      sprint2.displayFocusSkillId(SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-story-specification');
    expect(
      sprint9.displayFocusSkillId(SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBeNull();
  });

  it('always shows live execution focus regardless of WIP rank', () => {
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      activeSkillId: 'abd-story-specification',
      activeAgent: 'product-owner',
    });
    const sprint9 = ticket({
      ticketId: 'inc-9-sprint-1-search',
      priority: 5,
      doneSkillIds: ['abd-domain-model'],
    });
    const peers = [sprint2, sprint9];

    expect(
      sprint2.displayFocusSkillId(SPEC_STAGE_SKILLS, 'ip', peers, PAWPLACE_TEAM),
    ).toBe('abd-story-specification');
  });
});

describe('resolveSlotState', () => {
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

  it('shows working for engaged slots regardless of session state', () => {
    expect(resolveSlotState(0, 1, undefined)).toBe('working');
    expect(resolveSlotState(1, 1, undefined)).toBe('idle');
  });

  it('shows idle when no session and role not engaged', () => {
    expect(resolveSlotState(0, 0, undefined)).toBe('idle');
  });

  it('shows working when session is running even without board engagement', () => {
    expect(resolveSlotState(0, 0, makeSession('running'))).toBe('working');
    expect(resolveSlotState(0, 1, makeSession('failed'))).toBe('working');
  });

  it('shows inactive when session completed or failed with no engagement', () => {
    expect(resolveSlotState(0, 0, makeSession('completed'))).toBe('inactive');
    expect(resolveSlotState(0, 0, makeSession('failed'))).toBe('inactive');
  });

  it('engagement wins over failed session for the engaged slot', () => {
    expect(resolveSlotState(0, 1, makeSession('failed'))).toBe('working');
  });
});

describe('countRoleEngagement', () => {
  it('counts only live execution or review — not idle queued active tickets', () => {
    const sprint1 = ticket({
      ticketId: 'inc-8-sprint-1-reviews',
      priority: 1,
      doneSkillIds: [
        'abd-domain-model',
        'abd-story-specification',
      ],
    });
    const sprint2 = ticket({
      ticketId: 'inc-8-sprint-2-preferences',
      priority: 2,
      activeSkillId: 'abd-domain-model',
      activeAgent: 'business-expert',
    });
    const columnViews: KanbanColumnView[] = [
      {
        id: 'active' as const,
        label: 'Active',
        tickets: [sprint1, sprint2],
      },
    ];

    const counts = Ticket.countRoleEngagement(columnViews);
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
      doneSkillIds: ['abd-domain-model'],
    });
    const done = t.skillRowDisplayState('abd-domain-model', null);
    expect(done.isDone).toBe(true);
    expect(done.showBot).toBe(false);
    expect(done.showMagnify).toBe(false);
  });

  it('highlights focus skill without bot when queued next up', () => {
    const t = ticket({
      ticketId: 't6',
      doneSkillIds: ['abd-domain-model'],
    });
    const focusId = t.focusSkillId(SPEC_SKILLS, 'ip')!;
    const next = t.skillRowDisplayState('abd-story-specification', focusId);
    expect(next.showBot).toBe(false);
    expect(next.showMagnify).toBe(false);
    expect(next.isFocus).toBe(true);
  });

  it('shows magnify when skill is in reviewingSkillIds', () => {
    const t = ticket({
      ticketId: 't7b',
      reviewingSkillIds: ['abd-story-specification'],
      reviewAgent: 'product-owner',
    });
    const row = t.skillRowDisplayState('abd-story-specification', null);
    expect(row.showMagnify).toBe(true);
    expect(row.showBot).toBe(false);
  });

  it('shows magnify on review skill only', () => {
    const t = ticket({
      ticketId: 't7',
      reviewSkillId: 'abd-story-specification',
      reviewingSkillIds: ['abd-story-specification'],
      reviewAgent: 'product-owner',
    });
    const focusId = t.focusSkillId(SPEC_SKILLS, 'ip')!;
    const review = t.skillRowDisplayState('abd-story-specification', focusId);
    const domainModel = t.skillRowDisplayState('abd-domain-model', focusId);
    expect(review.showMagnify).toBe(true);
    expect(review.showBot).toBe(false);
    expect(domainModel.showBot).toBe(false);
    expect(domainModel.showMagnify).toBe(false);
  });

  it('shows bot while executing even when stale intent still lists the skill', () => {
    const t = ticket({
      ticketId: 't7c',
      activeSkillId: 'abd-story-specification',
      executingSkillIds: ['abd-story-specification'],
      activeAgent: 'product-owner',
      pendingIntentSkillIds: ['abd-story-specification'],
    });
    const row = t.skillRowDisplayState('abd-story-specification', null);
    expect(row.showBot).toBe(true);
    expect(row.showPendingIntent).toBe(false);
  });
});

describe('resolveWorkingAgent', () => {
  it('returns agent only when execution is in progress', () => {
    const t = ticket({
      ticketId: 'w1',
      activeSkillId: 'abd-story-specification',
      activeAgent: 'product-owner',
    });
    expect(t.workingAgent()).toBe('product-owner');
  });

  it('returns reviewer role when review is in progress (legacy *-reviewer id)', () => {
    const t = ticket({
      ticketId: 'w2b',
      reviewSkillId: 'abd-domain-model',
      reviewAgent: 'business-expert-reviewer',
    });
    expect(t.workingAgent()).toBe('business-expert');
  });

  it('returns reviewer only when review is in progress', () => {
    const t = ticket({
      ticketId: 'w2',
      reviewSkillId: 'abd-story-specification',
      reviewAgent: 'product-owner',
    });
    expect(t.workingAgent()).toBe('product-owner');
  });

  it('returns null when focus skill is next up but no live work', () => {
    const t = ticket({
      ticketId: 'w3',
      doneSkillIds: ['abd-domain-model'],
    });
    expect(t.workingAgent()).toBeNull();
  });

  it('returns null when execution done and only awaiting review', () => {
    const t = ticket({
      ticketId: 'w4',
      awaitingReviewSkillId: 'abd-story-specification',
    });
    expect(t.workingAgent()).toBeNull();
  });
});

describe('ticketShowsLiveSkillIcon', () => {
  it('hides icon on IP sub-column when no skill is actively executing or under review', () => {
    const t = ticket({
      ticketId: 't8',
      doneSkillIds: ['abd-domain-model'],
    });
    expect(t.showsLiveSkillIcon('ip')).toBe(false);
  });

  it('feeds-next backlog resolves focus but never shows icon on card face', () => {
    const t = ticket({
      ticketId: 't8b',
      column: 'backlog',
      stage: 'specification',
      doneSkillIds: [],
    });
    const focusId = t.focusSkillId(SPEC_SKILLS, 'feeds-next');
    expect(focusId).toBe('abd-domain-model');
    expect(t.showsLiveSkillIcon('feeds-next')).toBe(false);
  });

  it('shows icon on active ticket while skill is executing', () => {
    const t = ticket({
      ticketId: 't8c',
      activeSkillId: 'abd-domain-model',
      activeAgent: 'business-expert',
    });
    expect(t.showsLiveSkillIcon('ip')).toBe(true);
  });

  it('hides icon for non-active tickets without feeds-next', () => {
    const t = ticket({ ticketId: 't9', column: 'archived' });
    expect(t.showsLiveSkillIcon()).toBe(false);
  });
});

describe('relocateScatterParents (via StageBucketLayout.build)', () => {
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

    const columnViews: KanbanColumnView[] = [
      { id: 'active', label: 'Active', tickets: [childA, childB] },
      { id: 'backlog', label: 'Backlog', tickets: [] },
      { id: 'done', label: 'Done', tickets: [] },
    ];
    const layout = StageBucketLayout.build(columnViews, [parent], []);
    const buckets = layout.buildStageBuckets();

    expect(buckets.get('exploration')!.done).toHaveLength(0);
    expect(buckets.get('engineering')!.ip[0]!.ticketId).toBe('inc-parent');
    expect(buckets.get('engineering')!.ip[0]!.isScatterParent()).toBe(true);
    expect(buckets.get('engineering')!.ip.map((t: Ticket) => t.ticketId)).toEqual([
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
      doneSkillIds: ['abd-domain-language', 'abd-story-acceptance-criteria'],
    });

    const columnViews: KanbanColumnView[] = [
      { id: 'active', label: 'Active', tickets: [childA, childB] },
      { id: 'backlog', label: 'Backlog', tickets: [] },
      { id: 'done', label: 'Done', tickets: [] },
    ];
    const stageSkillRails: StageSkillRail[] = [
      {
        stage: 'exploration',
        skills: [
          { skillId: 'abd-domain-language', label: 'UL', family: 'domain-driven-design', role: 'business-expert' },
          { skillId: 'abd-story-acceptance-criteria', label: 'AC', family: 'story-driven-delivery', role: 'product-owner' },
        ],
      },
    ];
    const layout = StageBucketLayout.build(columnViews, [parent], stageSkillRails);
    const buckets = layout.buildStageBuckets();

    expect(buckets.get('discovery')!.done).toHaveLength(0);
    expect(buckets.get('exploration')!.ip.map((t: Ticket) => t.ticketId)).toEqual([
      'project-all',
      '1-walk-in-driver',
    ]);
    expect(buckets.get('exploration')!.done.map((t: Ticket) => t.ticketId)).toEqual([
      '2-click-and-collect',
    ]);
  });

  it('project-all after module scatter shows in shaping feedsNext above backlog children', () => {
    const parent = ticket({
      ticketId: 'project-all',
      column: 'archived',
      stage: 'shaping',
      scopeLevel: 'all',
      lineage: ['PawPlace'],
      scatterTo: ['1-product-catalog', '2-store-operations', '3-checkout-and-fulfillment'],
    });
    const childDone = ticket({
      ticketId: '1-product-catalog',
      column: 'active',
      stage: 'discovery',
      scatterFrom: 'project-all',
      priority: 1,
      doneSkillIds: ['abd-domain-terms', 'abd-story-mapping'],
    });
    const childBacklogA = ticket({
      ticketId: '2-store-operations',
      column: 'backlog',
      stage: 'discovery',
      scatterFrom: 'project-all',
      priority: 2,
    });
    const childBacklogB = ticket({
      ticketId: '3-checkout-and-fulfillment',
      column: 'backlog',
      stage: 'discovery',
      scatterFrom: 'project-all',
      priority: 3,
    });

    const columnViews: KanbanColumnView[] = [
      { id: 'active', label: 'Active', tickets: [childDone] },
      { id: 'backlog', label: 'Backlog', tickets: [childBacklogA, childBacklogB] },
      { id: 'done', label: 'Done', tickets: [] },
    ];
    const stageSkillRails: StageSkillRail[] = [
      {
        stage: 'discovery',
        skills: [
          { skillId: 'abd-domain-terms', label: 'Terms', family: 'domain-driven-design', role: 'business-expert' },
          { skillId: 'abd-story-mapping', label: 'Story Map', family: 'story-driven-delivery', role: 'product-owner' },
        ],
      },
    ];
    const layout = StageBucketLayout.build(columnViews, [parent], stageSkillRails);
    const buckets = layout.buildStageBuckets();

    expect(layout.archivedColumnTickets([parent]).map((t: Ticket) => t.ticketId)).not.toContain(
      'project-all',
    );
    expect(buckets.get('shaping')!.feedsNext.map((t: Ticket) => t.ticketId)).toEqual([
      'project-all',
      '2-store-operations',
      '3-checkout-and-fulfillment',
    ]);
    expect(buckets.get('shaping')!.feedsNext[0]!.isScatterParent()).toBe(true);
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
      activeSkillId: 'abd-ux-specification',
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

    const columnViews: KanbanColumnView[] = [
      { id: 'active', label: 'Active', tickets: [walkInSprint2, ccSprint2, ccSprint3] },
      { id: 'backlog', label: 'Backlog', tickets: [] },
      { id: 'done', label: 'Done', tickets: [] },
    ];
    const layout = StageBucketLayout.build(columnViews, [project, walkIn, clickCollect], []);
    const buckets = layout.buildStageBuckets();

    expect(buckets.get('discovery')!.done).toHaveLength(0);
    expect(buckets.get('specification')!.ip.map((t: Ticket) => t.ticketId)).toEqual([
      'project-all',
      '2-click-and-collect',
      '2-click-and-collect-sprint-2',
      '2-click-and-collect-sprint-3',
    ]);
    expect(buckets.get('engineering')!.ip.map((t: Ticket) => t.ticketId)).toEqual([
      '1-walk-in-driver',
      '1-walk-in-driver-sprint-2',
    ]);
  });
});

describe('scopeCssClass', () => {
  it('maps scope_level to ticket CSS classes', () => {
    expect(ticket({ ticketId: 'p', scopeLevel: 'project' }).scopeCssClass()).toBe('kb-ticket--scope-project');
    expect(ticket({ ticketId: 'a', scopeLevel: 'all' }).scopeCssClass()).toBe('kb-ticket--scope-project');
    expect(ticket({ ticketId: 'pt', scopeLevel: 'partition' }).scopeCssClass()).toBe('kb-ticket--scope-partition');
    expect(ticket({ ticketId: 'i', scopeLevel: 'increment' }).scopeCssClass()).toBe('kb-ticket--scope-increment');
    expect(ticket({ ticketId: 's', scopeLevel: 'sprint' }).scopeCssClass()).toBe('kb-ticket--scope-sprint');
    expect(ticket({ ticketId: 'u', scopeLevel: 'unknown' }).scopeCssClass()).toBe('kb-ticket--scope-sprint');
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
            'abd-ux-specification': { execution_status: 'pending', agent: 'ux-designer' },
          },
        },
      ],
      done: [],
      archived: [],
      team: { engineer: 1 },
    });
    expect(
      board.active[0].skill_progress['abd-ux-specification'].execution_status,
    ).toBe('not_started');
  });
});

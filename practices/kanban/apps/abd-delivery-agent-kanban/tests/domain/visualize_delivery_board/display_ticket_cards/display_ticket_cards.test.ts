/**
 * Display Ticket Cards
 *
 * Epic:     Visualize Delivery Board
 * Sub-epic: Display Ticket Cards
 */
import { describe, expect, it } from 'vitest';
import {
  Ticket,
  StageBucketLayout,
  type KanbanColumnView,
  type StageSkillRail,
  type RawTicket,
  type SkillProgress,
  type StageSkill,
} from '@deliveryforge/kanban-shared';

const discoverySkills = [
  'abd-domain-terms',
  'abd-story-mapping',
  'abd-thin-slicing',
  'abd-architecture-blueprint',
];

function partitionDoneAwaitingScatter(): Ticket {
  const sp: Record<string, SkillProgress> = {};
  for (const id of discoverySkills) {
    sp[id] = { execution_status: 'done', review_status: 'done' };
  }
  const raw: RawTicket = {
    ticket_id: '2-shared-domain-schema-copybook-layer',
    lineage: ['BESS28 Replacement', 'Shared Domain Schema'],
    scope_level: 'partition',
    stage: 'discovery',
    priority: 2,
    skill_progress: sp,
    scatter_from: 'project-all',
    scatter_to: [],
    entered_stage: null,
    completed_stage: null,
    notes: '',
    stage_history: [],
  };
  return new Ticket(raw, 'done');
}

describe('Scatter Ticket at Scope Boundary', () => {
  it('detects partition with discovery skills done and no scatter_to', () => {
    const ticket = partitionDoneAwaitingScatter();
    expect(ticket.isAwaitingScatter(discoverySkills)).toBe(true);
  });

  it('buildStageBuckets queues awaiting-scatter partition in feeds-next not done', () => {
    const ticket = partitionDoneAwaitingScatter();
    const columnViews: KanbanColumnView[] = [
      { id: 'done', label: 'Done', tickets: [ticket] },
      { id: 'active', label: 'Active', tickets: [] },
      { id: 'backlog', label: 'Backlog', tickets: [] },
    ];
    const rails: StageSkillRail[] = [
      {
        stage: 'discovery',
        skills: discoverySkills.map((skillId) => ({
          skillId,
          label: skillId,
          family: 'architecture-centric-engineering' as const,
          role: 'engineer' as const,
        })),
      },
    ];
    const buckets = StageBucketLayout.build(columnViews, [], rails).buildStageBuckets();
    const discovery = buckets.get('discovery')!;
    expect(discovery.done.map((t) => t.ticketId)).not.toContain(ticket.ticketId);
    expect(discovery.feedsNext.map((t) => t.ticketId)).toContain(ticket.ticketId);
  });
});

describe('Show Agent Running on Ticket Card', () => {
  const explorationSkills: StageSkill[] = [
    { skillId: 'abd-domain-language', label: 'Domain Language', family: 'domain-driven-design', role: 'business-expert' },
    { skillId: 'abd-acceptance-criteria', label: 'Acceptance Criteria', family: 'story-driven-delivery', role: 'product-owner' },
    { skillId: 'abd-architecture-specification', label: 'Arch Spec', family: 'architecture-centric-engineering', role: 'engineer' },
  ];

  function makeIpTicket(skillProgress: Record<string, SkillProgress> = {}): Ticket {
    const raw: RawTicket = {
      ticket_id: 'alpha-1',
      lineage: ['Project', 'Alpha'],
      scope_level: 'increment',
      stage: 'exploration',
      priority: 1,
      skill_progress: skillProgress,
      scatter_from: 'parent-alpha',
      scatter_to: [],
      entered_stage: null,
      completed_stage: null,
      notes: '',
      stage_history: [],
    };
    const t = new Ticket(raw, 'active');
    return t;
  }

  it('showsLiveSkillIcon is false when no skill is executing and no agent session matches', () => {
    const ticket = makeIpTicket();
    expect(ticket.showsLiveSkillIcon('ip')).toBe(false);
  });

  it('showsAgentRunning is true when a running session role matches a pending intent skill role', () => {
    const ticket = makeIpTicket();
    ticket.pendingIntentSkillIds = ['abd-domain-language'];

    const activeRoles = new Set(['business-expert']);
    expect(ticket.showsAgentRunning(activeRoles, explorationSkills)).toBe(true);
  });

  it('showsAgentRunning is false when no running session matches the pending intent skill role', () => {
    const ticket = makeIpTicket();
    ticket.pendingIntentSkillIds = ['abd-domain-language'];

    const activeRoles = new Set(['engineer']); // engineer is not the domain-language role
    expect(ticket.showsAgentRunning(activeRoles, explorationSkills)).toBe(false);
  });

  it('showsAgentRunning is false when there are no pending intents even if a session is running', () => {
    const ticket = makeIpTicket();
    ticket.pendingIntentSkillIds = [];

    const activeRoles = new Set(['business-expert']);
    expect(ticket.showsAgentRunning(activeRoles, explorationSkills)).toBe(false);
  });
});

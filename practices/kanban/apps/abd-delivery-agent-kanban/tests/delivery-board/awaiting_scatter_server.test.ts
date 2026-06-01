import { describe, expect, it } from 'vitest';
import {
  buildStageBuckets,
  ticketAwaitingScatter,
  type KanbanColumnView,
  type StageSkillRail,
  type TicketView,
} from '@deliveryforge/delivery-board-shared';

const discoverySkills = [
  'abd-domain-terms',
  'abd-story-mapping',
  'abd-thin-slicing',
  'abd-architecture-blueprint',
];

function partitionDoneAwaitingScatter(): TicketView {
  return {
    ticketId: '2-shared-domain-schema-copybook-layer',
    column: 'done',
    stage: 'discovery',
    scopeLevel: 'partition',
    priority: 2,
    lineage: ['BESS28 Replacement', 'Shared Domain Schema'],
    scatterFrom: 'project-all',
    scatterTo: [],
    doneSkillIds: [...discoverySkills],
    activeSkillId: null,
    activeAgent: null,
    reviewSkillId: null,
    reviewAgent: null,
    awaitingReviewSkillId: null,
    awaitingReviewAgent: null,
    failedReviewSkillIds: [],
    isReviewing: false,
    completedStage: null,
    enteredStage: null,
    notes: '',
    displayLabel: 'Shared Domain Schema',
    chipLabel: '#2',
  } as TicketView;
}

describe('ticketAwaitingScatter', () => {
  it('detects partition with discovery skills done and no scatter_to', () => {
    const ticket = partitionDoneAwaitingScatter();
    expect(ticketAwaitingScatter(ticket, discoverySkills)).toBe(true);
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
    const buckets = buildStageBuckets(columnViews, [], rails);
    const discovery = buckets.get('discovery')!;
    expect(discovery.done.map((t) => t.ticketId)).not.toContain(ticket.ticketId);
    expect(discovery.feedsNext.map((t) => t.ticketId)).toContain(ticket.ticketId);
  });
});

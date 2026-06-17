import type { StageId, StageBucket, StageSkillRail } from './Stage';
import { Stage } from './Stage';
import { Ticket } from './Ticket';
import type { KanbanColumnView } from './Ticket';

/**
 * domain model: Stage — queue of tickets, in-progress tickets, done tickets.
 *
 * Domain collection class: partitions tickets into per-stage sub-columns
 * (IP / Done / FeedsNext) and handles scatter-parent relocation.
 */
export class StageBucketLayout {
  private readonly buckets: Map<StageId, StageBucket>;

  protected constructor(buckets: Map<StageId, StageBucket>) {
    this.buckets = buckets;
  }

  get(stage: StageId): StageBucket | undefined {
    return this.buckets.get(stage);
  }

  values(): IterableIterator<StageBucket> {
    return this.buckets.values();
  }

  entries(): IterableIterator<[StageId, StageBucket]> {
    return this.buckets.entries();
  }

  shownTicketIds(): Set<string> {
    const ids = new Set<string>();
    for (const bucket of this.buckets.values()) {
      for (const t of bucket.done) ids.add(t.ticketId);
      for (const t of bucket.feedsNext) ids.add(t.ticketId);
      for (const t of bucket.ip) ids.add(t.ticketId);
    }
    return ids;
  }

  buildStageBuckets(): Map<StageId, StageBucket> {
    const map = new Map<StageId, StageBucket>();
    for (const stage of Stage.ORDER) {
      const bucket = this.get(stage);
      if (bucket) map.set(stage, bucket);
    }
    return map;
  }

  archivedColumnTickets(archivedTickets: Ticket[]): Ticket[] {
    const shown = this.shownTicketIds();
    return archivedTickets.filter((t) => !shown.has(t.ticketId));
  }

  // ── Factory ────────────────────────────────────────────────────────────

  static build(
    columnViews: KanbanColumnView[],
    archivedTickets: Ticket[],
    stageSkillRails: StageSkillRail[],
  ): StageBucketLayout {
    const buckets = StageBucketLayout.empty();
    const skillsByStage = new Map(
      stageSkillRails.map((r) => [r.stage, r.skills.map((s) => s.skillId)]),
    );

    for (const col of columnViews) {
      if (col.id === 'archived') continue;
      for (const ticket of col.tickets) {
        if (!ticket.stage) continue;

        if (col.id === 'backlog') {
          const prev = Stage.previous(ticket.stage);
          if (prev) buckets.get(prev)?.feedsNext.push(ticket);
          continue;
        }

        const bucket = buckets.get(ticket.stage);
        if (!bucket) continue;
        const skillIds = skillsByStage.get(ticket.stage) ?? [];

        if (col.id === 'done') {
          if (ticket.isAwaitingScatter(skillIds)) {
            bucket.feedsNext.push(ticket);
          } else {
            bucket.done.push(ticket);
          }
        } else if (col.id === 'active') {
          if (ticket.holdInProgress) {
            bucket.ip.push(ticket);
          } else if (ticket.isAwaitingScatter(skillIds)) {
            bucket.feedsNext.push(ticket);
          } else if (ticket.completedStage) {
            bucket.done.push(ticket);
          } else if (!ticket.isStageSkillsComplete(skillIds)) {
            bucket.ip.push(ticket);
          } else {
            bucket.done.push(ticket);
          }
        }
      }
    }

    for (const bucket of buckets.values()) {
      bucket.feedsNext.sort((a, b) => a.priority - b.priority);
    }

    for (const ticket of archivedTickets) {
      if (ticket.scatterTo.length > 0) continue;
      const stage = ticket.resolveArchivedStageDone();
      if (!stage) continue;
      const bucket = buckets.get(stage);
      if (!bucket) continue;
      if (ticket.holdInProgress) {
        bucket.ip.push(ticket);
      } else {
        bucket.done.push(ticket);
      }
    }

    const layout = new StageBucketLayout(buckets);
    layout.relocateScatterParents(archivedTickets);
    return layout;
  }

  static globalBacklogTickets(columnViews: KanbanColumnView[]): Ticket[] {
    const backlogCol = columnViews.find((c) => c.id === 'backlog');
    if (!backlogCol) return [];
    return backlogCol.tickets.filter((t) => !t.stage);
  }

  // ── Scatter parent relocation ──────────────────────────────────────────

  private relocateScatterParents(archivedTickets: Ticket[]): void {
    const parents = archivedTickets
      .filter((t) => t.isScatterParent())
      .sort(
        (a, b) =>
          StageBucketLayout.scatterParentOrder(a) - StageBucketLayout.scatterParentOrder(b) ||
          a.priority - b.priority,
      );
    const maxPasses = Math.max(parents.length, 1);
    for (let pass = 0; pass < maxPasses; pass++) {
      let anyMoved = false;
      for (const parent of parents) {
        if (this.relocateOneScatterParent(parent)) anyMoved = true;
      }
      if (!anyMoved) break;
    }
  }

  private relocateOneScatterParent(parent: Ticket): boolean {
    const childIds = new Set(parent.scatterTo);
    type BucketKey = 'ip' | 'done' | 'feedsNext';

    const located: Array<{
      stage: StageId;
      key: BucketKey;
      ticket: Ticket;
      stageIdx: number;
    }> = [];

    for (const [stage, bucket] of this.buckets) {
      const stageIdx = Stage.ORDER.indexOf(stage);
      for (const key of ['ip', 'done', 'feedsNext'] as const) {
        for (const ticket of bucket[key]) {
          if (childIds.has(ticket.ticketId)) {
            located.push({ stage, key, ticket, stageIdx });
          }
        }
      }
    }

    if (located.length === 0) return false;

    located.sort((a, b) => {
      if (a.stageIdx !== b.stageIdx) return a.stageIdx - b.stageIdx;
      const rankA = SUB_COLUMN_TRAILING_RANK[a.key];
      const rankB = SUB_COLUMN_TRAILING_RANK[b.key];
      if (rankA !== rankB) return rankA - rankB;
      return a.ticket.priority - b.ticket.priority;
    });

    const { stage, key } = located[0]!;
    const removed = this.removeFromBuckets(parent.ticketId);
    const ticketToInsert = removed?.ticket ?? parent;

    const targetList = this.buckets.get(stage)![key];
    const ownChildIndices = targetList
      .map((t, i) => (childIds.has(t.ticketId) ? i : -1))
      .filter((i) => i >= 0);
    const insertAt = ownChildIndices.length > 0 ? Math.min(...ownChildIndices) : 0;
    targetList.splice(insertAt, 0, ticketToInsert);
    return true;
  }

  private removeFromBuckets(
    ticketId: string,
  ): { stage: StageId; key: 'ip' | 'done' | 'feedsNext'; ticket: Ticket } | null {
    for (const [stage, bucket] of this.buckets) {
      for (const key of ['ip', 'done', 'feedsNext'] as const) {
        const idx = bucket[key].findIndex((t) => t.ticketId === ticketId);
        if (idx >= 0) {
          const [ticket] = bucket[key].splice(idx, 1);
          return { stage, key, ticket };
        }
      }
    }
    return null;
  }

  private static scatterParentOrder(ticket: Ticket): number {
    switch (ticket.scopeLevel) {
      case 'sprint':
        return 0;
      case 'increment':
        return 1;
      case 'partition':
        return 2;
      default:
        return 3;
    }
  }

  private static empty(): Map<StageId, StageBucket> {
    const buckets = new Map<StageId, StageBucket>();
    for (const stage of Stage.ORDER) {
      buckets.set(stage, { ip: [], done: [], feedsNext: [] });
    }
    return buckets;
  }
}

const SUB_COLUMN_TRAILING_RANK: Record<'ip' | 'done' | 'feedsNext', number> = {
  ip: 0,
  feedsNext: 1,
  done: 2,
};

import type { SkillProgress } from './SkillProgress.schema';
import { SkillProgressEntry } from './SkillProgressEntry';

/**
 * Collection class wrapping a ticket's skill_progress map.
 * Provides domain-oriented query methods for skill state derivation.
 */
export class SkillProgressMap {
  private readonly entries: Map<string, SkillProgressEntry>;

  constructor(raw: Record<string, SkillProgress>) {
    this.entries = new Map(
      Object.entries(raw).map(([id, sp]) => [id, SkillProgressEntry.create(sp)]),
    );
  }

  get(skillId: string): SkillProgressEntry | undefined {
    return this.entries.get(skillId);
  }

  executingSkillIds(): string[] {
    return [...this.entries.entries()]
      .filter(([, e]) => e.isExecuting())
      .map(([id]) => id);
  }

  reviewingSkillIds(): string[] {
    return [...this.entries.entries()]
      .filter(([, e]) => e.isUnderReview())
      .map(([id]) => id);
  }

  awaitingReviewSkillIds(): string[] {
    return [...this.entries.entries()]
      .filter(([, e]) => e.isAwaitingReview())
      .map(([id]) => id);
  }

  doneSkillIds(): string[] {
    return [...this.entries.entries()]
      .filter(([, e]) => e.isComplete())
      .map(([id]) => id);
  }

  failedReviewSkillIds(): string[] {
    return [...this.entries.entries()]
      .filter(([, e]) => e.hasFailedReview())
      .map(([id]) => id);
  }

  firstExecuting(): { skillId: string; agent: string | null } | null {
    for (const [skillId, e] of this.entries) {
      if (e.isExecuting()) return { skillId, agent: e.agent };
    }
    return null;
  }

  firstReviewing(): { skillId: string; agent: string | null } | null {
    for (const [skillId, e] of this.entries) {
      if (e.isUnderReview()) return { skillId, agent: e.reviewer ?? e.agent };
    }
    return null;
  }

  firstAwaitingReview(): { skillId: string; agent: string | null } | null {
    for (const [skillId, e] of this.entries) {
      if (e.isAwaitingReview()) return { skillId, agent: e.reviewer ?? e.agent };
    }
    return null;
  }

  allComplete(): boolean {
    if (this.entries.size === 0) return false;
    for (const e of this.entries.values()) {
      if (!e.isComplete()) return false;
    }
    return true;
  }

  get size(): number {
    return this.entries.size;
  }

  toJSON(): Record<string, SkillProgress> {
    const out: Record<string, SkillProgress> = {};
    for (const [id, e] of this.entries) {
      out[id] = e.toJSON();
    }
    return out;
  }
}

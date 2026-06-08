import type { SkillProgress } from './SkillProgress.schema';

/**
 * Domain entity wrapping a skill progress record.
 * domain model: SkillProgress — invariant: execution must reach done before review leaves not_started.
 */
export class SkillProgressEntry {
  constructor(private readonly data: SkillProgress) {}

  get executionStatus(): string {
    return this.data.execution_status;
  }

  get reviewStatus(): string | null | undefined {
    return this.data.review_status;
  }

  get agent(): string | null {
    return this.data.agent ?? null;
  }

  get reviewer(): string | null {
    return this.data.reviewer ?? null;
  }

  isComplete(): boolean {
    return this.data.execution_status === 'done' && this.data.review_status === 'done';
  }

  isExecuting(): boolean {
    return this.data.execution_status === 'in_progress';
  }

  isUnderReview(): boolean {
    return this.data.review_status === 'in_progress';
  }

  isAwaitingReview(): boolean {
    return (
      this.data.execution_status === 'done' &&
      this.data.review_status !== 'done' &&
      this.data.review_status !== 'in_progress'
    );
  }

  hasFailedReview(): boolean {
    return this.data.review_status === 'failed';
  }

  toJSON(): SkillProgress {
    return { ...this.data };
  }

  static create(data: SkillProgress): SkillProgressEntry {
    return new SkillProgressEntry(data);
  }

  static skipped(role: string): SkillProgressEntry {
    const now = new Date().toISOString();
    return new SkillProgressEntry({
      execution_status: 'done',
      review_status: 'done',
      agent: role,
      reviewer: role,
      start: now,
      end: now,
      review_start: now,
      review_end: now,
    });
  }
}

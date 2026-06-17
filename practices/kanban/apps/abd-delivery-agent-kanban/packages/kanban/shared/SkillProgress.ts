/**
 * domain model: SkillProgress — tracks execution status of a single skill on a ticket.
 *      Immutable value object; create new instances to advance state.
 */

export type SkillExecutionStatus = 'not_started' | 'in_progress' | 'done';

export class SkillProgress {
  readonly ticketId: string;
  readonly skillName: string;
  readonly executionStatus: SkillExecutionStatus;

  private constructor(ticketId: string, skillName: string, status: SkillExecutionStatus) {
    this.ticketId = ticketId;
    this.skillName = skillName;
    this.executionStatus = status;
  }

  static create(
    ticketId: string,
    skillName: string,
    status: SkillExecutionStatus,
  ): SkillProgress {
    return new SkillProgress(ticketId, skillName, status);
  }

  markDone(): SkillProgress {
    return new SkillProgress(this.ticketId, this.skillName, 'done');
  }

  isComplete(): boolean {
    return this.executionStatus === 'done';
  }
}

/**
 * domain model: Stage — ordered delivery stages with queues of tickets.
 * Invariant: a ticket cannot skip a stage or move backward.
 */

export type StageId =
  | 'context'
  | 'shaping'
  | 'discovery'
  | 'exploration'
  | 'specification'
  | 'engineering';

export type SkillFamily =
  | 'domain-driven-design'
  | 'user-experience-design'
  | 'story-driven-delivery'
  | 'architecture-centric-engineering'
  | 'delivery'
  | 'idea-shaping'
  | 'context-to-memory';

export interface StageSkill {
  skillId: string;
  label: string;
  family: SkillFamily;
  role: string;
}

export interface StageSkillRail {
  stage: StageId;
  skills: StageSkill[];
}

export interface StageBucket {
  ip: import('./Ticket').Ticket[];
  done: import('./Ticket').Ticket[];
  feedsNext: import('./Ticket').Ticket[];
}

export type StageSubColumn = 'ip' | 'done' | 'feeds-next';

/** The two terminal columns in the kanban flow — before work begins and after it ends. */
export type KanbanEndColumn = 'backlog' | 'archived';

export class Stage {
  static readonly ORDER: StageId[] = [
    'context',
    'shaping',
    'discovery',
    'exploration',
    'specification',
    'engineering',
  ];

  static readonly LABELS: Record<StageId, string> = {
    context: 'Context',
    shaping: 'Shaping',
    discovery: 'Discovery',
    exploration: 'Exploration',
    specification: 'Specification',
    engineering: 'Engineering',
  };

  static normalize(raw: string): StageId | null {
    const key = raw.toLowerCase().trim();
    if (Stage.ORDER.includes(key as StageId)) return key as StageId;
    return null;
  }

  static previous(stage: StageId): StageId | null {
    const idx = Stage.ORDER.indexOf(stage);
    if (idx <= 0) return null;
    return Stage.ORDER[idx - 1]!;
  }

  static indexOf(stage: string): number {
    return Stage.ORDER.indexOf(stage as StageId);
  }

  // ── StageSubColumn helpers ─────────────────────────────────────────

  static readonly SUB_COLUMN_LABELS: Record<StageSubColumn, string> = {
    'ip': 'In Progress',
    'done': 'Done',
    'feeds-next': 'Feeds Next',
  };

  static isInProgress(subCol: StageSubColumn): boolean {
    return subCol === 'ip';
  }

  static isDone(subCol: StageSubColumn): boolean {
    return subCol === 'done';
  }

  static subColumnLabel(subCol: StageSubColumn): string {
    return Stage.SUB_COLUMN_LABELS[subCol];
  }

  // ── KanbanEndColumn helpers ────────────────────────────────────────

  static readonly END_COLUMN_LABELS: Record<KanbanEndColumn, string> = {
    backlog: 'Backlog',
    archived: 'Archived',
  };

  static isBacklog(col: KanbanEndColumn): boolean {
    return col === 'backlog';
  }

  static isArchived(col: KanbanEndColumn): boolean {
    return col === 'archived';
  }
}

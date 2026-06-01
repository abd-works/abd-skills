import {
  STAGE_ORDER,
  type KanbanBoard,
  type SkillProgress,
  type StageId,
  type Ticket,
} from './kanbanBoard';
import {
  isRequiredStageStep,
  type KanbanConfiguration,
  type StageDefinition,
  type StageWorkRequiredEntry,
} from './parseSystemOfWork';

export type ScatterChildSpec = {
  id: string;
  name: string;
  priority: number;
};

export type MoveTicketPlacement = 'in_progress' | 'stage_done';

const SCOPE_RANK: Record<string, number> = {
  all: 0,
  project: 1,
  partition: 2,
  increment: 3,
  sprint: 4,
  story: 5,
};

function scopeRank(scope: string): number {
  return SCOPE_RANK[scope] ?? 99;
}

function stageIndex(stage: string): number {
  return STAGE_ORDER.indexOf(stage as StageId);
}

function resolveDefinition(
  config: KanbanConfiguration,
  definitionName: string | null | undefined,
): { stages: StageDefinition[] } {
  const defName = definitionName ?? Object.keys(config.definitions)[0] ?? '';
  const def = config.definitions[defName];
  if (!def) throw new Error(`Unknown stage configuration: ${defName}`);
  return { stages: def.stages };
}

function getStageDef(stages: StageDefinition[], name: string): StageDefinition | undefined {
  return stages.find((s) => s.name === name);
}

function requiredSteps(stageDef: StageDefinition | undefined): StageWorkRequiredEntry[] {
  if (!stageDef) return [];
  const steps = stageDef.stage_work_required ?? stageDef.skills ?? [];
  return steps.filter(isRequiredStageStep);
}

function isSkillDone(sp: SkillProgress | undefined): boolean {
  return sp?.execution_status === 'done' && sp?.review_status === 'done';
}

function skippedSkillProgress(role: string): SkillProgress {
  const now = new Date().toISOString();
  return {
    execution_status: 'done',
    review_status: 'done',
    agent: role,
    reviewer: role,
    start: now,
    end: now,
    review_start: now,
    review_end: now,
  };
}

function completeRequiredSkillsForStage(
  ticket: Ticket,
  stageDef: StageDefinition | undefined,
): void {
  for (const step of requiredSteps(stageDef)) {
    const existing = ticket.skill_progress[step.skill];
    if (isSkillDone(existing)) continue;
    ticket.skill_progress[step.skill] = skippedSkillProgress(step.role);
  }
}

function recordStageCompleteAndAdvance(
  ticket: Ticket,
  completedStageName: string,
  nextStageName: string,
  skipped = true,
): void {
  const now = new Date().toISOString();
  if (ticket.stage && ticket.entered_stage) {
    ticket.stage_history = [
      ...(ticket.stage_history ?? []),
      {
        stage: completedStageName,
        entered: ticket.entered_stage,
        completed: now,
        skipped,
      },
    ];
  }
  ticket.stage = nextStageName;
  ticket.skill_progress = {};
  ticket.entered_stage = now;
  ticket.completed_stage = null;
}

/** First stage transition along the path where next stage scope is finer than ticket scope. */
export function scatterBoundaryOnPath(
  config: KanbanConfiguration,
  definitionName: string | null | undefined,
  ticketScopeLevel: string,
  fromStage: StageId,
  toStage: StageId,
): { boundaryStage: StageId; childStage: StageId; childScope: string } | null {
  const { stages } = resolveDefinition(config, definitionName);
  const fromIdx = stageIndex(fromStage);
  const toIdx = stageIndex(toStage);
  if (fromIdx < 0 || toIdx < 0) return null;
  const ticketRank = scopeRank(ticketScopeLevel);

  for (let i = fromIdx; i < toIdx; i++) {
    const curName = STAGE_ORDER[i]! as StageId;
    const nextName = STAGE_ORDER[i + 1]! as StageId;
    const curDef = getStageDef(stages, curName);
    const nextDef = getStageDef(stages, nextName);
    if (!curDef || !nextDef) continue;
    const curRank = scopeRank(curDef.scope);
    const nextRank = scopeRank(nextDef.scope);
    if (nextRank > curRank && ticketRank <= curRank) {
      return {
        boundaryStage: curName,
        childStage: nextName,
        childScope: nextDef.scope,
      };
    }
  }
  return null;
}

function advanceTicketToStage(
  ticket: Ticket,
  targetStage: StageId,
  stages: StageDefinition[],
): void {
  const currentStage = ticket.stage as StageId;
  const fromIdx = stageIndex(currentStage);
  const toIdx = stageIndex(targetStage);
  if (fromIdx < 0 || toIdx < 0 || toIdx <= fromIdx) return;

  completeRequiredSkillsForStage(ticket, getStageDef(stages, currentStage));

  for (let i = fromIdx + 1; i <= toIdx; i++) {
    const stageName = STAGE_ORDER[i]!;
    const prevName = STAGE_ORDER[i - 1]!;
    if (i < toIdx) {
      recordStageCompleteAndAdvance(ticket, prevName, stageName);
      completeRequiredSkillsForStage(ticket, getStageDef(stages, stageName));
    } else {
      recordStageCompleteAndAdvance(ticket, prevName, stageName);
    }
  }
}

function createChildTicket(
  spec: ScatterChildSpec,
  parent: Ticket,
  childStage: StageId,
  childScope: string,
  now: string,
): Ticket {
  return {
    ticket_id: spec.id,
    lineage: [...parent.lineage, spec.name],
    scope_level: childScope,
    stage: childStage,
    priority: spec.priority,
    created: now,
    entered_stage: now,
    completed_stage: null,
    stage_history: [],
    archived: null,
    scatter_from: parent.ticket_id,
    scatter_to: [],
    skill_progress: {},
    notes: '',
  };
}

function archiveParentAfterScatter(parent: Ticket, childrenSpec: ScatterChildSpec[]): Ticket {
  const now = new Date().toISOString();
  parent.completed_stage = now;
  parent.archived = now;
  parent.scatter_to = childrenSpec.map((c) => c.id);
  if (parent.stage && parent.entered_stage) {
    parent.stage_history = [
      ...(parent.stage_history ?? []),
      {
        stage: parent.stage,
        entered: parent.entered_stage,
        completed: now,
      },
    ];
  }
  return parent;
}

function existingTicketIds(board: KanbanBoard): Set<string> {
  const ids = new Set<string>();
  for (const t of [...board.active, ...board.backlog, ...board.done, ...board.archived]) {
    ids.add(t.ticket_id);
  }
  return ids;
}

/**
 * Scatter parent at a scope boundary, place children on the board, optionally skip ahead to targetStage.
 */
export function applyScatterAndAdvance(
  board: KanbanBoard,
  parent: Ticket,
  targetStage: StageId,
  childrenSpec: ScatterChildSpec[],
  config: KanbanConfiguration,
  definitionName: string | null | undefined,
  placement: MoveTicketPlacement = 'in_progress',
): KanbanBoard {
  const { stages } = resolveDefinition(config, definitionName);
  const boundary = scatterBoundaryOnPath(
    config,
    definitionName,
    parent.scope_level,
    parent.stage as StageId,
    targetStage,
  );
  if (!boundary) {
    throw new Error('applyScatterAndAdvance called without a scatter boundary on this path');
  }

  const ids = existingTicketIds(board);
  const collisions = childrenSpec.filter((c) => ids.has(c.id)).map((c) => c.id);
  if (collisions.length > 0) {
    throw new Error(
      `Scatter from ${parent.ticket_id} would create duplicate IDs: ${collisions.join(', ')}`,
    );
  }

  if (parent.scatter_to && parent.scatter_to.length > 0) {
    throw new Error(
      `Ticket ${parent.ticket_id} already scattered into ${parent.scatter_to.join(', ')}. ` +
        'Drag an increment ticket instead.',
    );
  }

  const workingParent: Ticket = {
    ...parent,
    skill_progress: { ...parent.skill_progress },
    stage_history: [...(parent.stage_history ?? [])],
  };
  completeRequiredSkillsForStage(workingParent, getStageDef(stages, boundary.boundaryStage));

  const now = new Date().toISOString();
  const archivedParent = archiveParentAfterScatter(workingParent, childrenSpec);

  const children: Ticket[] = childrenSpec.map((spec) =>
    createChildTicket(spec, workingParent, boundary.childStage, boundary.childScope, now),
  );

  for (const child of children) {
    if (stageIndex(targetStage) > stageIndex(boundary.childStage)) {
      advanceTicketToStage(child, targetStage, stages);
    }
    if (placement === 'stage_done') {
      completeRequiredSkillsForStage(child, getStageDef(stages, targetStage));
      delete child.hold_in_progress;
    } else {
      child.hold_in_progress = true;
    }
  }

  const active = board.active.filter((t) => t.ticket_id !== parent.ticket_id);
  const archived = [...board.archived, archivedParent];
  active.push(...children);

  return { ...board, active, archived };
}

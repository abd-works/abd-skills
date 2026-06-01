import {
  STAGE_ORDER,
  normalizeStage,
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
import {
  applyScatterAndAdvance,
  scatterBoundaryOnPath,
  type MoveTicketPlacement,
  type ScatterChildSpec,
} from './scatterOnMove';

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

/** @deprecated Use scatterBoundaryOnPath; kept for tests that detect boundary without children. */
export function scatterRequiredForJump(
  config: KanbanConfiguration,
  definitionName: string | null | undefined,
  ticketScopeLevel: string,
  fromStage: StageId,
  toStage: StageId,
): string | null {
  const boundary = scatterBoundaryOnPath(
    config,
    definitionName,
    ticketScopeLevel,
    fromStage,
    toStage,
  );
  if (!boundary) return null;
  return `Scope boundary at ${boundary.boundaryStage} → ${boundary.childStage}`;
}

export type MoveTicketOptions = {
  childrenSpec?: ScatterChildSpec[];
  placement?: MoveTicketPlacement;
  /** Cross-scope move advances the ticket when scatter artifacts are missing (no thin-slicing / sprint-groupings). */
  advanceWithoutScatter?: boolean;
};

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
): void {
  const now = new Date().toISOString();
  if (ticket.stage && ticket.entered_stage) {
    ticket.stage_history = [
      ...(ticket.stage_history ?? []),
      {
        stage: completedStageName,
        entered: ticket.entered_stage,
        completed: now,
        skipped: true,
      },
    ];
  }
  ticket.stage = nextStageName;
  ticket.skill_progress = {};
  ticket.entered_stage = now;
  ticket.completed_stage = null;
}

function extractTicket(board: KanbanBoard, ticketId: string): {
  board: KanbanBoard;
  ticket: Ticket;
} {
  const done = [...board.done];
  const archived = [...board.archived];
  let active = [...board.active];
  let backlog = [...board.backlog];

  const pull = (list: Ticket[]): Ticket | undefined => {
    const idx = list.findIndex((t) => t.ticket_id === ticketId);
    if (idx < 0) return undefined;
    return list.splice(idx, 1)[0];
  };

  // Queued / feeds-next tickets live in board.backlog (shown in prior stage Done).
  let ticket = pull(done) ?? pull(archived) ?? pull(backlog);
  if (!ticket) {
    const existing = active.find((t) => t.ticket_id === ticketId);
    if (!existing) throw new Error(`Ticket not found: ${ticketId}`);
    ticket = { ...existing };
    active = active.filter((t) => t.ticket_id !== ticketId);
  }

  return {
    board: { ...board, active, done, archived, backlog },
    ticket,
  };
}

/**
 * Manual board move: drop ticket onto a stage column (In Progress or Done).
 * Same stage → IP hold or Done complete. Forward → skip intermediate stages. Backward → reopen target stage.
 */
export function applyMoveTicketToStage(
  board: KanbanBoard,
  ticketId: string,
  targetStage: StageId,
  config: KanbanConfiguration,
  definitionName?: string | null,
  options?: MoveTicketOptions,
): KanbanBoard {
  const { stages } = resolveDefinition(config, definitionName);
  const { board: extracted, ticket } = extractTicket(board, ticketId);

  const currentStage = normalizeStage(ticket.stage);
  if (!currentStage) throw new Error(`Ticket ${ticketId} has no stage`);

  const fromIdx = stageIndex(currentStage);
  const toIdx = stageIndex(targetStage);
  if (fromIdx < 0 || toIdx < 0) throw new Error(`Invalid stage: ${ticket.stage} → ${targetStage}`);

  const placement = options?.placement ?? 'in_progress';

  if (toIdx < fromIdx) {
    return applyBackwardMove(extracted, ticket, targetStage, stages, placement);
  }

  if (toIdx === fromIdx) {
    const active = extracted.active.filter((t) => t.ticket_id !== ticketId);
    const landed = applyPlacementOnStage(ticket, placement);
    active.push(landed);
    return { ...extracted, active };
  }

  const boundary = scatterBoundaryOnPath(
    config,
    definitionName,
    ticket.scope_level,
    currentStage,
    targetStage,
  );
  if (boundary) {
    const childrenSpec = options?.childrenSpec;
    if (childrenSpec?.length) {
      return applyScatterAndAdvance(
        extracted,
        ticket,
        targetStage,
        childrenSpec,
        config,
        definitionName,
        placement,
      );
    }
    if (!options?.advanceWithoutScatter) {
      throw new Error(
        `Cannot move to ${targetStage}: ticket must scatter after ${boundary.boundaryStage} ` +
          `(${boundary.childScope} at ${boundary.childStage}). Thin-slicing children are required.`,
      );
    }
  }

  const working: Ticket = {
    ...ticket,
    skill_progress: { ...ticket.skill_progress },
    stage_history: [...(ticket.stage_history ?? [])],
  };

  completeRequiredSkillsForStage(working, getStageDef(stages, currentStage));

  for (let i = fromIdx + 1; i <= toIdx; i++) {
    const stageName = STAGE_ORDER[i]!;
    const prevName = STAGE_ORDER[i - 1]!;
    if (i < toIdx) {
      recordStageCompleteAndAdvance(working, prevName, stageName);
      completeRequiredSkillsForStage(working, getStageDef(stages, stageName));
    } else {
      recordStageCompleteAndAdvance(working, prevName, stageName);
    }
  }

  const active = extracted.active.filter((t) => t.ticket_id !== ticketId);
  active.push(applyPlacementOnStage(working, placement));
  return { ...extracted, active };
}

/** Manual drag to an earlier stage — reopen target stage work (scatter parents cannot move back). */
function applyBackwardMove(
  board: KanbanBoard,
  ticket: Ticket,
  targetStage: StageId,
  stages: StageDefinition[],
  placement: MoveTicketPlacement,
): KanbanBoard {
  if (ticket.scatter_to && ticket.scatter_to.length > 0) {
    throw new Error(
      `Cannot move ${ticket.ticket_id} backward: scatter parent. Drag an increment ticket instead.`,
    );
  }

  const now = new Date().toISOString();
  const active = board.active.filter((t) => t.ticket_id !== ticket.ticket_id);
  const working: Ticket = {
    ...ticket,
    stage: targetStage,
    entered_stage: now,
    completed_stage: null,
    skill_progress: {},
    stage_history: [...(ticket.stage_history ?? [])],
  };

  if (placement === 'stage_done') {
    working.completed_stage = now;
    delete working.hold_in_progress;
  } else {
    working.hold_in_progress = true;
  }

  active.push(working);
  return { ...board, active };
}

/** Same-stage Done vs In Progress, or landing column after a forward skip. */
function applyPlacementOnStage(
  ticket: Ticket,
  placement: MoveTicketPlacement,
): Ticket {
  if (placement === 'stage_done') {
    const now = new Date().toISOString();
    const out: Ticket = {
      ...ticket,
      skill_progress: { ...ticket.skill_progress },
      completed_stage: now,
    };
    delete out.hold_in_progress;
    return out;
  }
  return { ...ticket, hold_in_progress: true };
}

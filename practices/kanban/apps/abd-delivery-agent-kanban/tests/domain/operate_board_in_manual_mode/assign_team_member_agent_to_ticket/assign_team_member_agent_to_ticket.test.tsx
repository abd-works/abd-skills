/**
 * Assign Team Member Agent to Ticket
 *
 * Epic:     Operate Board in Manual Mode
 * Sub-epic: Assign Team Member Agent to Ticket
 *
 * Stories: Drag Team Member Agent onto Ticket,
 *          Move Ticket to In Progress on Agent Advance,
 *          Move Ticket to Done on Agent Completion
 */
import { describe, it, expect } from 'vitest';
import { Ticket } from '@deliveryforge/kanban-client';

// ============================================================================
// TYPES (domain model) — from operate_manual_mode_client.test.tsx
// ============================================================================

type BoardMode = 'automatic' | 'manual';
type ExecutionStatus = 'not_started' | 'in_progress' | 'done';
type ReviewStatus = 'not_started' | 'in_progress' | 'done' | 'failed' | null;

interface SkillProgress {
  execution_status: ExecutionStatus;
  review_status: ReviewStatus;
  agent: string | null;
  reviewer: string | null;
}

interface ManualTicket {
  ticket_id: string;
  lineage: string[];
  stage: string;
  priority: number;
  scope_level: string;
  skill_progress: Record<string, SkillProgress>;
  board_position: 'queue' | 'in_progress' | 'done';
}

interface StageWorkRequired {
  skill: string;
  role: string;
  optional?: boolean;
}

type DragResult = {
  accepted: boolean;
  assigned_skill: string | null;
  message: string | null;
};

// ============================================================================
// HELPER FUNCTIONS — Given
// ============================================================================

function given_board_mode(mode: BoardMode): BoardMode {
  return mode;
}

function given_ticket_with_skills(
  ticketId: string,
  stage: string,
  skillProgress: Record<string, SkillProgress>,
): ManualTicket {
  return {
    ticket_id: ticketId,
    lineage: ['PetStore', ticketId],
    stage,
    priority: 1,
    scope_level: 'story',
    skill_progress: skillProgress,
    board_position: 'in_progress',
  };
}

function given_skill_not_started(): SkillProgress {
  return {
    execution_status: 'not_started',
    review_status: null,
    agent: null,
    reviewer: null,
  };
}

function given_skill_assigned(agent: string): SkillProgress {
  return {
    execution_status: 'in_progress',
    review_status: null,
    agent,
    reviewer: null,
  };
}

function given_skill_fully_done(agent: string, reviewer: string): SkillProgress {
  return {
    execution_status: 'done',
    review_status: 'done',
    agent,
    reviewer,
  };
}

function given_stage_work_required(skills: Array<{ skill: string; role: string }>): StageWorkRequired[] {
  return skills.map((s) => ({ skill: s.skill, role: s.role }));
}

// ============================================================================
// HELPER FUNCTIONS — When
// ============================================================================

function when_drag_enabled(mode: BoardMode): boolean {
  return mode === 'manual';
}

function when_agent_dropped_on_ticket(
  mode: BoardMode,
  ticket: ManualTicket,
  agentRole: string,
  stageWorkRequired: StageWorkRequired[],
): DragResult {
  if (mode !== 'manual') {
    return { accepted: false, assigned_skill: null, message: null };
  }

  const ordered_skills = stageWorkRequired.map((swr) => swr.skill);

  for (const skill of ordered_skills) {
    const progress = ticket.skill_progress[skill];
    if (!progress || is_skill_incomplete_and_unassigned(progress)) {
      return { accepted: true, assigned_skill: skill, message: null };
    }
  }

  return {
    accepted: false,
    assigned_skill: null,
    message: 'No eligible skills remain',
  };
}

function is_skill_incomplete_and_unassigned(progress: SkillProgress): boolean {
  if (progress.execution_status === 'done' && progress.review_status === 'done') return false;
  if (progress.agent !== null) return false;
  return true;
}

// ============================================================================
// HELPER FUNCTIONS — Then
// ============================================================================

function then_drag_is_enabled(result: boolean): void {
  expect(result).toBe(true);
}

function then_drag_is_disabled(result: boolean): void {
  expect(result).toBe(false);
}

function then_drop_accepted_with_skill(result: DragResult, expectedSkill: string): void {
  expect(result.accepted).toBe(true);
  expect(result.assigned_skill).toBe(expectedSkill);
}

function then_drop_rejected_with_message(result: DragResult, expectedMessage: string): void {
  expect(result.accepted).toBe(false);
  expect(result.assigned_skill).toBeNull();
  expect(result.message).toBe(expectedMessage);
}

// ============================================================================
// STORY: Drag Team Member Agent onto Ticket
// ============================================================================

describe('Drag Team Member Agent onto Ticket', () => {
  it('assigns next incomplete skill in Stage Work Required order when Board Mode is manual', () => {
    const mode = given_board_mode('manual');
    const stage_work = given_stage_work_required([
      { skill: 'abd-domain-language', role: 'business-expert' },
      { skill: 'abd-domain-sketch', role: 'business-expert' },
      { skill: 'abd-acceptance-criteria', role: 'product-owner' },
    ]);
    const ticket = given_ticket_with_skills('#501', 'discovery', {
      'abd-domain-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_not_started(),
      'abd-acceptance-criteria': given_skill_not_started(),
    });

    const result = when_agent_dropped_on_ticket(mode, ticket, 'business-expert', stage_work);

    then_drop_accepted_with_skill(result, 'abd-domain-sketch');
  });

  it('drag interaction disabled when Board Mode is automatic — no error shown', () => {
    const mode = given_board_mode('automatic');

    const enabled = when_drag_enabled(mode);

    then_drag_is_disabled(enabled);
  });

  it('drop rejected with message when all Stage Work Required skills already assigned or complete', () => {
    const mode = given_board_mode('manual');
    const stage_work = given_stage_work_required([
      { skill: 'abd-domain-language', role: 'business-expert' },
      { skill: 'abd-domain-sketch', role: 'business-expert' },
    ]);
    const ticket = given_ticket_with_skills('#502', 'discovery', {
      'abd-domain-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_assigned('engineer'),
    });

    const result = when_agent_dropped_on_ticket(mode, ticket, 'business-expert', stage_work);

    then_drop_rejected_with_message(result, 'No eligible skills remain');
  });
});

// ============================================================================
// FROM: ticket_stage_drag_client.test.tsx
// ============================================================================

function el(html: string): HTMLElement {
  const wrap = document.createElement('div');
  wrap.innerHTML = html;
  return wrap.firstElementChild as HTMLElement;
}

describe('Ticket.resolveDropTarget — resolves Stage and placement from drop target element', () => {
  it('resolves in-progress sub-column as Stage + in_progress placement', () => {
    const root = el(`
      <div class="kb-stage-group" data-stage="discovery">
        <div class="kb-stage-sub-cols">
          <div class="kb-sub-col kb-sub-col--ip">
            <div class="kb-sub-col-tickets"></div>
          </div>
        </div>
      </div>
    `);
    const hit = root.querySelector('.kb-sub-col-tickets') as HTMLElement;
    expect(Ticket.resolveDropTarget(hit)).toEqual({ stage: 'discovery', placement: 'in_progress' });
  });

  it('resolves done sub-column as Stage + stage_done placement', () => {
    const root = el(`
      <div class="kb-stage-group" data-stage="shaping">
        <div class="kb-sub-col kb-sub-col--done">
          <div class="kb-sub-col-tickets"></div>
        </div>
      </div>
    `);
    const hit = root.querySelector('.kb-sub-col-tickets') as HTMLElement;
    expect(Ticket.resolveDropTarget(hit)).toEqual({ stage: 'shaping', placement: 'stage_done' });
  });

  it('returns null when drop target is outside any stage sub-column', () => {
    expect(Ticket.resolveDropTarget(el('<div class="kb-board-scroll"></div>'))).toBeNull();
  });
});

describe('Ticket.hasExplicitTicketDragData', () => {
  function transferWith(
    values: Record<string, string>,
    types: string[],
  ): DataTransfer {
    return {
      getData: (key: string) => values[key] ?? '',
      setData: () => undefined,
      clearData: () => undefined,
      dropEffect: 'none',
      effectAllowed: 'all',
      files: [] as unknown as FileList,
      items: [] as unknown as DataTransferItemList,
      types,
      setDragImage: () => undefined,
    } as unknown as DataTransfer;
  }

  it('is true for explicit ticket drag payload', () => {
    const dt = transferWith(
      {
        'application/ticket-id': 'project-all',
        'text/plain': 'ticket:project-all',
      },
      ['application/ticket-id', 'text/plain'],
    );
    expect(Ticket.hasExplicitTicketDragData(dt)).toBe(true);
  });

  it('is false for agent-role drag payload', () => {
    const dt = transferWith(
      {
        'application/agent-role': 'business-expert',
        'text/plain': '',
      },
      ['application/agent-role'],
    );
    expect(Ticket.hasExplicitTicketDragData(dt)).toBe(false);
  });
});

describe('Ticket.isTicketStageDrag', () => {
  function transferWith(
    values: Record<string, string>,
    types: string[],
  ): DataTransfer {
    return {
      getData: (key: string) => values[key] ?? '',
      setData: () => undefined,
      clearData: () => undefined,
      dropEffect: 'none',
      effectAllowed: 'all',
      files: [] as unknown as FileList,
      items: [] as unknown as DataTransferItemList,
      types,
      setDragImage: () => undefined,
    } as unknown as DataTransfer;
  }

  it('is false for pure agent-role drags', () => {
    const dt = transferWith(
      {
        'application/agent-role': 'business-expert',
        'text/plain': 'agent-role:business-expert',
      },
      ['application/agent-role', 'text/plain'],
    );
    expect(Ticket.isTicketStageDrag(dt)).toBe(false);
  });
});

describe('Ticket.readAgentRoleFromDataTransfer', () => {
  function transferWith(
    values: Record<string, string>,
    types: string[],
  ): DataTransfer {
    return {
      getData: (key: string) => values[key] ?? '',
      setData: () => undefined,
      clearData: () => undefined,
      dropEffect: 'none',
      effectAllowed: 'all',
      files: [] as unknown as FileList,
      items: [] as unknown as DataTransferItemList,
      types,
      setDragImage: () => undefined,
    } as unknown as DataTransfer;
  }

  it('reads role from application/agent-role payload', () => {
    const dt = transferWith(
      { 'application/agent-role': 'business-expert', 'text/plain': '' },
      ['application/agent-role'],
    );
    expect(Ticket.readAgentRoleFromDataTransfer(dt)).toBe('business-expert');
  });

  it('falls back to text/plain agent-role:<role> payload', () => {
    const dt = transferWith(
      { 'application/agent-role': '', 'text/plain': 'agent-role:product-owner' },
      ['text/plain'],
    );
    expect(Ticket.readAgentRoleFromDataTransfer(dt)).toBe('product-owner');
  });
});

/**
 * Ticket card moves to in-progress sub-column and receives movement animation.
 * Drop must commit before dragend clears the drag payload.
 */
describe('Move Ticket to In Progress on Agent Advance — drag commit ordering', () => {
  function createDropCommit() {
    let payload: { id: string; stage: string } | null = { id: 'project-all', stage: 'shaping' };
    let committed = false;
    const moves: Array<{ id: string; stage: string; placement: string }> = [];

    const endDrag = () => {
      payload = null;
    };

    const onDrop = (ticketId: string, targetStage: string, placement: string) => {
      if (committed || !payload) return;
      committed = true;
      moves.push({ id: ticketId, stage: targetStage, placement });
    };

    const onDragEnd = () => {
      requestAnimationFrame(() => {
        if (!committed) endDrag();
      });
    };

    const finishMove = () => {
      committed = false;
      endDrag();
    };

    return { onDrop, onDragEnd, finishMove, moves, getPayload: () => payload };
  }

  it('ticket move committed on drop before dragend clears payload', async () => {
    const d = createDropCommit();
    d.onDrop('project-all', 'discovery', 'in_progress');
    d.onDragEnd();
    await new Promise((r) => requestAnimationFrame(r));
    expect(d.moves).toEqual([
      { id: 'project-all', stage: 'discovery', placement: 'in_progress' },
    ]);
    d.finishMove();
    expect(d.getPayload()).toBeNull();
  });

  it('payload cleared on cancelled drag — no move recorded when drop does not occur', async () => {
    const d = createDropCommit();
    d.onDragEnd();
    await new Promise((r) => requestAnimationFrame(r));
    expect(d.moves).toEqual([]);
    expect(d.getPayload()).toBeNull();
  });
});

/**
 * Operate Board in Manual Mode — Client Tests
 *
 * Story: Drag Team Member Agent onto Ticket
 *
 * Tests pure domain logic for drag eligibility and skill assignment —
 * no React component imports.
 */
import { describe, it, expect } from 'vitest';

// ============================================================================
// TYPES (domain model)
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

interface Ticket {
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
): Ticket {
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
  ticket: Ticket,
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
  it('assigns next incomplete skill in stage work required order on manual-mode drop', () => {
    // Given:
    const mode = given_board_mode('manual');
    const stage_work = given_stage_work_required([
      { skill: 'abd-ubiquitous-language', role: 'business-expert' },
      { skill: 'abd-domain-sketch', role: 'business-expert' },
      { skill: 'abd-acceptance-criteria', role: 'product-owner' },
    ]);
    const ticket = given_ticket_with_skills('#501', 'discovery', {
      'abd-ubiquitous-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_not_started(),
      'abd-acceptance-criteria': given_skill_not_started(),
    });

    // When:
    const result = when_agent_dropped_on_ticket(mode, ticket, 'business-expert', stage_work);

    // Then:
    then_drop_accepted_with_skill(result, 'abd-domain-sketch');
  });

  it('drag disabled in automatic mode — no error shown', () => {
    // Given:
    const mode = given_board_mode('automatic');

    // When:
    const enabled = when_drag_enabled(mode);

    // Then:
    then_drag_is_disabled(enabled);
  });

  it('drop rejected when all skills already assigned or complete', () => {
    // Given:
    const mode = given_board_mode('manual');
    const stage_work = given_stage_work_required([
      { skill: 'abd-ubiquitous-language', role: 'business-expert' },
      { skill: 'abd-domain-sketch', role: 'business-expert' },
    ]);
    const ticket = given_ticket_with_skills('#502', 'discovery', {
      'abd-ubiquitous-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_assigned('engineer'),
    });

    // When:
    const result = when_agent_dropped_on_ticket(mode, ticket, 'business-expert', stage_work);

    // Then:
    then_drop_rejected_with_message(result, 'No eligible skills remain');
  });
});

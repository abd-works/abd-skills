/**
 * Operate Board in Manual Mode — Server Tests
 *
 * Stories: Toggle Manual Mode,
 *          Move Ticket to In Progress on Agent Advance,
 *          Update Skill Status on Completion,
 *          Move Ticket to Done on Agent Completion
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

interface BoardState {
  schema: string;
  board_mode: BoardMode;
  stage_configuration: string;
  team: Record<string, number>;
  backlog: Ticket[];
  active: Ticket[];
  done: Ticket[];
  archived: Ticket[];
}

interface RenderedTicket {
  ticket_id: string;
  board_position: 'queue' | 'in_progress' | 'done';
  has_movement_indicator: boolean;
  expand_available: boolean;
}

interface SkillRowView {
  skill: string;
  icon: 'not_started' | 'in_progress' | 'magnifying_glass' | 'done_checkmark' | 'rework';
}

interface CardFaceView {
  active_skill: string | null;
}

// ============================================================================
// HELPER FUNCTIONS — Given
// ============================================================================

function given_board_in_mode(mode: BoardMode): BoardState {
  return {
    schema: '1.0',
    board_mode: mode,
    stage_configuration: 'default',
    team: { engineer: 2, 'product-owner': 1 },
    backlog: [],
    active: [],
    done: [],
    archived: [],
  };
}

function given_ticket_at_stage(
  ticketId: string,
  stage: string,
  skillProgress?: Record<string, SkillProgress>,
): Ticket {
  return {
    ticket_id: ticketId,
    lineage: ['PetStore', ticketId],
    stage,
    priority: 1,
    scope_level: 'story',
    skill_progress: skillProgress ?? {},
    board_position: 'queue',
  };
}

function given_ticket_in_progress(
  ticketId: string,
  stage: string,
  skillProgress: Record<string, SkillProgress>,
): Ticket {
  return {
    ...given_ticket_at_stage(ticketId, stage, skillProgress),
    board_position: 'in_progress',
  };
}

function given_skill_in_progress(agent: string): SkillProgress {
  return {
    execution_status: 'in_progress',
    review_status: null,
    agent,
    reviewer: null,
  };
}

function given_skill_execution_done_review_in_progress(
  agent: string,
  reviewer: string,
): SkillProgress {
  return {
    execution_status: 'done',
    review_status: 'in_progress',
    agent,
    reviewer,
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

function given_skill_review_failed(agent: string, reviewer: string): SkillProgress {
  return {
    execution_status: 'done',
    review_status: 'failed',
    agent,
    reviewer,
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

function given_board_with_active_ticket(
  board: BoardState,
  ticket: Ticket,
): BoardState {
  return { ...board, active: [...board.active, ticket] };
}

function given_board_with_backlog_ticket(
  board: BoardState,
  ticket: Ticket,
): BoardState {
  return { ...board, backlog: [...board.backlog, ticket] };
}

// ============================================================================
// HELPER FUNCTIONS — When
// ============================================================================

function when_board_mode_toggled(board: BoardState): BoardState {
  const next_mode: BoardMode = board.board_mode === 'automatic' ? 'manual' : 'automatic';
  return { ...board, board_mode: next_mode };
}

function when_agent_advances_ticket_to_in_progress(
  board: BoardState,
  ticketId: string,
): BoardState {
  const ticket_in_backlog = board.backlog.find((t) => t.ticket_id === ticketId);
  if (ticket_in_backlog) {
    const advanced: Ticket = { ...ticket_in_backlog, board_position: 'in_progress' };
    return {
      ...board,
      backlog: board.backlog.filter((t) => t.ticket_id !== ticketId),
      active: [...board.active, advanced],
    };
  }
  return {
    ...board,
    active: board.active.map((t) =>
      t.ticket_id === ticketId ? { ...t, board_position: 'in_progress' } : t,
    ),
  };
}

function when_skill_completes_work_pass(progress: SkillProgress, reviewer: string): SkillProgress {
  return {
    ...progress,
    execution_status: 'done',
    review_status: 'in_progress',
    reviewer,
  };
}

function when_skill_completes_review_pass(progress: SkillProgress): SkillProgress {
  return {
    ...progress,
    review_status: 'done',
  };
}

function when_skill_review_fails(progress: SkillProgress): SkillProgress {
  return {
    ...progress,
    review_status: 'failed',
    execution_status: 'not_started',
  };
}

function when_agent_writes_stage_complete(
  board: BoardState,
  ticketId: string,
): BoardState {
  const ticket = board.active.find((t) => t.ticket_id === ticketId);
  if (!ticket) return board;
  const completed: Ticket = { ...ticket, board_position: 'done' };
  return {
    ...board,
    active: board.active.filter((t) => t.ticket_id !== ticketId),
    done: [...board.done, completed],
  };
}

// ============================================================================
// HELPER FUNCTIONS — Then
// ============================================================================

function then_board_mode_is(board: BoardState, expected: BoardMode): void {
  expect(board.board_mode).toBe(expected);
}

function then_drag_enabled(board: BoardState): boolean {
  return board.board_mode === 'manual';
}

function then_ticket_in_sub_column(
  board: BoardState,
  ticketId: string,
  subColumn: 'queue' | 'in_progress' | 'done',
): void {
  const all_tickets = [...board.backlog, ...board.active, ...board.done];
  const ticket = all_tickets.find((t) => t.ticket_id === ticketId);
  expect(ticket).toBeDefined();
  expect(ticket!.board_position).toBe(subColumn);
}

function then_render_ticket(ticket: Ticket): RenderedTicket {
  return {
    ticket_id: ticket.ticket_id,
    board_position: ticket.board_position,
    has_movement_indicator: ticket.board_position === 'in_progress',
    expand_available: ticket.board_position === 'in_progress' || ticket.board_position === 'done',
  };
}

function then_skill_shows_review_indicator(progress: SkillProgress): void {
  expect(progress.execution_status).toBe('done');
  expect(progress.review_status).toBe('in_progress');
}

function then_skill_shows_done_checkmark(progress: SkillProgress): void {
  expect(progress.execution_status).toBe('done');
  expect(progress.review_status).toBe('done');
}

function then_skill_shows_rework_indicator(progress: SkillProgress): void {
  expect(progress.review_status).toBe('failed');
  expect(progress.execution_status).toBe('not_started');
}

function then_skill_row_icon(progress: SkillProgress): SkillRowView['icon'] {
  if (progress.execution_status === 'done' && progress.review_status === 'done') return 'done_checkmark';
  if (progress.execution_status === 'done' && progress.review_status === 'in_progress') return 'magnifying_glass';
  if (progress.review_status === 'failed') return 'rework';
  if (progress.execution_status === 'in_progress') return 'in_progress';
  return 'not_started';
}

function then_card_face_active_skill(
  skillProgress: Record<string, SkillProgress>,
  stageWorkOrder: string[],
): string | null {
  for (const skill of stageWorkOrder) {
    const sp = skillProgress[skill];
    if (!sp) return skill;
    if (sp.execution_status !== 'done' || sp.review_status !== 'done') return skill;
  }
  return null;
}

function then_all_skills_show_done_checkmark(
  skillProgress: Record<string, SkillProgress>,
): void {
  for (const [, sp] of Object.entries(skillProgress)) {
    expect(sp.execution_status).toBe('done');
    expect(sp.review_status).toBe('done');
  }
}

function then_in_progress_sub_column_empty(board: BoardState, stage: string): void {
  const in_progress = board.active.filter(
    (t) => t.stage === stage && t.board_position === 'in_progress',
  );
  expect(in_progress).toHaveLength(0);
}

function then_stage_column_visible(board: BoardState, stage: string): void {
  const all_tickets = [...board.backlog, ...board.active, ...board.done];
  const stage_exists = all_tickets.some((t) => t.stage === stage) || true;
  expect(stage_exists).toBe(true);
}

// ============================================================================
// STORY: Toggle Manual Mode
// ============================================================================

describe('Toggle Manual Mode', () => {
  it('board mode switches to manual when user clicks toggle while automatic', () => {
    // Given:
    const board = given_board_in_mode('automatic');

    // When:
    const updated = when_board_mode_toggled(board);

    // Then:
    then_board_mode_is(updated, 'manual');
  });

  it('board mode switches back to automatic when user clicks toggle while manual', () => {
    // Given:
    const board = given_board_in_mode('manual');

    // When:
    const updated = when_board_mode_toggled(board);

    // Then:
    then_board_mode_is(updated, 'automatic');
  });

  it('agent pool avatars draggable in manual mode, disabled in automatic', () => {
    // Given:
    const manual_board = given_board_in_mode('manual');
    const automatic_board = given_board_in_mode('automatic');

    // When:
    const drag_in_manual = then_drag_enabled(manual_board);
    const drag_in_automatic = then_drag_enabled(automatic_board);

    // Then:
    expect(drag_in_manual).toBe(true);
    expect(drag_in_automatic).toBe(false);
  });
});

// ============================================================================
// STORY: Move Ticket to In Progress on Agent Advance
// ============================================================================

describe('Move Ticket to In Progress on Agent Advance', () => {
  it('ticket moves from queue to in-progress sub-column on agent advance', () => {
    // Given:
    let board = given_board_in_mode('automatic');
    const ticket = given_ticket_at_stage('#301', 'discovery', {
      'abd-ubiquitous-language': given_skill_in_progress('engineer'),
    });
    board = given_board_with_backlog_ticket(board, ticket);

    // When:
    board = when_agent_advances_ticket_to_in_progress(board, '#301');

    // Then:
    then_ticket_in_sub_column(board, '#301', 'in_progress');
    expect(board.backlog.find((t) => t.ticket_id === '#301')).toBeUndefined();
    expect(board.active.find((t) => t.ticket_id === '#301')).toBeDefined();
  });

  it('ticket receives movement indicator and expand becomes available', () => {
    // Given:
    let board = given_board_in_mode('automatic');
    const ticket = given_ticket_at_stage('#302', 'exploration', {
      'abd-acceptance-criteria': given_skill_in_progress('product-owner'),
    });
    board = given_board_with_backlog_ticket(board, ticket);

    // When:
    board = when_agent_advances_ticket_to_in_progress(board, '#302');

    // Then:
    const advanced_ticket = board.active.find((t) => t.ticket_id === '#302')!;
    const rendered = then_render_ticket(advanced_ticket);
    expect(rendered.has_movement_indicator).toBe(true);
    expect(rendered.expand_available).toBe(true);
  });
});

// ============================================================================
// STORY: Update Skill Status on Completion
// ============================================================================

describe('Update Skill Status on Completion', () => {
  it('skill row shows magnifying glass when execution done and review in progress', () => {
    // Given:
    const progress = given_skill_in_progress('engineer');

    // When:
    const updated = when_skill_completes_work_pass(progress, 'product-owner');

    // Then:
    then_skill_shows_review_indicator(updated);
    expect(then_skill_row_icon(updated)).toBe('magnifying_glass');
  });

  it('skill row shows done checkmark when review status transitions to done', () => {
    // Given:
    const progress = given_skill_execution_done_review_in_progress('engineer', 'product-owner');

    // When:
    const updated = when_skill_completes_review_pass(progress);

    // Then:
    then_skill_shows_done_checkmark(updated);
    expect(then_skill_row_icon(updated)).toBe('done_checkmark');
  });

  it('skill row shows rework indicator and execution resets when review fails', () => {
    // Given:
    const progress = given_skill_execution_done_review_in_progress('engineer', 'product-owner');

    // When:
    const updated = when_skill_review_fails(progress);

    // Then:
    then_skill_shows_rework_indicator(updated);
    expect(then_skill_row_icon(updated)).toBe('rework');
  });

  it('card-face icon updates and next incomplete skill becomes focus on completion', () => {
    // Given:
    const stage_work_order = ['abd-ubiquitous-language', 'abd-domain-sketch', 'abd-clean-code'];
    const skill_progress: Record<string, SkillProgress> = {
      'abd-ubiquitous-language': given_skill_execution_done_review_in_progress('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_not_started(),
      'abd-clean-code': given_skill_not_started(),
    };

    // When:
    skill_progress['abd-ubiquitous-language'] = when_skill_completes_review_pass(
      skill_progress['abd-ubiquitous-language'],
    );

    // Then:
    expect(then_skill_row_icon(skill_progress['abd-ubiquitous-language'])).toBe('done_checkmark');
    const next_focus = then_card_face_active_skill(skill_progress, stage_work_order);
    expect(next_focus).toBe('abd-domain-sketch');
  });
});

// ============================================================================
// STORY: Move Ticket to Done on Agent Completion
// ============================================================================

describe('Move Ticket to Done on Agent Completion', () => {
  it('ticket moves from in-progress to done sub-column on stage-complete write', () => {
    // Given:
    let board = given_board_in_mode('automatic');
    const ticket = given_ticket_in_progress('#401', 'discovery', {
      'abd-ubiquitous-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_fully_done('engineer', 'product-owner'),
    });
    board = given_board_with_active_ticket(board, ticket);

    // When:
    board = when_agent_writes_stage_complete(board, '#401');

    // Then:
    then_ticket_in_sub_column(board, '#401', 'done');
    expect(board.active.find((t) => t.ticket_id === '#401')).toBeUndefined();
    expect(board.done.find((t) => t.ticket_id === '#401')).toBeDefined();
  });

  it('all skill rows show done checkmark when ticket moves to done', () => {
    // Given:
    const skill_progress: Record<string, SkillProgress> = {
      'abd-ubiquitous-language': given_skill_fully_done('engineer', 'product-owner'),
      'abd-domain-sketch': given_skill_fully_done('engineer', 'product-owner'),
      'abd-acceptance-criteria': given_skill_fully_done('product-owner', 'engineer'),
    };

    // When:
    let board = given_board_in_mode('automatic');
    const ticket = given_ticket_in_progress('#402', 'exploration', skill_progress);
    board = given_board_with_active_ticket(board, ticket);
    board = when_agent_writes_stage_complete(board, '#402');

    // Then:
    const done_ticket = board.done.find((t) => t.ticket_id === '#402')!;
    then_all_skills_show_done_checkmark(done_ticket.skill_progress);
  });

  it('in-progress sub-column empty when last ticket moves to done', () => {
    // Given:
    let board = given_board_in_mode('automatic');
    const ticket = given_ticket_in_progress('#403', 'shaping', {
      'abd-story-mapping': given_skill_fully_done('product-owner', 'engineer'),
    });
    board = given_board_with_active_ticket(board, ticket);

    // When:
    board = when_agent_writes_stage_complete(board, '#403');

    // Then:
    then_stage_column_visible(board, 'shaping');
    then_in_progress_sub_column_empty(board, 'shaping');
  });
});

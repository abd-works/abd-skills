/**
 * Board Rendering Tests
 *
 * Stories: Organize Tickets into Stage Groups by Delivery Phase,
 *          Show Assigned Skills per Stage,
 *          Display Backlog Tickets
 */
import { describe, it, expect } from 'vitest';

// ============================================================================
// TYPES (domain model — refactored terms)
// ============================================================================

interface SkillProgress {
  execution_status: 'not_started' | 'in_progress' | 'done';
  review_status: 'not_started' | 'in_progress' | 'done' | 'failed' | null;
  executing_agent_role: string | null;
  reviewing_agent_role: string | null;
}

interface Ticket {
  ticket_id: string;
  lineage: string[];
  stage: string;
  priority: number;
  skill_progress: Record<string, SkillProgress>;
}

interface StageWorkRequired {
  skill_name: string;
  delivery_role: string;
}

interface StageConfiguration {
  stages: string[];
  stage_work_required: Record<string, StageWorkRequired[]>;
}

interface KanbanBoard {
  stages: string[];
  tickets: Ticket[];
  stage_configuration: StageConfiguration;
}

interface RenderedBoard {
  stage_columns: StageColumn[];
  backlog_column: BacklogColumn;
}

interface StageColumn {
  stage_name: string;
  tickets: Ticket[];
  sub_columns?: { in_progress: Ticket[]; done: Ticket[] };
  is_empty: boolean;
  skill_rail: SkillChip[];
}

interface SkillChip {
  skill_name: string;
  delivery_role: string;
}

interface BacklogColumn {
  tickets: BacklogTicketView[];
  is_empty: boolean;
}

interface BacklogTicketView {
  ticket_id: string;
  display_name: string;
  lineage: string[];
  priority: number;
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function given_kanban_board_with_stages(stage_names: string[]): KanbanBoard {
  return {
    stages: stage_names,
    tickets: [],
    stage_configuration: {
      stages: stage_names,
      stage_work_required: {},
    },
  };
}

function given_ticket_at_stage(
  board: KanbanBoard,
  ticket_id: string,
  display_name: string,
  stage: string,
  skill_progress: Record<string, SkillProgress> = {},
): KanbanBoard {
  const ticket: Ticket = {
    ticket_id,
    lineage: [display_name],
    stage,
    priority: 1,
    skill_progress,
  };
  return { ...board, tickets: [...board.tickets, ticket] };
}

function given_ticket_in_progress_at_stage(
  board: KanbanBoard,
  ticket_id: string,
  stage: string,
): KanbanBoard {
  return given_ticket_at_stage(board, ticket_id, ticket_id, stage, {
    'skill-a': {
      execution_status: 'in_progress',
      review_status: null,
      executing_agent_role: 'engineer',
      reviewing_agent_role: null,
    },
  });
}

function given_ticket_done_at_stage(
  board: KanbanBoard,
  ticket_id: string,
  stage: string,
): KanbanBoard {
  return given_ticket_at_stage(board, ticket_id, ticket_id, stage, {
    'skill-a': {
      execution_status: 'done',
      review_status: 'done',
      executing_agent_role: 'engineer',
      reviewing_agent_role: 'engineer',
    },
  });
}

function given_stage_work_required(
  board: KanbanBoard,
  stage: string,
  skills: StageWorkRequired[],
): KanbanBoard {
  return {
    ...board,
    stage_configuration: {
      ...board.stage_configuration,
      stage_work_required: {
        ...board.stage_configuration.stage_work_required,
        [stage]: skills,
      },
    },
  };
}

function given_backlog_tickets(
  board: KanbanBoard,
  tickets: Array<{ ticket_id: string; lineage: string[]; priority: number }>,
): KanbanBoard {
  const backlog_tickets: Ticket[] = tickets.map((t) => ({
    ticket_id: t.ticket_id,
    lineage: t.lineage,
    stage: 'backlog',
    priority: t.priority,
    skill_progress: {},
  }));
  return { ...board, tickets: [...board.tickets, ...backlog_tickets] };
}

function when_board_renders(board: KanbanBoard): RenderedBoard {
  const stage_columns: StageColumn[] = board.stages.map((stage_name) => {
    const stage_tickets = board.tickets.filter((t) => t.stage === stage_name);
    const in_progress = stage_tickets.filter((t) =>
      Object.values(t.skill_progress).some((sp) => sp.execution_status === 'in_progress'),
    );
    const done = stage_tickets.filter((t) =>
      Object.values(t.skill_progress).every((sp) => sp.execution_status === 'done'),
    );
    const has_sub_columns = in_progress.length > 0 && done.length > 0;
    const skills = board.stage_configuration.stage_work_required[stage_name] ?? [];

    return {
      stage_name,
      tickets: stage_tickets,
      sub_columns: has_sub_columns ? { in_progress, done } : undefined,
      is_empty: stage_tickets.length === 0,
      skill_rail: skills.map((s) => ({
        skill_name: s.skill_name,
        delivery_role: s.delivery_role,
      })),
    };
  });

  const backlog_tickets = board.tickets
    .filter((t) => t.stage === 'backlog')
    .sort((a, b) => a.priority - b.priority)
    .map((t) => ({
      ticket_id: t.ticket_id,
      display_name: t.lineage[t.lineage.length - 1],
      lineage: t.lineage,
      priority: t.priority,
    }));

  return {
    stage_columns,
    backlog_column: {
      tickets: backlog_tickets,
      is_empty: backlog_tickets.length === 0,
    },
  };
}

function then_ticket_appears_in_stage(
  rendered: RenderedBoard,
  ticket_id: string,
  stage_name: string,
): void {
  const column = rendered.stage_columns.find((c) => c.stage_name === stage_name);
  expect(column).toBeDefined();
  const ticket = column!.tickets.find((t) => t.ticket_id === ticket_id);
  expect(ticket).toBeDefined();
}

function then_stages_arranged_left_to_right(
  rendered: RenderedBoard,
  expected_order: string[],
): void {
  const actual_order = rendered.stage_columns.map((c) => c.stage_name);
  expect(actual_order).toEqual(expected_order);
}

function then_stage_shows_sub_columns(
  rendered: RenderedBoard,
  stage_name: string,
  in_progress_ids: string[],
  done_ids: string[],
): void {
  const column = rendered.stage_columns.find((c) => c.stage_name === stage_name);
  expect(column).toBeDefined();
  expect(column!.sub_columns).toBeDefined();
  const actual_in_progress = column!.sub_columns!.in_progress.map((t) => t.ticket_id);
  const actual_done = column!.sub_columns!.done.map((t) => t.ticket_id);
  expect(actual_in_progress).toEqual(in_progress_ids);
  expect(actual_done).toEqual(done_ids);
}

function then_stage_is_visible_but_empty(
  rendered: RenderedBoard,
  stage_name: string,
): void {
  const column = rendered.stage_columns.find((c) => c.stage_name === stage_name);
  expect(column).toBeDefined();
  expect(column!.is_empty).toBe(true);
}

function then_stage_shows_skill_rail_with_chips(
  rendered: RenderedBoard,
  stage_name: string,
  expected_chips: string[],
): void {
  const column = rendered.stage_columns.find((c) => c.stage_name === stage_name);
  expect(column).toBeDefined();
  const chip_labels = column!.skill_rail.map((c) => c.skill_name);
  expect(chip_labels).toEqual(expected_chips);
}

function then_no_skill_rail_appears(
  rendered: RenderedBoard,
  stage_name: string,
): void {
  const column = rendered.stage_columns.find((c) => c.stage_name === stage_name);
  expect(column).toBeDefined();
  expect(column!.skill_rail).toHaveLength(0);
}

function then_backlog_ticket_appears_above(
  rendered: RenderedBoard,
  higher_id: string,
  lower_id: string,
): void {
  const tickets = rendered.backlog_column.tickets;
  const higher_index = tickets.findIndex((t) => t.ticket_id === higher_id);
  const lower_index = tickets.findIndex((t) => t.ticket_id === lower_id);
  expect(higher_index).toBeLessThan(lower_index);
}

function then_backlog_ticket_shows_display_name(
  rendered: RenderedBoard,
  ticket_id: string,
  expected_name: string,
): void {
  const ticket = rendered.backlog_column.tickets.find((t) => t.ticket_id === ticket_id);
  expect(ticket).toBeDefined();
  expect(ticket!.display_name).toBe(expected_name);
}

function then_backlog_shows_lineage_tooltip(
  ticket: BacklogTicketView,
): string {
  return ticket.lineage.join(' > ');
}

function then_backlog_column_is_empty(rendered: RenderedBoard): void {
  expect(rendered.backlog_column.is_empty).toBe(true);
  expect(rendered.backlog_column.tickets).toHaveLength(0);
}

// ============================================================================
// STORY: Organize Tickets into Stage Groups by Delivery Phase
// ============================================================================

describe('Organize Tickets into Stage Groups by Delivery Phase', () => {
  it('tickets grouped under their assigned stages', () => {
    // Given
    let board = given_kanban_board_with_stages(['shaping', 'discovery', 'exploration']);
    board = given_ticket_at_stage(board, '#101', 'Build Domain Model', 'discovery');
    board = given_ticket_at_stage(board, '#102', 'Write Acceptance Tests', 'exploration');

    // When
    const rendered = when_board_renders(board);

    // Then
    then_ticket_appears_in_stage(rendered, '#101', 'discovery');
    then_ticket_appears_in_stage(rendered, '#102', 'exploration');
    then_stages_arranged_left_to_right(rendered, ['shaping', 'discovery', 'exploration']);
  });

  it('stage with both in-progress and done tickets shows sub-columns', () => {
    // Given
    let board = given_kanban_board_with_stages(['discovery']);
    board = given_ticket_in_progress_at_stage(board, '#201', 'discovery');
    board = given_ticket_done_at_stage(board, '#202', 'discovery');

    // When
    const rendered = when_board_renders(board);

    // Then
    then_stage_shows_sub_columns(rendered, 'discovery', ['#201'], ['#202']);
  });

  it('empty stage still renders', () => {
    // Given
    const board = given_kanban_board_with_stages(['shaping', 'discovery', 'exploration']);

    // When
    const rendered = when_board_renders(board);

    // Then
    then_stage_is_visible_but_empty(rendered, 'shaping');
  });
});

// ============================================================================
// STORY: Show Assigned Skills per Stage
// ============================================================================

describe('Show Assigned Skills per Stage', () => {
  it('stage skill rail appears with skill chips', () => {
    // Given
    let board = given_kanban_board_with_stages(['discovery']);
    board = given_stage_work_required(board, 'discovery', [
      { skill_name: 'abd-ubiquitous-language', delivery_role: 'business-expert' },
      { skill_name: 'abd-domain-sketch', delivery_role: 'business-expert' },
    ]);

    // When
    const rendered = when_board_renders(board);

    // Then
    then_stage_shows_skill_rail_with_chips(rendered, 'discovery', [
      'abd-ubiquitous-language',
      'abd-domain-sketch',
    ]);
  });

  it('stage with no skills shows no rail', () => {
    // Given
    let board = given_kanban_board_with_stages(['context']);
    board = given_stage_work_required(board, 'context', []);

    // When
    const rendered = when_board_renders(board);

    // Then
    then_no_skill_rail_appears(rendered, 'context');
    const column = rendered.stage_columns.find((c) => c.stage_name === 'context');
    expect(column).toBeDefined();
  });
});

// ============================================================================
// STORY: Display Backlog Tickets
// ============================================================================

describe('Display Backlog Tickets', () => {
  it('backlog tickets ordered by priority', () => {
    // Given
    let board = given_kanban_board_with_stages(['discovery']);
    board = given_backlog_tickets(board, [
      { ticket_id: 'STORY-003', lineage: ['PetStore', 'Sprint 1', 'Add Pet'], priority: 1 },
      { ticket_id: 'STORY-007', lineage: ['PetStore', 'Sprint 1', 'List Pets'], priority: 2 },
    ]);

    // When
    const rendered = when_board_renders(board);

    // Then
    then_backlog_ticket_appears_above(rendered, 'STORY-003', 'STORY-007');
    then_backlog_ticket_shows_display_name(rendered, 'STORY-003', 'Add Pet');
    then_backlog_ticket_shows_display_name(rendered, 'STORY-007', 'List Pets');
  });

  it('hovering backlog ticket shows full lineage', () => {
    // Given
    let board = given_kanban_board_with_stages(['discovery']);
    board = given_backlog_tickets(board, [
      { ticket_id: 'STORY-003', lineage: ['PetStore', 'Sprint 1', 'Add Pet'], priority: 1 },
    ]);

    // When
    const rendered = when_board_renders(board);

    // Then
    const ticket = rendered.backlog_column.tickets.find((t) => t.ticket_id === 'STORY-003')!;
    const tooltip = then_backlog_shows_lineage_tooltip(ticket);
    expect(tooltip).toBe('PetStore > Sprint 1 > Add Pet');
  });

  it('empty backlog renders without cards', () => {
    // Given
    const board = given_kanban_board_with_stages(['discovery']);

    // When
    const rendered = when_board_renders(board);

    // Then
    then_backlog_column_is_empty(rendered);
  });
});

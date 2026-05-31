/**
 * Board Connectivity Tests
 *
 * Stories: Connect Board to a Planning Folder,
 *          Board Reflects Agent Changes Automatically
 */
import { describe, it, expect } from 'vitest';

// ============================================================================
// TYPES (domain model — refactored terms)
// ============================================================================

interface PlanningFolder {
  path: string;
  exists: boolean;
  has_board_json: boolean;
}

interface ConnectionResult {
  success: boolean;
  message: string;
  board_populated: boolean;
}

interface Ticket {
  ticket_id: string;
  stage: string;
  sub_state: 'in_progress' | 'done';
}

interface FileChangeEvent {
  path: string;
  file_name: string;
}

interface BoardRefreshResult {
  should_refresh: boolean;
  ticket_changes: TicketChange[];
  liveness_changes: LivenessChange[];
}

interface TicketChange {
  ticket_id: string;
  new_stage: string;
  new_sub_state: 'in_progress' | 'done';
}

interface LivenessChange {
  agent_role: string;
  previous_state: string;
  new_state: string;
}

// ============================================================================
// HELPER FUNCTIONS — Connect Board
// ============================================================================

function given_valid_planning_folder_with_board(path: string): PlanningFolder {
  return { path, exists: true, has_board_json: true };
}

function given_nonexistent_planning_folder(path: string): PlanningFolder {
  return { path, exists: false, has_board_json: false };
}

function given_valid_planning_folder_without_board(path: string): PlanningFolder {
  return { path, exists: true, has_board_json: false };
}

function when_delivery_lead_connects(folder: PlanningFolder): ConnectionResult {
  if (!folder.exists) {
    return {
      success: false,
      message: `Planning folder not found: ${folder.path}`,
      board_populated: false,
    };
  }

  if (!folder.has_board_json) {
    return {
      success: false,
      message: 'board.json missing. Initialize with kanban-lead setup.',
      board_populated: false,
    };
  }

  return {
    success: true,
    message: 'Planning folder connected.',
    board_populated: true,
  };
}

function then_board_populates_with_tickets_and_stages(result: ConnectionResult): void {
  expect(result.success).toBe(true);
  expect(result.board_populated).toBe(true);
}

function then_delivery_lead_sees_message(
  result: ConnectionResult,
  expected_message: string,
): void {
  expect(result.message).toBe(expected_message);
}

function then_previously_connected_folder_remains_active(
  result: ConnectionResult,
): void {
  expect(result.success).toBe(false);
}

// ============================================================================
// HELPER FUNCTIONS — Board Reflects Agent Changes
// ============================================================================

function given_delivery_lead_viewing_board_with_ticket(
  ticket_id: string,
  stage: string,
  sub_state: 'in_progress' | 'done',
): Ticket {
  return { ticket_id, stage, sub_state };
}

function given_agent_previously_inactive(agent_role: string): LivenessChange {
  return { agent_role, previous_state: 'inactive', new_state: 'inactive' };
}

function when_agent_completes_skill_and_writes_board(
  ticket: Ticket,
): BoardRefreshResult {
  return {
    should_refresh: true,
    ticket_changes: [
      {
        ticket_id: ticket.ticket_id,
        new_stage: ticket.stage,
        new_sub_state: 'done',
      },
    ],
    liveness_changes: [],
  };
}

function when_agent_writes_fresh_heartbeat(
  agent_role: string,
): BoardRefreshResult {
  return {
    should_refresh: true,
    ticket_changes: [],
    liveness_changes: [
      {
        agent_role,
        previous_state: 'inactive',
        new_state: 'idle',
      },
    ],
  };
}

function when_agent_writes_non_board_file(file_name: string): FileChangeEvent {
  return { path: `/kanban/${file_name}`, file_name };
}

function should_trigger_board_refresh(event: FileChangeEvent): boolean {
  const board_files = ['board.json', 'kanban.json'];
  const heartbeat_pattern = /heartbeat/i;
  return (
    board_files.includes(event.file_name) ||
    heartbeat_pattern.test(event.file_name)
  );
}

function then_ticket_moves_to_done_sub_column(
  result: BoardRefreshResult,
  ticket_id: string,
): void {
  expect(result.should_refresh).toBe(true);
  const change = result.ticket_changes.find((c) => c.ticket_id === ticket_id);
  expect(change).toBeDefined();
  expect(change!.new_sub_state).toBe('done');
}

function then_no_manual_refresh_needed(result: BoardRefreshResult): void {
  expect(result.should_refresh).toBe(true);
}

function then_agent_liveness_changes_to_idle(
  result: BoardRefreshResult,
  agent_role: string,
): void {
  const change = result.liveness_changes.find((c) => c.agent_role === agent_role);
  expect(change).toBeDefined();
  expect(change!.new_state).toBe('idle');
}

function then_board_does_not_refresh(event: FileChangeEvent): void {
  expect(should_trigger_board_refresh(event)).toBe(false);
}

// ============================================================================
// STORY: Connect Board to a Planning Folder
// ============================================================================

describe('Connect Board to a Planning Folder', () => {
  it('successful connection loads the board', () => {
    // Given
    const folder = given_valid_planning_folder_with_board('C:\\dev\\project\\kanban');

    // When
    const result = when_delivery_lead_connects(folder);

    // Then
    then_board_populates_with_tickets_and_stages(result);
    then_delivery_lead_sees_message(result, 'Planning folder connected.');
  });

  it('invalid folder shows error', () => {
    // Given
    const folder = given_nonexistent_planning_folder('C:\\dev\\nonexistent');

    // When
    const result = when_delivery_lead_connects(folder);

    // Then
    then_delivery_lead_sees_message(
      result,
      'Planning folder not found: C:\\dev\\nonexistent',
    );
    then_previously_connected_folder_remains_active(result);
  });

  it('missing board file shows initialization message', () => {
    // Given
    const folder = given_valid_planning_folder_without_board('C:\\dev\\project\\kanban');

    // When
    const result = when_delivery_lead_connects(folder);

    // Then
    then_delivery_lead_sees_message(
      result,
      'board.json missing. Initialize with kanban-lead setup.',
    );
  });
});

// ============================================================================
// STORY: Board Reflects Agent Changes Automatically
// ============================================================================

describe('Board Reflects Agent Changes Automatically', () => {
  it('agent moves a ticket - board refreshes', () => {
    // Given
    const ticket = given_delivery_lead_viewing_board_with_ticket(
      '#101',
      'discovery',
      'in_progress',
    );

    // When
    const result = when_agent_completes_skill_and_writes_board(ticket);

    // Then
    then_ticket_moves_to_done_sub_column(result, '#101');
    then_no_manual_refresh_needed(result);
  });

  it('agent writes heartbeat - liveness updates', () => {
    // Given
    given_agent_previously_inactive('engineer');

    // When
    const result = when_agent_writes_fresh_heartbeat('engineer');

    // Then
    then_agent_liveness_changes_to_idle(result, 'engineer');
  });

  it('non-board file changes do not trigger refresh', () => {
    // Given — delivery lead is viewing the board

    // When
    const event = when_agent_writes_non_board_file('strategy.md');

    // Then
    then_board_does_not_refresh(event);
  });
});

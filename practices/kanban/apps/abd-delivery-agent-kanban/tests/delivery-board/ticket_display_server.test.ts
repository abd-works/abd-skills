/**
 * Ticket Display Tests
 *
 * Stories: Animate Ticket on Position Change,
 *          Show Active Skill and Agent on Ticket
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
  stage: string;
  sub_state: 'in_progress' | 'done';
  skill_progress: Record<string, SkillProgress>;
}

interface BoardPosition {
  ticket_id: string;
  stage: string;
  sub_state: 'in_progress' | 'done';
}

interface TicketAnimationResult {
  ticket_id: string;
  should_animate: boolean;
  target_position: BoardPosition;
}

interface TicketAgentDisplay {
  ticket_id: string;
  bot_icon_visible: boolean;
  bot_icon_discipline: string | null;
  agent_avatar_role: string | null;
  magnifying_glass_icon: boolean;
}

// ============================================================================
// HELPER FUNCTIONS — Animation
// ============================================================================

function given_previous_board_position(
  ticket_id: string,
  stage: string,
  sub_state: 'in_progress' | 'done',
): BoardPosition {
  return { ticket_id, stage, sub_state };
}

function given_ticket_with_skill_progress(
  ticket_id: string,
  stage: string,
  skill_progress: Record<string, SkillProgress>,
): Ticket {
  const all_done = Object.values(skill_progress).every(
    (sp) => sp.execution_status === 'done',
  );
  return {
    ticket_id,
    stage,
    sub_state: all_done ? 'done' : 'in_progress',
    skill_progress,
  };
}

function when_board_refreshes_with_position_change(
  ticket: Ticket,
  previous_position: BoardPosition | null,
): TicketAnimationResult {
  const current_position: BoardPosition = {
    ticket_id: ticket.ticket_id,
    stage: ticket.stage,
    sub_state: ticket.sub_state,
  };

  const should_animate =
    previous_position !== null &&
    (previous_position.stage !== current_position.stage ||
      previous_position.sub_state !== current_position.sub_state);

  return {
    ticket_id: ticket.ticket_id,
    should_animate,
    target_position: current_position,
  };
}

function then_ticket_animates_to_sub_column(
  result: TicketAnimationResult,
  expected_sub_state: 'in_progress' | 'done',
): void {
  expect(result.should_animate).toBe(true);
  expect(result.target_position.sub_state).toBe(expected_sub_state);
}

function then_ticket_renders_without_animation(
  result: TicketAnimationResult,
): void {
  expect(result.should_animate).toBe(false);
}

function then_position_is_recorded(result: TicketAnimationResult): void {
  expect(result.target_position).toBeDefined();
  expect(result.target_position.ticket_id).toBeDefined();
  expect(result.target_position.stage).toBeDefined();
}

// ============================================================================
// HELPER FUNCTIONS — Active Skill and Agent Display
// ============================================================================

function given_ticket_with_executing_skill(
  ticket_id: string,
  skill_name: string,
  execution_status: 'not_started' | 'in_progress' | 'done',
  executing_agent_role: string,
): Ticket {
  return {
    ticket_id,
    stage: 'discovery',
    sub_state: execution_status === 'done' ? 'done' : 'in_progress',
    skill_progress: {
      [skill_name]: {
        execution_status,
        review_status: null,
        executing_agent_role,
        reviewing_agent_role: null,
      },
    },
  };
}

function given_ticket_with_reviewing_skill(
  ticket_id: string,
  skill_name: string,
  reviewing_agent_role: string,
): Ticket {
  return {
    ticket_id,
    stage: 'discovery',
    sub_state: 'in_progress',
    skill_progress: {
      [skill_name]: {
        execution_status: 'done',
        review_status: 'in_progress',
        executing_agent_role: 'business-expert',
        reviewing_agent_role,
      },
    },
  };
}

function given_ticket_with_all_skills_done(ticket_id: string): Ticket {
  return {
    ticket_id,
    stage: 'discovery',
    sub_state: 'done',
    skill_progress: {
      'abd-ubiquitous-language': {
        execution_status: 'done',
        review_status: 'done',
        executing_agent_role: 'business-expert',
        reviewing_agent_role: 'engineer',
      },
    },
  };
}

function when_board_renders_ticket_agent_display(ticket: Ticket): TicketAgentDisplay {
  const active_skill = Object.entries(ticket.skill_progress).find(
    ([, sp]) => sp.execution_status === 'in_progress',
  );
  const reviewing_skill = Object.entries(ticket.skill_progress).find(
    ([, sp]) => sp.review_status === 'in_progress',
  );

  if (reviewing_skill) {
    return {
      ticket_id: ticket.ticket_id,
      bot_icon_visible: false,
      bot_icon_discipline: null,
      agent_avatar_role: reviewing_skill[1].reviewing_agent_role,
      magnifying_glass_icon: true,
    };
  }

  if (active_skill) {
    return {
      ticket_id: ticket.ticket_id,
      bot_icon_visible: true,
      bot_icon_discipline: active_skill[0],
      agent_avatar_role: active_skill[1].executing_agent_role,
      magnifying_glass_icon: false,
    };
  }

  return {
    ticket_id: ticket.ticket_id,
    bot_icon_visible: false,
    bot_icon_discipline: null,
    agent_avatar_role: null,
    magnifying_glass_icon: false,
  };
}

function then_ticket_shows_bot_icon_and_agent(
  display: TicketAgentDisplay,
  expected_role: string,
): void {
  expect(display.bot_icon_visible).toBe(true);
  expect(display.agent_avatar_role).toBe(expected_role);
}

function then_ticket_shows_no_indicators(display: TicketAgentDisplay): void {
  expect(display.bot_icon_visible).toBe(false);
  expect(display.agent_avatar_role).toBeNull();
  expect(display.magnifying_glass_icon).toBe(false);
}

function then_ticket_shows_magnifying_glass_and_reviewer(
  display: TicketAgentDisplay,
  expected_reviewer_role: string,
): void {
  expect(display.magnifying_glass_icon).toBe(true);
  expect(display.agent_avatar_role).toBe(expected_reviewer_role);
}

// ============================================================================
// STORY: Animate Ticket on Position Change
// ============================================================================

describe('Animate Ticket on Position Change', () => {
  it('ticket moves stage and animates', () => {
    // Given
    const previous = given_previous_board_position('#101', 'discovery', 'in_progress');
    const ticket = given_ticket_with_skill_progress('#101', 'discovery', {
      'abd-ubiquitous-language': {
        execution_status: 'done',
        review_status: 'done',
        executing_agent_role: 'business-expert',
        reviewing_agent_role: 'engineer',
      },
    });

    // When
    const result = when_board_refreshes_with_position_change(ticket, previous);

    // Then
    then_ticket_animates_to_sub_column(result, 'done');
  });

  it('new ticket does not animate', () => {
    // Given
    const ticket = given_ticket_with_skill_progress('#301', 'discovery', {
      'abd-ubiquitous-language': {
        execution_status: 'not_started',
        review_status: null,
        executing_agent_role: null,
        reviewing_agent_role: null,
      },
    });

    // When
    const result = when_board_refreshes_with_position_change(ticket, null);

    // Then
    then_ticket_renders_without_animation(result);
    then_position_is_recorded(result);
  });
});

// ============================================================================
// STORY: Show Active Skill and Agent on Ticket
// ============================================================================

describe('Show Active Skill and Agent on Ticket', () => {
  it('executing agent shown on ticket', () => {
    // Given
    const ticket = given_ticket_with_executing_skill(
      '#101',
      'abd-ubiquitous-language',
      'in_progress',
      'business-expert',
    );

    // When
    const display = when_board_renders_ticket_agent_display(ticket);

    // Then
    then_ticket_shows_bot_icon_and_agent(display, 'business-expert');
  });

  it('no active skill shows no indicators', () => {
    // Given
    const ticket = given_ticket_with_all_skills_done('#102');

    // When
    const display = when_board_renders_ticket_agent_display(ticket);

    // Then
    then_ticket_shows_no_indicators(display);
  });

  it('reviewing agent replaces executor', () => {
    // Given
    const ticket = given_ticket_with_reviewing_skill(
      '#101',
      'abd-ubiquitous-language',
      'engineer',
    );

    // When
    const display = when_board_renders_ticket_agent_display(ticket);

    // Then
    then_ticket_shows_magnifying_glass_and_reviewer(display, 'engineer');
  });
});

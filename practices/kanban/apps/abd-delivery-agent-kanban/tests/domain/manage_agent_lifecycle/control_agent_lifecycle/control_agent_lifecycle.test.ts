/**
 * Control Agent Lifecycle
 *
 * Epic:     Manage Agent Lifecycle via Cursor SDK
 * Sub-epic: Control Agent Lifecycle
 *
 * Stories:
 *   - Start Team Member Agent
 *   - Stop Team Member Agent
 *   - Report Agent Session Status via SDK
 *   - Restart Stale Agent
 *   - Detect Agent Completion via SDK
 */

import { describe, it, expect } from 'vitest';

import { KanbanLead, TeamMember, AgentSession } from '@deliveryforge/kanban-server';
import { Ticket, SkillProgress, StageDef } from '@deliveryforge/kanban-shared';

// ============================================================================
// HELPER FUNCTIONS — Start / Stop Team Member
// ============================================================================

function given_kanban_lead_running_scan_cycle(): KanbanLead {
  return KanbanLead.createForScanCycle();
}

function given_ticket_active_at_stage(
  ticketId: string,
  stage: string,
  skill: string,
  role: string,
): Ticket {
  return Ticket.createActive(ticketId, stage, skill, role);
}

function given_multiple_tickets_with_eligible_work(
  role: string,
  entries: Array<{ ticketId: string; stage: string; skill: string }>,
): Ticket[] {
  return entries.map((e) => Ticket.createActive(e.ticketId, e.stage, e.skill, role));
}

function given_no_agent_session_for_role(role: string): void {
  AgentSession.clearForRole(role);
}

function given_agent_session_active(role: string): AgentSession {
  return AgentSession.createActive(role);
}

function given_agent_idle(session: AgentSession): AgentSession {
  return session.setIdle();
}

function given_agent_executing_skill(
  session: AgentSession,
  skill: string,
  ticketId: string,
): AgentSession {
  return session.setExecuting(skill, ticketId);
}

function given_skill_progress_in_progress(
  ticketId: string,
  skill: string,
): SkillProgress {
  return SkillProgress.create(ticketId, skill, 'in_progress');
}

// ============================================================================
// HELPER FUNCTIONS — Report Agent Session Status
// ============================================================================

function given_agent_session_with_messages(
  role: string,
  messageCount: number,
  lastActivitySec: number,
): AgentSession {
  return AgentSession.createWithMessages(role, messageCount, lastActivitySec);
}

function given_agent_session_completed(role: string, finalMessage: string): AgentSession {
  return AgentSession.createCompleted(role, finalMessage);
}

function given_agent_session_failed(role: string, errorDetail: string): AgentSession {
  return AgentSession.createFailed(role, errorDetail);
}

function when_system_queries_session_status(session: AgentSession) {
  return session.queryStatus();
}

function then_status_reports(
  status: ReturnType<AgentSession['queryStatus']>,
  expected: Record<string, unknown>,
): void {
  for (const [key, value] of Object.entries(expected)) {
    expect(status[key as keyof typeof status]).toBe(value);
  }
}

// ============================================================================
// HELPER FUNCTIONS — Restart Stale Agent
// ============================================================================

function given_agent_session_stale(
  role: string,
  noOutputSeconds: number,
  skill: string,
  ticketId: string,
): AgentSession {
  return AgentSession.createStale(role, noOutputSeconds, skill, ticketId);
}

function given_agent_session_ended_with_remaining_work(
  role: string,
): AgentSession {
  return AgentSession.createCompleted(role, 'Previous work finished');
}

function when_kanban_lead_detects_stale(lead: KanbanLead, session: AgentSession) {
  return lead.detectStaleAndRestart(session);
}

function when_kanban_lead_detects_completed_with_remaining_work(
  lead: KanbanLead,
  session: AgentSession,
  eligibleTicket: Ticket,
) {
  return lead.detectCompletedAndRestart(session, eligibleTicket);
}

// ============================================================================
// HELPER FUNCTIONS — Start / Stop assertions
// ============================================================================

function when_kanban_lead_starts_team_member(
  lead: KanbanLead,
  role: string,
  tickets: Ticket | Ticket[],
): AgentSession {
  const ticketList = Array.isArray(tickets) ? tickets : [tickets];
  return lead.startTeamMember(role, ticketList);
}

function when_kanban_lead_stops_team_member(
  lead: KanbanLead,
  session: AgentSession,
): AgentSession {
  return lead.stopTeamMember(session);
}

function then_agent_session_is_running(session: AgentSession): void {
  expect(session.state).toBe('running');
}

function then_agent_session_is_terminated(session: AgentSession): void {
  expect(session.state).toBe('completed');
}

function then_agent_pool_shows_avatar_state(
  lead: KanbanLead,
  role: string,
  state: string,
): void {
  expect(lead.getPoolAvatarState(role)).toBe(state);
}

function then_agent_is_executing_skill(
  session: AgentSession,
  skill: string,
  ticketId: string,
): void {
  expect(session.currentSkill).toBe(skill);
  expect(session.currentTicketId).toBe(ticketId);
}

function then_skill_progress_retained(
  progress: SkillProgress,
  expectedStatus: string,
): void {
  expect(progress.executionStatus).toBe(expectedStatus);
}

function then_skill_not_marked_done(progress: SkillProgress): void {
  expect(progress.executionStatus).not.toBe('done');
}

// ============================================================================
// HELPER FUNCTIONS — Detect Agent Completion
// ============================================================================

function given_agent_executing_final_skill(
  role: string,
  skill: string,
  ticketId: string,
  stage: string,
): { session: AgentSession; ticket: Ticket } {
  const session = AgentSession.createActive(role).setExecuting(skill, ticketId);
  const ticket = Ticket.createWithAllSkillsDoneExcept(ticketId, stage, skill, role);
  return { session, ticket };
}

function when_agent_finishes_skill(
  lead: KanbanLead,
  session: AgentSession,
): { updatedProgress: SkillProgress; session: AgentSession } {
  return lead.handleSkillCompletion(session);
}

function then_skill_progress_is_done(progress: SkillProgress): void {
  expect(progress.executionStatus).toBe('done');
}

function then_ticket_moves_to_done_sub_column(
  lead: KanbanLead,
  ticketId: string,
  stage: string,
): void {
  expect(lead.getTicketSubColumn(ticketId, stage)).toBe('Done');
}

// ============================================================================
// STORY: Start Team Member Agent
// ============================================================================

describe('Start Team Member Agent', () => {
  it('KanbanLead starts engineer for eligible skill — session moves to running; agent pool shows working', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const ticket = given_ticket_active_at_stage(
      '1-inc-1-sprint-a', 'specification', 'abd-architecture-specification', 'engineer',
    );
    given_no_agent_session_for_role('engineer');

    const session = when_kanban_lead_starts_team_member(lead, 'engineer', ticket);

    then_agent_session_is_running(session);
    then_agent_is_executing_skill(session, 'abd-architecture-specification', '1-inc-1-sprint-a');
    then_agent_pool_shows_avatar_state(lead, 'engineer', 'working');
  });

  it('KanbanLead starts business-expert for first skill in rail order — pulls downstream first', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const tickets = given_multiple_tickets_with_eligible_work('business-expert', [
      { ticketId: '1-inc-1-sprint-a', stage: 'specification', skill: 'abd-domain-model' },
      { ticketId: '1-inc-2-sprint-b', stage: 'exploration', skill: 'abd-domain-language' },
    ]);
    given_no_agent_session_for_role('business-expert');

    const session = when_kanban_lead_starts_team_member(lead, 'business-expert', tickets);

    then_agent_is_executing_skill(session, 'abd-domain-model', '1-inc-1-sprint-a');
  });
});

// ============================================================================
// STORY: Stop Team Member Agent
// ============================================================================

describe('Stop Team Member Agent', () => {
  it('KanbanLead stops idle team member — session terminates cleanly, pool shows idle', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const session = given_agent_idle(given_agent_session_active('engineer'));

    const terminated = when_kanban_lead_stops_team_member(lead, session);

    then_agent_session_is_terminated(terminated);
    then_agent_pool_shows_avatar_state(lead, 'engineer', 'idle');
  });

  it('Stop agent with in-progress skill — skill progress preserved, session terminates, skill not marked done', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const session = given_agent_executing_skill(
      given_agent_session_active('business-expert'),
      'abd-domain-language',
      '1-inc-1-sprint-a',
    );
    const progress = given_skill_progress_in_progress('1-inc-1-sprint-a', 'abd-domain-language');

    const terminated = when_kanban_lead_stops_team_member(lead, session);

    then_agent_session_is_terminated(terminated);
    then_skill_progress_retained(progress, 'in_progress');
    then_skill_not_marked_done(progress);
  });
});

// ============================================================================
// STORY: Report Agent Session Status via SDK
// ============================================================================

describe('Report Agent Session Status via SDK', () => {
  it('Running session — state running, message_count 42, last_activity_sec 15', () => {
    const session = given_agent_session_with_messages('engineer', 42, 15);

    const status = when_system_queries_session_status(session);

    then_status_reports(status, { state: 'running', message_count: 42, last_activity_sec: 15 });
  });

  it('Completed session — state completed, final_message present', () => {
    const session = given_agent_session_completed(
      'business-expert',
      'Completed abd-domain-language execution',
    );

    const status = when_system_queries_session_status(session);

    then_status_reports(status, { state: 'completed', final_message: 'Completed abd-domain-language execution' });
  });

  it('Failed session — state failed, error_detail present', () => {
    const session = given_agent_session_failed(
      'engineer',
      'Agent session terminated unexpectedly',
    );

    const status = when_system_queries_session_status(session);

    then_status_reports(status, { state: 'failed', error_detail: 'Agent session terminated unexpectedly' });
  });
});

// ============================================================================
// STORY: Restart Stale Agent
// ============================================================================

describe('Restart Stale Agent', () => {
  it('Agent stale (120+ seconds no output) — stop old, create new session, resume work', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const staleSession = given_agent_session_stale(
      'engineer', 120, 'abd-architecture-specification', '1-inc-1-sprint-a',
    );

    const newSession = when_kanban_lead_detects_stale(lead, staleSession);

    then_agent_session_is_running(newSession);
    then_agent_is_executing_skill(newSession, 'abd-architecture-specification', '1-inc-1-sprint-a');
  });

  it('Agent completed but eligible work remains — create new session, claim next skill', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const completedSession = given_agent_session_ended_with_remaining_work('business-expert');
    const eligibleTicket = given_ticket_active_at_stage(
      '1-inc-2-sprint-b', 'exploration', 'abd-domain-terms', 'business-expert',
    );

    const newSession = when_kanban_lead_detects_completed_with_remaining_work(
      lead, completedSession, eligibleTicket,
    );

    then_agent_session_is_running(newSession);
    then_agent_is_executing_skill(newSession, 'abd-domain-terms', '1-inc-2-sprint-b');
  });
});

// ============================================================================
// STORY: Detect Agent Completion via SDK
// ============================================================================

describe('Detect Agent Completion via SDK', () => {
  it('Agent completes skill — KanbanLead updates skill progress to done', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const session = given_agent_executing_skill(
      given_agent_session_active('engineer'),
      'abd-architecture-specification',
      '1-inc-1-sprint-a',
    );

    const { updatedProgress } = when_agent_finishes_skill(lead, session);

    then_skill_progress_is_done(updatedProgress);
  });

  it('Agent completes ALL skills on ticket — KanbanLead marks stage complete, ticket moves to Done sub-column', () => {
    const lead = given_kanban_lead_running_scan_cycle();
    const { session } = given_agent_executing_final_skill(
      'business-expert',
      'abd-specification-by-example',
      '1-inc-1-sprint-a',
      'specification',
    );

    const { updatedProgress } = when_agent_finishes_skill(lead, session);

    then_skill_progress_is_done(updatedProgress);
    then_ticket_moves_to_done_sub_column(lead, '1-inc-1-sprint-a', 'specification');
  });
});

/**
 * Bootstrap Agent from Role Definition
 *
 * Epic:     Manage Agent Lifecycle via Cursor SDK
 * Sub-epic: Bootstrap Agent from Role Definition
 *
 * Stories:
 *   - Resolve Agent Definition from Role
 *   - Parse Skills from Agent Definition
 *   - Create Agent Session via Cursor SDK
 */

import { describe, it, expect } from 'vitest';

import {
  AgentDefinition,
} from '@deliveryforge/kanban-server';

import type {
  BootstrapPrompt,
} from '@deliveryforge/kanban-shared';

import {
  AgentSession,
  KanbanLead,
  TeamMember,
} from '@deliveryforge/kanban-server';

// ============================================================================
// HELPER FUNCTIONS — Resolve Agent Definition from Role
// ============================================================================

function given_workspace_root(path: string): string {
  return path;
}

function given_agent_definition_exists(workspace: string, role: string): void {
  AgentDefinition.seedFixture(workspace, role);
}

function given_no_agent_definition_exists(workspace: string, role: string): void {
  AgentDefinition.removeFixture(workspace, role);
}

function when_system_resolves_agent_definition(
  workspace: string,
  role: string,
): AgentDefinition {
  return AgentDefinition.resolveFromRole(workspace, role);
}

function then_resolved_path_is(definition: AgentDefinition, expected: string): void {
  expect(definition.path).toBe(expected);
}

function then_definition_content_is_loaded(definition: AgentDefinition): void {
  expect(definition.content).toBeDefined();
  expect(definition.content.length).toBeGreaterThan(0);
}

function then_resolution_fails_with_error(fn: () => AgentDefinition, message: string): void {
  expect(fn).toThrowError(message);
}

// ============================================================================
// HELPER FUNCTIONS — Parse Skills from Agent Definition
// ============================================================================

interface ResolvedSkills {
  stageWorkRequired: Array<{ skillName: string; stage: string }>;
  conditional: Array<{ skillName: string }>;
  orchestration: Array<{ skillName: string }>;
  workflowReference?: string;
  referencedFiles: string[];
}

function given_loaded_agent_definition(role: string): AgentDefinition {
  return AgentDefinition.loadFixture(role);
}

function given_kanban_json_assigns_skills_to_role(
  workspace: string,
  role: string,
  skills: Array<{ skillName: string; stage: string }>,
): void {
  AgentDefinition.seedKanbanJsonSkills(workspace, role, skills);
}

function when_system_resolves_eligible_skills(
  definition: AgentDefinition,
  workspace: string,
): ResolvedSkills {
  return definition.resolveEligibleSkills(workspace);
}

function then_stage_work_required_count_is(skills: ResolvedSkills, expected: number): void {
  expect(skills.stageWorkRequired).toHaveLength(expected);
}

function then_conditional_count_is(skills: ResolvedSkills, expected: number): void {
  expect(skills.conditional).toHaveLength(expected);
}

function then_parsed_result_includes_workflow_reference(
  skills: ResolvedSkills,
  workflowRef: string,
): void {
  expect(skills.workflowReference).toBe(workflowRef);
}

function then_referenced_files_include(
  skills: ResolvedSkills,
  ...files: string[]
): void {
  for (const file of files) {
    expect(skills.referencedFiles).toContain(file);
  }
}

function then_skill_list_contains(
  skills: ResolvedSkills,
  ...names: string[]
): void {
  const allNames = [
    ...skills.stageWorkRequired.map((e) => e.skillName),
    ...skills.conditional.map((e) => e.skillName),
    ...skills.orchestration.map((e) => e.skillName),
  ];
  for (const name of names) {
    expect(allNames).toContain(name);
  }
}

function then_skills_marked_as_orchestration(skills: ResolvedSkills): void {
  expect(skills.orchestration.length).toBeGreaterThan(0);
  expect(skills.stageWorkRequired).toHaveLength(0);
}

// ============================================================================
// HELPER FUNCTIONS — Create Agent Session via Cursor SDK
// ============================================================================

function given_kanban_lead_with_board_workspace(workspace: string): KanbanLead {
  return KanbanLead.create({ workspace });
}

function given_resolved_definition(role: string): AgentDefinition {
  return AgentDefinition.loadFixture(role);
}

function given_mcp_servers_configured(
  role: string,
  servers: string[],
): Record<string, string[]> {
  return { [role]: servers };
}

function given_cursor_sdk_returns_connection_error(): void {
  AgentSession.simulateConnectionError();
}

function when_kanban_lead_creates_session(
  lead: KanbanLead,
  definition: AgentDefinition,
  workspace: string,
): AgentSession {
  return lead.createAgentSession(definition, workspace);
}

function when_kanban_lead_creates_session_with_mcp(
  lead: KanbanLead,
  definition: AgentDefinition,
  workspace: string,
  mcpConfig: Record<string, string[]>,
): AgentSession {
  return lead.createAgentSession(definition, workspace, { mcpServers: mcpConfig });
}

function then_session_bootstrap_prompt_contains(
  session: AgentSession,
  field: keyof BootstrapPrompt,
  value: string,
): void {
  expect(session.bootstrapPrompt[field]).toBe(value);
}

function then_session_state_is(session: AgentSession, state: string): void {
  expect(session.state).toBe(state);
}

function then_session_creation_fails_with_log(
  fn: () => AgentSession,
  expectedMessage: string,
): void {
  expect(fn).toThrowError(expectedMessage);
}

function then_no_session_recorded_for_role(lead: KanbanLead, role: string): void {
  expect(lead.getSessionForRole(role)).toBeUndefined();
}

function then_session_includes_mcp_servers(
  session: AgentSession,
  ...servers: string[]
): void {
  for (const server of servers) {
    expect(session.mcpServers).toContain(server);
  }
}

// ============================================================================
// STORY: Resolve Agent Definition from Role
// ============================================================================

describe('Resolve Agent Definition from Role', () => {
  it('role "engineer" resolves to practices/kanban/agents/engineer/AGENT.md', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    given_agent_definition_exists(workspace, 'engineer');
    const definition = when_system_resolves_agent_definition(workspace, 'engineer');
    then_resolved_path_is(definition, 'practices/kanban/agents/engineer/AGENT.md');
    then_definition_content_is_loaded(definition);
  });

  it('role "kanban-lead" resolves to practices/kanban/agents/kanban-lead/AGENT.md', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    given_agent_definition_exists(workspace, 'kanban-lead');
    const definition = when_system_resolves_agent_definition(workspace, 'kanban-lead');
    then_resolved_path_is(definition, 'practices/kanban/agents/kanban-lead/AGENT.md');
    then_definition_content_is_loaded(definition);
  });

  it('unknown role returns error', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    given_no_agent_definition_exists(workspace, 'ux-designer');
    then_resolution_fails_with_error(
      () => when_system_resolves_agent_definition(workspace, 'ux-designer'),
      'Agent definition not found for role: ux-designer',
    );
  });
});

// ============================================================================
// STORY: Parse Skills from Agent Definition
// ============================================================================

describe('Parse Skills from Agent Definition', () => {
  it('engineer eligible skills come from kanban.json stage work required plus conditional from AGENT.md', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const definition = given_loaded_agent_definition('engineer');
    given_kanban_json_assigns_skills_to_role(workspace, 'engineer', [
      { skillName: 'abd-architecture-specification', stage: 'specification' },
      { skillName: 'abd-architecture-specification', stage: 'specification' },
      { skillName: 'abd-acceptance-test-driven-development', stage: 'specification' },
    ]);
    const skills = when_system_resolves_eligible_skills(definition, workspace);
    then_stage_work_required_count_is(skills, 3);
    then_conditional_count_is(skills, 1);
  });

  it('business expert AGENT.md references executor-workflow.md and shared reference files', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const definition = given_loaded_agent_definition('business-expert');
    const skills = when_system_resolves_eligible_skills(definition, workspace);
    then_parsed_result_includes_workflow_reference(skills, 'executor-workflow.md');
    then_referenced_files_include(skills, 'session-bootstrap.md', 'pull-model.md', 'work-queue.md');
  });

  it('kanban lead AGENT.md lists orchestration skills', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const definition = given_loaded_agent_definition('kanban-lead');
    const skills = when_system_resolves_eligible_skills(definition, workspace);
    then_skill_list_contains(skills, 'abd-kanban-planning', 'abd-kanban');
    then_skills_marked_as_orchestration(skills);
  });
});

// ============================================================================
// STORY: Create Agent Session via Cursor SDK
// ============================================================================

describe('Create Agent Session via Cursor SDK', () => {
  it('KanbanLead injects workspace from board config into bootstrap prompt', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const lead = given_kanban_lead_with_board_workspace(workspace);
    const definition = given_resolved_definition('engineer');
    const session = when_kanban_lead_creates_session(lead, definition, workspace);
    then_session_bootstrap_prompt_contains(session, 'workspace', 'C:\\dev\\project');
    then_session_bootstrap_prompt_contains(session, 'role', 'engineer');
    then_session_bootstrap_prompt_contains(session, 'agentDefinition', 'practices/kanban/agents/engineer/AGENT.md');
    then_session_state_is(session, 'running');
  });

  it('session creation fails — KanbanLead logs error and retries', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const lead = given_kanban_lead_with_board_workspace(workspace);
    const definition = given_resolved_definition('engineer');
    given_cursor_sdk_returns_connection_error();
    then_session_creation_fails_with_log(
      () => when_kanban_lead_creates_session(lead, definition, workspace),
      'Agent session creation failed for role: engineer',
    );
    then_no_session_recorded_for_role(lead, 'engineer');
  });

  it('agent session created with MCP server configuration', () => {
    const workspace = given_workspace_root('C:\\dev\\project');
    const lead = given_kanban_lead_with_board_workspace(workspace);
    const definition = given_resolved_definition('business-expert');
    const mcpConfig = given_mcp_servers_configured(
      'business-expert',
      ['user-story_bot', 'plugin-granola'],
    );
    const session = when_kanban_lead_creates_session_with_mcp(lead, definition, workspace, mcpConfig);
    then_session_includes_mcp_servers(session, 'user-story_bot', 'plugin-granola');
    then_session_state_is(session, 'running');
  });
});

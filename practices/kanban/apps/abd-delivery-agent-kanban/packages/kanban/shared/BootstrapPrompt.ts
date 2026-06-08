/**
 * domain model: BootstrapPrompt — assembled from an AgentDefinition by the KanbanLead.
 *      Workspace path is injected from the board's configuration, not derived
 *      from the AgentDefinition itself.
 *
 * Invariant: prompt must contain workspace and role before session creation.
 * Invariant: workspace path comes from the kanban board, not from the agent definition.
 */
export interface BootstrapPrompt {
  readonly workspace: string;
  readonly role: string;
  readonly agentDefinition: string;
}

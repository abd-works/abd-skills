import {
  TeamMembership as DomainTeamMembership,
  type AgentRole,
} from '@deliveryforge/kanban-shared';

/**
 * Presentation-layer TeamMembership — extends domain TeamMembership.
 * Adds display helpers for the agent pool bar (role labels, capacity badges).
 */
export class TeamMembership extends DomainTeamMembership {
  /** Human-readable capacity string for a role: "2 pairs", "1 pair". */
  static capacityLabel(role: AgentRole, count: number): string {
    return count === 1 ? '1 pair' : `${count} pairs`;
  }
}

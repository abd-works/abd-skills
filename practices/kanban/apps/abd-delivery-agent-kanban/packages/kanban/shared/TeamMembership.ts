/**
 * domain model: Agent — delivery roles that perform skills on tickets.
 * domain model: TeamMembership — pair counts per agent role; 1 membership per team role.
 * Invariant: Count must be >= 0.
 */

export const AGENT_ROLES = ['product-owner', 'business-expert', 'ux-designer', 'engineer'] as const;
export type AgentRole = (typeof AGENT_ROLES)[number];

export { TeamSchema, type Team } from './TeamMembership.schema';
import type { Team } from './TeamMembership.schema';

export const DEFAULT_TEAM: NonNullable<Team> = {
  'product-owner': 1,
  'business-expert': 1,
  'ux-designer': 1,
  engineer: 1,
};

export function normalizeDeliveryRole(agent: string | null | undefined): AgentRole | null {
  if (!agent) return null;
  if (AGENT_ROLES.includes(agent as AgentRole)) return agent as AgentRole;
  const reviewerMatch = agent.match(/^(.+)-reviewer$/);
  if (reviewerMatch && AGENT_ROLES.includes(reviewerMatch[1] as AgentRole)) {
    return reviewerMatch[1] as AgentRole;
  }
  return null;
}

export class TeamMembership {
  private readonly counts: NonNullable<Team>;

  constructor(counts?: Team) {
    this.counts = { ...DEFAULT_TEAM, ...(counts ?? {}) } as NonNullable<Team>;
  }

  count(role: AgentRole): number {
    return this.counts[role] ?? 1;
  }

  incrementPairCount(role: AgentRole): TeamMembership {
    return new TeamMembership({ ...this.counts, [role]: this.count(role) + 1 });
  }

  decrementPairCount(role: AgentRole): TeamMembership {
    return new TeamMembership({
      ...this.counts,
      [role]: Math.max(0, this.count(role) - 1),
    });
  }

  toJSON(): NonNullable<Team> {
    return { ...this.counts };
  }
}

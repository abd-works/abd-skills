import {
  TeamMembership as DomainTeamMembership,
  KanbanBoard,
  type AgentRole,
  type Team,
  type KanbanConfiguration,
} from '@deliveryforge/kanban-shared';
import type { PlanningFolderRepository } from './PlanningFolderRepository';

/**
 * Server-side TeamMembership — extends domain TeamMembership with persistence.
 * Owns reading the team from kanban config and writing it back to both
 * board.json and kanban.yaml when the pool is adjusted.
 */
export class TeamMembership extends DomainTeamMembership {
  /**
   * Resolve the effective team from kanban config (definition defaults)
   * merged with any board-level overrides, then wrap in a server TeamMembership.
   */
  static fromConfig(
    config: KanbanConfiguration,
    definitionName: string | null | undefined,
    boardTeam?: Team,
  ): TeamMembership {
    const resolved = KanbanBoard.resolveTeam(config, definitionName, boardTeam);
    return new TeamMembership(resolved);
  }

  /** Apply delta to one role; returns a new TeamMembership. */
  adjust(role: AgentRole, delta: number): TeamMembership {
    const next = delta > 0
      ? this.incrementPairCount(role)
      : this.decrementPairCount(role);
    return new TeamMembership(next.toJSON());
  }

  /**
   * Persist team counts to board.json.
   * Updates the `team` key in the existing board JSON without touching other fields.
   */
  async persistToBoard(
    boardFile: string,
    repo: PlanningFolderRepository,
  ): Promise<void> {
    const raw = (await repo.readJson(boardFile)) as Record<string, unknown>;
    raw.team = this.toJSON();
    await repo.writeJson(boardFile, raw);
  }

  /**
   * Persist team counts back into the kanban config definition so the
   * definition default matches the current board team.
   */
  async persistToConfig(
    configFile: string,
    config: KanbanConfiguration,
    definitionName: string,
    repo: PlanningFolderRepository,
  ): Promise<void> {
    if (!config.definitions[definitionName]) return;
    config.definitions[definitionName].team = { ...this.toJSON() };
    await repo.writeJson(configFile, config);
  }
}

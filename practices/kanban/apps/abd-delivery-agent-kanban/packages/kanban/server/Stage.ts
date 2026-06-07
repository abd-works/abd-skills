import { Stage as DomainStage } from '@deliveryforge/kanban-shared';
import type { KanbanConfiguration } from '@deliveryforge/kanban-shared';
import { KanbanBoard } from '@deliveryforge/kanban-shared';
import type { StageId } from '@deliveryforge/kanban-shared';

/**
 * Server-side Stage — extends domain Stage.
 * Adds config-driven stage flow resolution: reads active stages from the
 * kanban configuration file rather than defaulting to the full static order.
 */
export class Stage extends DomainStage {
  /**
   * Resolve the stage flow from a loaded kanban config.
   * Returns active stages (those with at least one required skill) if defined;
   * falls back to Stage.ORDER without 'context'.
   */
  static resolveFlow(
    config: KanbanConfiguration,
    definitionName?: string | null,
  ): StageId[] {
    const active = KanbanBoard.activeStages(config, definitionName);
    return active.length > 0
      ? active
      : DomainStage.ORDER.filter((s: StageId) => s !== 'context');
  }
}

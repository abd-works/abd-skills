import {
  StageBucketLayout as DomainStageBucketLayout,
  type StageSkillRail,
  type KanbanColumnView,
  Ticket as DomainTicket,
} from '@deliveryforge/kanban-shared';

/**
 * Presentation layer for stage bucket layout — same domain logic, presentation ticket type.
 */
export class StageBucketLayout extends DomainStageBucketLayout {
  static build(
    columnViews: KanbanColumnView[],
    archivedTickets: DomainTicket[],
    stageSkillRails: StageSkillRail[],
  ): StageBucketLayout {
    return DomainStageBucketLayout.build(
      columnViews,
      archivedTickets,
      stageSkillRails,
    ) as StageBucketLayout;
  }
}

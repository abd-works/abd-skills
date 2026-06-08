import { StageBucketLayout as DomainStageBucketLayout } from '@deliveryforge/kanban-shared';

/**
 * Server-side StageBucketLayout — extends domain StageBucketLayout.
 * The layout computation is fully shared; this extension point exists
 * for any server-side layout validation or stage-flow overrides.
 */
export class StageBucketLayout extends DomainStageBucketLayout {}

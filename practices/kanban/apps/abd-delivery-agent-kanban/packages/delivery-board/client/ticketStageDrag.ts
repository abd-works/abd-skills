import { STAGE_ORDER, type StageId } from '@deliveryforge/delivery-board-shared';

export type TicketDragPayload = { id: string; stage: StageId };

export type MoveTicketPlacement = 'in_progress' | 'stage_done';

/** Called when a ticket is dropped on a stage sub-column (stage + placement are known). */
export type TicketStageDropHandler = (
  ticketId: string,
  targetStage: StageId,
  placement: MoveTicketPlacement,
) => void;

export type TicketDropTarget = {
  stage: StageId;
  placement: MoveTicketPlacement;
};

/** Resolve drop coordinates (DOM hit target) to stage column + placement. */
export function resolveTicketDropTarget(
  target: HTMLElement | null,
  stageOrder: readonly StageId[] = STAGE_ORDER,
): TicketDropTarget | null {
  if (!target) return null;

  const stageEl = target.closest('[data-stage]');
  const stageAttr = stageEl?.getAttribute('data-stage');
  if (!stageAttr || !stageOrder.includes(stageAttr as StageId)) return null;

  const ipCol = target.closest('.kb-sub-col--ip');
  const doneCol = target.closest('.kb-sub-col--done');
  if (ipCol || doneCol) {
    const placement: MoveTicketPlacement = doneCol && !ipCol ? 'stage_done' : 'in_progress';
    return { stage: stageAttr as StageId, placement };
  }

  // Drop on stage header / skill chips still targets that stage's In Progress.
  if (stageEl?.classList.contains('kb-stage-group')) {
    return { stage: stageAttr as StageId, placement: 'in_progress' };
  }

  return null;
}

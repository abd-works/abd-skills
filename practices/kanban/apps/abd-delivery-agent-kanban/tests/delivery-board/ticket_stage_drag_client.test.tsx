import { describe, it, expect } from 'vitest';
import { resolveTicketDropTarget } from '../../packages/delivery-board/client/ticketStageDrag';

function el(html: string): HTMLElement {
  const wrap = document.createElement('div');
  wrap.innerHTML = html;
  return wrap.firstElementChild as HTMLElement;
}

describe('resolveTicketDropTarget', () => {
  it('resolves Discovery In Progress column', () => {
    const root = el(`
      <div class="kb-stage-group" data-stage="discovery">
        <div class="kb-stage-sub-cols">
          <div class="kb-sub-col kb-sub-col--ip">
            <div class="kb-sub-col-tickets"></div>
          </div>
        </div>
      </div>
    `);
    const hit = root.querySelector('.kb-sub-col-tickets') as HTMLElement;
    expect(resolveTicketDropTarget(hit)).toEqual({ stage: 'discovery', placement: 'in_progress' });
  });

  it('resolves Done column as stage_done', () => {
    const root = el(`
      <div class="kb-stage-group" data-stage="shaping">
        <div class="kb-sub-col kb-sub-col--done">
          <div class="kb-sub-col-tickets"></div>
        </div>
      </div>
    `);
    const hit = root.querySelector('.kb-sub-col-tickets') as HTMLElement;
    expect(resolveTicketDropTarget(hit)).toEqual({ stage: 'shaping', placement: 'stage_done' });
  });

  it('returns null outside stage columns', () => {
    expect(resolveTicketDropTarget(el('<div class="kb-board-scroll"></div>'))).toBeNull();
  });
});

/** Drop must commit before dragend clears payload (see DeliveryKanbanBoard). */
describe('ticket stage drop commit ordering', () => {
  function createDropCommit() {
    let payload: { id: string; stage: string } | null = { id: 'project-all', stage: 'shaping' };
    let committed = false;
    const moves: Array<{ id: string; stage: string; placement: string }> = [];

    const endDrag = () => {
      payload = null;
    };

    const onDrop = (ticketId: string, targetStage: string, placement: string) => {
      if (committed || !payload) return;
      committed = true;
      moves.push({ id: ticketId, stage: targetStage, placement });
    };

    const onDragEnd = () => {
      requestAnimationFrame(() => {
        if (!committed) endDrag();
      });
    };

    const finishMove = () => {
      committed = false;
      endDrag();
    };

    return { onDrop, onDragEnd, finishMove, moves, getPayload: () => payload };
  }

  it('commits move on drop before dragend clears payload', async () => {
    const d = createDropCommit();
    d.onDrop('project-all', 'discovery', 'in_progress');
    d.onDragEnd();
    await new Promise((r) => requestAnimationFrame(r));
    expect(d.moves).toEqual([
      { id: 'project-all', stage: 'discovery', placement: 'in_progress' },
    ]);
    d.finishMove();
    expect(d.getPayload()).toBeNull();
  });

  it('clears payload on cancel drag (no drop)', async () => {
    const d = createDropCommit();
    d.onDragEnd();
    await new Promise((r) => requestAnimationFrame(r));
    expect(d.moves).toEqual([]);
    expect(d.getPayload()).toBeNull();
  });
});

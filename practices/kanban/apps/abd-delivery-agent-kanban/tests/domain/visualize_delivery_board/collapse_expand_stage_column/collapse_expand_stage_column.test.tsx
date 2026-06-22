/**
 * Collapse and Expand Stage Column
 *
 * Epic:     Visualize Delivery Board
 * Sub-epic: Display Board Layout
 * Story:    Delivery Lead --> Collapse and Expand Stage Column
 */
import { describe, expect, it } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { StageGroupView } from '../../../../packages/app-client/StageGroupView';
import { createRef } from 'react';
import type { TicketDragPayload } from '@deliveryforge/kanban-client';

function renderStageGroup() {
  const draggingTicketRef = createRef<TicketDragPayload | null>() as React.MutableRefObject<TicketDragPayload | null>;
  draggingTicketRef.current = null;

  return render(
    <StageGroupView
      stage="exploration"
      bucket={{ ip: [], done: [], feedsNext: [] }}
      skills={[{ skillId: 'abd-domain-language', label: 'Domain Language', family: 'domain', role: 'business-expert' }]}
      skillsByStage={new Map()}
      peersByTargetStage={new Map()}
      team={{ 'product-owner': 1, 'business-expert': 1, 'ux-designer': 1, engineer: 1 }}
      draggingTicketRef={draggingTicketRef}
    />,
  );
}

describe('Collapse and Expand Stage Column', () => {
  it('renders sub-columns and skill rail visible by default', () => {
    renderStageGroup();
    expect(document.querySelector('.kb-stage-sub-cols')).toBeVisible();
    expect(document.querySelector('.kb-stage-skills')).toBeVisible();
  });

  it('collapses sub-columns and skill rail when toggle is clicked', () => {
    renderStageGroup();
    const toggle = screen.getByRole('button', { name: /collapse/i });
    fireEvent.click(toggle);
    expect(document.querySelector('.kb-stage-group')).toHaveClass('kb-stage-group--collapsed');
  });

  it('expands back when toggle is clicked again', () => {
    renderStageGroup();
    const toggle = screen.getByRole('button', { name: /collapse/i });
    fireEvent.click(toggle);
    fireEvent.click(toggle);
    expect(document.querySelector('.kb-stage-group')).not.toHaveClass('kb-stage-group--collapsed');
  });

  it('toggle button aria-label changes to reflect collapsed state', () => {
    renderStageGroup();
    const toggle = screen.getByRole('button', { name: /collapse/i });
    fireEvent.click(toggle);
    expect(screen.getByRole('button', { name: /expand/i })).toBeInTheDocument();
  });

  it('stage label remains visible when collapsed', () => {
    renderStageGroup();
    const toggle = screen.getByRole('button', { name: /collapse/i });
    fireEvent.click(toggle);
    expect(screen.getByText(/exploration/i)).toBeVisible();
  });
});

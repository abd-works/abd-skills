import { join } from 'node:path';

import { describe, it, expect } from 'vitest';

import { engagementWorkspaceFromPlanningRoot } from '@deliveryforge/delivery-board-shared';

import {
  resolveScatterChildren,
  tryResolveScatterChildren,
} from '../../packages/delivery-board/server/resolveScatterChildren';

const seedPlanning = join(__dirname, '../e2e/_seed/pawplace-mini/docs/planning');
const seedEngagement = engagementWorkspaceFromPlanningRoot(seedPlanning);
const sprintFixtureEngagement = join(__dirname, '../fixtures/pawplace-sprint-resolve');

const incParent = 'project-all-inc-1-find-products-and-check-store-stock';

describe('engagementWorkspaceFromPlanningRoot', () => {
  it('strips docs/planning from planning root', () => {
    expect(seedEngagement.replace(/\\/g, '/')).toMatch(/pawplace-mini$/);
    expect(seedEngagement).not.toContain('docs/planning');
  });
});

describe('resolveScatterChildren', () => {
  it('reads discovery thin-slicing for project-all → increment only', () => {
    const children = resolveScatterChildren(seedEngagement, 'project-all', {
      childScope: 'increment',
    });
    expect(children).toHaveLength(1);
    expect(children[0]!.id).toBe('project-all-inc-1-find-products-and-check-store-stock');
    expect(children[0]!.id).toMatch(/^project-all-inc-\d+-/);
  });

  it('does not re-parse thin-slicing when increment parent crosses to sprint', () => {
    expect(
      tryResolveScatterChildren(seedEngagement, incParent, { childScope: 'sprint' }),
    ).toBeNull();
    expect(() =>
      resolveScatterChildren(seedEngagement, incParent, { childScope: 'sprint' }),
    ).toThrow(/sprint-groupings/);
  });

  it('reads sprint-groupings for increment → sprint when file exists', () => {
    const children = resolveScatterChildren(sprintFixtureEngagement, incParent, {
      childScope: 'sprint',
    });
    expect(children.map((c) => c.id)).toEqual([
      '1-find-products-and-check-store-stock-sprint-1',
      '1-find-products-and-check-store-stock-sprint-2',
    ]);
  });

  it('returns null from tryResolve when engagement root is wrong (planning path)', () => {
    expect(
      tryResolveScatterChildren(seedPlanning, 'project-all', { childScope: 'increment' }),
    ).toBeNull();
  });
});

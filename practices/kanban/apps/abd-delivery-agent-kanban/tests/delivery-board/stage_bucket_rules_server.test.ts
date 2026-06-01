import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import {
  KanbanBoardLoader,
  buildStageBuckets,
  type KanbanConfiguration,
} from '@deliveryforge/delivery-board-shared';

const bessPlanning = 'C:/dev/bess-replacement/docs/planning';

describe('buildStageBuckets — BESS28 discovery scatter', () => {
  it('puts module 1 increment tickets in Discovery feeds-next after scatter', () => {
    const boardJson = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/board.json`, 'utf8'),
    );
    const kanbanConfig = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/kanban.json`, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(bessPlanning, boardJson, kanbanConfig);
    const buckets = buildStageBuckets(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    );

    const discovery = buckets.get('discovery')!;
    const module1Increments = [
      ...discovery.feedsNext,
      ...(buckets.get('exploration')?.ip ?? []),
    ].filter(
      (t) => t.scopeLevel === 'increment' && t.scatterFrom === '1-terminal-requestor-screen-composition',
    );
    expect(module1Increments.length).toBe(8);

    const explorationRail = snapshot.stageSkillRails.find((r) => r.stage === 'exploration');
    expect(explorationRail?.skills.map((s) => s.skillId)).toContain(
      'abd-architecture-reference',
    );
    const specRail = snapshot.stageSkillRails.find((r) => r.stage === 'specification');
    expect(specRail?.skills.map((s) => s.skillId)).toContain('abd-architecture-template');

    expect(discovery.done.map((t) => t.ticketId)).not.toContain(
      '2-shared-domain-schema-copybook-layer',
    );
    const module2Increments = discovery.feedsNext.filter(
      (t) => t.scopeLevel === 'increment' && t.scatterFrom === '2-shared-domain-schema-copybook-layer',
    );
    expect(module2Increments.length).toBe(9);
  });

  it('puts exploration increments in Exploration IP when pulled active', () => {
    const boardJson = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/board.json`, 'utf8'),
    );
    const kanbanConfig = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/kanban.json`, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(bessPlanning, boardJson, kanbanConfig);
    const buckets = buildStageBuckets(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    );

    const exploration = buckets.get('exploration')!;
    expect(exploration.ip.length).toBeGreaterThanOrEqual(1);
    expect(exploration.ip.some((t) => t.ticketId.startsWith('1-'))).toBe(true);
  });
});

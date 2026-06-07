/**
 * Display Board Layout
 *
 * Epic:     Visualize Delivery Board
 * Sub-epic: Display Board Layout
 */
import { readFileSync, existsSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import {
  KanbanBoardLoader,
  Ticket,
  StageBucketLayout,
  type KanbanConfiguration,
  type StageSkillRail,
  type StageSkill,
} from '@deliveryforge/kanban-shared';

const bessPlanning = 'C:/dev/bess-replacement/docs/planning';
const bessExists = existsSync(`${bessPlanning}/delivery-war-room/board.json`);

describe('Organize Tickets into Stage Groups by Delivery Phase', () => {
  it.skipIf(!bessExists)('puts module 1 increment tickets in Discovery feeds-next after scatter', () => {
    const boardJson = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/board.json`, 'utf8'),
    );
    const kanbanConfig = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/kanban.json`, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(bessPlanning, boardJson, kanbanConfig);
    const buckets = StageBucketLayout.build(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    ).buildStageBuckets();

    const discovery = buckets.get('discovery')!;
    const module1Increments = [
      ...discovery.feedsNext,
      ...(buckets.get('exploration')?.ip ?? []),
    ].filter(
      (t: Ticket) => t.scopeLevel === 'increment' && t.scatterFrom === '1-terminal-requestor-screen-composition',
    );
    expect(module1Increments.length).toBe(8);

    const explorationRail = snapshot.stageSkillRails.find((r: StageSkillRail) => r.stage === 'exploration');
    expect(explorationRail?.skills.map((s: StageSkill) => s.skillId)).toContain(
      'abd-architecture-specification',
    );
    const specRail = snapshot.stageSkillRails.find((r: StageSkillRail) => r.stage === 'specification');
    expect(specRail?.skills.map((s: StageSkill) => s.skillId)).toContain('abd-architecture-specification');

    expect(discovery.done.map((t: Ticket) => t.ticketId)).not.toContain(
      '2-shared-domain-schema-copybook-layer',
    );
    const module2Increments = discovery.feedsNext.filter(
      (t: Ticket) => t.scopeLevel === 'increment' && t.scatterFrom === '2-shared-domain-schema-copybook-layer',
    );
    expect(module2Increments.length).toBe(9);
  });

  it.skipIf(!bessExists)('puts exploration increments in Exploration IP when pulled active', () => {
    const boardJson = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/board.json`, 'utf8'),
    );
    const kanbanConfig = JSON.parse(
      readFileSync(`${bessPlanning}/delivery-war-room/kanban.json`, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(bessPlanning, boardJson, kanbanConfig);
    const buckets = StageBucketLayout.build(
      snapshot.columnViews,
      snapshot.archivedTickets,
      snapshot.stageSkillRails,
    ).buildStageBuckets();

    const exploration = buckets.get('exploration')!;
    expect(exploration.ip.length).toBeGreaterThanOrEqual(1);
    expect(exploration.ip.some((t: Ticket) => t.ticketId.startsWith('1-'))).toBe(true);
  });
});

/**
 * Compose Snapshot from Planning Artifacts
 *
 * Epic:     Load Board Snapshot
 * Sub-epic: Compose Snapshot from Planning Artifacts
 */
import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  KanbanBoard,
  KanbanBoardLoader,
  Ticket,
  SkillProgressEntry,
  StageBucketLayout,
  parseKanbanBoard,
  type AgentSessionInfo,
  type KanbanConfiguration,
} from '@deliveryforge/kanban-shared';

const petStorePlanning = 'C:/dev/abd-pet-store-demo/docs/planning';

describe('Read Board JSON and System of Work from Disk', () => {
  const paths = KanbanBoard.resolvePlanningPaths(petStorePlanning);
  const boardExists = existsSync(paths.boardFile);
  const kanbanExists = existsSync(paths.kanbanFile);

  it.skipIf(!boardExists || !kanbanExists)('loads board and kanban configuration', () => {
    const boardJson = JSON.parse(readFileSync(paths.boardFile, 'utf8'));
    const kanbanConfig = JSON.parse(
      readFileSync(paths.kanbanFile, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(
      petStorePlanning,
      boardJson,
      kanbanConfig,
    );

    expect(snapshot.board.toJSON().schema).toBe('abd-delivery-kanban/v2');
    expect(snapshot.stageFlow.length).toBeGreaterThan(0);
    expect(snapshot.stageSkillRails.length).toBeGreaterThan(0);
    expect(snapshot.team).toBeDefined();
    expect(snapshot.team['business-expert']).toBe(2);
  });

  it.skipIf(!boardExists || !kanbanExists)('builds column views from board arrays', () => {
    const boardJson = JSON.parse(readFileSync(paths.boardFile, 'utf8'));
    const kanbanConfig = JSON.parse(
      readFileSync(paths.kanbanFile, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(
      petStorePlanning,
      boardJson,
      kanbanConfig,
    );

    const colIds = snapshot.columnViews.map((c) => c.id);
    expect(colIds).toContain('backlog');
    expect(colIds).toContain('active');
    expect(colIds).toContain('done');
  });

  it.skipIf(!boardExists || !kanbanExists)('stage skill rails reflect kanban configuration', () => {
    const boardJson = JSON.parse(readFileSync(paths.boardFile, 'utf8'));
    const kanbanConfig = JSON.parse(
      readFileSync(paths.kanbanFile, 'utf8'),
    ) as KanbanConfiguration;

    const snapshot = KanbanBoardLoader.fromSources(
      petStorePlanning,
      boardJson,
      kanbanConfig,
    );

    const shapingRail = snapshot.stageSkillRails.find((r) => r.stage === 'shaping');
    expect(shapingRail).toBeDefined();
    if (shapingRail && shapingRail.skills.length > 0) {
      expect(shapingRail.skills[0].skillId).toContain('abd-');
    }
  });
});

describe('Validate Board Data Structure', () => {
  it('requires both execution and review done', () => {
    expect(
      SkillProgressEntry.create({ execution_status: 'done', review_status: 'done' }).isComplete(),
    ).toBe(true);
    expect(
      SkillProgressEntry.create({ execution_status: 'done', review_status: undefined }).isComplete(),
    ).toBe(false);
  });

  it('sprint tickets appear in backlog after increment scatter', () => {
    const board = parseKanbanBoard({
      schema: 'abd-delivery-kanban/v2',
      backlog: [
        {
          ticket_id: 'inc-1-sprint-1-checkout',
          lineage: ['PawPlace', 'Inc 1', 'Sprint 1 - Checkout'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 1,
          scatter_from: 'inc-1-find-products',
        },
        {
          ticket_id: 'inc-1-sprint-2-search',
          lineage: ['PawPlace', 'Inc 1', 'Sprint 2 - Search'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 2,
          scatter_from: 'inc-1-find-products',
        },
      ],
      active: [],
      done: [],
      archived: [
        {
          ticket_id: 'inc-1-find-products',
          lineage: ['PawPlace', 'Inc 1 - Find Products'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          scatter_to: ['inc-1-sprint-1-checkout', 'inc-1-sprint-2-search'],
        },
      ],
    });

    const backlogIds = board.backlog.map((t) => t.ticket_id);
    expect(backlogIds).toContain('inc-1-sprint-1-checkout');
    expect(backlogIds).toContain('inc-1-sprint-2-search');
    expect(board.backlog[0]!.scatter_from).toBe('inc-1-find-products');
  });
});

describe('Map System of Work to Stage Skill Rails', () => {
  const paths = KanbanBoard.resolvePlanningPaths(petStorePlanning);
  const boardExists = existsSync(paths.boardFile);
  const kanbanExists = existsSync(paths.kanbanFile);

  function loadSnapshot() {
    const boardJson = JSON.parse(readFileSync(paths.boardFile, 'utf8'));
    const kanbanConfig = JSON.parse(
      readFileSync(paths.kanbanFile, 'utf8'),
    ) as KanbanConfiguration;
    return KanbanBoardLoader.fromSources(petStorePlanning, boardJson, kanbanConfig);
  }

  it.skipIf(!boardExists || !kanbanExists)(
    'idle-active tickets with incomplete skills appear in IP, not Done feeds-next',
    () => {
      const snapshot = loadSnapshot();
      const layout = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      );
      const buckets = layout.buildStageBuckets();

      for (const stage of snapshot.stageFlow) {
        const bucket = buckets.get(stage);
        if (!bucket) continue;
        for (const t of bucket.feedsNext) {
          expect(t.column).toBe('backlog');
        }
        for (const t of bucket.ip) {
          if (t.column === 'active' && !t.hasLiveAgentWork()) {
            const skillIds =
              snapshot.stageSkillRails.find((r) => r.stage === stage)?.skills.map((s) => s.skillId) ??
              [];
            expect(t.doneSkillIds.length).toBeLessThan(skillIds.length);
          }
        }
      }

      const eng = buckets.get('engineering')!;
      const idleActiveEng = eng.ip.filter(
        (t) => t.column === 'active' && !t.hasLiveAgentWork(),
      );
      expect(idleActiveEng.length).toBeGreaterThan(0);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'scatter parents follow trailing child and sit on top of that column',
    () => {
      const snapshot = loadSnapshot();
      const layout2 = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      );
      const buckets = layout2.buildStageBuckets();

      const archivedOnly = layout2.archivedColumnTickets(snapshot.archivedTickets);
      const archivedOnlyIds = archivedOnly.map((t) => t.ticketId);
      expect(archivedOnlyIds).not.toContain('inc-8-marketing-engine');
      expect(archivedOnlyIds).not.toContain('inc-9-power-ups');

      const explorationDoneIds = buckets.get('exploration')!.done.map((t) => t.ticketId);
      expect(explorationDoneIds).not.toContain('inc-8-marketing-engine');
      expect(explorationDoneIds).not.toContain('inc-9-power-ups');

      for (const parentId of ['inc-8-marketing-engine', 'inc-9-power-ups']) {
        let parentIdx = -1;
        let firstChildIdx = -1;
        for (const bucket of buckets.values()) {
          for (const list of [bucket.ip, bucket.done, bucket.feedsNext]) {
            const pIdx = list.findIndex((t) => t.ticketId === parentId);
            if (pIdx < 0) continue;
            parentIdx = pIdx;
            const childIds = new Set(
              snapshot.archivedTickets.find((t) => t.ticketId === parentId)?.scatterTo ?? [],
            );
            firstChildIdx = list.findIndex((t) => childIds.has(t.ticketId));
            expect(list[pIdx]!.isScatterParent()).toBe(true);
            break;
          }
          if (parentIdx >= 0) break;
        }
        expect(parentIdx).toBeGreaterThanOrEqual(0);
        expect(firstChildIdx).toBeGreaterThanOrEqual(0);
        expect(parentIdx).toBeLessThan(firstChildIdx);
      }
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'only active sprints with a live agent appear in specification in-progress',
    () => {
      const snapshot = loadSnapshot();
      const buckets = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      ).buildStageBuckets();
      const specIpIds = buckets.get('specification')!.ip.map((t) => t.ticketId);
      expect(specIpIds).toHaveLength(0);
      expect(specIpIds).not.toContain('inc-8-sprint-1-reviews');
      expect(specIpIds).not.toContain('inc-8-sprint-2-preferences');
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'ticketCanExpand allows active, feeds-next backlog, and archived stage-done',
    () => {
      const snapshot = loadSnapshot();
      const engSkills =
        snapshot.stageSkillRails.find((r) => r.stage === 'engineering')?.skills.map((s) => s.skillId) ??
        [];
      const explorationSkills =
        snapshot.stageSkillRails.find((r) => r.stage === 'exploration')?.skills.map((s) => s.skillId) ??
        [];

      const activeTickets = snapshot.columnViews.find((c) => c.id === 'active')!.tickets;
      const engTicket = activeTickets.find((t) => t.stage === 'engineering')!;
      expect(engTicket.canExpand(engSkills, 'ip')).toBe(true);

      const feedTicket =
        activeTickets.find((t) => t.ticketId === 'inc-8-sprint-2-preferences') ??
        activeTickets.find((t) => t.stage === 'engineering')!;
      expect(feedTicket.canExpand(engSkills, 'feeds-next')).toBe(true);

      const archivedDone = snapshot.archivedTickets.find(
        (t) => t.ticketId === 'inc-8-marketing-engine',
      )!;
      expect(archivedDone.hasSkillProgress()).toBe(true);
      expect(archivedDone.canExpand(explorationSkills, 'done')).toBe(true);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'focus skill advances to next incomplete skill on idle active engineering ticket',
    () => {
      const snapshot = loadSnapshot();
      const engIp = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      ).buildStageBuckets()
        .get('engineering')!
        .ip.filter((t) => t.column === 'active' && t.doneSkillIds.length > 0);
      expect(engIp.length).toBeGreaterThan(0);
      const queued = engIp[0]!;
      const engSkills =
        snapshot.stageSkillRails.find((r) => r.stage === 'engineering')!.skills.map((s) => s.skillId);

      const focus = queued.focusSkillId(engSkills, 'ip');
      expect(focus).not.toBeNull();
      expect(engSkills).toContain(focus!);

      const doneRow = queued.skillRowDisplayState(queued.doneSkillIds[0]!, focus);
      expect(doneRow.isDone).toBe(true);
      expect(doneRow.showBot).toBe(false);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'idle active engineering tickets sit in IP sub-column',
    () => {
      const snapshot = loadSnapshot();
      const engIp = StageBucketLayout.build(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      ).buildStageBuckets()
        .get('engineering')!
        .ip.filter((t) => t.column === 'active' && !t.activeSkillId && !t.reviewSkillId);
      expect(engIp.length).toBeGreaterThan(0);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'agent pool lights up roles with live board engagement only',
    () => {
      function resolveSlotState(
        slotIndex: number,
        engagedCount: number,
        session: AgentSessionInfo | undefined,
      ): 'idle' | 'working' | 'inactive' {
        if (slotIndex < engagedCount) return 'working';
        if (!session) return 'idle';
        if (session.state === 'running') return 'working';
        return 'inactive';
      }

      const snapshot = loadSnapshot();
      const engaged = Ticket.countRoleEngagement(snapshot.columnViews);

      expect(engaged['business-expert']).toBe(0);
      expect(engaged['product-owner']).toBe(0);
      expect(resolveSlotState(0, engaged['business-expert'], undefined)).toBe('idle');
      expect(resolveSlotState(1, engaged['business-expert'], undefined)).toBe('idle');
      expect(resolveSlotState(0, engaged['product-owner'], undefined)).toBe('idle');
    },
  );
});

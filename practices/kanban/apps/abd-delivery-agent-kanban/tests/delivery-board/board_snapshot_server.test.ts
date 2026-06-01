import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  KanbanBoardLoader,
  resolvePlanningPaths,
  isSkillComplete,
  parseKanbanBoard,
  buildStageBuckets,
  buildGlobalBacklogTickets,
  buildArchivedColumnTickets,
  ticketCanExpand,
  hasSkillProgress,
  resolveFocusSkillId,
  resolveDisplayFocusSkillId,
  countRoleEngagement,
  resolvePoolAvatarState,
  skillRowDisplayState,
  ticketHasLiveAgentWork,
  isScatterParent,
  relocateScatterParents,
  type KanbanConfiguration,
} from '@deliveryforge/delivery-board-shared';

const petStorePlanning = 'C:/dev/abd-pet-store-demo/docs/planning';

describe('KanbanBoardLoader from v2 board.json', () => {
  const paths = resolvePlanningPaths(petStorePlanning);
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

    expect(snapshot.board.schema).toBe('abd-delivery-kanban/v2');
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

describe('Skill completion gate', () => {
  it('requires both execution and review done', () => {
    expect(
      isSkillComplete({ execution_status: 'done', review_status: 'done' }),
    ).toBe(true);
    expect(
      isSkillComplete({ execution_status: 'done', review_status: undefined }),
    ).toBe(false);
  });

  it.skipIf(!existsSync(resolvePlanningPaths(petStorePlanning).boardFile))(
    'sprint tickets appear in backlog after increment scatter',
    () => {
      const paths = resolvePlanningPaths(petStorePlanning);
      const board = parseKanbanBoard(JSON.parse(readFileSync(paths.boardFile, 'utf8')));
      const sprintIds = [...board.backlog, ...board.active].map((t) => t.ticket_id);
      expect(sprintIds.some((id) => id.startsWith('inc-8-sprint-'))).toBe(true);
      expect(sprintIds.some((id) => id.startsWith('inc-9-sprint-'))).toBe(true);
    },
  );
});

describe('Stage bucket mapping', () => {
  const paths = resolvePlanningPaths(petStorePlanning);
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
      const buckets = buildStageBuckets(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      );

      for (const stage of snapshot.stageFlow) {
        const bucket = buckets.get(stage);
        if (!bucket) continue;
        for (const t of bucket.feedsNext) {
          expect(t.column).toBe('backlog');
        }
        for (const t of bucket.ip) {
          if (t.column === 'active' && !ticketHasLiveAgentWork(t)) {
            const skillIds =
              snapshot.stageSkillRails.find((r) => r.stage === stage)?.skills.map((s) => s.skillId) ??
              [];
            expect(t.doneSkillIds.length).toBeLessThan(skillIds.length);
          }
        }
      }

      const eng = buckets.get('engineering')!;
      const idleActiveEng = eng.ip.filter(
        (t) => t.column === 'active' && !ticketHasLiveAgentWork(t),
      );
      expect(idleActiveEng.length).toBeGreaterThan(0);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'scatter parents follow trailing child and sit on top of that column',
    () => {
      const snapshot = loadSnapshot();
      const buckets = buildStageBuckets(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      );

      const archivedOnly = buildArchivedColumnTickets(snapshot.archivedTickets, buckets);
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
            expect(isScatterParent(list[pIdx]!)).toBe(true);
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
      const buckets = buildStageBuckets(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      );
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
      expect(ticketCanExpand(engTicket, engSkills, 'ip')).toBe(true);

      const feedTicket =
        activeTickets.find((t) => t.ticketId === 'inc-8-sprint-2-preferences') ??
        activeTickets.find((t) => t.stage === 'engineering')!;
      expect(ticketCanExpand(feedTicket, engSkills, 'feeds-next')).toBe(true);

      const archivedDone = snapshot.archivedTickets.find(
        (t) => t.ticketId === 'inc-8-marketing-engine',
      )!;
      expect(hasSkillProgress(archivedDone)).toBe(true);
      expect(ticketCanExpand(archivedDone, explorationSkills, 'done')).toBe(true);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'focus skill advances to next incomplete skill on idle active engineering ticket',
    () => {
      const snapshot = loadSnapshot();
      const engIp = buildStageBuckets(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      )
        .get('engineering')!
        .ip.filter((t) => t.column === 'active' && t.doneSkillIds.length > 0);
      expect(engIp.length).toBeGreaterThan(0);
      const queued = engIp[0]!;
      const engSkills =
        snapshot.stageSkillRails.find((r) => r.stage === 'engineering')!.skills.map((s) => s.skillId);

      const focus = resolveFocusSkillId(queued, engSkills, 'ip');
      expect(focus).not.toBeNull();
      expect(engSkills).toContain(focus!);

      const doneRow = skillRowDisplayState(queued.doneSkillIds[0]!, queued, focus);
      expect(doneRow.isDone).toBe(true);
      expect(doneRow.showBot).toBe(false);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'idle active engineering tickets sit in IP sub-column',
    () => {
      const snapshot = loadSnapshot();
      const engIp = buildStageBuckets(
        snapshot.columnViews,
        snapshot.archivedTickets,
        snapshot.stageSkillRails,
      )
        .get('engineering')!
        .ip.filter((t) => t.column === 'active' && !t.activeSkillId && !t.reviewSkillId);
      expect(engIp.length).toBeGreaterThan(0);
    },
  );

  it.skipIf(!boardExists || !kanbanExists)(
    'agent pool lights up roles with live board engagement only',
    () => {
      const snapshot = loadSnapshot();
      const engaged = countRoleEngagement(
        snapshot.columnViews,
        snapshot.stageSkillRails,
        snapshot.team!,
      );

      expect(engaged['business-expert']).toBe(0);
      expect(engaged['product-owner']).toBe(0);
      expect(resolvePoolAvatarState(0, engaged['business-expert'], null)).toBe('idle');
      expect(resolvePoolAvatarState(1, engaged['business-expert'], null)).toBe('idle');
      expect(resolvePoolAvatarState(0, engaged['product-owner'], null)).toBe('idle');
    },
  );
});

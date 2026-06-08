/**
 * KanbanDomainOps — pure functional domain logic for the kanban board.
 * Mirrors Python delivery_model.py, kanban_lead.py domain methods.
 * All functions are stateless and operate on plain WrBoard/WrTicket objects.
 */

import { nowIso } from './WarRoomService';
import type { WrTicket, WrSkillProgress, WrBoard, WrStageDef, WrKanbanBoard } from './WarRoomService';

// ── SkillProgress helpers ────────────────────────────────────────────────────

export function isSkillProgressDone(sp: WrSkillProgress): boolean {
  return sp.execution_status === 'done' && sp.review_status === 'done';
}

export function isClaimable(sp: WrSkillProgress): boolean {
  const s = sp.execution_status;
  if (s === 'not_started' || s == null) return true;
  return s !== 'in_progress' && s !== 'done';
}

// ── Stage completion ─────────────────────────────────────────────────────────

/** Invariant: stage complete only when every required skill has execution+review done. */
export function isStageComplete(ticket: WrTicket, stageDef: WrStageDef): boolean {
  if (!stageDef.stage_work_required || stageDef.stage_work_required.length === 0) return false;
  for (const skillDef of stageDef.stage_work_required) {
    if (skillDef.optional) continue;
    const sp = ticket.skill_progress[skillDef.skill];
    if (!sp || !isSkillProgressDone(sp)) return false;
  }
  return true;
}

export function hasSkillInProgress(ticket: WrTicket): boolean {
  for (const sp of Object.values(ticket.skill_progress)) {
    if (sp.execution_status === 'in_progress' || sp.review_status === 'in_progress') return true;
  }
  return false;
}

// ── Priors gate ──────────────────────────────────────────────────────────────

/** All skills before skillName in the rail are done (or optional+absent). */
export function priorsDone(ticket: WrTicket, stageDef: WrStageDef, skillName: string): boolean {
  for (const skillDef of stageDef.stage_work_required) {
    if (skillDef.skill === skillName) return true;
    const sp = ticket.skill_progress[skillDef.skill];
    if (skillDef.optional && sp == null) continue;
    if (!sp || !isSkillProgressDone(sp)) return false;
  }
  return false;
}

// ── Next eligible skill for a role on a ticket ───────────────────────────────

export function nextEligibleSkill(
  ticket: WrTicket,
  stageDef: WrStageDef,
  role: string,
): string | null {
  for (const skillDef of stageDef.stage_work_required) {
    if (skillDef.role !== role) continue;
    const sp = ticket.skill_progress[skillDef.skill];
    // If already in_progress for this role, return immediately — priors gate doesn't apply.
    if (sp?.execution_status === 'in_progress' && sp.agent === role) return skillDef.skill;
    if (!priorsDone(ticket, stageDef, skillDef.skill)) break;
    if (sp && isSkillProgressDone(sp)) continue;
    if (sp && !isClaimable(sp)) break;
    return skillDef.skill;
  }
  return null;
}

// ── Stage advance ────────────────────────────────────────────────────────────

/** Move ticket to next stage: record history, clear skill_progress. Mutates in place. */
export function advanceToNextStage(ticket: WrTicket, nextStageDef: WrStageDef): void {
  const now = nowIso();
  if (ticket.stage && ticket.entered_stage) {
    ticket.completed_stage = now;
    ticket.stage_history ??= [];
    ticket.stage_history.push({ stage: ticket.stage, entered: ticket.entered_stage, completed: now });
  }
  ticket.stage = nextStageDef.name;
  ticket.skill_progress = {};
  ticket.entered_stage = now;
  ticket.completed_stage = null;
}

// ── Scatter detection ────────────────────────────────────────────────────────

export function needsScatter(ticket: WrTicket, kb: WrKanbanBoard): boolean {
  const stageDef = getStage(kb, ticket.stage);
  if (!stageDef || !isStageComplete(ticket, stageDef)) return false;
  const nxt = nextStage(kb, ticket.stage);
  if (!nxt || nxt.scope === stageDef.scope) return false;
  return true;
}

// ── Scatter execution ────────────────────────────────────────────────────────

export interface ChildSpec {
  id: string;
  name: string;
  priority: number;
}

/** Scatter parent into children. Parent stays visible (done bucket) with scatter_to set; it is NOT archived. */
export function scatterIntoChildren(
  parent: WrTicket,
  nextStageDef: WrStageDef,
  childrenSpec: ChildSpec[],
  existingIds: Set<string>,
): WrTicket[] {
  const collisions = childrenSpec.filter((c) => existingIds.has(c.id));
  if (collisions.length > 0) {
    throw new Error(
      `Scatter from ${parent.ticket_id} would create duplicate IDs: ${collisions.map((c) => c.id).join(', ')}`,
    );
  }
  const now = nowIso();
  parent.completed_stage = now;
  parent.scatter_to = childrenSpec.map((c) => c.id);
  parent.stage_history ??= [];
  if (parent.stage && parent.entered_stage) {
    parent.stage_history.push({ stage: parent.stage, entered: parent.entered_stage, completed: now });
  }
  return childrenSpec.map((spec) => ({
    ticket_id: spec.id,
    lineage: [...parent.lineage, spec.name ?? spec.id],
    scope_level: nextStageDef.scope,
    stage: nextStageDef.name,
    priority: spec.priority ?? 1,
    created: now,
    entered_stage: now,
    completed_stage: null,
    skill_progress: {},
    scatter_from: parent.ticket_id,
    scatter_to: [],
    stage_history: [],
    notes: '',
  }));
}

// ── Board stage helpers ──────────────────────────────────────────────────────

export function getStage(kb: WrKanbanBoard, stageName: string): WrStageDef | null {
  return kb.stages.find((s) => s.name === stageName) ?? null;
}

export function nextStage(kb: WrKanbanBoard, currentStage: string): WrStageDef | null {
  const idx = kb.stages.findIndex((s) => s.name === currentStage);
  if (idx < 0 || idx + 1 >= kb.stages.length) return null;
  return kb.stages[idx + 1]!;
}

// ── Ticket find / save in board ──────────────────────────────────────────────

export function findTicketInBoard(
  board: WrBoard,
  ticketId: string,
): { bucket: 'active' | 'backlog' | 'done'; index: number; ticket: WrTicket } | null {
  for (const bucket of ['active', 'backlog', 'done'] as const) {
    const list = board[bucket] as WrTicket[];
    const idx = list.findIndex((t) => t.ticket_id === ticketId);
    if (idx >= 0) return { bucket, index: idx, ticket: list[idx]! };
  }
  return null;
}

export function saveTicketInBoard(
  board: WrBoard,
  bucket: string,
  index: number,
  ticket: WrTicket,
): void {
  (board[bucket] as WrTicket[])[index] = ticket;
}

// ── Aggregate counts ─────────────────────────────────────────────────────────

export function countInProgressForRole(tickets: WrTicket[], role: string): number {
  let n = 0;
  for (const ticket of tickets) {
    for (const sp of Object.values(ticket.skill_progress)) {
      if (sp.agent === role && sp.execution_status === 'in_progress') n++;
    }
  }
  return n;
}

export function countActiveAtStage(board: WrBoard, stageName: string): number {
  return board.active.filter((t) => t.stage === stageName).length;
}

// ── WIP limit resolution ─────────────────────────────────────────────────────

/** Resolution order: explicit <scope>_wip_limit → team size of first required role → default 3 (1 for partition). */
export function wipLimitForScope(
  board: WrBoard,
  scope: string,
  team: Record<string, number>,
  stageDef?: WrStageDef,
): number {
  const explicit = board[`${scope}_wip_limit`] as number | undefined;
  if (typeof explicit === 'number' && explicit > 0) return explicit;
  if (team && stageDef) {
    for (const sd of stageDef.stage_work_required) {
      if (!sd.optional) {
        const roleCap = team[sd.role] ?? 0;
        if (roleCap > 0) return roleCap;
      }
    }
  }
  return scope === 'partition' ? 1 : 3;
}

export function pullSlotsForStage(
  board: WrBoard,
  stageDef: WrStageDef,
  team: Record<string, number>,
): number {
  const wip = wipLimitForScope(board, stageDef.scope, team, stageDef);
  const firstRequired = stageDef.stage_work_required.find((sd) => !sd.optional);
  if (!firstRequired) {
    return Math.max(0, wip - countActiveAtStage(board, stageDef.name));
  }
  let needing = 0;
  for (const raw of board.active) {
    if (raw.stage !== stageDef.name) continue;
    const sp = raw.skill_progress[firstRequired.skill];
    if (!sp || !isSkillProgressDone(sp)) needing++;
  }
  return Math.max(0, wip - needing);
}

export function selectBacklogForStage(
  board: WrBoard,
  stageName: string,
  limit: number,
): WrTicket[] {
  const candidates = board.backlog
    .filter((t) => t.stage === stageName)
    .sort((a, b) => a.priority - b.priority);
  return candidates.slice(0, limit);
}

// ── Downstream-first eligibility ─────────────────────────────────────────────

export function findNextEligible(
  kb: WrKanbanBoard,
  tickets: WrTicket[],
  role: string,
  skipKeys: Set<string> = new Set(),
): { ticket: WrTicket; skill: string; stageDef: WrStageDef } | null {
  for (const stageDef of [...kb.stages].reverse()) {
    const stageTickets = tickets
      .filter((t) => t.stage === stageDef.name)
      .sort((a, b) => a.priority - b.priority);
    for (const ticket of stageTickets) {
      const skill = nextEligibleSkill(ticket, stageDef, role);
      if (skill == null) continue;
      const key = `${ticket.ticket_id}:${skill}`;
      if (skipKeys.has(key)) continue;
      return { ticket, skill, stageDef };
    }
  }
  return null;
}

/**
 * Find next eligible skill across ALL board columns (active, backlog, done).
 * Downstream stages first (rightmost column priority).
 * Returns the source column so the caller can promote backlog tickets to active.
 */
export function findNextEligibleAcrossBoard(
  kb: WrKanbanBoard,
  board: WrBoard,
  role: string,
  skipKeys: Set<string> = new Set(),
): { ticket: WrTicket; skill: string; stageDef: WrStageDef; source: 'active' | 'backlog' | 'done' } | null {
  const tagged: Array<{ ticket: WrTicket; source: 'active' | 'backlog' | 'done' }> = [
    ...board.active.map((t) => ({ ticket: t, source: 'active' as const })),
    ...board.done.map((t) => ({ ticket: t, source: 'done' as const })),
    ...board.backlog.map((t) => ({ ticket: t, source: 'backlog' as const })),
  ];

  for (const stageDef of [...kb.stages].reverse()) {
    const stageEntries = tagged
      .filter((e) => e.ticket.stage === stageDef.name)
      .sort((a, b) => a.ticket.priority - b.ticket.priority);
    for (const entry of stageEntries) {
      const skill = nextEligibleSkill(entry.ticket, stageDef, role);
      if (skill == null) continue;
      const key = `${entry.ticket.ticket_id}:${skill}`;
      if (skipKeys.has(key)) continue;
      return { ticket: entry.ticket, skill, stageDef, source: entry.source };
    }
  }
  return null;
}

export function listEligiblePulls(
  kb: WrKanbanBoard,
  tickets: WrTicket[],
  role: string,
): Array<[string, string]> {
  const skip = new Set<string>();
  const out: Array<[string, string]> = [];
  const maxIter = Math.max(1, tickets.length) + 8;
  for (let i = 0; i < maxIter; i++) {
    const match = findNextEligible(kb, tickets, role, skip);
    if (!match) break;
    const key = `${match.ticket.ticket_id}:${match.skill}`;
    out.push([match.ticket.ticket_id, match.skill]);
    skip.add(key);
  }
  return out;
}

export function countEligibleClaims(
  kb: WrKanbanBoard,
  tickets: WrTicket[],
  role: string,
  skipKeys: Set<string> = new Set(),
): Array<[string, string]> {
  const out: Array<[string, string]> = [];
  const skip = new Set<string>(skipKeys);
  for (const ticket of tickets) {
    const match = findNextEligible(kb, [ticket], role, skip);
    if (match) {
      const key = `${match.ticket.ticket_id}:${match.skill}`;
      out.push([match.ticket.ticket_id, match.skill]);
      skip.add(key);
    }
  }
  return out;
}

export function inProgressClaimsForRole(
  kb: WrKanbanBoard,
  tickets: WrTicket[],
  role: string,
): Array<[WrTicket, string]> {
  const claims: Array<[WrTicket, string]> = [];
  for (const stageDef of [...kb.stages].reverse()) {
    const stageTickets = tickets
      .filter((t) => t.stage === stageDef.name)
      .sort((a, b) => a.priority - b.priority);
    for (const ticket of stageTickets) {
      for (const [skillId, sp] of Object.entries(ticket.skill_progress)) {
        const ownsExecution = sp.execution_status === 'in_progress' && sp.agent === role;
        const ownsReview =
          sp.review_status === 'in_progress' && (sp.reviewer === role || sp.agent === role);
        if (ownsExecution || ownsReview) claims.push([ticket, skillId]);
      }
    }
  }
  return claims;
}

// ── Backlog sort key ─────────────────────────────────────────────────────────

const SCOPE_ORDER = ['project', 'partition', 'increment', 'sprint'];

function moduleNumberFromTicketId(ticketId: string): number | null {
  const head = ticketId.split('-', 1)[0]!;
  if (!/^\d+$/.test(head)) return null;
  return Number(head);
}

export function backlogSortKey(ticket: WrTicket): [number, number, number] {
  const si = SCOPE_ORDER.indexOf(ticket.scope_level ?? 'all');
  const scopeIdx = si >= 0 ? si : 99;
  if (ticket.scope_level === 'increment') {
    const mod = moduleNumberFromTicketId(ticket.ticket_id) ?? 99;
    return [scopeIdx, mod, ticket.priority];
  }
  return [scopeIdx, ticket.priority, 0];
}

export function sortBacklog(tickets: WrTicket[]): WrTicket[] {
  return [...tickets].sort((a, b) => {
    const ka = backlogSortKey(a);
    const kb = backlogSortKey(b);
    for (let i = 0; i < 3; i++) {
      if (ka[i]! !== kb[i]!) return ka[i]! - kb[i]!;
    }
    return 0;
  });
}

// ── Existing board ID set ────────────────────────────────────────────────────

export function existingBoardIds(board: WrBoard): Set<string> {
  const ids = new Set<string>();
  for (const bucket of ['active', 'backlog', 'done'] as const) {
    for (const t of board[bucket]) {
      if (t.ticket_id) ids.add(t.ticket_id);
    }
  }
  return ids;
}

// ── Tickets needing scatter ──────────────────────────────────────────────────

export function ticketsNeedingScatter(board: WrBoard, kb: WrKanbanBoard): WrTicket[] {
  return board.done.filter(
    (t) => !t.archived && !(t.scatter_to?.length) && needsScatter(t, kb),
  );
}

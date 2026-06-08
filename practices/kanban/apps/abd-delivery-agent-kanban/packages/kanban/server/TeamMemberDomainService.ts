/**
 * TeamMemberDomainService — TypeScript port of Python agent.py.
 *
 * Provides the core delivery-agent operations:
 *   pullSkill, claimSkill, completeSkill, signalReady,
 *   claimNextIntent, findInProgressClaim, applySkillFixture.
 *
 * All functions are async and own their own board I/O (load/save).
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';
import {
  loadBoard,
  saveBoard,
  appendMetricsLog,
  nowIso,
  resolveKb,
  type WrBoard,
  type WrTicket,
  type WrSkillProgress,
  type WrKanbanBoard,
} from './WarRoomService';
import { writeHeartbeat, readRegisteredSpawnEpoch } from './HeartbeatService';
import {
  findFirstIntentForRole,
  loadActionIntents,
  removeActionIntentEntry,
  type ActionIntentEntry,
} from './ActionStateService';
import {
  findTicketInBoard,
  saveTicketInBoard,
  countInProgressForRole,
  inProgressClaimsForRole,
  findNextEligible,
  findNextEligibleAcrossBoard,
} from './KanbanDomainOps';

// ── Result type ──────────────────────────────────────────────────────────────

export interface AgentOperationResult {
  action: string;
  ticket_id?: string;
  skill?: string;
  stage?: string;
  role?: string;
  instance?: number;
  reason?: string;
  released_claims?: Array<{ ticket_id: string; skill: string; stage: string }>;
}

// ── Internal heartbeat helper ─────────────────────────────────────────────────

async function beat(
  warRoom: string,
  role: string,
  status: string,
  note: string,
  instance: number,
  spawnEpoch: number | null,
): Promise<void> {
  await writeHeartbeat(warRoom, role, status, note, instance, spawnEpoch ?? undefined);
}

// ── Role capacity from board ──────────────────────────────────────────────────

function roleCapacity(board: WrBoard, role: string): number {
  const team = board.team as Record<string, number> | undefined;
  if (team && Object.keys(team).length > 0) return Number(team[role] ?? 3);
  return 3;
}

// ── Resume existing claim ─────────────────────────────────────────────────────

async function resumeExistingClaim(
  warRoom: string,
  kb: WrKanbanBoard,
  active: WrTicket[],
  role: string,
  instance: number,
  spawnEpoch: number | null,
): Promise<AgentOperationResult | null> {
  const claims = inProgressClaimsForRole(kb, active, role);
  if (!claims.length) return null;
  const [ticket, skill] = claims[0]!;
  await beat(warRoom, role, 'working', `resume ${skill} on ${ticket.ticket_id}`, instance, spawnEpoch);
  await appendMetricsLog(warRoom, {
    event: 'skill_resume',
    agent_role: role,
    instance,
    ticket_id: ticket.ticket_id,
    skill,
    stage: ticket.stage,
  });
  return { action: 'resume', ticket_id: ticket.ticket_id, skill, stage: ticket.stage, role, instance };
}

// ── Find matching intent ──────────────────────────────────────────────────────

async function findMatchingIntent(
  warRoom: string,
  ticketId: string,
  skill: string,
  role: string,
): Promise<ActionIntentEntry | null> {
  const intents = await loadActionIntents(warRoom);
  return intents.find((i) => i.ticket_id === ticketId && i.skill === skill && i.agent_role === role) ?? null;
}

// ── Pull (find + claim) ───────────────────────────────────────────────────────

export async function pullSkill(
  warRoom: string,
  kb: WrKanbanBoard,
  role: string,
  instance = 1,
  reserve = false,
): Promise<AgentOperationResult> {
  const board = await loadBoard(warRoom);
  const active = board.active;
  const spawnEpoch = await readRegisteredSpawnEpoch(warRoom, role, instance);

  if (board.board_mode === 'manual') {
    const resume = await resumeExistingClaim(warRoom, kb, active, role, instance, spawnEpoch);
    if (resume) return resume;
    return { action: 'none', reason: 'manual_mode_await_operator_drop' };
  }

  const resume = await resumeExistingClaim(warRoom, kb, active, role, instance, spawnEpoch);
  if (resume) return resume;

  const match = findNextEligibleAcrossBoard(kb, board, role);
  if (!match) {
    return { action: 'none', reason: 'no_eligible_skill' };
  }

  if (match.source === 'backlog') {
    const idx = board.backlog.findIndex((t) => t.ticket_id === match.ticket.ticket_id);
    if (idx >= 0) {
      const [promoted] = board.backlog.splice(idx, 1);
      promoted!.entered_stage = new Date().toISOString();
      board.active.push(promoted!);
      await saveBoard(warRoom, board);
    }
  }

  return claimSkillOnBoard(
    warRoom,
    kb,
    role,
    match.ticket.ticket_id,
    match.skill,
    reserve,
    instance,
    spawnEpoch,
  );
}

// ── Claim ─────────────────────────────────────────────────────────────────────

/**
 * Claim a skill on a ticket. Mutates board.json.
 * Invariant: first-come, first-serve; in_progress → already_claimed or error.
 */
export async function claimSkillOnBoard(
  warRoom: string,
  kb: WrKanbanBoard,
  role: string,
  ticketId: string,
  skill: string,
  reserve = false,
  instance = 1,
  spawnEpoch: number | null = null,
): Promise<AgentOperationResult> {
  const board = await loadBoard(warRoom);
  const found = findTicketInBoard(board, ticketId);
  if (!found) throw new Error(`Ticket not found: ${ticketId}`);

  let { bucket, index } = found;
  const ticket = { ...found.ticket, skill_progress: { ...found.ticket.skill_progress } };

  // Manual mode: promote backlog children to active on claim
  if (board.board_mode === 'manual' && bucket === 'backlog') {
    board.backlog = board.backlog.filter((t) => t.ticket_id !== ticketId);
    board.active.push(ticket);
    bucket = 'active';
    index = board.active.length - 1;
  }

  const sp = ticket.skill_progress[skill] as WrSkillProgress | undefined;

  if (board.board_mode === 'manual') {
    if (sp?.execution_status === 'in_progress' && sp.agent === role) {
      await beat(warRoom, role, 'working', `resume ${skill} on ${ticketId}`, instance, spawnEpoch);
      return { action: 'resume', ticket_id: ticketId, skill, stage: ticket.stage, role, instance };
    }
    const intent = await findMatchingIntent(warRoom, ticketId, skill, role);
    if (!intent) return { action: 'none', reason: 'manual_mode_await_operator_drop' };
    if (sp?.execution_status === 'done') {
      await removeActionIntentEntry(warRoom, intent);
      throw new Error(`Skill ${skill} already done on ${ticketId}`);
    }
    if (sp?.execution_status === 'in_progress') {
      if (sp.agent !== role) return { action: 'none', reason: 'skill_in_progress_by_other_role' };
      await removeActionIntentEntry(warRoom, intent);
      await beat(warRoom, role, 'working', `resume ${skill} on ${ticketId}`, instance, spawnEpoch);
      return { action: 'resume', ticket_id: ticketId, skill, stage: ticket.stage, role, instance };
    }
    await removeActionIntentEntry(warRoom, intent);
  } else {
    if (sp?.execution_status === 'in_progress') {
      if (sp.agent === role) {
        await beat(warRoom, role, 'working', `resume ${skill} on ${ticketId}`, instance, spawnEpoch);
        return { action: 'already_claimed', ticket_id: ticketId, skill };
      }
      throw new Error(`Skill ${skill} already in_progress by ${sp.agent}`);
    }
    if (sp?.execution_status === 'done') {
      throw new Error(`Skill ${skill} already done on ${ticketId}`);
    }
  }

  const now = nowIso();
  ticket.skill_progress[skill] = {
    execution_status: 'in_progress',
    agent: role,
    start: now,
    review_status: 'not_started',
  };
  saveTicketInBoard(board, bucket, index, ticket);
  await saveBoard(warRoom, board);

  const hbStatus = reserve ? 'reserved' : 'working';
  await beat(warRoom, role, hbStatus, `in_progress ${skill} on ${ticketId}`, instance, spawnEpoch);
  await appendMetricsLog(warRoom, {
    event: 'skill_claim',
    agent_role: role,
    instance,
    ticket_id: ticketId,
    skill,
    stage: ticket.stage,
  });

  return { action: 'claimed', ticket_id: ticketId, skill, stage: ticket.stage, role, instance };
}

// ── Complete ──────────────────────────────────────────────────────────────────

/**
 * Two-pass completion:
 *   Pass 1 (execution in_progress) → execution done, review in_progress
 *   Pass 2 (review in_progress)    → review done (skill fully complete)
 */
export async function completeSkillOnBoard(
  warRoom: string,
  role: string,
  ticketId: string,
  skill: string,
  notes?: string,
  instance = 1,
  spawnEpoch: number | null = null,
): Promise<AgentOperationResult> {
  const board = await loadBoard(warRoom);
  const found = findTicketInBoard(board, ticketId);
  if (!found) throw new Error(`Ticket not found: ${ticketId}`);

  const { bucket, index } = found;
  const ticket = { ...found.ticket, skill_progress: { ...found.ticket.skill_progress } };
  let sp = ticket.skill_progress[skill] as WrSkillProgress | undefined;
  if (!sp) {
    sp = { execution_status: 'not_started' };
    ticket.skill_progress[skill] = sp;
  }

  if (sp.execution_status === 'done' && sp.review_status === 'done') {
    throw new Error(`Skill ${skill} already done on ${ticketId}`);
  }

  if (sp.execution_status === 'in_progress') {
    return completeWorkPass(warRoom, board, bucket, index, ticket, skill, sp, notes, role, instance, spawnEpoch);
  }
  if (sp.execution_status === 'done' && sp.review_status === 'in_progress') {
    return completeReviewPass(warRoom, board, bucket, index, ticket, skill, sp, notes, role, instance, spawnEpoch);
  }
  if (sp.execution_status === 'done' && (!sp.review_status || sp.review_status === 'not_started')) {
    const now = nowIso();
    sp.review_status = 'in_progress';
    sp.reviewer = role;
    sp.review_start = now;
    saveTicketInBoard(board, bucket, index, ticket);
    await saveBoard(warRoom, board);
    await beat(warRoom, role, 'working', `review ${skill} on ${ticketId}`, instance, spawnEpoch);
    return { action: 'review_started', ticket_id: ticketId, skill, stage: ticket.stage };
  }

  throw new Error(
    `Cannot complete skill ${skill} on ${ticketId}: execution=${sp.execution_status} review=${sp.review_status}`,
  );
}

async function completeWorkPass(
  warRoom: string,
  board: WrBoard,
  bucket: string,
  index: number,
  ticket: WrTicket,
  skill: string,
  sp: WrSkillProgress,
  notes: string | undefined,
  role: string,
  instance: number,
  spawnEpoch: number | null,
): Promise<AgentOperationResult> {
  const now = nowIso();
  sp.execution_status = 'done';
  sp.agent = role;
  sp.end = now;
  sp.review_status = 'in_progress';
  sp.reviewer = role;
  sp.review_start = now;
  if (notes) sp.notes = notes;

  saveTicketInBoard(board, bucket, index, ticket);
  await saveBoard(warRoom, board);
  await beat(warRoom, role, 'working', `work done ${skill} on ${ticket.ticket_id}`, instance, spawnEpoch);
  await appendMetricsLog(warRoom, {
    event: 'skill_work_done',
    agent_role: role,
    instance,
    ticket_id: ticket.ticket_id,
    skill,
    stage: ticket.stage,
  });
  return { action: 'work_done', ticket_id: ticket.ticket_id, skill, stage: ticket.stage };
}

async function completeReviewPass(
  warRoom: string,
  board: WrBoard,
  bucket: string,
  index: number,
  ticket: WrTicket,
  skill: string,
  sp: WrSkillProgress,
  notes: string | undefined,
  role: string,
  instance: number,
  spawnEpoch: number | null,
): Promise<AgentOperationResult> {
  const now = nowIso();
  sp.review_status = 'done';
  sp.reviewer = sp.reviewer ?? role;
  sp.review_end = now;
  if (notes) sp.notes = notes;

  saveTicketInBoard(board, bucket, index, ticket);
  await saveBoard(warRoom, board);
  await beat(warRoom, role, 'working', `done ${skill} on ${ticket.ticket_id}`, instance, spawnEpoch);
  await appendMetricsLog(warRoom, {
    event: 'skill_done',
    agent_role: role,
    instance,
    ticket_id: ticket.ticket_id,
    skill,
    stage: ticket.stage,
  });
  return { action: 'completed', ticket_id: ticket.ticket_id, skill, stage: ticket.stage };
}

// ── Signal ready ──────────────────────────────────────────────────────────────

export async function signalReady(
  warRoom: string,
  role: string,
  instance = 1,
  spawnEpoch: number | null = null,
  reason = 'no_eligible_skill_on_active_tickets',
): Promise<AgentOperationResult> {
  const released = await releaseOwnClaims(warRoom, role, instance, reason);
  await beat(warRoom, role, 'ready', reason, instance, spawnEpoch);
  await appendMetricsLog(warRoom, {
    event: 'agent_ready',
    agent_role: role,
    instance,
    reason,
    released_claims: released,
  });
  return { action: 'ready', role, instance, reason, released_claims: released };
}

async function releaseOwnClaims(
  warRoom: string,
  role: string,
  instance: number,
  reason: string,
): Promise<Array<{ ticket_id: string; skill: string; stage: string }>> {
  const board = await loadBoard(warRoom);
  const released: Array<{ ticket_id: string; skill: string; stage: string }> = [];
  let changed = false;

  for (let i = 0; i < board.active.length; i++) {
    const ticket = { ...board.active[i]!, skill_progress: { ...board.active[i]!.skill_progress } };
    const ticketReleased: string[] = [];
    for (const [skillId, sp] of Object.entries(ticket.skill_progress)) {
      if (sp.agent !== role || sp.execution_status !== 'in_progress') continue;
      delete ticket.skill_progress[skillId];
      ticketReleased.push(skillId);
    }
    if (!ticketReleased.length) continue;
    for (const skillId of ticketReleased) {
      const entry = { ticket_id: ticket.ticket_id, skill: skillId, stage: ticket.stage };
      released.push(entry);
      await appendMetricsLog(warRoom, {
        event: 'claim_released_self',
        agent_role: role,
        instance,
        reason,
        ...entry,
      });
    }
    saveTicketInBoard(board, 'active', i, ticket);
    changed = true;
  }

  if (changed) await saveBoard(warRoom, board);
  return released;
}

// ── Claim next intent (manual mode) ──────────────────────────────────────────

export async function claimNextIntent(
  warRoom: string,
  role: string,
  instance = 1,
): Promise<AgentOperationResult> {
  const board = await loadBoard(warRoom);
  if (board.board_mode !== 'manual') return { action: 'none', reason: 'not_manual_mode' };

  const kb = await resolveKb(warRoom, board);
  const active = board.active;
  const spawnEpoch = await readRegisteredSpawnEpoch(warRoom, role, instance);
  const resume = await resumeExistingClaim(warRoom, kb, active, role, instance, spawnEpoch);
  if (resume) return resume;

  const intent = await findFirstIntentForRole(warRoom, role);
  if (!intent) return { action: 'none', reason: 'no_pending_intent' };

  return claimSkillOnBoard(warRoom, kb, role, intent.ticket_id, intent.skill, false, instance, spawnEpoch);
}

// ── Find in-progress claim ────────────────────────────────────────────────────

export async function findInProgressClaim(
  warRoom: string,
  role: string,
): Promise<{ ticket_id: string; skill: string } | null> {
  const board = await loadBoard(warRoom);
  const kb = await resolveKb(warRoom, board);
  const active = board.active;
  const claims = inProgressClaimsForRole(kb, active, role);
  if (!claims.length) return null;
  const [ticket, skill] = claims[0]!;
  return { ticket_id: ticket.ticket_id, skill };
}

// ── Apply skill fixture ───────────────────────────────────────────────────────

export async function applySkillFixture(
  warRoom: string,
  engagementRoot: string,
  role: string,
  ticketId: string,
  skill: string,
  instance = 1,
  spawnEpoch: number | null = null,
): Promise<Record<string, unknown>> {
  const board = await loadBoard(warRoom);
  const found = findTicketInBoard(board, ticketId);
  if (!found) throw new Error(`Ticket not found: ${ticketId}`);
  const { ticket } = found;

  const fixtures = await loadFixturesIndex(engagementRoot);
  const entry = pickFixtureEntry(fixtures, skill, ticket.scope_level ?? 'all');
  const copied = await copyFixtureFiles(engagementRoot, entry);

  let postCopyResults: Array<Record<string, unknown>> = [];
  if (Array.isArray(entry['post_copy'])) {
    postCopyResults = await runPostCopy(engagementRoot, entry['post_copy'] as string[]);
  }

  const notes = 'fixture_mode: copied from skill-fixtures';
  const complete1 = await completeSkillOnBoard(warRoom, role, ticketId, skill, notes, instance, spawnEpoch);
  const complete2 = await completeSkillOnBoard(warRoom, role, ticketId, skill, notes, instance, spawnEpoch);

  const event: Record<string, unknown> = {
    event: 'skill_fixture_applied',
    ts: nowIso(),
    ticket_id: ticketId,
    skill,
    agent_role: role,
    instance,
    scope_level: ticket.scope_level,
    copies: copied,
    post_copy: postCopyResults,
    complete: [complete1.action, complete2.action],
  };
  await appendMetricsLog(warRoom, event);
  return event;
}

async function loadFixturesIndex(engagementRoot: string): Promise<Record<string, unknown>> {
  const fixturePath = path.join(engagementRoot, 'skill-fixtures.json');
  const raw = await fs.readFile(fixturePath, 'utf8');
  return JSON.parse(raw) as Record<string, unknown>;
}

function pickFixtureEntry(
  fixtures: Record<string, unknown>,
  skill: string,
  scopeLevel: string,
): Record<string, unknown> {
  const skillEntries = (
    fixtures['fixtures'] as Record<string, Record<string, unknown>> | undefined
  )?.[skill];
  if (!skillEntries) throw new Error(`No fixture entry for skill '${skill}'`);
  const scopeKey = `scope_${scopeLevel}`;
  if (scopeKey in skillEntries) return skillEntries[scopeKey]! as Record<string, unknown>;
  if ('default' in skillEntries) return skillEntries['default']! as Record<string, unknown>;
  const first = Object.entries(skillEntries).find(([k]) => !k.startsWith('scope_'));
  if (first) return first[1] as Record<string, unknown>;
  throw new Error(`No fixture variant for skill '${skill}' scope '${scopeLevel}'`);
}

async function copyFixtureFiles(
  engagementRoot: string,
  entry: Record<string, unknown>,
): Promise<Array<{ source: string; target: string }>> {
  const copies = (entry['copies'] as Array<{ source: string; target: string }> | undefined) ?? [];
  const result: Array<{ source: string; target: string }> = [];
  for (const item of copies) {
    const src = path.join(engagementRoot, item.source);
    const dst = path.join(engagementRoot, item.target);
    await fs.mkdir(path.dirname(dst), { recursive: true });
    await fs.copyFile(src, dst);
    result.push({ source: item.source, target: item.target });
  }
  return result;
}

async function runPostCopy(
  engagementRoot: string,
  commands: string[],
): Promise<Array<Record<string, unknown>>> {
  const { exec } = await import('node:child_process');
  const { promisify } = await import('node:util');
  const execAsync = promisify(exec);
  const results: Array<Record<string, unknown>> = [];
  for (const cmd of commands) {
    try {
      const { stdout, stderr } = await execAsync(cmd, { cwd: engagementRoot });
      results.push({
        command: cmd,
        returncode: 0,
        stdout: stdout.slice(-500),
        stderr: stderr.slice(-500),
      });
    } catch (e) {
      const err = e as { code?: number; stdout?: string; stderr?: string; message?: string };
      const rc = err.code ?? 1;
      results.push({
        command: cmd,
        returncode: rc,
        stdout: (err.stdout ?? '').slice(-500),
        stderr: (err.stderr ?? err.message ?? '').slice(-500),
      });
      throw new Error(`post_copy failed (${rc}): ${cmd}\n${err.stderr ?? err.message ?? ''}`);
    }
  }
  return results;
}

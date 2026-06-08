/**
 * LeadScanService — TypeScript port of Python KanbanLead.run_tick() and full scan cycle.
 *
 * Replaces the Python run_kanban_lead_tick.py and kanban_cli.py lead sync shell-outs
 * in app-server. Produces identical JSON output to the Python implementation.
 *
 * Scan cycle (automatic mode):
 *   sync_board → detect_duplicates → scatter_pending → pull_backlog →
 *   release_stale_reserved → release_orphan_claims → dispatch_claims →
 *   build_role_report → compute_spawns → write_heartbeat
 */

import { readFileSync, accessSync } from 'node:fs';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import {
  resolveWarRoomDir,
  loadBoard,
  saveBoard,
  loadKanbanConfig,
  parseKanbanBoards,
  appendMetricsLog,
  nowIso,
  loadTeam,
  readJson,
  writeJson,
  type WrBoard,
  type WrTicket,
  type WrStageDef,
  type WrKanbanBoard,
} from './WarRoomService';
import {
  writeHeartbeat,
  countLiveAgents,
  countWorkingAgents,
  listHeartbeatFiles,
  readHeartbeatAge,
  registerExecutorSpawn,
  purgeUnregisteredHeartbeats,
  hasFreshHeartbeatWithStatus,
} from './HeartbeatService';
import {
  actionStateFileExists,
  loadActionIntents,
  removeActionIntentEntry,
  countIntentsByRole,
  type ActionIntentEntry,
} from './ActionStateService';
import {
  isStageComplete,
  needsScatter,
  advanceToNextStage,
  scatterIntoChildren,
  getStage,
  nextStage,
  findTicketInBoard,
  saveTicketInBoard,
  countInProgressForRole,
  selectBacklogForStage,
  pullSlotsForStage,
  listEligiblePulls,
  countEligibleClaims,
  sortBacklog,
  existingBoardIds,
  ticketsNeedingScatter,
  type ChildSpec,
} from './KanbanDomainOps';
import { pullSkill } from './TeamMemberDomainService';
import { Ticket } from './Ticket';

// ── Constants ─────────────────────────────────────────────────────────────────

const ROLES = ['business-expert', 'product-owner', 'ux-designer', 'engineer'] as const;
type Role = (typeof ROLES)[number];

// ── Public report types ───────────────────────────────────────────────────────

export interface RoleReportEntry {
  team: number;
  live_agents: number;
  working_agents: number;
  in_progress: number;
  eligible_claims: Array<[string, string]>;
  spawn_needed: number;
  dispatch_needed: number;
  pending_intents?: number;
}

export interface SpawnEntry {
  role: string;
  instance: number;
  reason: string;
  spawn_epoch: number;
}

export interface SpawnPrompt {
  role: string;
  instance: number;
  prompt: string;
}

export interface LeadScanReport {
  cycle: number;
  timestamp: string;
  board_mode?: string;
  active_tickets: number;
  backlog_count: number;
  roles: Record<string, RoleReportEntry>;
  spawns: SpawnEntry[];
  actions: string[];
  must_spawn: boolean;
  dispatch_summary: Record<string, number>;
  spawn_prompts: SpawnPrompt[];
  orchestrator_rule: string;
}

// ── Lead session persistence ──────────────────────────────────────────────────

async function readLeadSession(warRoom: string): Promise<Record<string, unknown>> {
  try {
    return await readJson<Record<string, unknown>>(path.join(warRoom, 'lead-session.json'));
  } catch {
    return { cycle: 0 };
  }
}

async function writeLeadSession(warRoom: string, data: Record<string, unknown>): Promise<void> {
  await writeJson(path.join(warRoom, 'lead-session.json'), data);
}

// ── Stage advance / flag ──────────────────────────────────────────────────────

async function advanceOrFlag(
  ticket: WrTicket,
  kb: WrKanbanBoard,
  warRoom: string,
): Promise<'no_change' | 'complete' | 'scatter_needed' | 'advanced'> {
  const currentDef = getStage(kb, ticket.stage);
  if (!currentDef) return 'no_change';
  if (!isStageComplete(ticket, currentDef)) return 'no_change';

  const nxt = nextStage(kb, ticket.stage);
  if (!nxt) {
    ticket.completed_stage = nowIso();
    await appendMetricsLog(warRoom, {
      event: 'ticket_complete',
      ticket_id: ticket.ticket_id,
      lineage: ticket.lineage,
      stage: ticket.stage,
    });
    return 'complete';
  }

  if (nxt.scope !== currentDef.scope) {
    ticket.completed_stage = nowIso();
    await appendMetricsLog(warRoom, {
      event: 'scatter_needed',
      ticket_id: ticket.ticket_id,
      from_scope: currentDef.scope,
      to_scope: nxt.scope,
      next_stage: nxt.name,
    });
    return 'scatter_needed';
  }

  const oldStage = ticket.stage;
  advanceToNextStage(ticket, nxt);
  await appendMetricsLog(warRoom, {
    event: 'stage_advance',
    ticket_id: ticket.ticket_id,
    lineage: ticket.lineage,
    from_stage: oldStage,
    to_stage: nxt.name,
  });
  return 'advanced';
}

// ── Board sync ────────────────────────────────────────────────────────────────

async function syncBoardState(warRoom: string, kb: WrKanbanBoard): Promise<WrBoard> {
  const board = await loadBoard(warRoom);
  const archived = [...board.archived];
  const newActive: WrTicket[] = [];
  const newDone: WrTicket[] = [];

  for (const ticketRaw of board.active) {
    const ticket = deepCopyTicket(ticketRaw);
    const action = await advanceOrFlag(ticket, kb, warRoom);
    if (action === 'complete') archived.push(ticket);
    else if (action === 'scatter_needed') newDone.push(ticket);
    else newActive.push(ticket);
  }

  for (const ticketRaw of board.done) {
    const ticket = deepCopyTicket(ticketRaw);
    if (ticket.completed_stage && !needsScatter(ticket, kb)) archived.push(ticket);
    else newDone.push(ticket);
  }

  board.active = newActive;
  board.done = newDone;
  board.archived = archived;
  board.synced_at = nowIso();
  await saveBoard(warRoom, board);
  return board;
}

// ── Duplicate ID detection ────────────────────────────────────────────────────

async function detectDuplicateIds(warRoom: string): Promise<string[]> {
  const board = await loadBoard(warRoom);
  const counter: Record<string, number> = {};
  for (const bucket of ['active', 'backlog', 'done'] as const) {
    for (const t of board[bucket]) counter[t.ticket_id] = (counter[t.ticket_id] ?? 0) + 1;
  }
  const dupes = Object.fromEntries(Object.entries(counter).filter(([, v]) => v > 1));
  if (Object.keys(dupes).length === 0) return [];
  await appendMetricsLog(warRoom, { event: 'duplicate_ticket_ids_detected', duplicates: dupes });
  return Object.entries(dupes).sort().map(([tid, count]) => `DUPLICATE_ID:${tid}:x${count}`);
}

// ── Scatter ───────────────────────────────────────────────────────────────────

function resolveChildrenSpec(ticket: WrTicket, engagementRoot: string): ChildSpec[] {
  const result = Ticket.tryResolveScatterChildren(engagementRoot, ticket.ticket_id, {
    childScope: ticket.scope_level === 'increment' ? 'sprint' : 'increment',
    ticketScopeLevel: ticket.scope_level,
  });
  if (!result) throw new Error(`No scatter spec for ${ticket.ticket_id}`);
  return result;
}

async function executeScatter(
  parent: WrTicket,
  kb: WrKanbanBoard,
  childrenSpec: ChildSpec[],
  warRoom: string,
): Promise<WrTicket[]> {
  const board = await loadBoard(warRoom);
  const existing = existingBoardIds(board);

  const nxt = nextStage(kb, parent.stage);
  if (!nxt) throw new Error(`No next stage after ${parent.stage}`);

  // Parent stays in done (trails its children); move from active to done if needed
  const activeIdx = board.active.findIndex((t) => t.ticket_id === parent.ticket_id);
  if (activeIdx >= 0) {
    board.active.splice(activeIdx, 1);
    board.done.push(deepCopyTicket(parent));
  }

  const parentInDone = board.done.find((t) => t.ticket_id === parent.ticket_id);
  if (!parentInDone) throw new Error(`Parent ${parent.ticket_id} not found in done after scatter prep`);
  const children = scatterIntoChildren(parentInDone, nxt, childrenSpec, existing);

  board.backlog = sortBacklog([...board.backlog, ...children]);
  await saveBoard(warRoom, board);

  await appendMetricsLog(warRoom, {
    event: 'scatter',
    parent_ticket: parent.ticket_id,
    parent_lineage: parent.lineage,
    children: children.map((c) => c.ticket_id),
    from_stage: parent.stage,
    to_stage: children[0]?.stage ?? '',
    from_scope: parent.scope_level,
    to_scope: children[0]?.scope_level ?? '',
  });
  return children;
}

async function scatterPending(
  warRoom: string,
  kb: WrKanbanBoard,
  engagementRoot: string,
): Promise<string[]> {
  const board = await loadBoard(warRoom);
  const actions: string[] = [];
  for (const ticket of ticketsNeedingScatter(board, kb)) {
    try {
      const childrenSpec = resolveChildrenSpec(ticket, engagementRoot);
      const children = await executeScatter(ticket, kb, childrenSpec, warRoom);
      actions.push(`scatter:${ticket.ticket_id}->${children.map((c) => c.ticket_id).join(',')}`);
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      actions.push(`scatter_failed:${ticket.ticket_id}:${msg}`);
      await appendMetricsLog(warRoom, {
        event: 'scatter_failed',
        ticket_id: ticket.ticket_id,
        error: msg,
      });
    }
  }
  return actions;
}

// ── Pull backlog ──────────────────────────────────────────────────────────────

async function pullForStage(
  warRoom: string,
  stageDef: WrStageDef,
  team: Record<string, number>,
): Promise<string[]> {
  const board = await loadBoard(warRoom);
  const slots = pullSlotsForStage(board, stageDef, team);
  if (slots <= 0) return [];

  const candidates = selectBacklogForStage(board, stageDef.name, slots);
  if (candidates.length === 0) return [];

  const actions: string[] = [];
  const candidateIds = new Set(candidates.map((c) => c.ticket_id));
  board.backlog = board.backlog.filter((t) => !candidateIds.has(t.ticket_id));

  for (const raw of candidates) {
    const ticket = {
      ...raw,
      entered_stage: nowIso(),
      notes: `Lead pulled to ${stageDef.name} active`,
    };
    board.active.push(ticket);
    actions.push(`pulled:${ticket.ticket_id}:${stageDef.name}:${stageDef.scope}`);
    await appendMetricsLog(warRoom, {
      event: 'ticket_pulled',
      agent: 'kanban-lead',
      ticket_id: ticket.ticket_id,
      from: 'backlog',
      to: 'active',
      scope_level: ticket.scope_level,
      stage: stageDef.name,
    });
  }

  await saveBoard(warRoom, board);
  return actions;
}

async function pullBacklog(
  warRoom: string,
  kb: WrKanbanBoard,
  team: Record<string, number>,
): Promise<string[]> {
  const actions: string[] = [];
  for (const stageDef of kb.stages) {
    actions.push(...(await pullForStage(warRoom, stageDef, team)));
  }
  return actions;
}

// ── Release stale / orphan claims ─────────────────────────────────────────────

async function releaseRoleClaims(
  warRoom: string,
  role: string,
  prefix: string,
): Promise<string[]> {
  const board = await loadBoard(warRoom);
  const actions: string[] = [];
  let changed = false;
  for (let i = 0; i < board.active.length; i++) {
    const ticket = deepCopyTicket(board.active[i]!);
    const released: string[] = [];
    for (const [skillId, sp] of Object.entries(ticket.skill_progress)) {
      if (sp.agent !== role || sp.execution_status !== 'in_progress') continue;
      delete ticket.skill_progress[skillId];
      released.push(skillId);
    }
    if (!released.length) continue;
    for (const skillId of released) actions.push(`${prefix}:${role}:${ticket.ticket_id}:${skillId}`);
    saveTicketInBoard(board, 'active', i, ticket);
    changed = true;
  }
  if (changed) await saveBoard(warRoom, board);
  return actions;
}

async function purgeReservedHeartbeats(warRoom: string, role: string): Promise<void> {
  for (const filePath of await listHeartbeatFiles(warRoom, role)) {
    try {
      const raw = await readJson<Record<string, unknown>>(filePath);
      if (raw['status'] === 'reserved') await fs.unlink(filePath);
    } catch { /* ignore */ }
  }
}

async function releaseStaleReserved(
  warRoom: string,
  team: Record<string, number>,
): Promise<string[]> {
  const actions: string[] = [];
  for (const role of ROLES) {
    if (!(role in team)) continue;
    if ((await countWorkingAgents(warRoom, role)) > 0) continue;
    if (await hasFreshHeartbeatWithStatus(warRoom, role, 'reserved', 30)) continue;
    actions.push(...(await releaseRoleClaims(warRoom, role, 'release_stale')));
    await purgeReservedHeartbeats(warRoom, role);
  }
  return actions;
}

async function releaseOrphanClaims(
  warRoom: string,
  team: Record<string, number>,
): Promise<string[]> {
  const actions: string[] = [];
  const board = await loadBoard(warRoom);
  for (const role of ROLES) {
    if (!(role in team)) continue;
    const inProgress = countInProgressForRole(board.active, role);
    if (inProgress <= 0) continue;
    const working = await countWorkingAgents(warRoom, role, 120);
    const hasFreshWorking = await hasFreshHeartbeatWithStatus(warRoom, role, 'working', 120);
    if (working === 0 && !hasFreshWorking) {
      actions.push(...(await releaseRoleClaims(warRoom, role, 'release_orphan')));
    }
  }
  return actions;
}

// ── Dispatch claims ───────────────────────────────────────────────────────────

async function dispatchForRole(
  warRoom: string,
  kb: WrKanbanBoard,
  role: string,
  team: Record<string, number>,
): Promise<string[]> {
  const capacity = team[role] ?? 0;
  if (capacity <= 0) return [];
  const live = await countLiveAgents(warRoom, role);
  if (live <= 0) return [];

  const actions: string[] = [];
  const effectiveCap = Math.min(capacity, live);

  for (let instance = 1; instance <= capacity; instance++) {
    const board = await loadBoard(warRoom);
    const active = board.active;
    const eligible = countEligibleClaims(kb, active, role);
    if (eligible.length === 0) break;
    const inProgress = countInProgressForRole(active, role);
    if (inProgress >= effectiveCap) break;

    try {
      const result = await pullSkill(warRoom, kb, role, instance, true);
      if (result.action === 'claimed') {
        actions.push(`auto_claim:${role}:${result.ticket_id}:${result.skill}`);
        await appendMetricsLog(warRoom, {
          event: 'auto_claim',
          agent_role: role,
          instance,
          ticket_id: result.ticket_id,
          skill: result.skill,
        });
      } else {
        break;
      }
    } catch {
      actions.push(`dispatch_failed:${role}:${instance}`);
      break;
    }
  }

  return actions;
}

async function dispatchClaims(
  warRoom: string,
  kb: WrKanbanBoard,
  team: Record<string, number>,
): Promise<string[]> {
  const actions: string[] = [];
  for (const role of ROLES) {
    if (role in team) actions.push(...(await dispatchForRole(warRoom, kb, role, team)));
  }
  return actions;
}

// ── Process action intents (manual mode) ──────────────────────────────────────

async function processActionIntents(warRoom: string, board: WrBoard): Promise<string[]> {
  if (!(await actionStateFileExists(warRoom))) return [];
  const intents = await loadActionIntents(warRoom);
  if (!intents.length) return [];
  const actions: string[] = [];
  for (const intent of intents) {
    const skipReason = checkIntentSkipReason(board, intent);
    if (skipReason) {
      await removeActionIntentEntry(warRoom, intent);
      actions.push(`skipped:${intent.ticket_id}:${intent.skill}:${intent.agent_role}:${skipReason}`);
    } else {
      actions.push(`queued:${intent.ticket_id}:${intent.skill}:${intent.agent_role}`);
    }
  }
  return actions;
}

function checkIntentSkipReason(board: WrBoard, intent: ActionIntentEntry): string | null {
  const found = findTicketInBoard(board, intent.ticket_id);
  if (!found) return 'ticket_not_found';
  if (found.bucket !== 'active') return 'ticket_not_active';
  const sp = found.ticket.skill_progress[intent.skill];
  if (sp?.execution_status === 'done') return 'skill_done';
  if (sp?.execution_status === 'in_progress') return 'skill_in_progress';
  return null;
}

// ── Role reports ──────────────────────────────────────────────────────────────

async function buildRoleReport(
  warRoom: string,
  kb: WrKanbanBoard,
  active: WrTicket[],
  team: Record<string, number>,
): Promise<Record<string, RoleReportEntry>> {
  const report: Record<string, RoleReportEntry> = {};
  for (const role of ROLES) {
    if (!(role in team)) continue;
    const capacity = team[role]!;
    const eligible = listEligiblePulls(kb, active, role);
    const inProgress = countInProgressForRole(active, role);
    const working = await countWorkingAgents(warRoom, role);
    const live = await countLiveAgents(warRoom, role);
    const unclaimed = Math.max(0, eligible.length - inProgress);
    report[role] = {
      team: capacity,
      live_agents: live,
      working_agents: working,
      in_progress: inProgress,
      eligible_claims: eligible,
      spawn_needed: Math.min(Math.max(0, capacity - live), unclaimed),
      dispatch_needed: Math.min(Math.max(0, live - working), unclaimed),
    };
  }
  return report;
}

async function buildManualRoleReport(
  warRoom: string,
  active: WrTicket[],
  team: Record<string, number>,
): Promise<Record<string, RoleReportEntry>> {
  const intentCounts = await countIntentsByRole(warRoom);
  const report: Record<string, RoleReportEntry> = {};
  for (const role of ROLES) {
    if (!(role in team)) continue;
    const capacity = team[role]!;
    const pending = intentCounts[role] ?? 0;
    const inProgress = countInProgressForRole(active, role);
    const working = await countWorkingAgents(warRoom, role);
    const live = await countLiveAgents(warRoom, role);
    const workUnits = pending + inProgress;
    const deadSlots = Math.max(0, capacity - live);
    report[role] = {
      team: capacity,
      live_agents: live,
      working_agents: working,
      in_progress: inProgress,
      eligible_claims: [],
      pending_intents: pending,
      spawn_needed: workUnits > 0 ? Math.min(deadSlots, workUnits) : 0,
      dispatch_needed: workUnits > 0 ? Math.min(Math.max(0, live - working), workUnits) : 0,
    };
  }
  return report;
}

async function computeSpawns(
  warRoom: string,
  roleReport: Record<string, RoleReportEntry>,
): Promise<SpawnEntry[]> {
  const spawns: SpawnEntry[] = [];
  for (const role of ROLES) {
    if (!(role in roleReport)) continue;
    const data = roleReport[role]!;
    const working = data.working_agents;
    for (let i = 0; i < data.spawn_needed; i++) {
      const instance = working + spawns.filter((s) => s.role === role).length + 1;
      const epoch = await registerExecutorSpawn(warRoom, role, instance);
      spawns.push({ role, instance, reason: 'pool_fill', spawn_epoch: epoch });
    }
  }
  return spawns;
}

// ── Spawn prompt generation ───────────────────────────────────────────────────

function isFixtureModeSync(engagementRoot: string): boolean {
  try {
    const text = readFileSync(path.join(engagementRoot, 'CONTEXT.md'), 'utf8');
    if (!/fixture_mode/i.test(text)) return false;
    return /fixture_mode[^\n]*\btrue\b/i.test(text);
  } catch {
    return false;
  }
}

function tryFileExistsSync(filePath: string): boolean {
  try {
    accessSync(filePath);
    return true;
  } catch {
    return false;
  }
}

function buildSpawnPromptText(
  engagementRoot: string,
  boardMode: string,
  role: string,
  instance: number,
  spawnEpoch?: number,
): string {
  const fixture = isFixtureModeSync(engagementRoot);
  const manual = boardMode === 'manual';

  const instLine = instance > 1 ? `  instance: ${instance}\n` : '';
  const seedPath = path.join(engagementRoot, 'AGENT-SEED.md');
  const firstRead =
    fixture && tryFileExistsSync(seedPath)
      ? `Read ${seedPath} FIRST (fixture mode — team member executor).\n\n`
      : 'Read practices/kanban/agents/reference/session-bootstrap.md FIRST.\n\n';

  const _cli = 'python practices/kanban/skills/abd-kanban/scripts/kanban_cli.py';

  let fixtureBlock = '';
  if (fixture) {
    if (manual) {
      fixtureBlock =
        '\nFIXTURE MODE + MANUAL BOARD: team member executor — NOT kanban-lead.\n' +
        'Do NOT run kanban_cli.py member pull to self-assign.\n' +
        'When operator has dropped work (action-state intent), start with:\n' +
        `  ${_cli} member intent --workspace ${engagementRoot} --role ${role}\n` +
        'Then apply fixture:\n' +
        `  ${_cli} member fixture --workspace ${engagementRoot} --role ${role}\n` +
        'On idle ticks: heartbeat ready — do not claim without a pending intent.\n' +
        'See agents/reference/skill-fixture-mode.md.\n';
    } else {
      fixtureBlock =
        '\nFIXTURE MODE (mandatory): You are a team member executor — NOT kanban-lead. ' +
        'Do NOT read practice skill SKILL.md or run scanners.\n' +
        'After kanban_cli.py member pull (or resume manual assignment), run:\n' +
        `  ${_cli} member fixture --workspace ${engagementRoot} --role ${role} --ticket <id> --skill <name>\n` +
        'Or if skill is already in_progress from manual drop:\n' +
        `  ${_cli} member fixture --workspace ${engagementRoot} --role ${role}\n` +
        'Then pull again. See agents/reference/skill-fixture-mode.md.\n';
    }
  }

  const epochLine =
    spawnEpoch != null
      ? `\nExecutor spawn_epoch: ${spawnEpoch} (registered by kanban-lead — your heartbeats must carry this epoch).\n`
      : '';

  const workLoop = manual
    ? `Arm AGENT_LOOP_TICK_${role} on turn 1 (30s, notify_on_output). ` +
      `MANUAL MODE: on each tick run \`${_cli} member intent\` when idle — ` +
      `never \`${_cli} member pull\`. Idle with no intent → \`${_cli} member ready\`.`
    : `Arm AGENT_LOOP_TICK_${role} on turn 1. ` +
      `Pull via \`${_cli} member pull\` (never hand-edit board.json).`;

  let prompt =
    `${firstRead}Bootstrap:\n  workspace: ${engagementRoot}\n  delivery-role: ${role}\n` +
    `${instLine}${epochLine}\n` +
    `Then read agents/${role}/AGENT.md, agents/reference/pull-model.md, ` +
    `agents/reference/work-queue.md, and reference/artifact-layout.md.\n` +
    `${workLoop}${fixtureBlock}` +
    '\nNever exit after one skill.';

  if (!fixture) prompt += ' Execute and review per executor-workflow.md.';
  return prompt;
}

// ── Core scan loops ───────────────────────────────────────────────────────────

interface ScanResult {
  cycle: number;
  actions: string[];
  roleReport: Record<string, RoleReportEntry>;
  spawns: SpawnEntry[];
  activeCount: number;
  backlogCount: number;
  boardMode: string;
}

async function runAutomaticScan(
  warRoom: string,
  kb: WrKanbanBoard,
  team: Record<string, number>,
  engagementRoot: string,
  session: Record<string, unknown>,
): Promise<ScanResult> {
  const cycle = (Number(session['cycle']) || 0) + 1;
  const actions: string[] = [];

  await writeHeartbeat(warRoom, 'kanban-lead', 'working', `Scan cycle ${cycle} started`);
  await syncBoardState(warRoom, kb);
  actions.push('board_sync');
  actions.push(...(await detectDuplicateIds(warRoom)));
  actions.push(...(await scatterPending(warRoom, kb, engagementRoot)));
  actions.push(...(await pullBacklog(warRoom, kb, team)));

  let board = await loadBoard(warRoom);
  let active = board.active;

  const stale = await releaseStaleReserved(warRoom, team);
  actions.push(...stale);
  const orphan = await releaseOrphanClaims(warRoom, team);
  actions.push(...orphan);
  if (stale.length || orphan.length) {
    board = await loadBoard(warRoom);
    active = board.active;
  }

  const dispatched = await dispatchClaims(warRoom, kb, team);
  actions.push(...dispatched);
  if (dispatched.length) {
    board = await loadBoard(warRoom);
    active = board.active;
  }

  const roleReport = await buildRoleReport(warRoom, kb, active, team);
  const spawns = await computeSpawns(warRoom, roleReport);
  for (const s of spawns) actions.push(`spawn_${s.role}_${s.instance}`);

  const backlogCount = board.backlog.length;
  await appendMetricsLog(warRoom, {
    event: 'scan_cycle',
    cycle,
    agent: 'kanban-lead',
    actions,
    active_tickets: active.length,
    backlog_count: backlogCount,
    eligible_by_role: Object.fromEntries(
      Object.entries(roleReport).map(([r, d]) => [r, d.eligible_claims.length]),
    ),
    spawn_needed_by_role: Object.fromEntries(
      Object.entries(roleReport).map(([r, d]) => [r, d.spawn_needed]),
    ),
  });

  await writeHeartbeat(warRoom, 'kanban-lead', 'working', `Scan cycle ${cycle}; spawns=${spawns.length}`);
  await writeLeadSession(warRoom, { ...session, cycle, last_scan: nowIso(), last_spawns: spawns });

  return { cycle, actions, roleReport, spawns, activeCount: active.length, backlogCount, boardMode: 'automatic' };
}

async function runManualScan(
  warRoom: string,
  kb: WrKanbanBoard,
  team: Record<string, number>,
  engagementRoot: string,
  session: Record<string, unknown>,
): Promise<ScanResult> {
  const cycle = (Number(session['cycle']) || 0) + 1;
  const actions: string[] = [];

  await writeHeartbeat(warRoom, 'kanban-lead', 'working', `Manual scan cycle ${cycle}`);

  for (const role of ROLES) {
    const purged = await purgeUnregisteredHeartbeats(warRoom, role);
    if (purged > 0) actions.push(`purged_ghost_heartbeats:${role}:${purged}`);
  }

  await syncBoardState(warRoom, kb);
  actions.push('board_sync');
  actions.push(...(await scatterPending(warRoom, kb, engagementRoot)));

  const boardAfterSync = await loadBoard(warRoom);
  actions.push(...(await processActionIntents(warRoom, boardAfterSync)));

  const boardFinal = await loadBoard(warRoom);
  const active = boardFinal.active;
  const backlogCount = boardFinal.backlog.length;
  const boardMode = boardFinal.board_mode ?? 'automatic';

  const roleReport = await buildManualRoleReport(warRoom, active, team);
  const spawns = await computeSpawns(warRoom, roleReport);
  for (const s of spawns) actions.push(`spawn_${s.role}_${s.instance}`);

  await appendMetricsLog(warRoom, {
    event: 'manual_scan_cycle',
    cycle,
    agent: 'kanban-lead',
    board_mode: boardMode,
    actions,
    eligible_by_role: Object.fromEntries(
      Object.entries(roleReport).map(([r, d]) => [r, d.eligible_claims.length]),
    ),
    spawn_needed_by_role: Object.fromEntries(
      Object.entries(roleReport).map(([r, d]) => [r, d.spawn_needed]),
    ),
  });

  await writeHeartbeat(warRoom, 'kanban-lead', 'working', `Manual scan cycle ${cycle}; spawns=${spawns.length}`);
  await writeLeadSession(warRoom, { ...session, cycle, last_scan: nowIso(), last_spawns: spawns });

  return { cycle, actions, roleReport, spawns, activeCount: active.length, backlogCount, boardMode };
}

// ── Deep copy helper ──────────────────────────────────────────────────────────

function deepCopyTicket(ticket: WrTicket): WrTicket {
  return {
    ...ticket,
    skill_progress: Object.fromEntries(
      Object.entries(ticket.skill_progress).map(([k, v]) => [k, { ...v }]),
    ),
    stage_history: ticket.stage_history ? [...ticket.stage_history] : [],
    lineage: [...ticket.lineage],
    scatter_to: ticket.scatter_to ? [...ticket.scatter_to] : [],
  };
}

// ── Public API ────────────────────────────────────────────────────────────────

export class LeadScanService {
  private readonly warRoomPromise: Promise<string>;

  constructor(private readonly engagementRoot: string) {
    this.warRoomPromise = resolveWarRoomDir(engagementRoot);
  }

  /** Run the full lead tick: scan + spawn prompts. Returns JSON-serialisable report. */
  async runTick(): Promise<LeadScanReport> {
    const warRoom = await this.warRoomPromise;
    const board = await loadBoard(warRoom);
    const config = await loadKanbanConfig(warRoom);
    const kbMap = parseKanbanBoards(config);
    const configName = board.stage_configuration ?? board.system_of_work ?? '';
    const kb = kbMap[configName];
    if (!kb) throw new Error(`Unknown stage_configuration: ${configName}`);

    const kbBlock = config.definitions[configName];
    const team = loadTeam(board, kbBlock);
    const session = await readLeadSession(warRoom);
    const isManual = board.board_mode === 'manual';

    const result = isManual
      ? await runManualScan(warRoom, kb, team, this.engagementRoot, session)
      : await runAutomaticScan(warRoom, kb, team, this.engagementRoot, session);

    const finalBoard = await loadBoard(warRoom);
    const boardMode = result.boardMode ?? finalBoard.board_mode ?? 'automatic';

    const dispatchSummary: Record<string, number> = {};
    for (const [role, data] of Object.entries(result.roleReport)) {
      if (data.dispatch_needed > 0) dispatchSummary[role] = data.dispatch_needed;
    }

    const spawnPrompts: SpawnPrompt[] = result.spawns.map((s) => ({
      role: s.role,
      instance: s.instance,
      prompt: buildSpawnPromptText(this.engagementRoot, boardMode, s.role, s.instance, s.spawn_epoch),
    }));

    return {
      cycle: result.cycle,
      timestamp: nowIso(),
      board_mode: boardMode,
      active_tickets: result.activeCount,
      backlog_count: result.backlogCount,
      roles: result.roleReport,
      spawns: result.spawns,
      actions: result.actions,
      must_spawn: result.spawns.length > 0,
      dispatch_summary: dispatchSummary,
      spawn_prompts: spawnPrompts,
      orchestrator_rule:
        'Dispatch already handled by scan (reserved skills for idle agents). ' +
        'If must_spawn is true, spawn every entry in spawn_prompts NOW ' +
        '(Task/subagent, run_in_background). Spawns are ONLY for dead/missing ' +
        'agent slots — live idle agents already got work dispatched.',
    };
  }

  /** Sync the board only (subset of run_tick). Used by fixture automation. */
  async syncBoard(): Promise<Record<string, unknown>> {
    const warRoom = await this.warRoomPromise;
    const board = await loadBoard(warRoom);
    const config = await loadKanbanConfig(warRoom);
    const kbMap = parseKanbanBoards(config);
    const configName = board.stage_configuration ?? board.system_of_work ?? '';
    const kb = kbMap[configName];
    if (!kb) throw new Error(`Unknown stage_configuration: ${configName}`);
    const synced = await syncBoardState(warRoom, kb);
    return synced as Record<string, unknown>;
  }

  /** Resolve the war room directory for this engagement root. */
  async getWarRoomDir(): Promise<string> {
    return this.warRoomPromise;
  }
}

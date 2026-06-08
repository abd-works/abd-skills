/**
 * HeartbeatService — read, write, and query heartbeat files.
 * Mirrors Python delivery_model.py heartbeat functions.
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { readJson, writeJson, nowIso } from './WarRoomService';

// ── File path helpers ────────────────────────────────────────────────────────

export function heartbeatPath(warRoom: string, role: string, instance = 1): string {
  if (instance <= 1) return path.join(warRoom, `heartbeat-${role}.json`);
  return path.join(warRoom, `heartbeat-${role}-${instance}.json`);
}

export async function listHeartbeatFiles(warRoom: string, role: string): Promise<string[]> {
  const primary = path.join(warRoom, `heartbeat-${role}.json`);
  const all: string[] = [];
  try {
    await fs.access(primary);
    all.push(primary);
  } catch { /* not present */ }
  try {
    const entries = await fs.readdir(warRoom);
    const escaped = role.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
    const pattern = new RegExp(`^heartbeat-${escaped}-(\\d+)\\.json$`);
    const numbered = entries
      .filter((e) => pattern.test(e))
      .sort()
      .map((e) => path.join(warRoom, e))
      .filter((p) => !all.includes(p));
    all.push(...numbered);
  } catch { /* dir unreadable */ }
  return all;
}

// ── Age computation ──────────────────────────────────────────────────────────

export async function readHeartbeatAge(filePath: string): Promise<number | null> {
  try {
    const raw = await readJson<Record<string, unknown>>(filePath);
    const ts = raw['ts'] as string | undefined;
    if (!ts) return null;
    const dt = new Date(ts);
    const age = (Date.now() - dt.getTime()) / 1000;
    return age < 0 ? null : age;
  } catch {
    return null;
  }
}

// ── Write ────────────────────────────────────────────────────────────────────

export async function writeHeartbeat(
  warRoom: string,
  role: string,
  status: string,
  note = '',
  instance = 1,
  spawnEpoch?: number,
): Promise<void> {
  const filePath = heartbeatPath(warRoom, role, instance);
  const payload: Record<string, unknown> = {
    agent_role: role,
    role,
    instance,
    ts: nowIso(),
    status,
  };
  if (spawnEpoch != null) payload['spawn_epoch'] = spawnEpoch;
  if (note) payload['note'] = note;
  await writeJson(filePath, payload);
}

// ── Spawn epoch management ───────────────────────────────────────────────────

const EXECUTOR_SPAWNS_FILE = 'executor-spawns.json';

async function loadExecutorSpawns(warRoom: string): Promise<Record<string, unknown>> {
  try {
    return await readJson<Record<string, unknown>>(path.join(warRoom, EXECUTOR_SPAWNS_FILE));
  } catch {
    return {};
  }
}

export async function registerExecutorSpawn(warRoom: string, role: string, instance = 1): Promise<number> {
  const spawns = await loadExecutorSpawns(warRoom);
  if (typeof spawns[role] !== 'object' || spawns[role] === null) spawns[role] = {};
  const roleBlock = spawns[role] as Record<string, unknown>;
  const instKey = String(instance);
  const currentBlock = roleBlock[instKey] as Record<string, unknown> | undefined;
  const current = Number(currentBlock?.['epoch'] ?? 0);
  const epoch = current + 1;
  roleBlock[instKey] = { epoch, registered_at: nowIso() };
  await writeJson(path.join(warRoom, EXECUTOR_SPAWNS_FILE), spawns);
  return epoch;
}

export async function readRegisteredSpawnEpoch(
  warRoom: string,
  role: string,
  instance = 1,
): Promise<number | null> {
  const spawns = await loadExecutorSpawns(warRoom);
  const roleBlock = spawns[role] as Record<string, Record<string, unknown>> | undefined;
  if (!roleBlock) return null;
  const block = roleBlock[String(instance)];
  if (!block) return null;
  const epoch = Number(block['epoch'] ?? 0);
  return epoch > 0 ? epoch : null;
}

export async function heartbeatMatchesRegisteredSpawn(
  warRoom: string,
  role: string,
  raw: Record<string, unknown>,
): Promise<boolean> {
  const instance = Number(raw['instance'] ?? 1);
  const registered = await readRegisteredSpawnEpoch(warRoom, role, instance);
  if (registered == null) return false;
  const hbEpoch = raw['spawn_epoch'];
  if (hbEpoch == null) return false;
  return Number(hbEpoch) === registered;
}

export async function purgeUnregisteredHeartbeats(warRoom: string, role: string): Promise<number> {
  let removed = 0;
  for (const filePath of await listHeartbeatFiles(warRoom, role)) {
    if (path.basename(filePath) === 'heartbeat-kanban-lead.json') continue;
    try {
      const raw = await readJson<Record<string, unknown>>(filePath);
      const matches = await heartbeatMatchesRegisteredSpawn(warRoom, role, raw);
      if (!matches) {
        await fs.unlink(filePath);
        removed++;
      }
    } catch {
      try { await fs.unlink(filePath); } catch { /* ignore */ }
      removed++;
    }
  }
  return removed;
}

// ── Agent liveness counts ────────────────────────────────────────────────────

export async function countLiveAgents(
  warRoom: string,
  role: string,
  staleSeconds = 120,
): Promise<number> {
  let live = 0;
  for (const filePath of await listHeartbeatFiles(warRoom, role)) {
    const age = await readHeartbeatAge(filePath);
    if (age == null || age > staleSeconds) continue;
    try {
      const raw = await readJson<Record<string, unknown>>(filePath);
      if (await heartbeatMatchesRegisteredSpawn(warRoom, role, raw)) live++;
    } catch { /* ignore */ }
  }
  return live;
}

export async function countWorkingAgents(
  warRoom: string,
  role: string,
  staleSeconds = 120,
): Promise<number> {
  let working = 0;
  for (const filePath of await listHeartbeatFiles(warRoom, role)) {
    const age = await readHeartbeatAge(filePath);
    if (age == null || age > staleSeconds) continue;
    try {
      const raw = await readJson<Record<string, unknown>>(filePath);
      if (raw['status'] === 'working' && (await heartbeatMatchesRegisteredSpawn(warRoom, role, raw))) {
        working++;
      }
    } catch { /* ignore */ }
  }
  return working;
}

export async function hasFreshHeartbeatWithStatus(
  warRoom: string,
  role: string,
  status: string,
  staleSeconds: number,
): Promise<boolean> {
  for (const filePath of await listHeartbeatFiles(warRoom, role)) {
    const age = await readHeartbeatAge(filePath);
    if (age == null || age > staleSeconds) continue;
    try {
      const raw = await readJson<Record<string, unknown>>(filePath);
      if (raw['status'] === status) return true;
    } catch { /* ignore */ }
  }
  return false;
}

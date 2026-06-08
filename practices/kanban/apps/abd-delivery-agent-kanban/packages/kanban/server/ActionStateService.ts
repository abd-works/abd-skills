/**
 * ActionStateService — read/write action-state.json (manual board drops).
 * Mirrors Python action_state.py.
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { readJson, writeJson, nowIso } from './WarRoomService';

export interface ActionIntentEntry {
  ticket_id: string;
  skill: string;
  agent_role: string;
  created_at: string;
}

const ACTION_STATE_FILE = 'action-state.json';

function actionStatePath(warRoom: string): string {
  return path.join(warRoom, ACTION_STATE_FILE);
}

export async function actionStateFileExists(warRoom: string): Promise<boolean> {
  try {
    await fs.access(actionStatePath(warRoom));
    return true;
  } catch {
    return false;
  }
}

export async function loadActionIntents(warRoom: string): Promise<ActionIntentEntry[]> {
  try {
    const raw = await readJson<{ intents?: unknown[] }>(actionStatePath(warRoom));
    const intents = Array.isArray(raw?.intents) ? raw.intents : [];
    return intents.filter(
      (e): e is ActionIntentEntry =>
        typeof e === 'object' &&
        e !== null &&
        typeof (e as Record<string, unknown>)['ticket_id'] === 'string' &&
        typeof (e as Record<string, unknown>)['skill'] === 'string' &&
        typeof (e as Record<string, unknown>)['agent_role'] === 'string',
    );
  } catch {
    return [];
  }
}

export async function removeActionIntentEntry(
  warRoom: string,
  intent: ActionIntentEntry,
): Promise<void> {
  const filePath = actionStatePath(warRoom);
  try {
    const raw = await readJson<{ intents?: ActionIntentEntry[] }>(filePath);
    const entries = Array.isArray(raw.intents) ? raw.intents : [];
    raw.intents = entries.filter(
      (e) =>
        !(
          e.ticket_id === intent.ticket_id &&
          e.skill === intent.skill &&
          e.agent_role === intent.agent_role
        ),
    );
    await writeJson(filePath, raw);
  } catch { /* no-op when file missing */ }
}

export async function findFirstIntentForRole(
  warRoom: string,
  role: string,
): Promise<ActionIntentEntry | null> {
  const intents = await loadActionIntents(warRoom);
  return intents.find((i) => i.agent_role === role) ?? null;
}

export async function countIntentsByRole(
  warRoom: string,
): Promise<Record<string, number>> {
  const intents = await loadActionIntents(warRoom);
  const counts: Record<string, number> = {};
  for (const intent of intents) {
    counts[intent.agent_role] = (counts[intent.agent_role] ?? 0) + 1;
  }
  return counts;
}

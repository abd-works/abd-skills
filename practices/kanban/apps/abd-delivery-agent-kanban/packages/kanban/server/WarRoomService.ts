/**
 * WarRoomService — resolves and reads/writes war-room files.
 *
 * The war-room directory is the kanban-board's planning folder on disk:
 *   <engagement-root>/docs/planning/kanban/              (primary)
 *   <engagement-root>/docs/planning/delivery-war-room/   (legacy)
 *
 * Mirrors Python delivery_model.war_room_dir() and persistence helpers.
 */

import { promises as fs } from 'node:fs';
import path from 'node:path';

// ── Raw war-room data types (mirror Python delivery_model dataclasses) ────────

export interface WrSkillProgress {
  execution_status: string;
  agent?: string | null;
  start?: string | null;
  end?: string | null;
  review_status?: string | null;
  reviewer?: string | null;
  review_start?: string | null;
  review_end?: string | null;
  notes?: string | null;
}

export interface WrStageHistoryEntry {
  stage: string;
  entered?: string | null;
  completed?: string | null;
  skipped?: boolean;
}

export interface WrTicket {
  ticket_id: string;
  lineage: string[];
  scope_level: string;
  stage: string;
  priority: number;
  created?: string | null;
  entered_stage?: string | null;
  completed_stage?: string | null;
  stage_history?: WrStageHistoryEntry[];
  skill_progress: Record<string, WrSkillProgress>;
  archived?: string | null;
  scatter_from?: string | null;
  scatter_to?: string[];
  notes?: string;
}

export interface WrBoard {
  schema?: string;
  synced_at?: string | null;
  stage_configuration?: string | null;
  system_of_work?: string | null;
  board_mode?: string;
  backlog: WrTicket[];
  active: WrTicket[];
  done: WrTicket[];
  archived: WrTicket[];
  team: Record<string, number>;
  [key: string]: unknown;
}

export interface WrSkillDef {
  skill: string;
  role: string;
  optional?: boolean;
  run_when?: string | null;
}

export interface WrStageDef {
  name: string;
  scope: string;
  stage_work_required: WrSkillDef[];
}

export interface WrKanbanBoard {
  name: string;
  label: string;
  stages: WrStageDef[];
}

export interface WrKanbanConfigEntry {
  label?: string;
  team?: Record<string, number>;
  stages: Array<{
    name: string;
    scope?: string;
    skills?: WrSkillDef[];
    stage_work_required?: WrSkillDef[];
  }>;
}

export interface WrKanbanConfig {
  definitions: Record<string, WrKanbanConfigEntry>;
}

// ── Path resolution ──────────────────────────────────────────────────────────

export async function resolveWarRoomDir(engagementRoot: string): Promise<string> {
  const primary = path.join(engagementRoot, 'docs', 'planning', 'kanban');
  try {
    await fs.access(primary);
    return primary;
  } catch { /* not found */ }
  const legacy = path.join(engagementRoot, 'docs', 'planning', 'delivery-war-room');
  try {
    await fs.access(legacy);
    return legacy;
  } catch { /* not found */ }
  return primary;
}

// ── Generic JSON I/O ─────────────────────────────────────────────────────────

export async function readJson<T = unknown>(filePath: string): Promise<T> {
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw) as T;
}

export async function writeJson(filePath: string, data: unknown): Promise<void> {
  await fs.writeFile(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

// ── Board I/O ────────────────────────────────────────────────────────────────

const DEFAULT_BOARD_MODE = 'automatic';

export async function loadBoard(warRoom: string): Promise<WrBoard> {
  const boardPath = path.join(warRoom, 'board.json');
  try {
    const raw = await readJson<WrBoard>(boardPath);
    raw.board_mode ??= DEFAULT_BOARD_MODE;
    raw.backlog = Array.isArray(raw.backlog) ? raw.backlog : [];
    raw.active = Array.isArray(raw.active) ? raw.active : [];
    raw.done = Array.isArray(raw.done) ? raw.done : [];
    raw.archived = Array.isArray(raw.archived) ? raw.archived : [];
    raw.team = typeof raw.team === 'object' && raw.team !== null ? raw.team as Record<string, number> : {};
    return raw;
  } catch {
    return {
      schema: 'abd-delivery-kanban/v2',
      synced_at: null,
      stage_configuration: null,
      board_mode: DEFAULT_BOARD_MODE,
      backlog: [],
      active: [],
      done: [],
      archived: [],
      team: {},
    };
  }
}

export async function saveBoard(warRoom: string, board: WrBoard): Promise<void> {
  board.synced_at = new Date().toISOString();
  board.board_mode ??= DEFAULT_BOARD_MODE;
  await writeJson(path.join(warRoom, 'board.json'), board);
}

// ── Kanban config (kanban.json / system-of-work.json) ───────────────────────

export async function loadKanbanConfig(warRoom: string): Promise<WrKanbanConfig> {
  for (const name of ['kanban.json', 'system-of-work.json']) {
    try {
      return await readJson<WrKanbanConfig>(path.join(warRoom, name));
    } catch { /* try next */ }
  }
  return { definitions: {} };
}

export function parseKanbanBoards(config: WrKanbanConfig): Record<string, WrKanbanBoard> {
  const out: Record<string, WrKanbanBoard> = {};
  for (const [name, block] of Object.entries(config.definitions)) {
    const stages: WrStageDef[] = (block.stages ?? []).map((stageRaw) => {
      const skillsRaw = stageRaw.stage_work_required ?? stageRaw.skills ?? [];
      return {
        name: stageRaw.name,
        scope: stageRaw.scope ?? 'all',
        stage_work_required: skillsRaw.map((s) => ({
          skill: s.skill,
          role: s.role,
          optional: Boolean(s.optional),
          run_when: s.run_when ?? null,
        })),
      };
    });
    out[name] = { name, label: block.label ?? name, stages };
  }
  return out;
}

export async function resolveKb(warRoom: string, board: WrBoard): Promise<WrKanbanBoard> {
  const config = await loadKanbanConfig(warRoom);
  const kbMap = parseKanbanBoards(config);
  const configName = board.stage_configuration ?? board.system_of_work ?? '';
  const kb = kbMap[configName];
  if (!kb) throw new Error(`Unknown stage_configuration: ${configName}`);
  return kb;
}

export function loadTeam(board: WrBoard, kbBlock?: WrKanbanConfigEntry): Record<string, number> {
  const teamRaw = (board.team as Record<string, unknown> | undefined) ??
    (board['wip_policy'] as Record<string, unknown> | undefined) ?? {};
  if (Object.keys(teamRaw).length > 0) {
    return Object.fromEntries(Object.entries(teamRaw).map(([k, v]) => [k, Number(v)]));
  }
  if (kbBlock?.team) {
    return Object.fromEntries(Object.entries(kbBlock.team).map(([k, v]) => [k, Number(v)]));
  }
  return {};
}

// ── Metrics log ──────────────────────────────────────────────────────────────

export async function appendMetricsLog(warRoom: string, event: Record<string, unknown>): Promise<void> {
  const logPath = path.join(warRoom, 'metrics-log.jsonl');
  event['timestamp'] ??= new Date().toISOString();
  try {
    await fs.appendFile(logPath, JSON.stringify(event) + '\n', 'utf8');
  } catch { /* best-effort */ }
}

// ── Time helper ──────────────────────────────────────────────────────────────

export function nowIso(): string {
  return new Date().toISOString();
}

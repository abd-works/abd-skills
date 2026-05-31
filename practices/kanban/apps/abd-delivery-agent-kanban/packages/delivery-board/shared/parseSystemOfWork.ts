import type { AgentRole, StageId, StageSkillRail, Team } from './kanbanBoard';
import { AGENT_ROLES, DEFAULT_TEAM, STAGE_ORDER } from './kanbanBoard';
import { skillFamilyFor, skillLabel } from './skillCatalog';

export interface StageWorkRequiredEntry {
  skill: string;
  role: string;
}

export interface StageDefinition {
  name: string;
  scope: string;
  optional?: boolean;
  skills?: StageWorkRequiredEntry[];
  stage_work_required?: StageWorkRequiredEntry[];
}

export interface KanbanConfigurationDefinition {
  label?: string;
  team?: Partial<Record<AgentRole, number>>;
  stages: StageDefinition[];
}

export interface KanbanConfiguration {
  schema: string;
  definitions: Record<string, KanbanConfigurationDefinition>;
}

function resolveSteps(stageDef: StageDefinition): StageWorkRequiredEntry[] {
  return stageDef.stage_work_required ?? stageDef.skills ?? [];
}

function stepsToSkills(steps: StageWorkRequiredEntry[]): StageSkillRail['skills'] {
  return steps.map((step) => ({
    skillId: step.skill,
    label: skillLabel(step.skill),
    family: skillFamilyFor(step.skill),
    role: step.role,
  }));
}

/**
 * Build stage skill rails from kanban.json.
 * Uses the named definition (or the first one) and maps its stages array
 * onto the canonical STAGE_ORDER.
 */
export function buildStageSkillRails(
  config: KanbanConfiguration,
  definitionName?: string | null,
): StageSkillRail[] {
  const defName = definitionName ?? Object.keys(config.definitions)[0] ?? '';
  const def = config.definitions[defName];
  if (!def) {
    return STAGE_ORDER.map((stage) => ({ stage, skills: [] }));
  }

  const stageMap = new Map<string, StageDefinition>();
  for (const stageDef of def.stages) {
    stageMap.set(stageDef.name, stageDef);
  }

  return STAGE_ORDER.map((stage) => {
    const stageDef = stageMap.get(stage);
    const steps = stageDef ? resolveSteps(stageDef) : [];
    if (!steps.length) {
      return { stage, skills: [] };
    }
    return { stage, skills: stepsToSkills(steps) };
  });
}

function definitionNameFromConfig(
  config: KanbanConfiguration,
  definitionName?: string | null,
): string {
  return definitionName ?? Object.keys(config.definitions)[0] ?? '';
}

/** Resolve team counts: kanban definition is canonical; board.json team overrides if present. */
export function resolveTeamFromConfig(
  config: KanbanConfiguration,
  definitionName?: string | null,
  boardTeam?: Team,
): NonNullable<Team> {
  const defName = definitionNameFromConfig(config, definitionName);
  const defTeam = config.definitions[defName]?.team ?? {};
  const merged = { ...DEFAULT_TEAM, ...defTeam, ...boardTeam } as NonNullable<Team>;
  for (const role of AGENT_ROLES) {
    merged[role] = merged[role] ?? DEFAULT_TEAM[role];
  }
  return merged;
}

/** Return active stages (those with at least one skill defined) for a definition. */
export function activeStagesFromConfig(
  config: KanbanConfiguration,
  definitionName?: string | null,
): StageId[] {
  const defName = definitionName ?? Object.keys(config.definitions)[0] ?? '';
  const def = config.definitions[defName];
  if (!def) return [];

  const activeNames = new Set(
    def.stages.filter((s) => resolveSteps(s).length > 0).map((s) => s.name),
  );
  return STAGE_ORDER.filter((s) => activeNames.has(s));
}

import { readdir, access } from 'node:fs/promises';
import { join } from 'node:path';
import {
  SkillCatalog as DomainSkillCatalog,
  type SkillFamily,
} from '@deliveryforge/kanban-shared';

export interface DiscoveredSkill {
  skillId: string;
  label: string;
  family: SkillFamily;
  role: string | null;
  sourcePath: string;
}

/**
 * Server-side SkillCatalog — extends domain SkillCatalog with filesystem discovery.
 * Scans the practices directory for SKILL.md files and the agents directory for
 * AGENT.md files to discover available skills and their agent role associations.
 * Supplements (never replaces) the hardcoded catalog in the shared layer.
 */
export class SkillCatalog extends DomainSkillCatalog {
  /**
   * Scan a practices root directory for SKILL.md files.
   * Returns skill IDs derived from folder names alongside their catalogued family/label.
   * Folders without a SKILL.md entry in the shared catalog are classified as
   * 'architecture-centric-engineering' by default (matching shared fallback).
   */
  static async discoverFromPractices(
    practicesRoot: string,
  ): Promise<DiscoveredSkill[]> {
    const skills: DiscoveredSkill[] = [];

    let topLevel: string[] = [];
    try {
      topLevel = await readdir(practicesRoot);
    } catch {
      return skills;
    }

    for (const practiceDir of topLevel) {
      const practicePath = join(practicesRoot, practiceDir);
      let skillDirs: string[] = [];
      try {
        skillDirs = await readdir(practicePath);
      } catch {
        continue;
      }

      for (const skillDir of skillDirs) {
        const skillPath = join(practicePath, skillDir);
        const skillMdPath = join(skillPath, 'SKILL.md');
        try {
          await access(skillMdPath);
        } catch {
          continue;
        }

        skills.push({
          skillId: skillDir,
          label: DomainSkillCatalog.label(skillDir),
          family: DomainSkillCatalog.familyFor(skillDir),
          role: null,
          sourcePath: skillMdPath,
        });
      }
    }

    return skills;
  }

  /**
   * Scan the agents directory for role folders with AGENT.md files.
   * Returns agent role names found on the filesystem.
   * Useful for validating that a registered role has a corresponding agent definition.
   */
  static async discoverAgentRoles(
    agentsRoot: string,
  ): Promise<Array<{ role: string; agentMdPath: string }>> {
    const agents: Array<{ role: string; agentMdPath: string }> = [];

    let roleDirs: string[] = [];
    try {
      roleDirs = await readdir(agentsRoot);
    } catch {
      return agents;
    }

    for (const roleDir of roleDirs) {
      const agentMdPath = join(agentsRoot, roleDir, 'AGENT.md');
      try {
        await access(agentMdPath);
        agents.push({ role: roleDir, agentMdPath });
      } catch {
        // no AGENT.md — skip
      }
    }

    return agents;
  }
}

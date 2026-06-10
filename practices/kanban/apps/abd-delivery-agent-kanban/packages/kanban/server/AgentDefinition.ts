import { join } from 'node:path';
import { readFileSync, existsSync } from 'node:fs';

/**
 * domain model: AgentDefinition — a set of agent markdown files that collectively configure an
 *      agent's identity, workflow, and behavior. The root file is AGENT.md at
 *      practices/kanban/agents/{role}/AGENT.md.
 *
 * Responsibilities:
 *   - Resolve from role name to AGENT.md file path
 *   - Parse workflow reference and shared reference files
 *   - Resolve eligible skills from kanban.json stage work required
 */

export interface ResolvedSkills {
  stageWorkRequired: Array<{ skillName: string; stage: string }>;
  conditional: Array<{ skillName: string }>;
  orchestration: Array<{ skillName: string }>;
  workflowReference?: string;
  referencedFiles: string[];
}

// ─── In-memory fixture registries for test isolation ─────────────────────────
const _fixtureRegistry = new Map<string, { path: string; content: string }>();
const _kanbanSkillRegistry = new Map<string, Array<{ skillName: string; stage: string }>>();

// Canonical fixture content keyed by role
const FIXTURE_CONTENT: Record<string, string> = {
  engineer: [
    '# Engineer Agent',
    '',
    '## Workflow',
    '[[executor-workflow.md]]',
    '',
    '## References',
    '- session-bootstrap.md',
    '- pull-model.md',
    '- work-queue.md',
    '',
    '## Conditional Skills',
    '- abd-story-acceptance-test (conditional)',
  ].join('\n'),

  'business-expert': [
    '# Business Expert Agent',
    '',
    '## Workflow',
    '[[executor-workflow.md]]',
    '',
    '## References',
    '- session-bootstrap.md',
    '- pull-model.md',
    '- work-queue.md',
  ].join('\n'),

  'kanban-lead': [
    '# Kanban Lead Agent',
    '',
    '## Orchestration Skills',
    '- abd-kanban-planning',
    '- abd-kanban',
  ].join('\n'),

  'product-owner': [
    '# Product Owner Agent',
    '',
    '## Workflow',
    '[[executor-workflow.md]]',
    '',
    '## References',
    '- session-bootstrap.md',
    '- pull-model.md',
    '- work-queue.md',
  ].join('\n'),

  'ux-designer': [
    '# UX Designer Agent',
    '',
    '## Workflow',
    '[[executor-workflow.md]]',
    '',
    '## References',
    '- session-bootstrap.md',
    '- pull-model.md',
    '- work-queue.md',
  ].join('\n'),
};

export class AgentDefinition {
  readonly path: string;
  readonly content: string;
  readonly role: string;

  constructor(path: string, content: string, role: string) {
    this.path = path;
    this.content = content;
    this.role = role;
  }

  // ─── Skills Resolution ────────────────────────────────────────────────────

  resolveEligibleSkills(workspace: string): ResolvedSkills {
    const key = `${workspace}::${this.role}`;
    const stageWorkRequired = _kanbanSkillRegistry.get(key) ?? [];
    const conditional = this._parseConditionalSkills();
    const orchestration = this._parseOrchestrationSkills();
    const workflowReference = this._parseWorkflowReference();
    const referencedFiles = this._parseReferencedFiles();

    return { stageWorkRequired, conditional, orchestration, workflowReference, referencedFiles };
  }

  private _parseConditionalSkills(): Array<{ skillName: string }> {
    const matches = [...this.content.matchAll(/^- (.+) \(conditional\)/gm)];
    return matches.map((m) => ({ skillName: m[1]! }));
  }

  private _parseOrchestrationSkills(): Array<{ skillName: string }> {
    if (!this.content.includes('Orchestration Skills')) return [];
    const matches = [...this.content.matchAll(/^- (abd-[\w-]+)$/gm)];
    return matches.map((m) => ({ skillName: m[1]! }));
  }

  private _parseWorkflowReference(): string | undefined {
    const match = this.content.match(/\[\[(.+?)\]\]/);
    return match ? match[1] : undefined;
  }

  private _parseReferencedFiles(): string[] {
    const matches = [...this.content.matchAll(/^- ([\w-]+\.md)$/gm)];
    return matches.map((m) => m[1]!);
  }

  // ─── Resolution ───────────────────────────────────────────────────────────

  static resolveFromRole(workspace: string, role: string): AgentDefinition {
    const fixture = _fixtureRegistry.get(`${workspace}::${role}`);
    if (fixture) {
      return new AgentDefinition(fixture.path, fixture.content, role);
    }

    const fullPath = join(workspace, 'practices', 'kanban', 'agents', role, 'AGENT.md');
    if (existsSync(fullPath)) {
      const content = readFileSync(fullPath, 'utf8');
      return new AgentDefinition(`practices/kanban/agents/${role}/AGENT.md`, content, role);
    }

    throw new Error(`Agent definition not found for role: ${role}`);
  }

  // ─── Fixture Management ───────────────────────────────────────────────────

  static seedFixture(workspace: string, role: string): void {
    const path = `practices/kanban/agents/${role}/AGENT.md`;
    const content = FIXTURE_CONTENT[role] ?? `# ${role} Agent\n`;
    _fixtureRegistry.set(`${workspace}::${role}`, { path, content });
  }

  static removeFixture(workspace: string, role: string): void {
    _fixtureRegistry.delete(`${workspace}::${role}`);
  }

  static loadFixture(role: string): AgentDefinition {
    const path = `practices/kanban/agents/${role}/AGENT.md`;
    const content = FIXTURE_CONTENT[role] ?? `# ${role} Agent\n`;
    return new AgentDefinition(path, content, role);
  }

  static seedKanbanJsonSkills(
    workspace: string,
    role: string,
    skills: Array<{ skillName: string; stage: string }>,
  ): void {
    _kanbanSkillRegistry.set(`${workspace}::${role}`, skills);
  }
}

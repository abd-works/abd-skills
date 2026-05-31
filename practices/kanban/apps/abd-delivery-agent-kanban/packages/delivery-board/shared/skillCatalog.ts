import type { SkillFamily } from './kanbanBoard';

const SKILL_FAMILY: Record<string, SkillFamily> = {
  'abd-convert-to-markdown': 'context-to-memory',
  'abd-semantic-context-chunker': 'context-to-memory',
  'abd-chunk-markdown': 'context-to-memory',
  'abd-embed-vectors': 'context-to-memory',
  'abd-search-memory': 'context-to-memory',
  'abd-domain-terms': 'domain-driven-design',
  'abd-ubiquitous-language': 'domain-driven-design',
  'abd-module-partition': 'domain-driven-design',
  'abd-class-responsibility-collaborator': 'domain-driven-design',
  'abd-scenario-walkthrough': 'domain-driven-design',
  'abd-object-model': 'domain-driven-design',
  'abd-bounded-context-map': 'domain-driven-design',
  'abd-information-architecture': 'user-experience-design',
  'abd-ux-mockup': 'user-experience-design',
  'abd-interface-design': 'user-experience-design',
  'abd-impact-mapping': 'user-experience-design',
  'abd-story-mapping': 'story-driven-delivery',
  'abd-thin-slicing': 'story-driven-delivery',
  'abd-acceptance-criteria': 'story-driven-delivery',
  'abd-specification-by-example': 'story-driven-delivery',
  'abd-acceptance-test-driven-development': 'story-driven-delivery',
  'abd-architecture-outline': 'architecture-centric-engineering',
  'abd-architecture-blueprint': 'architecture-centric-engineering',
  'abd-architecture-template': 'architecture-centric-engineering',
  'abd-architecture-reference': 'architecture-centric-engineering',
  'abd-service-level-objectives': 'architecture-centric-engineering',
  'abd-clean-code': 'architecture-centric-engineering',
  'mern-technical-architecture': 'architecture-centric-engineering',
  'abd-kanban': 'delivery',
  'abd-kanban-planning': 'delivery',
  'abd-kanban-repo': 'delivery',
  'kanban-estimation': 'delivery',
  'drawio-domain-sync': 'domain-driven-design',
  'drawio-story-sync': 'story-driven-delivery',
};

const LABEL_OVERRIDES: Record<string, string> = {
  'abd-convert-to-markdown': 'convert to markdown',
  'abd-semantic-context-chunker': 'context chunker',
  'abd-chunk-markdown': 'chunk markdown',
  'abd-embed-vectors': 'embed vectors',
  'abd-search-memory': 'search memory',
  'abd-class-responsibility-collaborator': 'CRC',
  'abd-acceptance-test-driven-development': 'ATDD',
  'abd-specification-by-example': 'spec by example',
  'abd-acceptance-criteria': 'acceptance criteria',
  'abd-information-architecture': 'information architecture',
  'abd-ux-mockup': 'ux mockup',
  'abd-interface-design': 'interface design',
  'abd-object-model': 'object model',
  'abd-clean-code': 'clean code',
  'abd-story-mapping': 'story mapping',
  'abd-thin-slicing': 'thin slicing',
  'abd-domain-terms': 'domain terms',
  'abd-ubiquitous-language': 'ubiquitous language',
  'abd-architecture-blueprint': 'architecture blueprint',
  'abd-architecture-template': 'architecture template',
  'abd-architecture-reference': 'architecture reference',
  'abd-service-level-objectives': 'service level objectives',
  'abd-scenario-walkthrough': 'scenario walkthrough',
  'abd-module-partition': 'module partition',
  'abd-impact-mapping': 'impact mapping',
  'abd-architecture-outline': 'architecture outline',
  'mern-technical-architecture': 'MERN stack',
  'abd-delivery-planning': 'delivery planning',
  'abd-kanban': 'kanban board',
  'abd-kanban-planning': 'kanban planning',
};

export function skillFamilyFor(skillId: string): SkillFamily {
  return SKILL_FAMILY[skillId] ?? 'architecture-centric-engineering';
}

export function skillLabel(skillId: string): string {
  if (LABEL_OVERRIDES[skillId]) return LABEL_OVERRIDES[skillId];
  return skillId
    .replace(/^abd-/, '')
    .replace(/-/g, ' ');
}

export function familyCssClass(family: SkillFamily): string {
  const map: Record<SkillFamily, string> = {
    'domain-driven-design': 'aad-fam-ddd',
    'user-experience-design': 'aad-fam-uxd',
    'story-driven-delivery': 'aad-fam-sdd',
    'architecture-centric-engineering': 'aad-fam-arc',
    delivery: 'aad-fam-delivery',
    'idea-shaping': 'aad-fam-idea',
    'context-to-memory': 'aad-fam-ctm',
  };
  return map[family];
}

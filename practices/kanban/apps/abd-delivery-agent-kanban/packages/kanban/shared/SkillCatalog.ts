import type { SkillFamily } from './Stage';

export class SkillCatalog {
  private static readonly FAMILY: Record<string, SkillFamily> = {
    'abd-convert-to-markdown': 'context-to-memory',
    'abd-semantic-context-chunker': 'context-to-memory',
    'abd-chunk-markdown': 'context-to-memory',
    'abd-embed-vectors': 'context-to-memory',
    'abd-search-memory': 'context-to-memory',
    'abd-domain-terms': 'domain-driven-design',
    'abd-domain-language': 'domain-driven-design',
    'abd-domain-partition': 'domain-driven-design',
    'abd-domain-model': 'domain-driven-design',
    'abd-domain-walk': 'domain-driven-design',
    'abd-domain-implementation': 'domain-driven-design',
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
    'abd-architecture-specification': 'architecture-centric-engineering',
    'abd-architecture-specification': 'architecture-centric-engineering',
    'abd-service-level-objectives': 'architecture-centric-engineering',
    'abd-clean-code': 'architecture-centric-engineering',
    'abd-architecture-code': 'architecture-centric-engineering',
    'abd-kanban': 'delivery',
    'abd-kanban-planning': 'delivery',
    'abd-kanban-repo': 'delivery',
    'kanban-estimation': 'delivery',
    'drawio-domain-sync': 'domain-driven-design',
    'drawio-story-sync': 'story-driven-delivery',
  };

  private static readonly LABELS: Record<string, string> = {
    'abd-convert-to-markdown': 'convert to markdown',
    'abd-semantic-context-chunker': 'context chunker',
    'abd-chunk-markdown': 'chunk markdown',
    'abd-embed-vectors': 'embed vectors',
    'abd-search-memory': 'search memory',
    'abd-domain-model': 'domain model',
    'abd-acceptance-test-driven-development': 'ATDD',
    'abd-specification-by-example': 'spec by example',
    'abd-acceptance-criteria': 'acceptance criteria',
    'abd-information-architecture': 'information architecture',
    'abd-ux-mockup': 'ux mockup',
    'abd-interface-design': 'interface design',
    'abd-domain-implementation': 'Class Model',
    'abd-clean-code': 'clean code',
    'abd-story-mapping': 'story mapping',
    'abd-thin-slicing': 'thin slicing',
    'abd-domain-terms': 'domain terms',
    'abd-domain-language': 'Domain Language',
    'abd-architecture-blueprint': 'architecture blueprint',
    'abd-architecture-specification': 'architecture template',
    'abd-architecture-specification': 'architecture reference',
    'abd-service-level-objectives': 'service level objectives',
    'abd-domain-walk': 'scenario walkthrough',
    'abd-domain-partition': 'module partition',
    'abd-impact-mapping': 'impact mapping',
    'abd-architecture-outline': 'architecture outline',
    'abd-architecture-code': 'MERN stack',
    'abd-delivery-planning': 'delivery planning',
    'abd-kanban': 'kanban board',
    'abd-kanban-planning': 'kanban planning',
  };

  private static readonly FAMILY_CSS: Record<SkillFamily, string> = {
    'domain-driven-design': 'aad-fam-ddd',
    'user-experience-design': 'aad-fam-uxd',
    'story-driven-delivery': 'aad-fam-sdd',
    'architecture-centric-engineering': 'aad-fam-arc',
    delivery: 'aad-fam-delivery',
    'idea-shaping': 'aad-fam-idea',
    'context-to-memory': 'aad-fam-ctm',
  };

  static familyFor(skillId: string): SkillFamily {
    return SkillCatalog.FAMILY[skillId] ?? 'architecture-centric-engineering';
  }

  static label(skillId: string): string {
    if (SkillCatalog.LABELS[skillId]) return SkillCatalog.LABELS[skillId];
    return skillId.replace(/^abd-/, '').replace(/-/g, ' ');
  }

  static familyCssClass(family: SkillFamily): string {
    return SkillCatalog.FAMILY_CSS[family];
  }
}

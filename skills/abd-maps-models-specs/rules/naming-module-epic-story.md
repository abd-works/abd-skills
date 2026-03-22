---
rule_id: naming-module-epic-story
phase_files:
  - story-map.md
  - domain-types.md
  - integrate.md
---

## Naming: modules, epics, stories

Names should read as **capabilities and behaviors**, not undifferentiated nouns. **Verb–noun** patterns at story level help reviewers see **who does what**.

**Story map** (`mm3_story_map.json`): epic and story names stay **behaviorally legible** when integrated with terms from Phase 2.
**Domain types** (`concepts[]` / module groupings): concept names are **domain language**, not framework jargon—avoid “Manager/Helper/Utils” unless the domain truly uses those words.
**Integrate:** when merging synonyms, **preserve** behavioral readability—integration is not a license to collapse distinct capabilities into one vague label.

Other skills may use stricter templates (e.g. interaction-tree prose). This rule **aligns intent** without copying their filenames or scanners.

**DO**

- Use **verb + noun** (or equivalent) for stories and behavior-led epic titles where the story map conventions allow.
- Keep concept names aligned to **domain vocabulary** from the corpus.

```json
{ "epic": "Capture customer order", "story": "Customer places order via API" }
```

**DON'T**

- Use the same string for module name, epic title, and story title **without** a deliberate reason, or use **generic placeholders** that hide missing decomposition.

```json
{ "epic": "Platform", "story": "Stuff" }
```

Opaque labels—**violation** (reviewer cannot infer behavior or ownership).

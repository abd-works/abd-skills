# Domain-driven design package

Domain glossary, language, model, specification, domain code; supporting DDD skills.

**Skills:** abd-domain-glossary, abd-domain-language, abd-domain-model, abd-domain-specification, abd-domain-code; supporting: abd-bounded-context-map, abd-ddd-design-building-blocks, abd-domain-walk

**Per skill:** `reference/` (all files, including `generate.md` when present), `templates/` (all files). Workflow: [`common/reference/skill-workflow.md`](../../common/reference/skill-workflow.md). Validation: [`common/reference/rule-checklist.md`](../../common/reference/rule-checklist.md) + practice [`validate-checklist.md`](reference/validate-checklist.md).

**Shared reference:** [`reference/domain-perspective.md`](reference/domain-perspective.md)

## Practice-wide references

Shared artifacts under [`references/`](references/):

| File | Purpose |
| --- | --- |
| [`references/domain-model-json.md`](references/domain-model-json.md) | `domain-model.json` schema (`abd-domain-model/v1`) |
| [`references/domain-model-template.json`](references/domain-model-template.json) | Empty scaffold template |
| [`references/domain-model-outline.json`](references/domain-model-outline.json) | Minimal valid example graph |
| [`references/domain-model-example.json`](references/domain-model-example.json) | Filled Check Resolution example |
| [`skills/supporting/domain-ops/`](skills/supporting/domain-ops/SKILL.md) | `domain-ops` — validate/read/write `domain-model.json` |

Conceptual reference under [`reference/`](reference/) (oo-concepts, domain-perspective).

## Deploy

```powershell
& scripts/deploy-skills.ps1 -Force
```

# Domain-driven design package

Domain glossary, language, model, specification, domain code; supporting DDD and diagram sync.

**Skills:** abd-domain-glossary, abd-domain-language, abd-domain-model, abd-domain-specification, abd-domain-code

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

---
rule_id: module-depends-on
phases: [step1]
order: 42
impact: MEDIUM
---

## Module dependency shape (`depends_on`)

After modules and their primary concepts are drafted, record **explicit dependencies** between modules so deepen, integrate, and scanners can order work and detect cycles.

**JSON shape (per dependency entry)**

Use this structure (field names may match your existing schema; align with `map-model-spec.json` conventions in the repo):

```json
"depends_on": [
  {
    "dependent_concepts": ["ConceptA", "ConceptB"],
    "module": "Other Module Name",
    "provides_concepts": ["BaseType", "SharedPolicy"],
    "reason": "Short text: why this module needs the other (cite chunk ids in narrative or in linked evidence)."
  }
]
```

**DO**

- List dependencies from **foundational / shared** modules toward **consumers** (the consumer module holds `depends_on` pointing to providers).
- Tie each dependency to **concepts** on both sides — not vague “uses other module.”
- Prefer **acyclic** graphs at scaffold time; if a cycle is real, document it in `open_questions` and justify.

**DON'T**

- Omit `depends_on` when two modules clearly share vocabulary — either merge synonyms in integrate or record the dependency.
- Use `depends_on` as a substitute for **duplicate concepts** — resolve duplicates per `no-duplicates.md` first.

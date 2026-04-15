---
rule_id: scaffold-concept-story-name-alignment
phases: [step1]
order: 45
impact: HIGH
---

## Scaffold: concepts and stories match exactly (100%)

**Non-negotiable.** Nothing in this rule is optional.

**Spine and breadth are understood through `concepts[]`, not through epic titles.** This rule complements **`domain-interaction-sync.md`** (later: bolded names in triggers/responses). At **scaffold** time, **`concepts[].name`** and **story text** ( **`epic.statement`** bold names, **`confirming_stories[]`** object nouns) are **one vocabulary**. They must **match 100%** — **the same identifier strings** as in **`concepts[].name`** for every domain object the epic or story names.

- **No synonyms** in story titles when the model uses a canonical **`concepts[].name`**.
- **No drift** (“close enough”, “related term”, informal shorthand).
- **No** domain object in **`confirming_stories`** or **`epic.statement`** that does not appear as **`name`** on a **`concepts[]`** row in that module (add the concept first, or fix the text).

If the source material uses two terms for one thing, resolve via **`classify-variants-before-modeling.md`** and/or record a single canonical **`concepts[].name`** plus an explicit note in **`open_questions`** — **not** two different strings in stories vs JSON.

**DO**

- For each **`**ConceptName**`** in **`epic.statement`**, assert **`ConceptName`** exists in **`module.concepts[].name`** (exact string match).
- For each **`confirming_stories[]`** entry, extract **object noun(s)** that refer to domain things; each must **equal** some **`concepts[].name`** in the same module (or document cross-module reference in **`open_questions`** with the **same** spelling as the owning module’s concept).
- If the story needs a new domain object, **add** **`concepts[]`** first (minimal row + chunk evidence), **then** write the story using **that exact `name`**.
- Run this check **after** epics and confirming stories exist, **before** finalize scanners.

**DON'T**

- Treat story titles or epic statements as free prose unrelated to **`concepts[].name`**.
- Use “matching or related” — **exact match** only, unless **`open_questions`** defines an alias table the whole spec follows.

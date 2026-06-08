---
scanner: plan-shape
---

# Rule: Plan has an explicit context inventory

**Scanner:** `scanners/plan-shape-scanner.py` â€” `PlanShapeScanner` (rule id `plan-has-context-inventory`)

The saved plan at `<workspace>/docs/kanban/agile-delivery-plan.md` must include a **context inventory** section that lists **Provided** context and **Missing** (or "not yet provided") context separately, and â€” when critical context is missing â€” the implications for run sequencing.

This exists so reviewers and downstream agents can see gaps immediately, instead of inferring from chat that a named platform / integration was "probably understood."

## DO

- Include a heading like `## Context inventory` (or `### Context Inventory`).
- Under it, list or table both **Provided context** (concrete inputs used â€” file paths, repo URLs, doc links, API refs, versions) and **Missing context** (explicit "not yet provided" flags).
- When critical context is missing, say what must happen before implementation runs (spike, doc pass, user drops links, clone repo).
- Use neutral wording for gaps â€” *not yet provided* â€” not "TBD" buried in prose.

## DON'T

- Treat a named platform (Foundry, Salesforce, your monolith, Acme API, etc.) as understood without any provided source.
- Skip the inventory because "the brief is short." A short brief means the inventory is a one-liner â€” still write it.
- Hide gaps inside run rationales instead of surfacing them in the inventory.

## Example (wrong)

```markdown
# Agile Delivery Plan

## Context Assessment
- Acme SSO integration, React front-end.

## Runs
| Run | Stages | ... |
| 1 | Discovery | ... |
```

(No context inventory section. Acme SSO is named but no source is declared and no "missing" flag appears.)

## Example (correct)

```markdown
## Context inventory

**Provided:**
- Brief: `docs/engagement/brief.md`
- React repo: `git@host:acme/frontend.git` (main @ 1a2b3c4)

**Missing (not yet provided):**
- Acme SSO OpenAPI or vendor docs
- Acme SSO sandbox credentials

**Implications:** Run 2 (first end-to-end slice) blocked until SSO docs are provided or a documentation-spike run lands first.
```

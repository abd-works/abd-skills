# Strategy: Legacy Migration

**When to use:** Replacing or rewriting an existing system; **legacy behavior is truth**. Backward compatibility, data migration, phased cutover.

**Typical scope:** Grouped by existing boundaries (endpoints, modules, domains).

**Related:** `brownfield-current-state.md` (mapping without replacing). `bug-fix.md` (single defect on existing).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Context (optional) | all | convert-to-markdown, semantic-context-chunker, chunk-markdown, embed-vectors |
| Shaping | all | module-partition, architecture-outline, story-mapping (from existing system), thin-slicing |
| Discovery | increment | domain-terms, architecture-blueprint, information-architecture (optional) |
| Exploration | increment | domain-language, acceptance-criteria (legacy behavior is spec), ux-mockup (optional), architecture-template (conditional — skip when mechanisms exist) |
| Specification | sprint | domain model, spec-by-example (concrete legacy values), interface-design (optional), architecture-reference (conditional) |
| Engineering | sprint | class-model (BE), ATDD (PO, tests pass on OLD system first), clean-code (EN, new implementation) |

### Context stage (when to include)

Include context stage when legacy material is in non-markdown formats (PDF, PPTX, DOCX, runbooks), there are many files to index, or agents need RAG during later stages. Skip when the codebase and existing tests are the only sources and are already readable.

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Shaping (all) → Discovery (increment) | One increment per module/boundary from partition. Order by migration risk. |
| Exploration (increment) → Specification (sprint) | Group endpoints/stories by data domain. 3-4 per sprint. |

### Increment ordering (migration-safe)

1. **Simplest boundary** — prove the migration pattern on lowest risk
2. **Dependencies** — modules that other modules depend on
3. **Remaining** — by effort/value

---

## JIT policy

- Scatter all increments after shaping (boundaries are known from partition)
- Scatter sprints JIT — only current increment
- After first module proves pattern: scatter next 2 increments

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | First module (prove migration pattern) |
| Per story | Tests pass on old system before new implementation |
| Per module | After first module: review against patterns |
| Per sprint | Systematic rollout for remaining modules |

---

## Key constraints

- Legacy behavior **is** the spec — do not invent new behavior during migration.
- Tests must pass on the **old** system first (characterization), then on the new system.
- Data migration and backward compatibility are first-class concerns in every increment.
- Forward-only changes (new features) go in separate increments after migration proves.
- Wrong map means wrong migration — confirm contracts before build.

---

## AI error rate adjustment

- First module at per-skill (migration pattern is critical to get right)
- If pattern proves clean: expand to per-sprint for subsequent modules
- If data mapping errors appear: shrink to per-endpoint scope

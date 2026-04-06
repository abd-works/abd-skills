<!--
  OOAD STRATEGY — workspace template
  Copy to: <workspace>/abd-ooad/strategy.md
  Canonical filename: strategy.md (lowercase).
-->

# OOAD Strategy — {{project_name}}

**Progress and ticks (only place for checkboxes):** [`abd-ooad/progress/`](abd-ooad/progress/) — see **`library/base/checklist.md`** and **`library/strategy-execution-and-checklists.md`**.

---

## Modeling scope

*What slices of the source you will model in this pass — be explicit so phases stay aligned.*

- **Primary focus:** {{e.g. Chapter 5 only; anchors Payment + Ledger; module `billing/`}}
- **In scope (bullets):** {{sections, files, anchors, or “full spec after scan”}}
- **Out of scope for now:** {{explicit deferrals}}
- **Granularity rule:** {{e.g. one chapter at a time; or full vertical slice on anchor X}}

---

## Execution plan (normative)

*Ordered list of **phases** (use **`skill-config.json` → `phase_files`** slugs) and, for each, **what context** you apply. This is the contract: **no checkboxes here** — live ticks go in **`progress/strategy-run-checklist.md`**, which you keep in sync with this section.*

1. **domain-scan** — scope: {{e.g. whole source map; or Ch.5 only}}
2. **nouns-verbs-rules-and-states** — scope: {{e.g. Ch.5}}
3. **raw-candidate-list** — scope: {{same or narrower}}
4. {{add or remove rows; reorder as needed — e.g. “run next three steps per chapter” means repeat blocks of 3 phases for Ch.5, then Ch.6}}

*Examples:*

- *Single slice:* domain-scan → nouns-verbs → … → validate-with-scenarios — all on **anchor X** only.
- *Chapter ladder:* for each chapter: nouns-verbs → raw-candidate-list → thing-vs-data — then next chapter.
- *Full pipeline once:* list every phase from `domain-scan` through `model-in-layers` on **full** scope.

When this plan changes, update **`strategy-run-checklist.md`** under `progress/` to match (same order and scope notes), then log the pivot under *Ongoing strategic decisions*.

---

## Approach going forward

*Short narrative — priorities and “why this order,” not a recap of the scan (that lives in `domain-scan-results.md`).*

- **Next focus:** {{subsystem, chapter, or risk to resolve first}}
- **Order / sequencing:** {{what before what; what is explicitly deferred}}
- **Defer / skip:** {{later phases, out-of-scope for now}}

---

## Ongoing strategic decisions

*Short dated log when you pivot, unblock, or change sequencing.*

### {{YYYY-MM-DD}}
- {{What changed and why}}

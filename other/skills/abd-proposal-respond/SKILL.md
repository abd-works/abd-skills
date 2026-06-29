---
name: abd-proposal-respond
catalogue_one_liner: >-
  RFP and proposal response: ingest to memory (abd-context-to-memory), strategy, batched Q&A with RAG.
description: >-
  Respond to client proposals (RFP, Q&A, requirements) by converting materials
  to memory, creating a response strategy, and answering questions iteratively.
  Depends on abd-context-to-memory for RAG. Use when responding to proposals,
  creating response plans, answering RFP questions, or iterating on proposal strategy.
---
# abd-proposal-respond

## Purpose

Respond to client proposals by converting materials to memory, creating a response strategy, and answering questions in small batches. Uses abd-context-to-memory for RAG. Same iterate-on-strategy pattern as abd-shaping.

---

## Output file

**Deliverables folder:** see `../common/reference/skill-workflow.md` — Output file resolution.

**File name:** `response/strategy.md` for the strategy; answer files per batch in `response/`. Add an `Accelerator Table.md` when answers reference appendix items.

---

## Agent Instructions

> **MANDATORY — read `../common/reference/skill-workflow.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read every file in **`rules/`** — `response-format.md` (structure, lead paragraph, bullet prose, labels, tailoring) and `answer-from-memory.md` (RAG-first answering).

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Operations:**

| Operation | Trigger |
|-----------|---------|
| `create_strategy` | "Create strategy," "propose response plan," "analyze and plan" |
| `answer_questions` | "Answer questions," "answer a few," "next batch" |
| `improve_strategy` | "Correct," "fix that," "wrong" |
| `proceed_slice` | "Proceed," "expand," "next slice" |

**Process:**

1. **Setup** — Convert proposal to memory (`index_memory.py --path <proposal_source>`); create response folder (`setup_response.py --proposal <folder>`); symlink.
2. **Strategy first** — Analyze documents; propose response plan; save to `response/strategy.md`. Get approval.
3. **Answer a few questions ONLY** — 3–5 per batch; use `search_memory.py` for RAG; get approval.
4. **Accelerators** — When answers reference `*See Appendix X (Name)*`, define and accumulate in the **Accelerator Table** (add/update row: slide file, numbers, URL). When done, run `build_appendix_deck.py` to assemble the appendix deck.
5. **Iterate** — Corrections → add DO/DO NOT to strategy; re-run or proceed.

**Scripts:**

- `setup_response.py --proposal <folder>` — Create response folder and symlink
- `build_appendix_deck.py --table <Accelerator_Table.md> [--output <path>]` — Assemble appendix deck from Accelerator Table

### 3. Validate

Emit per-rule verdicts per `../common/reference/skill-workflow.md`.

---

## Validate

**Goal:** Inspect what was built — read artifacts as reviewers.

- **Response format** — lead paragraph + bulleted list with bold labels + source references; consistent structure per question.
- **Memory-backed** — answers cite retrieved chunks; no general-knowledge answers when proposal content is indexed.
- **Strategy corrections** — every "correct" adds DO/DO NOT to strategy with wrong/correct examples; not just inline fix.
- **Accelerator table** — every `*See Appendix X*` reference has a corresponding row in the table.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---

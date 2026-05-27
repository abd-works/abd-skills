---
name: abd-query-practice-sources
description: >-
  Pull defensible excerpts from the content hub so a new practice can cite real sources,
  not guesswork: one auditable log of what you kept and why it matters.
---
# abd-query-practice-sources

## Purpose

Before anyone writes **instructions** or **rules** for a practice, you need a **single, honest record** of what the hub actually contains on that topic: what you read, where it lives, and how each piece supports the skill. This skill is about **finding and recording** that evidence so later work stays **anchored** to real content.

## When to use

- You are defining a **new or revised** practice under **`agilebydesign-skills/skills/<skill-name>/`** and need **hub-backed** material.
- You must **not** treat model memory or paraphrase as a substitute for **logged** excerpts and locations.
- You want **scoped** search (folders, memory roots) and queries that **match** how the hub is already indexed.

## Not in this pass

**Re-chunking** or designing a **chunking strategy** for the hub. The index is fixed; you **retrieve** and **record**, you do not reshape the corpus here.

**Target package — authoring is later:** Do **not** create or edit the practice skill's **`rules/*.md`**, **`SKILL.md`**, **`templates/`**, or run **`bundle_rules_into_skill_md.py`** here. Those belong to **abd-author-practice-skill**. This pass may create **`skills/<skill-name>/`** and **`inputs/`** and must finish **`inputs/abd-answers-retrieval.md`**. *Relevance* tag **`rule`** means "this chunk will support a future **rules/** file" — it is **not** permission to write **`rules/`** during retrieval.

## Output log (canonical)

**Path (target skill):** `skills/<skill-name>/inputs/abd-answers-retrieval.md`

Create **`skills/<skill-name>/`** and **`inputs/`** if they do not exist (the practice package root under **agilebydesign-skills**). One **shared log** per skill package (not a generic scratch pool). Optionally copy **`templates/inputs-readme.md`** from **this** skill to **`inputs/README.md`**.

**Every kept chunk** must be recorded so **authoring does not need a second query**:

| Field | Required |
| --- | --- |
| **Verbatim body** | Yes — under **`### Kept chunk N`**, paste the **full** chunk text you will use (fenced block). Prefer the pipeline markdown file for that slide; `npm run rag:query` **`bodyPreview`** only when you will replace it if truncated. |
| **Source / title** | Yes — chunk title, `sourceUrl`, or hub path from the chunk header |
| **Relevance** | Yes — one of: **`rule`**, **`core_concept`**, **`example`**, **`procedure`**, **`glossary`**, **`diagram_ref`**, **`other`** |
| **Relevance note** | Yes for **`other`**; otherwise short (why this chunk supports the skill) |
| **Query** | Yes — which query string produced this hit |
| **Rank** | Recommended — 1-based rank in result set or score if present in JSON |

A **summary-only table** without fenced bodies is **not** enough.

The log file itself should be **data only** (kept chunks and optional JSON trail). Do **not** paste long format instructions or a **Run parameters** table into **`inputs/abd-answers-retrieval.md`** — how to fill the log is **this SKILL.md** and the thin **`templates/abd-answers-retrieval-input.md`** starter.

Start from **`templates/abd-answers-retrieval-input.md`** (copy into the target skill and fill).

### Relevance tags (use consistently)

- **rule** — normative constraint / DO / DON'T for **rules/** or Validate
- **core_concept** — definitions and teaching points for **Purpose** / **Core concepts**
- **example** — samples for **Example**, templates, or manual figures
- **procedure** — steps for **Agent instructions** / **Build**
- **glossary** — terms / vocabulary
- **diagram_ref** — visuals to mirror in a **manual**
- **other** — rare; explain in **Relevance note**

## Core concepts

- **Audit trail** — Anything later presented as **from the hub** should trace to a **row** in this file (**#** + **source location**).
- **Retrieve, not re-chunk** — Tune **queries** and **k**; do not invent a new chunking plan for abd-answers here.

Apply the **bundled rules** at the end of this file when deciding what to keep and how to record it.

## Retrieval workflow

1. **Decompose the skill topic** into 3-7 **short queries** (phrases the hub would index), not one vague sentence.
2. **Map to folders** — set `--folders` when the engagement names hub paths (comma-separated, forward slashes).
3. **Choose k** — start **8**; **12-15** if thin; lower if noisy.
4. **Match indexed chunks** — phrase queries so hits align with **titles** and **bodyPreview** in results.

## Run queries

After steps **1–4**, from the **abd-answers** repository root:

```bash
npm run rag:query -- "your primary query" --k 8
```

**Scoped:**

```bash
npm run rag:query -- "your query" --folders "path/one,path/two" --k 10
```

Optional: `--memory-root-id "<id>"` or `--rag-ref pinecone://...` per abd-answers docs.

5. **Write `inputs/abd-answers-retrieval.md`** — required. Ensure the target **`skills/<skill-name>/inputs/`** folder exists. Start from **`skills/abd-practice-skill-builder/abd-query-practice-sources/templates/abd-answers-retrieval-input.md`** (copy into the target **`inputs/`** if the log file is new). For **each kept chunk**, add **`### Kept chunk N`** with the metadata fields in **Output log** above and paste the **verbatim** body in a fenced block. Merge all queries into **one** file; **dedupe** identical **Source location** / slide bodies.

## Validate

**Goal:** Treat the log as a reviewer would before any authoring depends on it.

- **Exists and complete** — **`inputs/abd-answers-retrieval.md`** is present; each **Kept chunk** has metadata and a **fenced verbatim body** (not summary-only).
- **Coverage** — At least one chunk supports each major **SKILL.md** section you plan to ship (or a documented gap elsewhere).
- **Rules trace** — You do not plan **normative** **rules/** bullets without a supporting **`rule`** or **`procedure`** chunk.
- **Honesty** — Each chunk records **Query** (and similarity/rank when available); obvious **dupes** merged by **Source location** / body.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Hub retrieval discipline

**Scanner:** Manual review

#### DO

- **Log what you keep** — If you would quote or paraphrase the hub in a rule, that text appears under **`### Kept chunk N`** in **`inputs/abd-answers-retrieval.md`** as a **verbatim** fenced body (full pipeline markdown when available), not only a summary table cell — so authoring does not need a **second** query.
- **Dedupe** — Same chunk hit twice → one **Kept chunk** (same **Source location** / slide body).
- **Tag honestly** — **Relevance** reflects how you will **use** the chunk (rule vs example vs diagram_ref), not a generic **`other`** to skip thinking.

#### DO NOT

- **Invent hub claims** with no matching **Kept chunk** (verbatim body) in the retrieval log.
- **Design a chunking strategy** for the hub in this step; only **query** and **record**.
- **Author the target practice package** in this step — no **`rules/*.md`**, **`SKILL.md`**, **`templates/`**, or **`bundle_rules_into_skill_md.py`** on the target. **`Relevance: rule`** means the chunk will back a rule **later** in **abd-author-practice-skill**, not "create **rules/** now."

**Source:** Practice-skill builder convention (abd-query-practice-sources).
<!-- execute_rules:bundle_rules:end -->

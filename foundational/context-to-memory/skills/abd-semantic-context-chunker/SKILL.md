---
name: abd-semantic-context-chunker
description: >-
  Index scattered source content by the kind of context it provides — Story, Domain,
  Architecture, UX — so you know what you have before deeper analysis begins.
  Use when you have lots of files from many sources and need a coverage index,
  when pointing downstream work at the right source material, or when you need
  context-aware retrieval rather than generic keyword search.
---
# abd-semantic-context-chunker

## Purpose

Scan all source content, tag every piece by the kind of context it provides (Story, Domain, Architecture, UX), and produce a coverage index showing what you have across all four views — before any deeper analysis begins.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** One chunk file per segment (with YAML front matter) plus one `context-chunking-report.md` coverage report.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what the context index is, the four views, hierarchical tags, chunking threshold, coverage report.
- **`references/four-view-taxonomy.md`** — the full tag vocabulary for all four views.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Build steps:**

1. **Scan the source folder.** List all source content — markdown files from abd-convert-to-markdown, code files, specs, notes. Measure each file's size.

2. **Split large files when needed.** Files over roughly 1,500 characters often cover multiple topics. Split at heading boundaries (`##` preferred, then `###`). Aim for 800–3,000 characters per segment. Smaller files pass through as-is. Assign `chunk_id` as `source-file__chunk_NN` and record `section_path`.

3. **Tag every piece by context type.** Read each segment and assign `primary_views` (story, domain, architecture, ux). Fill orientation-level tags using the vocabulary in `references/four-view-taxonomy.md`. Stay at **broad tagging altitude** — identify the capability area, the module, the platform, the screen — not individual stories, structured terms, component interactions, or UI controls.

4. **Write chunk files with front matter.** Save each chunk with YAML front matter following **`templates/tagged-chunk.md`**: `chunk_id`, `source_file`, `section_path`, `chunk_size_chars`, `primary_views`, `tags`, `evidence_type`.

5. **Generate the coverage index.** Produce a report following **`templates/context-chunking-report.md`**: group by view, then by top hierarchy level. List untagged items at the end.

**Before:** `abd-convert-to-markdown`
**After:** `abd-chunk-markdown` or view-specific downstream analysis (story mapping, domain modeling, architecture analysis, UX design)

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-semantic-context-chunker \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect the tagged output and coverage index as a reviewer.

- **Every piece of content** has YAML front matter with `chunk_id`, `source_file`, non-empty `primary_views`, and at least one view's hierarchical tags.
- **Tags use only values** from `references/four-view-taxonomy.md` — no invented tag names.
- **Tags stay at orientation level** — epics/actors for Story, modules/abstractions for Domain, platforms/components for Architecture, screens/regions for UX. Downstream analysis does the decomposition.
- **Pass-through files** (< ~1,500 chars) were not split; they have view tags but no chunk subdivision.
- **The coverage index** accounts for every source file and every tagged piece — totals match, no orphans.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---

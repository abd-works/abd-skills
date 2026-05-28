---
name: abd-semantic-context-chunker
description: >-
  Index scattered source content by the kind of context it provides — Story, Domain, Architecture, UX — so you know what you have before deeper analysis begins.
---
# abd-semantic-context-chunker

## Purpose

Engagements accumulate context from many places — requirements documents, code repositories, design files, meeting notes, technical specs — and nobody knows what they actually have until someone reads it all. This skill scans the full corpus, tags every piece by the kind of context it provides — Story, Domain, Architecture, UX — and produces a coverage index so teams and agents know what evidence exists and where the gaps are, before any deeper analysis begins.

## When to use

Load this skill when **any** of the following apply:

- You have **lots of files or content from many sources** — documents, code, specs, notes — and need to know **what kind of context you actually have** before starting delivery work.
- You want a **coverage index** that shows which views (Story, Domain, Architecture, UX) are well-covered and where the gaps are, so you can prioritize what to read or request.
- You are about to start **story mapping, domain modeling, architecture analysis, or UX design** and want to **point that work at the right source material** instead of dumping everything in.
- Content has been converted to markdown and you need **context-aware retrieval** rather than generic keyword search.

## Core concepts

### Context index

The primary output is **tagged, chunked content** — every piece of source material broken into retrieval-sized segments and labelled by the kind of context it provides. The **context index** is the companion report that shows what you ended up with: "31 pieces of domain context, 23 story, 12 architecture, 8 UX — and here is exactly where each one lives." The chunks feed downstream retrieval; the index tells you what you have and where the gaps are.

### Four views

Every piece of source content provides context for at least one of four views:

- **Story** — what users and systems do: interactions, behaviors, processes, journeys, acceptance criteria, scenarios, flows.
- **Domain** — what the system knows and enforces: business vocabulary, data structures, rules, invariants, entity relationships, state transitions.
- **Architecture** — what the system is made of: components, platforms, technology choices, deployment, integration points, cross-cutting concerns, patterns, non-functional targets.
- **UX** — what the user sees and touches: screens, layouts, navigation, controls, wireframes, mockups, accessibility.

A single chunk can inform **multiple views** — for example, a paragraph describing an order submission form touches both Story (the user journey) and UX (the form layout).

### Hierarchical tags

Each view has a small set of tags that locate content at a **broad orientation level** — enough to know what area it belongs to, not enough to constitute full modeling. Story tags identify capability areas (epics) and actors, not individual stories. Domain tags identify modules and key abstractions, not every term and relationship. Architecture tags identify platforms, components, and mechanism types. UX tags identify screens and regions. The full vocabulary lives in **`references/four-view-taxonomy.md`**. Deeper structuring — decomposing epics into stories, extracting domain terms, mapping component interactions, specifying UI controls — is what downstream analysis is for, not this tagging pass.

### Chunking (when needed)

Most files are tagged as-is. When a file is large enough that it covers multiple topics (roughly over 1,500 characters), it gets split into 1–2 page segments so each piece can be tagged independently. Smaller files pass through intact — they still receive view tags but are not subdivided. The chunking is a means to accurate tagging, not the point of the skill.

### Coverage report

After chunking and tagging, the skill produces a report that groups every chunk by view, then by hierarchy level. This makes gaps visible: if the Story view shows no chunks under a known epic, the source corpus is missing behavioral content for that area. The report also lists pass-through files and any chunks that could not be tagged.

## Build

**Goal:** Scan all source content, tag every piece by the kind of context it provides, and produce a coverage index showing what you have across all four views.

1. **Scan the source folder.** List all source content — markdown files from **abd-convert-to-markdown**, code files, specs, notes, anything that has been collected. Measure each file's size and note it for the report.

2. **Split large files when needed.** Files over roughly 1,500 characters often cover multiple topics. Split those at heading boundaries (`##` preferred, then `###`) so each piece can be tagged independently. Aim for segments between 800 and 3,000 characters. Smaller files pass through as-is. Assign each segment a `chunk_id` in the form `source-file__chunk_NN` and record its `section_path` (the heading trail from the source).

3. **Tag every piece by context type.** Read each segment's content and assign one or more entries to `primary_views` (story, domain, architecture, ux). Then fill the orientation-level tags for each assigned view using the vocabulary in **`references/four-view-taxonomy.md`**. Stay at a **broad tagging altitude** — identify the capability area, the module, the platform, the screen — not individual stories, structured terms, component interactions, or UI controls. That detail is what downstream analysis produces. When the engagement already has project artifacts, use their names as anchors to keep tags consistent.

4. **Write chunk files with front matter.** Save each chunk to the output folder with YAML front matter following the shape in **`templates/tagged-chunk.md`**. Front matter includes `chunk_id`, `source_file`, `section_path`, `chunk_size_chars`, `primary_views`, `tags` (nested by view), and `evidence_type`.

5. **Generate the coverage index.** Produce a report following **`templates/context-chunking-report.md`**. Group all tagged content by view, then by the top hierarchy level within each view (epic for Story, module for Domain, depth for Architecture, screen for UX). List untagged items at the end. This index is the deliverable — it tells you what context you have and where the gaps are.

6. **Review against the rules.** Walk each bundled rule (chunk size threshold, view tagging required, tag depth accuracy) and verify the output passes. Fix any violations before declaring done.

- **Outputs:** One chunk file per segment (with YAML front matter) plus one coverage report. Pass-through files get a single front-matter-only companion or are listed in the report with their tags.
- **While writing:** Use only tag values from `references/four-view-taxonomy.md`. When a chunk's content does not clearly fit any view, tag it as the closest match and note the uncertainty in the report's untagged section.

## Validate

**Goal:** Inspect the tagged output and coverage index as a reviewer — check completeness, tag quality, and report accuracy.

- **Every piece of content** (file or segment) has YAML front matter with `chunk_id`, `source_file`, `primary_views` (non-empty list), and at least one view's hierarchical tags.
- **Nothing is untagged** — every item has at least one `primary_views` entry.
- **Tags use only values** from `references/four-view-taxonomy.md` — no invented tag names.
- **Tags stay at orientation level** — epics and actors for Story, modules and key abstractions for Domain, platforms and components for Architecture, screens and regions for UX. Do not decompose into individual stories, structured terms, component interactions, or UI controls — that is downstream analysis.
- **Pass-through files** (< ~1,500 chars) were not split; they have view tags but no chunk subdivision.
- **The coverage index** accounts for every source file and every tagged piece — totals match, no orphans.
- **Architecture chunks** that describe custom-built components carry `provenance: custom`; out-of-box platform features carry `provenance: ootb`.
- **Multi-view chunks** are tagged with all applicable views, not forced into a single one.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Chunk size threshold

Chunks should only be created from source files large enough to benefit from splitting. A file that is already 1–2 pages or shorter produces fragments too small for useful retrieval when subdivided. Passing means every chunk comes from a file that exceeded the size threshold, and no chunk is smaller than the minimum useful size. Failing means a short file was needlessly split, or a chunk is so small it carries no retrievable context.

#### DO

- Only create chunks from source files that exceed roughly 1,500 characters (about 2 printed pages).

  **Example (pass):** `requirements.md` is 4,200 characters — split into two chunks of ~2,100 characters each. Both chunks carry enough context for retrieval.

- Pass through files at or below the threshold intact — assign view tags but do not subdivide.

  **Example (pass):** `glossary.md` is 900 characters — listed in the report as a pass-through with `primary_views: [domain]` and hierarchical tags, but no `chunk_NN` files are created from it.

- Keep individual chunks between roughly 800 and 3,000 characters so each piece is large enough to carry context but small enough for focused retrieval.

  **Example (pass):** A 6,000-character file is split into three chunks of approximately 2,000 characters each, each one covering a coherent section under its own heading.

#### DO NOT

- Split a source file that is already at or below the size threshold (~1,500 characters).

  **Example (fail):** `api-notes.md` is 1,100 characters — the chunker produces `api-notes__chunk_01` (600 chars) and `api-notes__chunk_02` (500 chars). Both fragments are too small and the file should have passed through intact.

- Produce a chunk smaller than roughly 400 characters unless it is the final tail of a file and merging it with the prior chunk would exceed 3,000 characters.

  **Example (fail):** `requirements__chunk_07` is 180 characters containing only a heading and one sentence. It should have been merged with the preceding chunk.

- Ignore the threshold and chunk every file regardless of size.

  **Example (fail):** A batch of 20 source files includes 8 files under 1,000 characters. All 20 are split into chunks. The 8 small files should have been pass-throughs.

### Rule: Tag depth accuracy

This is a **tagging exercise, not full modeling**. Tags should stay at an orientation level — broad enough to classify and locate content, not so deep that the tagger is doing the work of downstream analysis. Passing means tags identify the right area (epic, module, platform, screen) without decomposing into individual stories, structured terms, component interactions, or UI controls. Failing means the tagger either over-structures content that should be left for later analysis, or speculates on details the content does not contain.

#### DO

- Tag at the **orientation level** for each view — the level that answers "what area is this about?" not "what is the detailed structure?"

  **Example (pass):** The chunk discusses order processing workflows and validation. Tags include:

  ```yaml
  story:
    epic: Manage Orders
    actor: user
  domain:
    module: Order Management
    key_abstraction: Order
  ```

  The tagger identifies the capability area and the key abstraction — enough to locate this content. Decomposing into individual stories, specific terms like `Order Line`, or stereotypes like `aggregate` is downstream work.

- Tag `arch.provenance` for architecture content so it is clear what is custom-built versus platform-provided.

  **Example (pass):** The chunk says "Authentication uses AWS Cognito with custom token enrichment middleware." Tags include:

  ```yaml
  architecture:
    mechanism: security
    platform: AWS Cognito
    provenance: extended
  ```

  Cognito is out-of-box but the custom middleware makes this `extended`.

- Leave deeper tag levels empty — partial depth is expected and correct for a tagging pass.

  **Example (pass):** The chunk says "The system handles order management." Tags include:

  ```yaml
  domain:
    module: Order Management
  ```

  The content names the module but no specific abstractions — stopping at `module` is accurate.

#### DO NOT

- Over-structure content by tagging at levels that belong to downstream analysis — individual stories, domain terms, DDD stereotypes, UI controls, or component interactions.

  **Example (fail):** The chunk discusses order processing. Tags include:

  ```yaml
  domain:
    module: Order Management
    key_abstraction: Order
    term: Order Line
    stereotype: aggregate
  story:
    epic: Manage Orders
    sub_epic: Process Order
    story: Submit Order
  ```

  The tagger decomposed into stories and domain terms — that is story mapping and domain modeling work, not tagging.

- Speculate on tag values the content does not actually contain — do not infer details from assumptions or external knowledge.

  **Example (fail):** The chunk says "The system processes customer orders." Tags include:

  ```yaml
  domain:
    module: Order Management
    key_abstraction: Order
    term: Order Line
    stereotype: aggregate
  ```

  The content never mentions `Order Line` or aggregate boundaries. The tagger guessed from general e-commerce knowledge instead of reading the text.

- Assign `arch.provenance` without evidence from the content about whether the component is custom or platform-provided.

  **Example (fail):** The chunk describes "a caching layer for product queries" with no mention of Redis, Memcached, or any platform. Tags include `arch.provenance: ootb`. There is no basis for the `ootb` claim — omit `provenance` or note it as unknown in the report.

### Rule: View tagging required

Every chunk and every pass-through file must be tagged with at least one primary view and the corresponding hierarchical tags from the taxonomy reference. Passing means no chunk exists without a `primary_views` list and at least one view's tag hierarchy filled in. Failing means chunks are left untagged, or tags are invented outside the vocabulary in `references/four-view-taxonomy.md`.

#### DO

- Assign at least one entry in `primary_views` (story, domain, architecture, ux) to every chunk and every pass-through file.

  **Example (pass):**

  ```yaml
  primary_views: [domain, architecture]
  tags:
    domain:
      module: Order Management
      key_abstraction: Order
    architecture:
      component: Order Service
      provenance: custom
  ```

  The chunk describes order data and the service that manages it — both views are tagged with hierarchical detail.

- Tag content that legitimately informs multiple views with all applicable views — do not force a single assignment.

  **Example (pass):** A paragraph about "users cancel orders from the order detail screen if status is Pending" is tagged `primary_views: [story, ux, domain]` because it describes a user action (story), names a screen (ux), and references a status constraint (domain).

- Use only tag names and enum values defined in `references/four-view-taxonomy.md`.

  **Example (pass):** `story.actor: user` — the value `user` is in the taxonomy's enum for `story.actor`.

#### DO NOT

- Leave any chunk or pass-through file with an empty or missing `primary_views` list.

  **Example (fail):**

  ```yaml
  chunk_id: requirements__chunk_04
  primary_views: []
  tags: {}
  ```

  The chunk has no view assignment and no tags — a reviewer cannot tell which practice this content informs.

- Invent tag names or values that do not appear in the taxonomy reference.

  **Example (fail):** `domain.category: business_logic` — the taxonomy defines `domain.module_kind` with specific enum values, not `domain.category`. The tagger invented a field.

- Tag a chunk with all four views when its content clearly serves only one or two.

  **Example (fail):** A paragraph that only lists database column definitions is tagged `primary_views: [story, domain, architecture, ux]`. It should be `[domain]` or at most `[domain, architecture]` — there is no story behavior, no screen layout.
<!-- execute_rules:bundle_rules:end -->

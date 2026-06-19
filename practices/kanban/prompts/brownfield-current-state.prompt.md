---
description: >-
  Map brownfield / legacy current-state behavior through the story-driven-delivery
  pipeline. Story map = what the system does today, including observed quirks.
agent: agent
---

Run the brownfield current-state strategy. Read **`abd-kanban-planning/strategies/brownfield-current-state.md`** first for sequencing and constraints.

The user will provide **workspace** and **boundary** (module, service, flow). If not provided, ask.

**Sequence (per boundary):**

**Context extraction** (when source is scattered):
1. **Convert** — `abd-convert-to-markdown`
2. **Chunk + tag** — `abd-semantic-context-chunker`
3. **Embed** _(optional)_ — `abd-embed-vectors`

**Shaping:**
4. **Module partition** — `abd-module-partition`
5. **Bounded context map** _(optional)_ — `abd-bounded-context-map`
6. **Architecture outline** — `abd-architecture-outline`

**Discovery:**
7. **Story Map (brownfield)** — `abd-story-mapping` — trace code then map; every story needs evidence; no fix-while-mapping
8. **Domain Terms** — `abd-domain-terms`
9. **Ubiquitous Language** — `abd-ubiquitous-language`
10. **Architecture blueprint** — `abd-architecture-blueprint`
11. **Information Architecture** _(optional)_ — `abd-information-architecture`
12. **Thin Slicing** — `abd-thin-slicing` — separate characterize vs change slices
13. **Brownfield boundary gate** — reviewer checklist before exploration

**Exploration (per slice):**
14. **UL refresh** — `abd-ubiquitous-language` — for the increment
15. **Acceptance Criteria** — `abd-acceptance-criteria` — observed quirks as `intent: observed`
16. **UX Mockup** _(optional)_ — `abd-ux-mockup` — lo-fi wireframes
17. **Architecture template** _(optional)_ — `abd-architecture-template` — mechanism patterns

**Specification (optional OOAD pass):**
18. **CRC** — `abd-class-responsibility-collaborator`
19. **Spec by Example** — `abd-specification-by-example` — concrete scenarios; drives story-spec-driven tests
20. **Scenario Walkthrough** — `abd-scenario-walkthrough` — walk specs through CRC model

**Engineering:**
21. **Interface design** _(optional)_ — `abd-interface-design` — runnable UI from mockup
22. **Object model** _(optional)_ — `abd-object-model` — typed domain surface from CRC/UL
23. **Acceptance Tests (RED)** — `abd-acceptance-test-driven-development` — green on **current** system; from spec scenarios when available, from AC directly when skipped
24. **Change slice (optional)** — `abd-clean-code` / stack skill — only with approved delta

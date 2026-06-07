---
description: >-
  Map brownfield / legacy current-state behavior through the story-driven-delivery
  pipeline. Story map = what the system does today, including observed quirks.
mode: agent
---

Run the brownfield current-state strategy. Read **`abd-kanban-planning/strategies/brownfield-current-state.md`** first for sequencing and constraints.

The user will provide **workspace** and **boundary** (module, service, flow). If not provided, ask.

**Sequence (per boundary):**

**Context extraction** (when source is scattered):
1. **Convert** — `abd-convert-to-markdown`
2. **Chunk + tag** — `abd-semantic-context-chunker`
3. **Embed** _(optional)_ — `abd-embed-vectors`

**Shaping:**
4. **Module partition** — `abd-domain-partition`
5. **Bounded context map** _(optional)_ — `abd-bounded-context-map`
6. **Architecture outline** — `abd-architecture-outline`

**Discovery:**
7. **Story Map (brownfield)** — `abd-story-mapping` — trace code then map; every story needs evidence; no fix-while-mapping
8. **Domain Terms** — `abd-domain-terms`
9. **Architecture blueprint** — `abd-architecture-blueprint`
10. **Information Architecture** _(optional)_ — `abd-information-architecture`
11. **Thin Slicing** — `abd-thin-slicing` — separate characterize vs change slices
12. **Brownfield boundary gate** — reviewer checklist before exploration

**Exploration (per slice):**
13. **Domain Language** — `abd-domain-language` — for the increment
14. **Acceptance Criteria** — `abd-acceptance-criteria` — observed quirks as `intent: observed`
15. **UX Mockup** _(optional)_ — `abd-ux-mockup` — lo-fi wireframes
16. **Architecture template** _(conditional)_ — `abd-architecture-specification` — mechanism templates **only when increment scope needs undocumented mechanisms**; otherwise skip with assign notes

**Specification (optional OOAD pass):**
17. **domain model** — `abd-domain-model`
18. **Spec by Example** — `abd-specification-by-example` — concrete scenarios; drives story-spec-driven tests

**Engineering:**
19. **Interface design** _(optional)_ — `abd-interface-design` — runnable UI from mockup
20. **Class Model** _(optional)_ — `abd-domain-implementation` — typed domain surface from domain model/UL
21. **Acceptance Tests (RED)** — `abd-acceptance-test-driven-development` — green on **current** system; from spec scenarios when available, from AC directly when skipped
22. **Change slice (optional)** — `abd-clean-code` / `abd-architecture-code` — only with approved delta

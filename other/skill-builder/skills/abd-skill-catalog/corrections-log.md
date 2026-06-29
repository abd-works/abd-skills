# Corrections — abd-skill-catalog (generated AI Garden HTML)

---

## Entry — duplicate home link vs global nav — 2026-05-05

**Status:** fixed (templates + regenerated `catalog/`)

**Context:** AI Garden HTML when served under abd.works loads `commons/brand-nav.js`, which already provides the ABD.WORKS wordmark/link and logo.

**DO:** Rely on `brand-nav.js` for hub wayfinding only; omit a second `.site-home-link` in `.panel-header`. Include `<script src="/commons/brand-nav.js"></script>` on every catalog page shell that users open on the hub (hub, skills, agents, detail, markdown mirror).

**Example (wrong):** Panel header duplicated a text “← abd.works” stripe (via CSS `::before`) / logo markup alongside the injected global nav.

**Example (correct):** `.panel-header` leads with page title/tagline (`header-text` only); `← All skills` / hub nav remain for intra-garden jumps.

**Likely source:** `unclear expectation` (overlap between page chrome and shared subsite chrome)

---

## Entry — practices/ layout (core vs supporting, stage paths) — 2026-06-09

**Status:** confirmed

**Context:** Practice plugins moved under `practices/<plugin>/` with core skills at `skills/<skill>/` and supporting skills at `skills/supporting/<skill>/`. Stage definitions live at `common/reference/stages/`. UX package moved to `practices/user-experience-design/`.

**DO:** Discover skills recursively under `<plugin>/skills/`; on plugin pages group **core** vs **supporting**; load kanban stage tables from `common/reference/stages/`; map `user-experience-design` to `practices/user-experience-design/`; keep supporting/background skills off the kanban grid via existing exclusion rules.

**DO NOT:** Assume flat repo-root family folders (`delivery/`, `story-driven-delivery/`); scan only immediate `skills/` children on plugin pages; read stages from `content/stages/` or `practices/kanban/user-experience-design/`.

**Example (wrong):** Plugin page listed five story-driven-delivery skills and omitted `drawio-story-sync`; kanban loaded zero stages; UX skills missing after path change.

**Example (correct):** Plugin page shows core skills plus a Supporting skills subsection; kanban renders five stages from `reference/stages/`; UX package discovers six skills at `practices/user-experience-design/skills/`.

**Likely source:** `prompt gap` (organizational format change not reflected in catalog scripts)

---

## Entry — supporting / foundational crosscut groups — 2026-06-09

**Status:** confirmed

**Context:** User specified orange **Supporting** rows (Kanban, Diagram, Planning, Modeling) and grey **Foundational** rows (context-to-memory, skill-builder, helpers) below the delivery kanban.

**DO:** Render crosscut from `catalog_supporting_groups.py`; show Supporting + Foundational stacks on hub kanban embed and kanban overview slide; group plugin-page supporting skills under the same labels when a skill is in the map.

**DO NOT:** Flatten all supporting skills into one row; omit foundational crosscut; show supporting skills on stage columns.

**Example (wrong):** Hub kanban ends at stage questions with no crosscut; DDD plugin lists four supporting skills with no Diagram vs Modeling subheadings.

**Example (correct):** Hub embed shows Supporting (Kanban with agents + skills, Diagram, Planning, Modeling) and Foundational (three plugin rows); SDD plugin page has Diagram and Planning subsections under Supporting skills.

**Likely source:** `unclear expectation` (taxonomy stated in chat, not yet encoded in generator)

---

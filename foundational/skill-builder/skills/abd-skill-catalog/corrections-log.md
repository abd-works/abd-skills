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

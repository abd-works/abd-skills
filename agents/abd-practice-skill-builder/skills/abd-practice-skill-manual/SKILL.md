---
name: abd-practice-skill-manual
description: >-
  Ship a readable HTML companion for a practice: longer walkthroughs, figures, and
  sources so people can study the method without parsing SKILL.md alone.
---

# abd-practice-skill-manual

## Purpose

**SKILL.md** is the **compact** source of truth; many readers still want a **browser-friendly** walkthrough with **room for diagrams**, **step layout**, and **quoted evidence**. This skill produces that **HTML manual** next to the skill, using **self-contained** styling assets so it opens **offline** without another repo.

## When to use

- The **target** practice has **stable** **SKILL.md**, **`rules/*.md`**, and **`inputs/abd-answers-retrieval.md`** (and optionally **`README.md`**) you want to reflect in long form.
- You need **section pages**, **figures**, or **Sources** blocks that are **heavy** for a single **SKILL.md**.
- You want the manual to **cite** the same hub rows as the skill (**#** + **source location**).

## Not in this pass

Changing **normative** **SKILL.md** or **`rules/*.md`** meaning — only **HTML**, **assets**, and **links** that **mirror** what is already decided.

## Layout conventions

- **Path:** `skills/<skill-name>/manual/index.html` (one manual root per practice skill package — no extra subfolder named after the skill).
- **Sections:** `manual/sections/NN-slug.html` — link from index with anchors.
- **Assets:** Copy this skill's **`assets/`** into **`manual/assets/`** on the target package:
  - **`assets/css/`** — shell, hyperlinks, icons, manual layout (`.abd-doc-*`).
  - **`assets/images/`** — starters (`overview-placeholder.svg`, `icon-hub-catalog.svg`, `manual.png`, `document.png`); optional **`abd-logo.png`** for nav (hidden if missing).
  - **`assets/fragments/`** — optional snippets; **templates** inline the same chrome.

## SKILL.md citations (target package)

1. **Top of body** (after YAML):

   ```markdown
   **Manual:** [Practice manual](./manual/index.html)
   ```

2. **Inside sections** when pointing to long form:

   ```markdown
   See **Manual:** [Purpose](./manual/index.html#purpose) (section **Purpose**).
   ```

## Agent instructions

Apply the **bundled rules** at the end of this file for **Sources** and **asset** discipline.

1. Create **`manual/`** on the target package and copy **`assets/`** from this skill's **`assets/`** folder into **`manual/assets/`** (recursive).
2. Copy **`templates/manual-index.html`** and **`templates/manual-section.html`** into **`manual/`** (and under **`sections/`** as you add pages).
3. Fill **title**, **skill name**, **revision**, **Sources** from **`inputs/abd-answers-retrieval.md`** (especially **diagram_ref** or **example** rows).
4. For each **SKILL.md** H2, add a **section** page or index anchor; add figures under **`manual/assets/images/`** as needed.
5. Customize **Hub** links in the cross-site bar if the manual is published with real URLs; keep **`aria-current="page"`** on the active manual link.
6. Every manual page **Sources** block lists **Source location** (and row **#**) from **`inputs/abd-answers-retrieval.md`**.
7. Keep HTML **ASCII** unless the source material requires otherwise.

## Validate

**Goal:** Inspect as a reader opening files locally.

- **Evidence** — Every page has **Sources** or **See also** tied to **`inputs/abd-answers-retrieval.md`**.
- **Links** — **SKILL.md** **Manual:** links resolve with **relative** paths from the repo root.
- **Assets** — **`index.html`** loads **`assets/css/*.css`** and referenced **`assets/images/*`** without 404.
- **Parity** — Section titles and order **roughly** match what **SKILL.md** promises for the long form.

## Templates

| File | Role |
| --- | --- |
| `templates/manual-index.html` | Landing page, TOC, chrome header/footer, local CSS |
| `templates/manual-section.html` | One expanded section shell |

| Bundled path | Role |
| --- | --- |
| `assets/css/*` | Shell + prose links + manual layout |
| `assets/images/*` | Starter figures and icons |
| `assets/fragments/*` | Optional HTML partials |

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Manual evidence and assets

**Scanner:** Manual review

#### DO

- **Cite rows** — **Sources** on each page point to **hub evidence** via **`inputs/abd-answers-retrieval.md`** (**row #** + **source location**).
- **Ship assets** — Every **CSS** and **image** path in HTML resolves under **`manual/assets/`** for local open.

#### DO NOT

- Ship a page with **no** evidence pointer when the page claims hub or rule content.
- Rely on **another repo** for core CSS; keep this manual **self-contained** per this skill's **`assets/`** copy step.

**Source:** Practice-skill builder convention (abd-practice-skill-manual).
<!-- execute_rules:bundle_rules:end -->

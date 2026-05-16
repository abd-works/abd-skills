# Rule: Tab states fully decomposed; every story and domain term traceable

**Scanner:** AI review (run after `initial-ia.md` is authored and after the canvas is drawn)

An IA region that contains tabs, mode-switches, or sub-screens is **not one region** — each tab state is a distinct user-visible state with its own sub-regions, data shown, key actions, domain terms, and stories. Similarly, every in-scope domain concept that the user perceives must be traceable to at least one visible element on the canvas (screen name, region name, content type, label, or key action). If you cannot walk from a story to a visible action, or from a domain term to a visible name, the IA is incomplete.

---

## Rule 1 — Tab / mode states are each fully decomposed

A region that presents content through tabs, segmented controls, mode toggles, or side-panel navigation exposes **different sub-regions, data, and actions** depending on which tab or mode is active. Each state must be documented separately.

### DO

- Treat each tab state as a named sub-region of the containing region.
- Give each sub-region its own: layout within the parent region, data shown, key actions, linked domain terms, and linked stories.

  **Example (pass):**
  ```
  character detail panel — tab: Identities
    identity list: name · type badge · active/default indicator
    actions: add, remove, set default, set active
    domain terms: identity, model identity, costume identity, active identity, default identity

  character detail panel — tab: Abilities
    ability list: name · activation key · persistent flag · attack flag
    ability editor: animation-element tree (FX / MOV / sound / pause / sequence / reference / identity)
    actions: create, delete, play, stop, set activation key, toggle persistence, add element, reorder
    domain terms: animated ability, animation element, FX effect element, MOV element, ...

  character detail panel — tab: Movements
    movement list: name · default indicator · activation key
    movement detail: type, distance limit
    actions: add, remove, set default, set activation key
    domain terms: character movement, movement instruction
  ```

- On the canvas, show tab states as separate labeled boxes side by side (or as a vertically stacked variant group), clearly associated with the containing screen.

### DO NOT

- Describe a tabbed panel as a single region with "tabs: X, Y, Z" and nothing else.

  **Example (fail):**
  ```
  character detail panel — tabs: Identities, Abilities, Movements
  ```
  This tells the reader nothing about what is visible in each state. Each tab is a separate sub-region and must be documented fully.

- Merge the data and actions of multiple tab states into one undifferentiated list.

  **Example (fail):**
  ```
  character detail panel — actions: add identity, create ability, set activation key, add movement, ...
  ```
  Actions from different tab states are mixed together; the reader cannot tell which actions apply to which state.

---

## Rule 2 — Every in-scope domain term is visible on the canvas

Every domain term, concept, or class in scope must appear as at least one of: a screen name, a region name, a content type name, a sub-region label, a key action label, or a listed domain term annotation on a screen. If a domain term names something the user reads, edits, or acts on directly, it must appear in a content sub-region or key-actions list — not only in the per-screen domain term annotation.

A domain concept that has **its own sub-concepts or option-group items** (e.g. `animated ability → animation elements: FX effect element, MOV element, sound element, …`) requires a sub-region or expandable section for each sub-concept if a user story targets that sub-concept directly.

### DO

- For every domain concept that a user can create, edit, or interact with, include it as a named region, sub-region, content type, or key action label.
- For option groups with typed members, show each member type as a sub-item in the region where that type appears.

  **Example (pass):**
  ```
  ability editor region:
    element tree rows:
      FX effect element — add, edit (FX resource, position, scale), delete
      MOV element — add, edit (animation resource), delete
      sound element — add, edit (sound file, volume), delete
      pause element — add, edit (duration), delete
      sequence element — add, edit (type: And / Or), delete
      reference ability — add, edit (target ability), delete
      identity element — add, edit (target identity), delete
  ```

### DO NOT

- List a domain term only in the per-screen annotation without tracing it to a visible region or action.

  **Example (fail):**
  ```
  Domain terms: animated ability, animation element, FX effect element, MOV element
  ```
  …with no corresponding region or action in the spec. The annotation is a cross-reference; it is not a substitute for representation.

- Omit sub-types of a domain concept that users interact with individually.

  **Example (fail):**
  ```
  ability editor — animation element list (add, edit, delete)
  ```
  This hides the fact that there are seven distinct element types with different parameters. The IA must show each type.

---

## Rule 3 — Every in-scope user story is traceable to a screen action or transition

Every **user story** in scope must be reachable from the IA in one of two ways:
1. It appears as a **key action** on the screen where its interaction occurs, or
2. It appears as a **transition trigger** between screens.

System stories must be grouped with the closest user-visible screen.

### DO

- Walk the story list and confirm each story resolves to an action label or a transition label. If a story has no home, either a screen is missing or a key action has been omitted.

### DO NOT

- List stories only in the per-screen annotation without ensuring the action they describe is visible somewhere in the region content.

  **Example (fail):**
  ```
  Stories: Browse FX / Movement / Sound Resources
  ```
  …but no region on the screen lists "browse resources" as an action, and no transition is triggered by browsing. The story is orphaned.

---

## Completeness test (run before marking the IA done)

For each item in the completeness checklist, verify against `docs/ux/initial-ia.md` **and** against the canvas:

- [ ] A **story trace table** exists showing every in-scope GM story mapped to: screen, region, key action or transition trigger. No row has an empty region or action cell. (Built in step 4a.)
- [ ] A **domain term trace table** exists showing every in-scope domain term mapped to: screen, visible element (screen/region/sub-region/content type/label/action). No term is "annotation only" without justification. (Built in step 4b.)
- [ ] Every region that has tabs, modes, or sub-screens is decomposed into per-state sub-regions in the spec.
- [ ] Every tab state has: data shown, key actions, linked domain terms, linked stories.
- [ ] Every in-scope domain term appears by name in at least one region, sub-region, content type name, or key action label.
- [ ] Every in-scope domain concept with typed sub-concepts has those sub-concepts listed as separate items in the region where they appear.
- [ ] Every in-scope user story maps to a key action or a transition trigger — no orphaned stories.
- [ ] The canvas visually shows each tab state as a distinct labeled box (not a single panel with tab names in a comment).

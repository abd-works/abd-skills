# Corrections log

Project: abd-specification-by-example skill
Source: abd-specification-by-example skill (pipeline runs)

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** story-driven phase output filename
- **DO / DO NOT:** DO default to the template filename � `story-map.md`, `thin-slicing.md`, `acceptance-criteria.md`, `specification-by-example.md` (and their `.txt` partners where applicable). DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, multiple stories sharing one folder, or the user asks for it. DO NOT mandate the prefix as the only valid form, and DO NOT invent a sub-folder like `stories/`, `specs/`, `slices/`, `docs/` � write next to other engagement deliverables.
- **Example (wrong, forced prefix and folder):** Writing `docs/paw-place-thin-slicing.md` when the engagement workspace already keeps deliverables in `docs/` and only hosts one product. The `paw-place-` prefix is noise.
- **Example (correct):** Default to `thin-slicing.md` written next to existing engagement deliverables. Add a prefix only when disambiguation is needed.
- **Likely source:** earlier in this session the skill emitted `<name>-<phase>.md` unconditionally, then writing into a hardcoded folder; the user moved the files manually and asked that the prefix be optional and the folder driven by where other deliverables already live.

---

## Entry: Invariants become scenarios; Then is observable only; no data-equality assertions

- **Status:** confirmed
- **Context:** writing `specification-by-example.md` from upstream artifacts (UL, CRC, AC) that carry invariants
- **DO / DO NOT:**
  - **DO** translate every invariant of the form "X must hold when Y" into a scenario whose `When` triggers Y and whose `Then` is the observable that proves X. Each invariant earns at least one scenario; two-sided invariants (e.g. "set on change; cleared on save") earn one per side.
  - **DO** restrict `Then` clauses to things a human, the file system, another system actor, or the UI can verify: writes, error messages, refusals, UI state, file contents, status text.
  - **DO NOT** write `Then` clauses that read internal state � "the *thing* has *flag* equal to *true*", "the *crowd* has *source file* equal to *path*", "the dirty flag is *false*". Those are data assertions, not behavior.
  - **DO NOT** write a scenario whose only payoff is a data equality (e.g. "after load, the crowd has source file X"). The invariant is real, but it has to be exercised through an observable downstream behavior (save writes to that path; save of an unchanged crowd is a no-op; etc.). If the property never drives an observable, the scenario is not worth writing.
- **Example (wrong, internal-state assertion):**

  ```gherkin
  Scenario: A structural change marks the crowd dirty
    Given a **Crowd** *"Armageddon Squad"* with **dirty flag** *false*
    When the GM adds **Character** *"Battle Maiden"* to *"Armageddon Squad"*
    Then *"Armageddon Squad"* has **dirty flag** *true*
  ```

  The `Then` reads an internal flag the GM cannot see. The behavior the flag governs (save writes or skips) is what is actually observable.

- **Example (wrong, data-equality after load):**

  ```gherkin
  Scenario: Each loaded crowd remembers its single source file
    Given a **Crowd File** *"C:\COH\data\heroes.json"* containing **Crowd** *"Freedom Phalanx"*
    And the **Active Crowd List** contains *"C:\COH\data\heroes.json"*
    When the **Character Crowd Main Workspace** opens
    Then **Crowd** *"Freedom Phalanx"* has **Source File** *"C:\COH\data\heroes.json"*
  ```

  The `Then` reads a property nothing observes. The same invariant is provable through save behavior � that the changed crowd is written back to the file it came from.

- **Example (correct, observable-only):**

  ```gherkin
  Scenario: Save skips a clean crowd
    Given a **Crowd File** *"C:\COH\data\armageddons.json"* containing **Crowd** *"Armageddon Squad"*
    And the **Active Crowd List** contains *"C:\COH\data\armageddons.json"*
    And the **Character Crowd Main Workspace** has been opened
    And the GM has made no changes
    When the GM invokes **Save Dirty Crowds**
    Then *"C:\COH\data\armageddons.json"* is not opened for writing
    And no **Daily Backup** is created for that **Crowd File**

  Scenario: Saving a changed loaded crowd writes back to its original file
    Given a **Crowd File** *"C:\COH\data\heroes.json"* containing **Crowd** *"Freedom Phalanx"*
    And a **Crowd File** *"C:\COH\data\villains.json"* containing **Crowd** *"Council Empire"*
    And the **Active Crowd List** contains both paths
    And the **Character Crowd Main Workspace** has been opened
    And the GM has renamed **Crowd** *"Freedom Phalanx"* to *"Freedom Phalanx Reformed"*
    When the GM invokes **Save Dirty Crowds**
    Then *"C:\COH\data\heroes.json"* is overwritten with **Crowd** *"Freedom Phalanx Reformed"*
    And *"C:\COH\data\villains.json"* is not modified
  ```

  Same two invariants (dirty-flag lifecycle, one-source-file-per-crowd) � now exercised entirely through observable file writes.

- **Likely source:** instruction not read � the skill's bundled rules emphasise behavior over data, but the agent fell back on internal-state assertions when invariants happened to be phrased in data-shaped language ("flag is true", "field equals path"). The translation step from invariant phrasing to observable behavior needs to be explicit in the rule.

---

## Entry: Tables only attach to Scenario Outlines; tables must be relationship-based, never denormalized

- **Status:** confirmed
- **Context:** writing `specification-by-example.md` for a feature whose Givens describe rich one-to-many-to-many domain data (top-level *Crowd* ? nested *Crowd* ? *Character*), driven by user input "this is better as an outline due to the one-to-many-to-many relationships of crowds, nested crowds, characters".
- **DO / DO NOT:**
  - **DO** use plain **Scenarios with inline values** for distinct logical flows. Express nested hierarchy in step prose � `containing top-level **Crowd** *"X"* with **Characters** *"a"*, *"b"* and nested **Crowd** *"Y"* with **Character** *"c"*`. **bold** for domain concepts, *italic* for values.
  - **DO** use **Scenario Outlines with relationship-based Examples tables** when (and only when) the same steps repeat with row-by-row variation. One table per domain concept. Tables linked by foreign-key columns (`crowd_file_path`, `parent_crowd_name`). A `scenario` column joins all tables for a given example row.
  - **DO NOT** attach Gherkin data tables (the inline `| col | col |` blocks) **inside** plain Scenario step lists. The plain `Scenario` form does not take tables � tables belong only to Scenario Outlines, placed **above** Givens or **below** When/Then.
  - **DO NOT** flatten multiple concepts into one wide row (`top_level_crowd | nested_crowd | character`). That mashes three concepts (top-level *Crowd*, nested *Crowd*, *Character*) into a single row and breaks the relationship structure of the domain. Use three linked tables � `CrowdFile`, `Crowd` (with `crowd_file_path` and `parent_crowd_name` FKs), `Character` (with `crowd_name` FK).
  - **DO** run a **table-shape pre-check** before writing any Examples block: list the concepts referenced in the scenario data; if more than one, model them as separate tables linked by FK; never collapse into a wide row.

- **Example (wrong, table inside a plain Scenario AND denormalized flat row):**

  ```gherkin
  Scenario: Activate a single crowd file
    Given the file *"C:\COH\data\armageddons.json"* exists on disk containing:
      | top_level_crowd     | nested_crowd      | character        |
      | "Armageddon Squad"  |                   | "Battle Maiden"  |
      | "Armageddon Squad"  |                   | "Manticore"      |
      | "Armageddon Squad"  | "Demolition Team" | "Demo Lead"      |
    When the GM clicks **Browse Crowd Files** and selects *"C:\COH\data\armageddons.json"*
    Then the **Crowd Tree** shows top-level **Crowd** *"Armageddon Squad"*
  ```

  Two violations: (1) data table on a plain `Scenario` instead of inline values; (2) three concepts (*Crowd File*, top-level *Crowd*, nested *Crowd*, *Character*) collapsed into one wide row.

- **Example (correct, plain Scenario with inline values + nested hierarchy in prose):**

  ```gherkin
  Scenario: Activate a single crowd file
    Given a **Crowd File** *"C:\COH\data\armageddons.json"* exists on disk
      containing top-level **Crowd** *"Armageddon Squad"*
        with **Characters** *"Battle Maiden"* and *"Manticore"*
        and nested **Crowd** *"Demolition Team"* with **Character** *"Demo Lead"*
    And the persisted **Active Crowd List** is empty
    When the GM clicks **Browse Crowd Files** and selects *"C:\COH\data\armageddons.json"*
    Then the **Crowd Tree** shows top-level **Crowd** *"Armageddon Squad"* with the same nested structure
    And the **All Characters Crowd** lists *"Battle Maiden"*, *"Demo Lead"*, *"Manticore"* in alphabetical order
    And the persisted **Active Crowd List** contains exactly *"C:\COH\data\armageddons.json"*
  ```

- **Example (correct, Scenario Outline with relationship-based Examples � one table per concept, linked by FK):**

  ```gherkin
  Scenario Outline: Re-activating an active Crowd File picks the next available integer suffix

  Given a **Crowd File** *"C:\COH\data\armageddons.json"* exists on disk
    containing top-level **Crowd** *"Armageddon Squad"* (full nested contents described in prose)
    And the persisted **Active Crowd List** contains *"C:\COH\data\armageddons.json"*
      plus every {existing_clone_path} listed under **ActiveCrowdEntry** below for this {scenario}
  When the GM clicks **Browse Crowd Files** and selects *"C:\COH\data\armageddons.json"* a second time
  Then a new **Crowd File** {new_clone_path} exists on disk
    containing top-level **Crowd** {new_top_level_crowd_name}
    with the same nested structure as the original
  And the original **Crowd File** *"C:\COH\data\armageddons.json"* is byte-unchanged on disk
  ```

  **Examples**

  ActiveCrowdEntry (Given � above scenario):

  | scenario      | existing_clone_path                  |
  | ------------- | ------------------------------------ |
  | First clone   | (none � only the original)           |
  | Second clone  | C:\COH\data\armageddons (2).json     |
  | Third clone   | C:\COH\data\armageddons (2).json     |
  | Third clone   | C:\COH\data\armageddons (3).json     |
  | Fill the gap  | C:\COH\data\armageddons (3).json     |

  CloneResult (Then � below scenario):

  | scenario      | new_clone_path                       | new_top_level_crowd_name |
  | ------------- | ------------------------------------ | ------------------------ |
  | First clone   | C:\COH\data\armageddons (2).json     | Armageddon Squad (2)     |
  | Second clone  | C:\COH\data\armageddons (3).json     | Armageddon Squad (3)     |
  | Third clone   | C:\COH\data\armageddons (4).json     | Armageddon Squad (4)     |
  | Fill the gap  | C:\COH\data\armageddons (2).json     | Armageddon Squad (2)     |

  The `scenario` column joins `ActiveCrowdEntry` to `CloneResult`. Each table holds one concept; FK columns express the relationship.

- **Likely source:** instruction not read � the user asked for richer data and used the words "data tables" and "outline", and the agent reached for Gherkin data tables inside plain Scenarios as the literal interpretation. The skill rules require: (a) tables only on outlines, (b) one table per concept, (c) FK-linked, never flattened. A pre-write checklist that asks "how many concepts in this Given? if >1, are they in separate FK-linked tables on an Outline?" would have caught both errors.

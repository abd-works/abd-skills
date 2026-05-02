---
name: key-abstractions
description: >-
  Group UDL terms into named Key Abstractions with prose definitions and
  verbatim source extracts, elevating a flat term list into defined domain
  building blocks.
---
# key-abstractions

## Purpose

A shared vocabulary names the pieces of the domain, but it doesn't tell you which concepts carry the weight — which ones anchor the model, own specific responsibilities, and enforce the rules that keep the domain coherent. This skill identifies those **Key Abstractions** and defines each one: what role it plays, what it owns, how it relates to other abstractions, and what must always be true about it. The result is a set of stable domain building blocks that everyone — modelers, developers, domain experts — can reason about consistently.

---

## When to use this skill

- The module file's front matter shows `state: domain-language`.
- The user asks to "identify key abstractions," "define the abstractions," "run key abstractions," or "what are the building blocks."
- The next modeling step needs defined domain units — not just a flat term list.

---

## Core concepts

### Key Abstraction

A **Key Abstraction** is a named domain building block that groups related terms and carries a prose definition explaining what it owns, what it does, and what rules it enforces. It transforms a flat vocabulary into an architecture — stable units that modelers, developers, and domain experts can reason about without ambiguity.

Each KA definition is 1–2 paragraphs of flowing prose that weaves together five aspects:

- **Role** — the unique purpose this KA serves that no other does, including its behavior and interactions with other KAs.
- **Boundary** — what it owns (single source of truth for its concepts), what's external, and how it collaborates with other KAs and the constraints of those connections.
- **Relationships** — explicit connections between terms and other abstractions, with cardinality where obvious and natural.
- **Responsibilities** — the specific behaviors it performs and the services it provides to the rest of the system.
- **Rules / invariants** — non-negotiable truths that must always hold for the KA to exist and operate correctly.

### Two tests for every candidate

Not every term deserves promotion to a Key Abstraction. Apply both tests before promoting:

**1. Independence test.** Does this concept exist and make sense on its own, without the parent it came from? If it is just a component or output of another concept and has no meaning outside it, it stays as a term under a KA, not its own KA. Example: "degree of success" has no meaning outside a check, so it stays under Check.

**2. Module-fit test.** Does this concept fundamentally connect to the core purpose of THIS module, or does it just touch it tangentially? If only one of its many uses relates to this module, it doesn't belong here. Example: "hero point" is independent, but only one of six spend types touches checks — it belongs in Combat, not Check Resolution.

### Three outcomes for each term

- **Keep as KA term** — passes both tests. Group under a KA.
- **Move to boundary** — independent, but this module *depends on* it without owning it. Add to `## Boundary terms` with an `Owned by:` field.
- **Move to another module** — independent, but this module does not depend on it at all. It was incorrectly partitioned here. Remove entirely and add to the correct module's Core terms list, carrying its prose and refs.

Be ruthlessly critical on both tests. When in doubt, keep it as a term under a real KA, or move it out. Inflating the KA count or the boundary list with tangential concepts weakens the model. A typical module has 3–8 Key Abstractions.

### Decisions made

Every Key Abstraction carries a **Decisions made** list — the specific judgment calls the modeler had to make. Each decision is a short statement that names the choice and enough reasoning that a domain expert can challenge it. Decisions include independence-test calls ("X is a part of Y, not its own KA"), module-fit calls ("X belongs in module Z, not here"), grouping calls ("merged these terms into one KA because..."), and open questions the team still needs to resolve. Making decisions explicit is how the model stays auditable and improvable.

### Source extracts

Every term carries `**Ref —**` entries that trace its prose back to source. This skill reads each referenced source file, extracts the verbatim text, and adds a fenced `source` block beneath the ref. This grounds the model in evidence — no paraphrase, no cleanup, no reformatting.

---

## The shape of a Key Abstraction

```markdown
## Key Abstractions

### Check

A check is the core resolution mechanic — the single mechanism through which
any uncertain outcome in the game is determined. It interacts with Trait
(supplying the modifier), Difficulty Class (setting the threshold), and Degree
(interpreting the margin of success or failure). The check owns the
roll-plus-modifier-versus-DC formula and serves as the single source of truth
for whether an action succeeds or fails; no other abstraction may duplicate
this determination. A check must always produce a binary success/failure
result, and when graded, must yield a degree that downstream abstractions
(conditions, resistance) can interpret. The GM sets the DC and decides when
circumstances allow routine checks; the player rolls and applies modifiers.

#### check

- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
- Whenever a character attempts something where outcome is in doubt, it requires a check.

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

#### Decisions made
- Degree is a part of Check, not its own KA — it has no meaning outside a check (independence test).
- DC is kept under Check rather than made standalone — it is always set in the context of a check.
- Modifier stays under Check — it is the numeric contribution of a trait to a specific check, not an independent concept.

#### Difficulty Class (DC)

- The DC is a number set by the GM that a check result must equal or exceed.
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).

**Ref — Ch1 The Basics**
Source: context/rules/HeroesHandbook-rules__chunk_005.md
Locator: lines 244–284
Extract: whole
```

The prose definition under each `### KA` heading is what makes a Key Abstraction more than a term grouping. It is the analytical contribution of this skill.

---

## Output file

This skill enriches the growing module file in place at `<workspace>/abd-domain-driven-design/modules/<module-name>.md`. Read it, extend it, write it back to the same path.

**Copy-output mode:** when the user says "copy output," also produce a snapshot at `<workspace>/abd-domain-driven-design/modules/<module-name>-key-abstractions.md`.

## Build

1. **Read the module file.** Confirm `state: domain-language`.
2. **Read all terms and prose.** Understand what each term means and how terms relate to each other.
3. **Group terms into Key Abstractions.** Apply both the independence test and the module-fit test to every candidate. Name each KA using the source's own vocabulary. Three outcomes per term: keep under a KA, move to boundary (depends on, doesn't own), or move to another module entirely (doesn't depend on at all — carry prose and refs to the destination).
4. **Update the Core terms list.** Remove any terms that were moved to another module. Add a `**Moved to other modules**` list recording where each moved term went (e.g. `- hero point → Combat`).
5. **Write the prose definition** for each KA — 1–2 paragraphs covering role, boundary, relationships, responsibilities, and rules/invariants in flowing prose.
6. **Record decisions.** Add a `#### Decisions made` bullet list under each KA after the prose definition, listing every judgment call: independence-test results, module-fit results, grouping choices, and open questions.
7. **Insert the KA grouping layer.** In the `# Core Domain` section, insert a `## KAName` heading above each group of `### term` headings that belong to it. The `### term` headings stay at the same level — the `##` heading is inserted above them. Each `## KA` contains: prose definition, `#### Decisions made`, then its `### term` headings. Do not rename, remove, or reorder any `### term` headings or `#### Domain Language` bullets.
8. **Add source blocks** under every `**Ref —**` entry in `#### References` sections (core and boundary). Copy bytes as-is from the source file.
9. **Bump state** to `key-abstractions`.
10. **Write the file** back to the same path. Follow the template in `templates/key-abstractions-template.md`.

---

## Validate

After completion, check:

1. **No terms lost.** Every `###` term heading from the UDL stage is present under exactly one `## KA` in `# Core Domain`, or as a `##` heading under `# Boundary Domain`.
2. **No prose lost.** Every `#### Domain Language` bullet under each term is unchanged.
3. **Every KA has a prose definition.** 1–2 paragraphs immediately after the `## KA` heading, before `#### Decisions made`, covering role, boundary, responsibilities, and rules/invariants.
4. **Every KA has decisions recorded.** A `#### Decisions made` bullet list is present under the prose definition, listing independence-test, module-fit, grouping, and open-question calls.
5. **Every ref has a source block.** Every `**Ref —**` entry in `#### References` is followed by a fenced `source` block with verbatim content.
6. **Ref entry format.** Every `**Ref —**` block has `Source:`, `Locator:`, and `Extract: whole|partial` — no missing or malformed fields.
7. **Partial extracts have Part line.** Every `Extract: partial` has a `Part:` line naming the slice; no `Part:` on `Extract: whole`.
8. **Verbatim accuracy.** Spot-check three source blocks against their source files — character-level identity.
9. **State marker.** Front matter reads `state: key-abstractions`.
10. **No old-model jargon.** No `Intent:`, `Shape hint:`, `Tension:`, `Core terms (absorbed`.
11. **No class-level commitments.** No stereotypes, typed properties, method signatures, or cardinality notation outside of verbatim source blocks.
12. **Boundary terms intact.** `Owned by:` fields preserved under `# Boundary Domain`. Source blocks added.
13. **Independence and module-fit tests passed.** Every `## KA` is an independent concept that fundamentally connects to this module's core purpose.
14. **Moved terms landed.** Every term in the `**Moved to other modules**` list appears in the destination module's `**Core terms**` bullet list.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Every ref has a source block

After key-abstractions enrichment, every `**Ref —**` entry in the module file must be followed by a fenced `source` block containing verbatim text from the referenced chunk. Passing means every ref has a non-empty source block. Failing means a ref exists without a corresponding source block.

#### DO

- Place a fenced `source` block immediately after the `Extract:` line of each `**Ref —**` entry.

  **Example (pass):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole

  ```source
  GAME PLAY
  …verbatim text from chunk…
  ```
  ```

- Ensure the source block is non-empty — at least one line of content.

  **Example (pass):** Source block has 20 lines of verbatim text.

#### DO NOT

- Leave a `**Ref —**` entry without a source block.

  **Example (fail):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole

  #### next term
  ```
  (No source block between the ref and the next heading.)

- Place an empty source block.

  **Example (fail):**
  ```
  ```source
  ```
  ```
  (Empty body — must contain verbatim text.)

### Rule: Every term accounted for — no drops

After key-abstractions enrichment, every term from the original `**Core terms**` bullet list must be accounted for in exactly one of three places:

1. As a `#### term` heading under exactly one `### KA` section inside `## Key Abstractions`.
2. As a `### term` heading under `## Boundary terms` (if the KA step determined the term is depended on but not owned by this module).
3. As an entry in the `**Moved to other modules**` list (if the KA step determined the term does not belong in this module at all), AND the destination module's `**Core terms**` bullet list must contain the term.

No term dropped, no term duplicated across KAs, no term vanished without a trace.

#### DO

- Place every term that was under `## Core terms` in the UDL stage as a `#### term` heading under exactly one `### KA` section inside `## Key Abstractions`.

  **Example (pass):** `#### check`, `#### DC`, and `#### modifier` all appear under `### Check` and nowhere else.

- When a term is moved to another module, record it in the `**Moved to other modules**` list with its destination.

  **Example (pass):**
  ```
  **Moved to other modules**:
  - hero point → Combat
  - extra effort → Combat
  ```

  And `combat.md`'s `**Core terms**` list includes `hero point` and `extra effort`.

- Keep the `**Core terms**` bullet list in the module header as a reference inventory (minus moved terms).

#### DO NOT

- Drop a term that existed in the UDL stage without recording where it went.

  **Example (fail):** `#### routine check` existed in UDL but does not appear under any `### KA` section, is not in `## Boundary terms`, and is not in the moved list.

- Place the same term under two different KAs.

  **Example (fail):** `#### modifier` appears under both `### Check` and `### Degree`.

- Record a moved term without actually adding it to the destination module.

  **Example (fail):** `- hero point → Combat` in the moved list, but `combat.md`'s Core terms does not include `hero point`.

### Rule: Ref entry format compliance

Every `**Ref — …**` block must carry the required header fields: `Source:`, `Locator:`, and `Extract: whole|partial`. These fields are inherited from the UDL stage and must not be removed or malformed during key-abstractions enrichment. Passing means every ref block has a complete, well-formed header. Failing means a header field is missing or malformed.

#### DO

- Preserve the `Source:` line pointing to the chunk file path.

  **Example (pass):**
  ```
  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole
  ```

- Preserve the `Locator:` line with a precise locator (lines, section heading, etc.).

  **Example (pass):** `Locator: lines 1238–1344`

- Set `Extract:` to exactly `whole` or `partial` (no other values).

  **Example (pass):** `Extract: whole`

#### DO NOT

- Remove the `Source:` line from a ref header during enrichment.

  **Example (fail):** A ref block with title, Locator, and Extract but no Source line.

- Change `Extract:` to a value other than `whole` or `partial`.

  **Example (fail):** `Extract: summary` or `Extract: verbatim`.

- Malform the `**Ref —**` header (e.g. `##Ref —` or `*Ref —*`).

  **Example (fail):** `##Ref — Game Play##` instead of `**Ref — Game Play**`.

### Rule: No class-level commitments

The module file at `state: key-abstractions` must contain no stereotypes, typed properties, method signatures, cardinality arrows, or other class-level notation. The key-abstractions step adds verbatim source extracts — it does not introduce modeling decisions. Passing means the file stays at the enrichment level. Failing means class-level decisions have leaked in.

#### DO

- Keep behavioral lines as plain prose bullets — observations about what the term means and how it works.

  **Example (pass):**
  ```
  - A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
  ```

- Keep `Owned by:` fields on boundary terms as simple module names.

  **Example (pass):** `Owned by: Power`

#### DO NOT

- Use UML stereotype tags like `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Event>>`, `<<Aggregate>>`.

  **Example (fail):** `<<Entity>> with lifecycle states` anywhere in the file.

- Add typed properties like `amount: Decimal`, `status: String`, or `checkId: UUID`.

  **Example (fail):** A behavioral line includes `rollResult: Int` or `dc: Integer`.

- Include method signatures like `resolve(modifier, dc) -> Result`.

  **Example (fail):** `Operations: roll(d20) -> int, compare(result, dc) -> bool`

- Use cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** `Check 1..* --> Condition` in any section.

- Commit to super/sub hierarchies or Entity/ValueObject distinctions.

  **Example (fail):** `Condition <<extends>> BasicCondition` — this belongs to later skills.

### Rule: No identification-model jargon or labeled definition sections

The key-abstractions step must not introduce fields from the old identification model (`Intent:`, `Shape hint:`, `Tension:`, `Core terms (absorbed`) and must not use labeled sections to define a KA (`Role:`, `Boundary:`, `Responsibilities:`, `Invariants:`). KA definitions are flowing prose paragraphs. Passing means none of these appear. Failing means any of them are present.

#### DO

- Write KA definitions as 1–2 paragraphs of flowing prose covering role, boundary, responsibilities, and rules/invariants naturally.

  **Example (pass):** A paragraph that says "A check is the core resolution mechanic — it interacts with Trait and DC, owns the roll-versus-DC formula, and must always produce a binary result."

#### DO NOT

- Add `Intent:` lines to any term or KA.

  **Example (fail):** `Intent: The atomic resolution mechanic that determines success or failure.`

- Add `Shape hint:` lines.

  **Example (fail):** `Shape hint: Procedure-like — verb-shaped with trigger and outcome.`

- Add `Tension:` lines.

  **Example (fail):** `Tension: May merge with opposed check in later modeling.`

- Add `Core terms (absorbed` lists that group terms under another term.

  **Example (fail):**
  ```
  Core terms (absorbed from this module's Core terms list):
  - d20
  - modifier
  ```

- Use labeled sections to structure the KA definition.

  **Example (fail):**
  ```
  Role: Determines success or failure of uncertain actions.
  Boundary: Owns the roll+modifier vs DC formula.
  Responsibilities: Resolves checks, produces degrees.
  Invariants: Must always yield binary success/failure.
  ```
  (These must be woven into prose, not listed as fields.)

### Rule: Partial extracts have Part line

Every extract marked `Extract: partial` must have a corresponding `Part:` line that names the slice in source-grounded terms. Conversely, `Extract: whole` must not have a `Part:` line. This ensures reviewers can reassemble sliced upstream extracts. Passing means the pairing is correct on every extract. Failing means a partial without `Part:` or a whole with an unnecessary `Part:`.

#### DO

- When `Extract: partial`, include `Part:` naming the specific slice (paragraph range, bullet list, sentence group).

  **Example (pass):**
  ```
  Extract: partial
  Part: Sentences that define the generic transfer mechanism — before the wire/KYC paragraph.
  ```

- Name the slice in source-grounded terms a reviewer can locate in the upstream extract.

  **Example (pass):** `Part: The three-bullet list under "Outbound Wire Limits".`

- Omit `Part:` when `Extract: whole` (the entire passage lives here).

  **Example (pass):**
  ```
  Extract: whole
  ```
  (No `Part:` line.)

#### DO NOT

- Set `Extract: partial` without a `Part:` line.

  **Example (fail):**
  ```
  Extract: partial
  ```
  (Missing `Part:` — reviewer cannot identify which slice this is.)

- Add a `Part:` line to a `Extract: whole` block (contradicts the "whole" claim).

  **Example (fail):**
  ```
  Extract: whole
  Part: First two paragraphs only.
  ```
  (If it is only part of the passage, it should be `Extract: partial`.)

### Rule: State marker is key-abstractions

After this skill runs, the module file's YAML front matter must contain `state: key-abstractions`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: key-abstractions`.

  **Example (pass):**
  ```
  ---
  state: key-abstractions
  ---
  ```

#### DO NOT

- Leave the state at `domain-language` (the previous step).

  **Example (fail):**
  ```
  ---
  state: domain-language
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

- Use a different field name or value.

  **Example (fail):** `stage: key-abstractions` or `state: ka` or `state: key_abstractions`.

### Rule: Verbatim source blocks trace to disk

Every fenced `source` block must contain text copied byte-for-byte from a file on disk. The `Source:` line in the parent `**Ref —**` entry must reference a resolvable path — not agent memory, training data, or generated content. Passing means every source block can be traced to a real file. Failing means a source block uses generated content or points to a non-existent file.

#### DO

- Reference real files on disk in the `Source:` line (context chunk files).

  **Example (pass):** `Source: context/rules/HeroesHandbook-rules__chunk_009.md`

- Copy text character-for-character from the source — preserve whitespace, bullets, markdown formatting, OCR artifacts.

  **Example (pass):** The source block body matches the file byte-for-byte.

- Stop and report to the user when a referenced source file does not exist on disk.

  **Example (pass):** Agent says "chunk_009.md not found — cannot add source extract."

#### DO NOT

- Use markers that indicate generated content: `domain-knowledge`, `from memory`, `reconstructed`, `agent knowledge`.

  **Example (fail):** `Source: domain-knowledge — "Resolution Rules"` — no file to verify.

- Paraphrase, clean up, or reformat the source text inside source blocks.

  **Example (fail):** Agent rewrites bullet points into clean prose before placing them in the source block.

- Proceed with source block creation when the referenced file does not exist on disk.

  **Example (fail):** `Source: context/rules/HeroesHandbook-rules__chunk_099.md` but that file is not in the workspace.
<!-- execute_rules:bundle_rules:end -->

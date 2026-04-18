# Sequence Diagrams and Walkthroughs (Draw.io and Markdown)

## Templates — use these for every create/update

All walkthrough / sequence work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):


| Role         | Template file                                  | When to use it                                                                                                                                                                                                                                                                           |
| ------------ | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Draw.io**  | `templates/domain realization template.drawio` | **New diagram:** duplicate this file into the workspace, rename, replace `{{placeholders}}`, then edit lifelines and messages. **Existing diagram:** when adding lifelines or messages, keep lifeline alignment, execution bars, and arrow-to-activation conventions as in the template. |
| **Markdown** | `templates/domain walkthrough template.md`     | **New companion doc:** copy its scenario, walks, and walkthrough structure. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass so steps and activations stay aligned.                                                                  |


## Terminology (same concept)

These names refer to the **same** kind of artifact:

- **Domain walkthrough**
- **Domain realization**
- **Domain interaction**
- **Sequence diagram**

Use whichever label the user prefers. In deliverables, pick one label per document and stay consistent.

## What to keep in sync

When the user asks to **create or update** modeling diagrams, treat **sequence / walkthrough** as a pair: a **`*.drawio`** grounded in **`templates/domain realization template.drawio`** and a Markdown companion with the **same structure** as **`templates/domain walkthrough template.md`**.

**Rule:** If both files exist for a topic, **update both** in the same pass so walk steps do not drift. If only one exists, create the missing companion **from those templates** unless the user opts out.

## Sequence / walkthrough — Draw.io (what the template encodes)

`templates/domain realization template.drawio` illustrates:

- **Initiator** lifeline (optional actor driving the scenario)
- **Object lifelines** (`{{object}}:{{Class}}`)
  - **Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
- **Synchronous messages** (filled arrow) and **returns** (open arrow, dashed)
  - **Crucial Connection Rule:** Message arrows must *always* snap exactly to the outer edge of the **execution bar (activation rectangle)**, NEVER to the center dashed lifeline itself.
  - **Message Angles:** All message arrows must be perfectly horizontal (0-degree angle).
- **Nested execution** (activation bars / self-segment notation)
  - **Positioning:** Execution bars must be placed *exactly centered* on the vertical dashed line of the lifeline.
  - **Nesting:** For internal behavior or nested calls, the nested execution bar must be stacked precisely on the right edge of the parent execution bar, offset slightly downwards to indicate time progression.
  - **Time Flow:** Vertical space strictly represents time. Elements must flow downwards cleanly without any vertical overlap of independent, sequential operations.
- Small **edge labels** for `new`, parameters, and call text

**CLI (`scripts/drawio_cli.py`):** Sequence commands use the same entry point as class diagrams. `sequence-init` copies **`templates/domain realization template.drawio`** to your file; `sequence-add-lifeline`, `sequence-add-sync`, and `sequence-add-return` add lifelines and messages (styles match the template); `sequence-list` lists lifeline labels. Activation bars, strict horizontal alignment of message rows, and nested activations are still usually finished in Draw.io — see **using-diagram-cli**.

**Template-only workflow:** duplicate **`domain realization template.drawio`** (see **Templates** above), replace placeholders, then adjust lifeline heights and messages as needed.

## Sequence / walkthrough — Markdown

**Narrative walkthrough** — Follow `templates/domain walkthrough template.md` (required structure; see **Templates** above):

- One **Scenario** block per flow.
- **Walk N: Covers** — scope (what responsibilities this walk exercises).
- Indented walkthrough lines showing object creation, calls, returns, and nesting (same story as the Draw.io diagram).

## Creating Sequence Diagrams from Walkthroughs (Step-by-step)

### Step 1: Extract lifelines from the walkthrough

Read the walkthrough and identify all **distinct objects/participants**:

```
{object}: {Type} = new {Class}()
{result}: {Type} = {object}.{method}()
    {collaborator}: {CollaboratingClass} = {getter}
    {inner}: {InnerType} = {collaborator}.{method}()
```

**Participants:**

- `{object}:{Class}` ← lifeline 1
- `{collaborator}:{CollaboratingClass}` ← lifeline 2
- Any other objects mentioned ← additional lifelines

### Step 2: Translate the walkthrough to messages

For each call in the walkthrough, create a **message arrow** in Draw.io:


| Walkthrough line        | Draw.io Message                                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------------------------------- |
| `{object}.{method}()`   | Synchronous message arrow (filled) from **{object}** to **{collaborator}** labeled `method()` with params       |
| `return {value}`        | Return arrow (dashed, open) from callee back to caller labeled with `{value}` (if non-void)                     |
| `{var} = new {Class}()` | Create message (labeled `«new»`) from initiator to the new object's lifeline                                    |
| Nested calls            | Stack activation bars (execution rectangles) vertically; nested calls go to the right edge of parent activation |


### Step 3: Align with Template

When creating the `.drawio` file:

1. **Duplicate** `templates/domain realization template.drawio`
2. **Replace placeholder lifelines** with actual participant names from Step 1
3. **Add messages** following the order in the walkthrough (top to bottom = time flow)
4. **Verify alignment:**
  - All lifelines top-aligned (horizontal line at y=0)
  - All message arrows **horizontal** (0° angle)
  - Message arrows snap to **outer edge of execution bars**, not center lifeline
  - Execution bars centered on lifeline, nested bars stacked right

### Step 4: Keep Markdown ↔ Draw.io in Sync

- **If updating the `.drawio`:** Update the `.md` walkthrough to match new messages/lifelines
- **If updating the `.md`:** Update the `.drawio` diagram to match new walkthrough steps
- **Test alignment:** Trace each line of the walkthrough to a message in the diagram; each message should appear in the `.md`

### Example: Character Creation Scenario

**Walkthrough excerpt (Walk 1: Create ability):**

```
player: Player = initiator
character: Character = new Character(power_level: 5)
    abilities: Ability[] = []
strength_ability: Ability = new Ability(type: Strength, rank: 3)
character.add_ability(strength_ability)
    character.spend_power_points(cost: 3)
return character with Strength:3
```

**Lifelines in `.drawio`:**

1. `player:Player`
2. `character:Character`
3. `strength_ability:Ability`

**Messages in `.drawio`:**

1. `player` → `character` : `create(power_level: 5)`
2. `character` → `abilities` : `add(strength_ability)`
3. `character` → `character` : `spend_power_points(3)` (self-call)
4. Return: `character` → `player` : character object

## File naming (suggested)

The **domain class model** stays **`*-domain-model.md`** (+ class **`*-domain-model.drawio`**) — **one** evolving pair, not a new domain-model file per pipeline phase. **Walkthrough** files are separate: scenario narrative + sequence diagram.


| Artifact                   | Example                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| Domain (class) model       | `domain.md`, `domain.drawio` — same pair through the whole pipeline                                  |
| Walkthrough (one scenario) | `walkthrough-<scenario>.md` + `walkthrough-<scenario>.drawio`                                        |
| Optional tutorial layout   | `{lesson}-walkthrough.md` + `{lesson}-walkthrough.drawio` (still **one** `domain.md` for the domain) |


Use a **shared stem** per walkthrough so Markdown and Draw.io stay obviously paired.

---

## Tips for Large Walkthroughs

If a single scenario has **many walks** (e.g., 5+ different message flows):

- **Option 1:** Create **one `.drawio`** per walk (e.g., `step-1-walkthrough-create.drawio`, `step-1-walkthrough-combat.drawio`)
- **Option 2:** Create **one merged `.md`** with all walks, but only extract **critical walks** to `.drawio` (mark non-diagrammed walks with `[Not diagrammed]`)

**Rule:** Keep the pairing obvious (shared stem) and the `.drawio` count manageable (1–3 per major flow).
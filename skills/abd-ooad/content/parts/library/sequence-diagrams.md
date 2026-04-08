# Sequence Diagrams and Walkthroughs (Draw.io and Markdown)

## Templates — use these for every create/update

All walkthrough / sequence work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):

| Role | Template file | When to use it |
|------|----------------|----------------|
| **Draw.io** | `templates/domain realization template.drawio` | **New diagram:** duplicate this file into the workspace, rename, replace `{{placeholders}}`, then edit lifelines and messages. **Existing diagram:** when adding lifelines or messages, keep lifeline alignment, execution bars, and arrow-to-activation conventions as in the template. |
| **Markdown** | `templates/domain walkthrough template.md` | **New companion doc:** copy its scenario / walk / pseudo-code structure. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass so steps and activations stay aligned. |

Optional: add a **Mermaid** `sequenceDiagram` block in the Markdown file for quick preview (GitHub / readers), using **participant names that match** the lifeline headers in the `.drawio` file.

There is **no** `drawio_cli.py` automation for sequence lifelines yet — **always** ground new Draw.io work in `domain realization template.drawio`.

## Terminology (same concept)

These names refer to the **same** kind of artifact:

- **Domain walkthrough**
- **Domain realization**
- **Domain interaction**
- **Sequence diagram**

Use whichever label the user prefers. In deliverables, pick one label per document and stay consistent.

## What to keep in sync

When the user asks to **create or update** modeling diagrams:

| Artifact | Draw.io | Markdown companion |
|----------|---------|-------------------|
| **Sequence / walkthrough** | `*.drawio` (start from `templates/domain realization template.drawio`) | Same structure as `templates/domain walkthrough template.md` |

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

There is **no** `drawio_cli.py` automation for lifelines yet. **New diagrams:** duplicate the template into the workspace (see **Templates** above), replace placeholders, then adjust lifeline heights and messages as needed.

## Sequence / walkthrough — Markdown

**Narrative + pseudo-code** — Follow `templates/domain walkthrough template.md` (required structure; see **Templates** above):
- One **Scenario** block per flow.
- **Walk N: Covers** — scope (what responsibilities this walk exercises).
- Indented pseudo-code showing object creation, calls, returns, and nesting (same story as the Draw.io diagram).

## Creating Sequence Diagrams from Walkthroughs (Step-by-step)

### Step 1: Extract Lifelines from Pseudo-code

Read the walkthrough pseudo-code and identify all **distinct objects/participants**:

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

### Step 2: Translate Pseudo-code to Messages

For each call in the pseudo-code, create a **message arrow** in Draw.io:

| Pseudo-code | Draw.io Message |
|-------------|-----------------|
| `{object}.{method}()` | Synchronous message arrow (filled) from **{object}** to **{collaborator}** labeled `method()` with params |
| `return {value}` | Return arrow (dashed, open) from callee back to caller labeled with `{value}` (if non-void) |
| `{var} = new {Class}()` | Create message (labeled `«new»`) from initiator to the new object's lifeline |
| Nested calls | Stack activation bars (execution rectangles) vertically; nested calls go to the right edge of parent activation |

### Step 3: Align with Template

When creating the `.drawio` file:

1. **Duplicate** `templates/domain realization template.drawio`
2. **Replace placeholder lifelines** with actual participant names from Step 1
3. **Add messages** following the order in the pseudo-code (top to bottom = time flow)
4. **Verify alignment:**
   - All lifelines top-aligned (horizontal line at y=0)
   - All message arrows **horizontal** (0° angle)
   - Message arrows snap to **outer edge of execution bars**, not center lifeline
   - Execution bars centered on lifeline, nested bars stacked right

### Step 4: Keep Markdown ↔ Draw.io in Sync

- **If updating the `.drawio`:** Update the `.md` pseudo-code to match new messages/lifelines
- **If updating the `.md`:** Update the `.drawio` diagram to match new pseudo-code steps
- **Test alignment:** Trace each line of pseudo-code to a message in the diagram; each message should appear in the `.md`

### Example: Character Creation Scenario

**Markdown pseudo-code (Walk 1: Create ability):**
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

| Pair | Example |
|------|---------|
| Model + Walkthrough | `step-1-model.md` (domain model) + `step-1-walkthrough.md` (scenarios & walks) + `step-1-walkthrough.drawio` (sequence diagram) |
| Pattern | `{step-name}-model.md`, `{step-name}-walkthrough.md`, `{step-name}-walkthrough.drawio` |

Use `{step-name}` consistently across all three artifacts so their relationship is obvious.

---

## Tips for Large Walkthroughs

If a single scenario has **many walks** (e.g., 5+ different message flows):

- **Option 1:** Create **one `.drawio`** per walk (e.g., `step-1-walkthrough-create.drawio`, `step-1-walkthrough-combat.drawio`)
- **Option 2:** Create **one merged `.md`** with all walks, but only extract **critical walks** to `.drawio` (mark non-diagrammed walks with `[Not diagrammed]`)

**Rule:** Keep the pairing obvious (shared stem) and the `.drawio` count manageable (1–3 per major flow).
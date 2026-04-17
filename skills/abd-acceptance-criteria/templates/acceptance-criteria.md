# Acceptance criteria (exploration)

<!-- Template migrated from agile_bots story_bot exploration behavior conventions. -->

For each **story**, list **acceptance_criteria** as behavioral outcomes using **WHEN / THEN / AND** (and **BUT** for negative outcomes). Reserve **Given** for **scenarios** (BDD), not for AC in `story-graph.json`.

In **Markdown**, wrap **domain-significant** nouns and short phrases in *italics* — *Title Case* for multi-word concepts (e.g. *Report UI*, *Wire Transfer*). Italicize terms that belong to *your* problem space, not filler or whole sentences. See the skill rule **Emphasize domain-significant terms**.

## Story: `Verb–Noun Title`

**Story type:** user | system | technical

### Acceptance criteria

**Illustrative pattern** (replace names and flows with your domain; keep the *italic* convention for domain terms):

1. **WHEN** *Operator* submits *Settlement File* in *Report UI*  
   **THEN** *Import Job* queues and *Filtered Report Rows* appear in the preview  
   **AND** *Export Job Progress* shows *Running*  
   **BUT** *Settlement Records* are not committed until *Operator* confirms  

**Variant (delta only — atomic rule):**

2. **WHEN** *Settlement File* fails *Schema Validation*  
   **THEN** *Import Job* stops with *Validation Error* summary  
   *(Avoid repeating the same WHEN/THEN/AND block across multiple AC — see atomic AC rule.)*

**Negative / error path:**

3. **WHEN** *Operator* cancels during preview  
   **THEN** queued *Import Job* is discarded  
   **BUT** no *Settlement Records* are written  

---

<!-- Notation below is for skill/template maintainers. Agents MUST NOT copy this section into generated acceptance-criteria.md files in projects. -->

## Instructions (template reference only — omit from generated files)

- Target roughly **4–9** WHEN/THEN-style steps worth of coverage per story (mechanical count uses WHEN + AND lines in combined AC text).
- Use **behavioral** language (user and system outcomes), not implementation (no file formats, APIs, class names) unless framed as `story_type: technical` and kept minimal.
- Prefer **channel-specific** detail where the product has distinct CLI vs Panel vs API surfaces (concrete examples, quoted labels, `cli.` paths).
- **Alternate** user and system steps; avoid long runs of the same actor without switching.
- For **multiple system reactions** in sequence, chain with **AND** rather than a new **WHEN** for each micro-step (unless a genuinely new trigger).
- **Domain emphasis:** in `.md` outputs, *italicize* domain-significant terms only (*Title Case* for multi-word concepts); stay consistent for the same concept across AC. Plain `.txt` has no markdown — use the same vocabulary without asterisks.

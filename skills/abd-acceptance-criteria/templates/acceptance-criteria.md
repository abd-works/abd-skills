# Acceptance criteria (exploration)  
  
<!-- Template migrated from agile_bots story_bot exploration behavior conventions. -->  
  
For each **story**, list **acceptance_criteria** as behavioral outcomes using **WHEN / THEN / AND** (and **BUT** for negative outcomes). Reserve **Given** for **scenarios** (BDD), not for AC in `story-graph.json`.  
  
## Story: `Verb–Noun Title`  
  
**Story type:** user | system | technical  
  
### Acceptance criteria  
  
**Complex flow (multiple reactions):**  
  
1. **WHEN** (trigger or condition)  
   **THEN** (observable outcome)  
   **AND** (additional outcome or chained reaction)  
   **AND** (additional outcome or chained reaction)  
   **BUT** (what does **not** happen — e.g. does not persist, does not allow)  
  
**Variant (delta only — atomic rule):**  
  
2. **WHEN** (variant)  
   **THEN** (only what differs from the general case above)  
   *(Avoid repeating the same WHEN/THEN/AND block across multiple AC — see atomic AC rule.)*  
  
**Negative / error path:**  
  
3. **WHEN** (error path)  
   **THEN** (error or prevention behavior)  
   **BUT** (what does **not** happen — e.g. does not persist, does not allow)  
  
---  
  
## Instructions  
  
- Target roughly **4–9** WHEN/THEN-style steps worth of coverage per story (mechanical count uses WHEN + AND lines in combined AC text).  
- Use **behavioral** language (user and system outcomes), not implementation (no file formats, APIs, class names) unless framed as `story_type: technical` and kept minimal.  
- Prefer **channel-specific** detail where the product has distinct CLI vs Panel vs API surfaces (concrete examples, quoted labels, `cli.` paths).  
- **Alternate** user and system steps; avoid long runs of the same actor without switching.  
- For **multiple system reactions** in sequence, chain with **AND** rather than a new **WHEN** for each micro-step (unless a genuinely new trigger).  

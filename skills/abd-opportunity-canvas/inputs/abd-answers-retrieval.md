# abd-answers retrieval input — abd-opportunity-canvas

**Companion (validation workflow):** **`../abd-simple-validated-learning/`** — assumptions → hypotheses, prioritised **Plan / Validate / Learn**; slides 12–14 below and **`../reference/`** also ground that package.

**Field-level source (complements RAG):** The index often returns only the shared **“why / when”** slide. The **eight-segment** canvas, **guiding questions**, **slides 12–14** (Validated Learning Kanban, uncertainty example, full assumption checklist), and **mapping** to the line-prefix template are in **`../reference/opportunity-canvas-source-materials.md`**, with verbatim **`02 Training/canvas.pptx`** in **`../reference/canvas-pptx-extract.md`** (updated when the PPTX is re-converted). Re-chunk/refresh the embed so retrieval catches those slides, not just slide 6.

## Agent and skill (how this file is produced)

- **Orchestrator:** `agilebydesign-skills/agents/abd-practice-skill-builder/AGENTS.md` — pipeline stage **Retrieve** = **abd-query-practice-sources** only under **`inputs/`** (no **`rules/`** or **`SKILL.md`** edits in that stage).
- **Retrieval skill:** `agilebydesign-skills/agents/abd-practice-skill-builder/skills/abd-query-practice-sources/SKILL.md` — decompose 3–7 short queries, set **`--folders`** when scoping, paste **verbatim** fenced bodies per **Kept chunk**, merge and dedupe.

### `data/assets/01 Agile Practices` vs RAG `--folders`

- **On disk / SharePoint,** source assets often live under a tree like **`data/assets/01 Agile Practices/...`** (see **abd-answers** conversion scripts).
- **In Pinecone,** `memoryFolder` for the Agile Practices embed is the **pipeline relative root** **`01 Agile Practices`**, not `data/assets/...`. The embed entry point is **`abd-answers/scripts/embed-agile-practices-pinecone.ts`** (`AGILE_REL = '01 Agile Practices'`, synced from chunked markdown under that rel).
- **For `npm run rag:query`,** scope Agile Practices with:
  - `--folders "01 Agile Practices"`
  - **not** `--folders "data/assets/01 Agile Practices"` (that string returned **0 chunks** in a test run — it does not match stored `memoryFolder` values).
- **Prefer full pipeline markdown** for each kept row when a mirror file exists; otherwise use the query JSON **body** field / bodyPreview and note truncation.

### Full-index (“weak”) search

- Omit **`--folders`** to search the **entire** default Pinecone namespace (no `memoryFolder` filter) — useful when a topic is sparse or you do not know which asset tree holds it.
- Use **short** or **multi-word** queries (`"opportunity canvas"`, `"exploring opportunity assumptions problem users"`) and raise **`--k`** (e.g. 12–15) to cast a wider semantic net; then **dedupe** repeated slide bodies and **keep** chunks that add new procedure, titles, or notes.

## Coverage and run log

| Run | Command / note | Result |
| --- | --- | --- |
| 1 | `npm run rag:query -- "opportunity canvas" --k 12` (no `--folders`, **abd-answers** root) | **12 hits**; kept chunks 1–4 below (deduped; many slides share the same “Why / When” text). |
| 2 | `npm run rag:query -- "opportunity canvas" --folders "data/assets/01 Agile Practices" --k 12` | **0 chunks** — wrong scope string for `memoryFolder` (see above). |
| 3 | `npm run rag:query -- "opportunity canvas" --folders "01 Agile Practices" --k 12` | **Blocked:** Pinecone **429** (read unit limit for the month). **Re-run** when quota resets to pull **01 Agile Practices**–scoped hits if opportunity-canvas content exists in that tree. |
| 4 | `Jeff Patton opportunity canvas assumptions validation` (no `--folders`) | **429** — read limit. |
| 5 | `npm run rag:query -- "opportunity canvas" --k 15` (full index, **2026-04-25**) | **15 hits**; same dominant slide family as run 1; confirms full-namespace retrieval. |
| 6 | `npm run rag:query -- "exploring opportunity assumptions problem users" --k 12` (full index, **2026-04-25**) | **12 hits**; added distinct **Module 2 — Opportunity Generation and Validation** and **Product Owner Training** slides → kept chunks 5–8. |

- **Manual pass:** With the **abd-answers** repo checked out, read **`data/pipeline/markdown/01 Agile Practices/...`** (or the chunked path your pipeline uses) for opportunity canvas **slides/chunks** and paste **verbatim** into new **Kept chunks** if RAG is unavailable — same **abd-query-practice-sources** shape.

---

## Kept chunks (verbatim)

### Kept chunk 1

- **Chunk title:** Opportunity Canvas Innovation -__slide_07.md
- **Similarity:** 0.8725492655
- **Relevance:** core_concept
- **Relevance note:** Establishes why/when: shared understanding of components, explicit assumptions and validation, accelerated path through uncertainty; when to start the team and align on vision and risks/unknowns/assumptions.
- **Query:** opportunity canvas
- **Rank in result set:** 1

```
<!-- Source: data/assets/06 Client Engagements/Active/EY-OLG/Innovation/Opportunity Canvas Innovation -.pptx, slide 7 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/06%20Client%20Engagements/Active/EY-OLG/Innovation/Opportunity%20Canvas%20Innovation%20-.pptx?csf=1&web=1 -->

<!-- Slide number: 7 -->
# Why should I use an opportunity canvas?
To gain a shared understanding of the key components required to realize an opportunity successfully. Make assumptions, and the activity required to validate those assumptions explicit, to plan an accelerated approach to exploring uncertainty.

![http://jaypgreene.files.wordpress.com/2011/06/confusion.jpg](GoogleShape2055p73.jpg)
When should I use an opportunity canvas?
Build a canvas to help the team get started, align on the vision and quickly organize around key risks / unknowns / assumption to get validated

### Notes:
```

### Kept chunk 2

- **Chunk title:** Opportunity Canvas Innovation -__slide_01.md
- **Similarity:** 0.8672775625
- **Relevance:** glossary
- **Relevance note:** Framing title for the practice as exploring an opportunity with the canvas.
- **Query:** opportunity canvas
- **Rank in result set:** 3

```
<!-- Source: data/assets/06 Client Engagements/Active/EY-OLG/Innovation/Opportunity Canvas Innovation -.pptx, slide 1 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/06%20Client%20Engagements/Active/EY-OLG/Innovation/Opportunity%20Canvas%20Innovation%20-.pptx?csf=1&web=1 -->

<!-- Slide number: 1 -->
# Exploring an Opportunity with the Opportunity Canvas

### Notes:
```

### Kept chunk 3

- **Chunk title:** Opportuniy Canvas__slide_01.md
- **Similarity:** 0.8665390909999999
- **Relevance:** glossary
- **Relevance note:** Alternative deck title: idea shaping and opportunity canvas.
- **Query:** opportunity canvas
- **Rank in result set:** 4

```
<!-- Source: data/assets/06 Client Engagements/Active/EY-OLG/Training/Lab Training/modules/Opportuniy Canvas.pptx, slide 1 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/06%20Client%20Engagements/Active/EY-OLG/Training/Lab%20Training/modules/Opportuniy%20Canvas.pptx?csf=1&web=1 -->

<!-- Slide number: 1 -->
# Idea Shaping and Opportunity Canvas

### Notes:
```

### Kept chunk 4

- **Chunk title:** Master Deck - Honda Agile Leadership Training - January 2021__slide_30.md
- **Similarity:** 0.8659527899999999
- **Relevance:** rule
- **Relevance note:** Speaker notes credit origin (Jeff Patton) and state primary purpose: define/frame the opportunity and gain alignment; body repeats why/when from other slides.
- **Query:** opportunity canvas
- **Rank in result set:** 6

```
<!-- Source: data/assets/06 Client Engagements/Inactive/Honda Canada/Honda Canada - Parts and Service/Training/Master Deck - Honda Agile Leadership Training - January 2021.pptx, slide 30 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/06%20Client%20Engagements/Inactive/Honda%20Canada/Honda%20Canada%20-%20Parts%20and%20Service/Training/Master%20Deck%20-%20Honda%20Agile%20Leadership%20Training%20-%20January%202021.pptx?csf=1&web=1 -->

<!-- Slide number: 30 -->
# Why use an opportunity canvas?
Gain a shared understanding of the key components required to realize an opportunity successfully. Make assumptions, and the activity required to validate those assumptions explicit, to plan an accelerated approach to exploring uncertainty.







When should I use an opportunity canvas?
Build a canvas to help the team get started, align on the vision and quickly organize around key risks / unknowns / assumption to get validated



![http://jaypgreene.files.wordpress.com/2011/06/confusion.jpg](GoogleShape538gb5370ea578_0_700.jpg)

### Notes:
Origin: Jeff Patton
Primary Purpose: define/frame the opportunity - gain alignment
Somet…
```

*Truncation after `Somet…` is as returned by the RAG result body; full notes were not available in the query payload.*

### Kept chunk 5

- **Chunk title:** Module 2 - Opportunity Generation and Validation2018-11-26 16-34-51 PM__slide_21.md
- **Similarity:** 0.804494828
- **Relevance:** procedure
- **Relevance note:** Breakout: validate assumptions, refine canvas, link canvas/story map risks, top 5 mitigation/validation.
- **Query:** exploring opportunity assumptions problem users
- **Rank in result set:** 1

```
<!-- Source: data/assets/02 Training/Complete Agile Curriculum/Individual Agile Training Modules/Module 2 - Opportunity Generation and Validation2018-11-26 16-34-51 PM.pptx, slide 21 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/02%20Training/Complete%20Agile%20Curriculum/Individual%20Agile%20Training%20Modules/Module%202%20-%20Opportunity%20Generation%20and%20Validation2018-11-26%2016-34-51%20PM.pptx?csf=1&web=1 -->

<!-- Slide number: 21 -->
# Breakout Activity

Validate your Assumptions

Refine the opportunity canvas as needed
Extract and prioritize risk / assumptions (from the canvas and / or story map). How would you mitigate / validate the top 5?
‹#›

### Notes:
```

### Kept chunk 6

- **Chunk title:** Module 2 - Opportunity Generation and Validation2018-11-26 16-34-51 PM__slide_05.md
- **Similarity:** 0.7899232805
- **Relevance:** core_concept
- **Relevance note:** “Opportunity model” framing; notes on shared business-model understanding and collaborative opportunity development.
- **Query:** exploring opportunity assumptions problem users
- **Rank in result set:** 6

```
<!-- Source: data/assets/02 Training/Complete Agile Curriculum/Individual Agile Training Modules/Module 2 - Opportunity Generation and Validation2018-11-26 16-34-51 PM.pptx, slide 5 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/02%20Training/Complete%20Agile%20Curriculum/Individual%20Agile%20Training%20Modules/Module%202%20-%20Opportunity%20Generation%20and%20Validation2018-11-26%2016-34-51%20PM.pptx?csf=1&web=1 -->

<!-- Slide number: 5 -->
# What is an Opportunity Model?

![](GoogleShape247p69.jpg)
‹#›

### Notes:
A lot of smart people talking but not understanding each other – lacking a shared understanding of what is a Business Model

Ability to facilitate a collaborative and innovative method to develop opportunity models for the 21st Centenary
```

### Kept chunk 7

- **Chunk title:** Product Owner Training v1.5__slide_21.md
- **Similarity:** 0.7937453685
- **Relevance:** procedure
- **Relevance note:** Chapter title “Exploring an Opportunity with the Opportunity Canvas”; speaker note on rethinking delivery / Agile.
- **Query:** exploring opportunity assumptions problem users
- **Rank in result set:** 3

```
<!-- Source: data/assets/02 Training/Client Specific/Wealth/Product Owner Training v1.5.pptx, slide 21 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/02%20Training/Client%20Specific/Wealth/Product%20Owner%20Training%20v1.5.pptx?csf=1&web=1 -->

<!-- Slide number: 21 -->
Chapter 2: Exploring an Opportunity with the Opportunity Canvas

### Notes:
Given these points there’s a need to rethink our delivery model.

Agile has come out as a way to improve delivery
```

*Notes may be truncated in the RAG payload; re-open the source slide for the full note block if needed.*

### Kept chunk 8

- **Chunk title:** GENERIC - Product Owner Training__slide_37.md
- **Similarity:** 0.790174186
- **Relevance:** glossary
- **Relevance note:** Section heading for the canvas in a Product Owner course deck.
- **Query:** exploring opportunity assumptions problem users
- **Rank in result set:** 5

```
<!-- Source: data/assets/06 Client Engagements/Inactive/CPAO/Other Reference Docs/GENERIC - Product Owner Training.pptx, slide 37 | https://agilebydesigncanada.sharepoint.com/sites/AgileByDesign/Shared%20Documents/Assets/06%20Client%20Engagements/Inactive/CPAO/Other%20Reference%20Docs/GENERIC%20-%20Product%20Owner%20Training.pptx?csf=1&web=1 -->

<!-- Slide number: 37 -->
# EXPLORING AN OPPORTUNITY WITH THE OPPORTUNITY CANVAS
37
```

## Optional: machine trail

```json
{
  "ragRef": "pinecone://abd-answers/abd-answers",
  "runs": [
    { "query": "opportunity canvas", "k": 12, "folders": null, "result": "12 chunks" },
    { "query": "opportunity canvas", "k": 12, "folders": ["data/assets/01 Agile Practices"], "result": "0 chunks" },
    { "query": "opportunity canvas", "k": 12, "folders": ["01 Agile Practices"], "result": "429" },
    { "query": "Jeff Patton opportunity canvas assumptions validation", "result": "429" },
    { "query": "opportunity canvas", "k": 15, "folders": null, "result": "15 chunks" },
    { "query": "exploring opportunity assumptions problem users", "k": 12, "folders": null, "result": "12 chunks" }
  ]
}
```

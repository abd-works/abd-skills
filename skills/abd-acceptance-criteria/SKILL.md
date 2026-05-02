---
name: abd-acceptance-criteria
catalog_garden_tier: practice
catalog_garden_order: 30
catalogue_one_liner: >-
  WHEN/THEN acceptance criteria for story-graph.json; ships rules and scanners for execute-skill-using-skills-rules.
description: >-
  Teaches exploration-phase acceptance criteria for story-graph.json: WHEN/THEN/AND/BUT,
  behavioral language, per-story domain terms, atomic AC, actor alternation, channel-specific detail, and
  verb–noun naming for story elements. Ships Markdown rules and Python scanners under this
  skill root for **execute-skill-using-skills-rules** (mechanical checks alongside human review).
  When building AC from sources, output **all** template artifacts in `templates/`
  (currently `acceptance-criteria.md` and `acceptance-criteria.txt`) with the same coverage.
  Use when writing or reviewing acceptance criteria, exploration behavior, WHEN/THEN
  quality, or story-graph.json AC arrays.
---
# abd-acceptance-criteria

## Purpose

Build acceptance criteria per **story**, that explain what must be true when users and systems interact: observable triggers (**WHEN**), expected outcomes (**THEN**), chained effects (**AND**), and explicit negatives (**BUT**). These act as informal first-draft BDD-style steps that guide downstream scenario work. Focus on interactions using domain terms, avoid implementation detail unless the story is technical, and even then keep it minimal.

This skill is the **practice standard** for that work: **templates** for deliverables, **rules** for what “good” means (atomic AC, actor alternation, domain emphasis, channel-specific detail, **source evidence** when AC come from documents), and **scanners** that can run predictable mechanical checks **alongside** human review.

## When to use this skill

Load this skill when **any** of the following apply:

- You are writing or reviewing **`acceptance_criteria`** arrays on stories in **`story-graph.json`** (exploration phase — not scenario BDD steps).
- A user or agent wants to turn interviews, requirements documentation, or informal notes into **concrete behavioral** AC (WHEN/THEN/AND/BUT).
- You need to document user and system interaction at a finer grain , but still pre-specification / test case level of detail.eg: linear **WHEN {action user},THEN {system response}, AND {another system response}, BUT {systems reaction that won't happen}** 
- An agent is asked to “explore” a story, “write AC”, “harden acceptance criteria”, or “align with exploration rules.”
---

## Agent Instructions

1. **Templates**
   Generate content using **every** template file in this skill’s `templates/` folder.
**Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT per **Core concepts** and **The shape of good acceptance criteria** below. Per story, include a **Domain terms** section (see template): key words and phrases for concepts, state, actions, and rules used in that story’s AC. **Source traceability:** each numbered AC must cite **Evidence** (chapter, section, page, paragraph, chunk id, etc.) or a per-story **Source evidence** table—see template. Optional title or short context at the top is fine. **Do not** paste the template’s `## Instructions` section (or an equivalent rules summary) into generated project files — that material documents the template for skill maintainers, not stakeholders reading the criteria. |
| `templates/acceptance-criteria.txt` | The **same** behavioral coverage, story semantics, **domain terms list**, and **source evidence** as **plain text** only — structure matching `acceptance-criteria.txt` style. |

**Consistency:** WHEN/THEN semantics, story coverage, **domain terms** (same vocabulary; italics only in `.md` AC lines and domain list if you italicize there), **source evidence per AC**, and ordering must match between `.md` and `.txt` for the same work. Generated artifacts contain **only** stakeholder-facing sections from the templates (plus optional brief context); notation and heuristics stay in this skill and in `templates/` for reference.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

When you **create or rewrite** acceptance criteria from requirements, you **must** deliver **one output artifact per file** in `templates/`. 


2. **Rules**
- Generate content following rules attached to this skill, listed below, assembled from rule files in `rules/`.
- Validate - once content is generated, take on the role of a *Peer Reviewer*  and validate that the content is correct by going through each of the skills rules one at a time and looking deeply for violations. Be helpful but critccal - compare contenct againstg each rules constraints, DO/DON’T sections and examples.


3. **Assembling this Skill**
This Skill file is  assembled from all template files  `templates/` and all rules in `rules/`. Use **`bundle_rules_into_skill_md.py`** to reassemble this skill. When ever rules or templates change.


2. **Validate** using rules mentioned in this skill.


---

## What are acceptance criteria?

**Acceptance criteria** (in this skill’s sense) are **story-level, behavioral statements** in `story-graph.json` that say **under what conditions** the product behaves **how**, including chained outcomes and explicit negatives. They sit **above** BDD **scenarios** (which use Given/When/Then on steps).

Exploration-phase AC answer four questions for each story:

1. **When** does the behavior apply? (trigger, precondition, or variant.)
2. **Then** what is observable? (primary user- or system-visible outcome.)
3. **And** what else happens in sequence? (extra outcomes, especially multiple system reactions — chain with AND, not a new WHEN for each micro-step unless the trigger truly changes.)
4. **But** what must **not** happen? (errors, prevention, no persistence — negative paths.)

They are **not** implementation checklists (API names, class names, file formats) unless the story is explicitly **`story_type: technical`** and scoped that way. A good AC set can be read by a **product owner**, a **tester**, and a **developer** — all at once — and still be **machine-checkable** via rules/scanners where applicable.

**Relationship to other artifacts:**

| Artifact | Role | Typical keywords |
| --- | --- | --- |
| **acceptance_criteria** (this skill) | Story-level outcomes in the graph | WHEN, THEN, AND, BUT |
| **scenarios** (later / other workflow) | BDD flows with steps | Given, When, Then on **steps** |

Reserve **Given** for **scenarios**, not for lines inside **`acceptance_criteria`** (exploration convention).

---

## Core concepts

### Step

AC describe **observable** user/system behavior in steps. Avoid implementation detail unless the story is explicitly technical.

- **WHEN** sets scope; **THEN** is the main observable; 
- **AND** chains extra outcomes; 
- **BUT** guards negatives.
- Second AC is a **delta** (error or other path), not a full repeat of the happy path.
- Language stays **behavioral**,  **channel-aware** where the product has distinct surfaces, and **system aware** when interacting with multiple system actors


- **Prefer** language a product owner can rehearse: who did what, on which surface, and what anyone can see or verify next. Example: WHEN the user submits the settlement file on the import screen, THEN the preview lists the filtered rows and the job status reads *Running*.
- **Prefer** channel-specific detail when the product has more than one surface—real CLI paths (e.g. `cli.shape.validate`), quoted control labels, or API-visible outcomes—so testers know *where* to look. That is not the same as naming internal classes or private methods.
- **Avoid** vague reassurance (“the system handles it”) with no observable signal, and avoid code-shaped triggers (`CliSession.submit()` unless the story is explicitly technical and scoped that way).

### Domain terms (vocabulary in AC)

**Domain terms** are words or short phrases that name the important ideas in the problem space: things (*Settlement File*, *Import Job*), their **state** (*Queued*, *Committed*), **actions** (*Confirm import*), and **rules or constraints** (*Schema Validation*, *Transactional Limit*). They align story AC with how stakeholders talk and with how tests will read—part of a shared **ubiquitous language**.

- Each story includes a **Domain terms** subsection **before** its acceptance criteria (see template and **Example**). Keep the list tight: only terms that anchor that story’s AC.
- In **`acceptance-criteria.md`**, use *italics* and *Title Case* inside multi-word phrases in the Domain terms list and in AC lines. Reuse the same italicized phrase for the same concept. See **Emphasize domain-significant terms** in the bundled rules.
- In the paired **`.txt`** artifact, use the **same words** with no markdown.
- Do not italicize filler, whole sentences, or low-signal words; spotlight **domain meaning**, not decoration.

### WHEN / THEN / AND / BUT

- **WHEN:** Trigger or precondition—the event or situation that starts this slice of behavior.
- **THEN:** Primary outcome—what becomes true or visible first.
- **AND:** More outcomes in the same beat—especially a second or third **system** reaction—without inventing a new trigger (see **Use AND for multiple reactions**).
- **BUT:** What **does not** happen—errors, prevention, or “no write” guarantees on negative paths.

### Atomic AC

State the **general** case **once**; follow-on AC only describe **deltas**. Reduces duplicated WHEN/THEN blocks (see **Atomic acceptance criteria** rule).

### Actor alternation

Interleave user-visible and system-visible emphasis. Avoid long runs of the same actor without switching (see **Alternate actors in steps** rule + scanner).

### Domain consistency

As domains grow, keep **parallel** AC structure across related areas; **split stories** when one AC mixes incompatible domain behaviors.

---

### Pitfalls for agents

**Don’t fabricate to fill gaps.** When context is incomplete — a business rule is unclear, a system interaction is unknown, a domain term has no definition — do not invent AC to cover the gap. Instead, capture the unknown explicitly: record what is missing, what assumption you are making, and what validation action would resolve it (e.g. “confirm with SME whether failed payments retry automatically or require manual re-submission”). Unknowns surfaced are more valuable than plausible-sounding AC that turn out to be wrong.

**Identify missing context dimensions.** Before writing AC, assess whether the available context covers the perspectives needed: business logic, technical constraints, operational concerns, regulatory or compliance requirements, and user experience. If an entire dimension is absent (e.g. no technical input on system-to-system behaviour, or no business rules for edge cases), flag it. Writing AC from a single perspective produces AC that will churn when the missing perspective surfaces later.

---

## Example

**Story:** Export Report To PDF  
**Story type:** user  

**Domain terms** (vocabulary for this story’s AC—things, state, actions, rules):

- *Report UI* — screen where the user runs the report and starts export  
- *Export a PDF* — user-triggered action for this flow  
- *Export Job Progress* — visible status while the export runs  
- *Filtered Report Data* — row set after filters; input to the PDF  
- *Report Export* — the delivered artifact / job outcome the user waits on  
- *Download* — completed file handoff to the user  
- *Zero Rows* / *Filters* — empty result after filtering; edge case  
- *Feedback* / *Nothing To Export* — user-visible outcome when there is nothing to build  
- *Report Export Service* — downstream dependency; failure mode  
- *Retry* — user-visible recovery path  
- *Partial* / *Empty File* — invalid success shapes to reject  

1. **WHEN** the user chooses to *Export a PDF* on the *Report UI*  
   **THEN** the *Report UI* indicates *Export Job Progress*  
   **AND** the system builds a *PDF* from the current *Filtered Report Data*  
   **AND** the user gets a normal completed *Download* for that *Report Export*  

2. **WHEN** the *Report* has *Zero Rows* after *Filters*  
   **THEN** the user sees clear *Feedback* that there is *Nothing To Export*  
   **BUT** no *PDF* is created and no *Download* starts  

3. **WHEN** the *Report Export Service* is unavailable  
   **THEN** the user sees that *Report Export* failed and can *Retry* later  
   **BUT** no *Partial* or *Empty File* is treated as a successful *Report Export*  

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Alternate actors in steps

**Scanner:** `scanners/actor-alternation-scanner.py` — **`ActorAlternationScanner`**

Alternate between actors every 1–2 steps. Show back-and-forth between user and system. System may chain 1–2 sequential actions before returning to the user.

#### DO

- When the actor acts, the system responds; when the system completes, the user reacts (or the system continues briefly).
- Allow short system chains (e.g. validate → save) before the next user-visible step.

#### DON'T

- Run more than **two** consecutive steps from the same actor without switching (warning heuristic in scanner).
- Stack many user-only lines without system response.

### Rule: Behavioral AC at story level

**Scanner:** `scanners/behavioral-ac-scanner.py` — **`BehavioralACScanner`**

Behavioral AC belongs at story level in `story-graph.json`. Use When/Then format (**no Given** in AC — reserve Given for scenarios). AC should describe behavioral outcomes, not technical implementation.

#### DO

- Use behavioral language for user actions and system responses.
- Focus on observable outcomes and system responses.
- WHEN/THEN/AND may appear as separate lines in structured AC entries.

#### DON'T

- Use technical implementation terms (config, json, api, sql, class, method) as the primary description.
- Use programming, database, or raw API terminology in place of behavior.

### Rule: Emphasize domain-significant terms

**Scanner:** Manual review (no automated scanner)

Call out **domain language** — the nouns, verbs, and short phrases that belong to the problem space and show up in stories, tests, and talk with stakeholders — so readers see what is *specific* to this product versus generic wording.

#### DO

- Wrap domain-significant terms in *italics*.
- Use *title-style capitalization* inside those phrases for multi-word concepts (e.g. *Report UI*, *Export Job Progress*, *Filtered Report Rows*). Keep acronyms and product names in their normal form (e.g. *PDF*).
- Apply emphasis consistently for the same concept across AC in a story.
- Prefer this pattern over **exact** quoted UI copy unless the literal string is required for a contract or compliance check.

#### DON'T

- Italicize filler or purely grammatical words, or entire sentences.
- Use emphasis as decoration on every line — only mark terms that carry domain meaning.
- Replace behavioral clarity with a wall of highlighted words; if everything is emphasized, nothing is.

### Rule: Enumerate all AC permutations

**Scanner:** `scanners/enumerate-ac-permutations-scanner.py` — **`EnumerateACPermutationsScanner`** (policy; mechanical pass is currently a no-op)

Enumerate **all** important acceptance criteria permutations: validation paths, calculation branches, happy path, errors, boundaries.

#### DO

- Cover validation paths explicitly.
- Include happy path, error path, and edge cases.
- Cover calculation branches where applicable.

#### DON'T

- Skip permutations (e.g. only happy path).
- Assume a single path when multiple outcomes exist.

### Rule: Keep AC consistent across connected domains

**Scanner:** `scanners/ac-domain-crossing-scanner.py` — **`ACDomainCrossingScanner`**

At small scale, AC can cover multiple domain objects. As behaviors diverge, scope AC to one domain and keep **structure** parallel across related domains. AC that mixes multiple domain behaviors signals **split the story**.

#### DO

- Keep parallel structure for parallel domains (same depth and pattern).
- Split when one AC mixes distinct domain behaviors that deserve separate stories.

#### DON'T

- Mix unrelated domain validations in one giant AC when at scale.
- Use inconsistent depth across connected domains without reason.

### Rule: Stories have 4–9 acceptance criteria (heuristic)

**Scanner:** `scanners/story-sizing-scanner.py` — **`StorySizingScanner`**

Stories should have enough acceptance criteria to reflect thorough exploration. The **mechanical** scanner counts **WHEN** + **AND** tokens across all AC text (see `scanners/story-sizing-scanner.py`). Target band in JSON: **4–9**; the scanner may use a **4–10** band — treat JSON as product intent and align the scanner when reconciling.

#### DO

- Target enough AC to cover the behavior (happy path, errors, edges).
- Split stories that grow too large.
- Expand under-explored stories.

#### DON'T

- Pad with trivial or redundant AC.
- Leave stories severely under-specified or monolithic.

### Rule: Use AND for multiple reactions

**Scanner:** `scanners/reaction-chaining-scanner.py` — **`ReactionChainingScanner`**

Chain sequential **system** reactions with **AND** under the same trigger. Avoid separate **WHEN** for each micro-step when the trigger is the same. Limit **AND** chains to a reasonable length (scanner warns when excessive).

#### DO

- Chain related system outcomes with AND.

#### DON'T

- Use separate WHEN/THEN pairs for sequential system-only actions that belong to one reaction chain.

### Rule: Atomic acceptance criteria

**Scanner:** `scanners/atomic-ac-scanner.py` — **`AtomicACScanner`**

Write atomic acceptance criteria. Avoid repeating common WHEN/THEN/AND blocks across multiple AC. State the general case once; additional AC should only state what differs.

#### DO

- State general behavior once in the first acceptance criteria.
- Variations only state what differs from the general case.
- Edge cases state only the edge behavior.
- Use "see previous" only when unavoidable (should be rare).

#### DON'T

- Repeat the same base logic across multiple acceptance criteria.
- Make variations repeat the full acceptance criteria text.

### Rule: Use BUT for negative conditions

**Scanner:** `scanners/negative-conditions-scanner.py` — **`NegativeConditionsScanner`**

When outcomes describe errors, validation failure, or prevention, include a **BUT** step stating what does **not** happen (e.g. does not save, does not allow).

#### DO

- Add BUT when error/prevention language appears and a negative outcome needs to be explicit.

#### DON'T

- Describe error outcomes without clarifying what is withheld or blocked.

### Rule: Use channel-specific language

**Scanner:** `scanners/channel-specific-language-scanner.py` — **`ChannelSpecificLanguageScanner`**

Prefer concrete CLI, Panel, or API surface detail over generic "Bot/System" wording when the product has distinct channels.

#### DO

- Include concrete examples: `cli.` paths, quoted UI labels, explicit panel copy.

#### DON'T

- Rely on generic "Bot …" steps without concrete syntax or UI cues (scanner warns).

### Rule: Verb–noun format for story elements

**Scanner:** `scanners/verb-noun-scanner.py` — **`VerbNounScanner`**

Use verb–noun format for **epic, sub-epic, and story names** (and align scenario/AC phrasing with the same bar). Prefer **base verb forms**; document actors separately (`story_type`, metadata).

#### DO

- Verb + noun for scenario sentences and AC phrasing where applicable.
- Base verb forms (imperative / infinitive style): Select item, Display confirmation.

#### DON'T

- Noun-only or capability labels where an action phrase is expected.
- Gerund-led titles (`Submitting order`) or third-person singular as the wrong pattern (`Selects item`).
<!-- execute_rules:bundle_rules:end -->

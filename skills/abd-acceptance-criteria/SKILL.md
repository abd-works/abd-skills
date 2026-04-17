---
name: abd-acceptance-criteria
description: >-
  Teaches exploration-phase acceptance criteria for story-graph.json: WHEN/THEN/AND/BUT,
  behavioral language, atomic AC, actor alternation, channel-specific detail, and
  verb–noun naming for story elements. Ships Markdown rules and Python scanners under this
  skill root for **execute_rules** (mechanical checks alongside human review).
  When building AC from sources, output **all** template artifacts in `templates/`
  (currently `acceptance-criteria.md` and `acceptance-criteria.txt`) with the same coverage.
  Use when writing or reviewing acceptance criteria, exploration behavior, WHEN/THEN
  quality, or story-graph.json AC arrays.
---
# abd-acceptance-criteria

## Steps

1. **Build** using **every** template file in this skill's `templates/` folder, and the `rules/` mentioned in this skill.
2. **Validate** using rules mentioned in this skill. For the **mechanical** scanner pass, use the **execute_rules** skill (same repo): run **`run_scanners.py`** with **`--skill-root`** = this skill directory and **`--workspace`** = the tree that contains **`docs/story/story-graph.json`** (or **`story-graph.json`**). To **list** which scanners would run, use **`rule_inventory.py --list-scanners`** with the same **`--skill-root`**. Full intent (AI/rules pass **plus** scanner pass) and exact commands are in **`skills/execute_using_rules/SKILL.md`** (Commands **§2** and **§3** where applicable). Implementation notes live in `scanners/README.md` when present. **Which** scanners run is defined only by **`rules/*.md`** (`scanner:` frontmatter → `scanners/<stem>-scanner.py`), not a separate manifest. **Story graph** types (`StoryMap`, `StoryScanner`, …) live in **`skills/story-graph-ops/scripts/`** (`story_map.py`, `story_scanner.py`, …); generic scanner types come from **`execute_using_rules`** **`scanner_bases`**. **`scanner_runner`** (execute_rules) drives every scanner CLI the same way (context holds files and/or graph JSON). For **CLI** read/search/filter/write on `story-graph.json` without the bot, use **`skills/story-graph-ops/`** (**story-graph-ops** skill).

### Use every template file (required)

When you **create or rewrite** acceptance criteria from requirements, you **must** deliver **one output artifact per file** in `templates/`. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

| Template | What to produce |
| --- | --- |
| `templates/acceptance-criteria.md` | Story-level AC using WHEN/THEN/AND/BUT; include the **`## Instructions`** block from that template file at the end of the Markdown artifact (or equivalent rules summary). |
| `templates/acceptance-criteria.txt` | The **same** behavioral coverage and story semantics as **plain text** only — structure matching `acceptance-criteria.txt` style (no requirement to duplicate the full Instructions block in `.txt`). |

**Consistency:** WHEN/THEN semantics, story coverage, and ordering must match between `.md` and `.txt` for the same work. Only the Markdown file carries the full Instructions block.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

**Purpose:** Describe what good **exploration-phase** acceptance criteria *are* (structure, language, rules). **How** to run the bot, workspace setup, and product-specific exploration flows belong in the agent and other skills — not here.

**Includes:** `templates/` — see **Use every template file** above; `rules/` — authoritative rule files (inlined into **SKILL.md** between the bundle markers; refresh with **`bundle_rules_into_skill_md.py`** — see **`skills/execute_using_rules/SKILL.md`**).

---

## When to use this skill

Load this skill when **any** of the following apply:

- You are writing or reviewing **`acceptance_criteria`** arrays on stories in **`story-graph.json`** (exploration phase — not scenario BDD steps).
- A user or agent wants to turn interviews, specs, or informal notes into **testable behavioral** AC (WHEN/THEN/AND/BUT).
- You need **WHEN/THEN/AND** quality, **atomic** AC (no duplicated blocks), **actor alternation**, **BUT** for negatives, or **channel-specific** CLI/Panel wording.
- An agent is asked to “explore” a story, “write AC”, “harden acceptance criteria”, or “align with exploration rules.”
- You are running **execute_rules** scanners against a workspace that contains a story graph.
- You want **parallel quality** with **abd-story-mapping** on **verb–noun** story elements while this skill owns exploration AC rules and scanners.

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

### Behavioral vs technical

AC describe **observable** user/system behavior. Avoid implementation detail unless the story is explicitly technical.

| Prefer | Avoid (unless technical story) |
| --- | --- |
| “WHEN user submits … THEN CLI returns success with timestamp” | “WHEN `submit()` is called on `CliSession`…” |
| Concrete channels: `cli.shape.validate`, Panel label text | Generic “the bot does the right thing” |

### WHEN / THEN / AND / BUT

| Keyword | Role |
| --- | --- |
| **WHEN** | Trigger or precondition. |
| **THEN** | Primary outcome. |
| **AND** | Additional or chained outcomes (especially multiple system reactions). |
| **BUT** | What does **not** happen (error/prevention paths). |

### Atomic AC

State the **general** case **once**; follow-on AC only describe **deltas**. Reduces duplicated WHEN/THEN blocks (see **Atomic acceptance criteria** rule).

### Actor alternation

Interleave user-visible and system-visible emphasis. Avoid long runs of the same actor without switching (see **Alternate actors in steps** rule + scanner).

### Domain consistency

As domains grow, keep **parallel** AC structure across related areas; **split stories** when one AC mixes incompatible domain behaviors.

---

## The shape of good acceptance criteria

```
Story: Submit Order
  acceptance_criteria:
  1. WHEN user has items in cart AND cart total is valid
     THEN checkout shows confirmation
     AND order id is displayed
  2. WHEN payment gateway times out
     THEN user sees retry message
     BUT order is not marked paid
```

Notice:

- **WHEN** sets scope; **THEN** is the main observable; **AND** chains extra outcomes; **BUT** guards negatives.
- Second AC is a **delta** (error path), not a full repeat of the happy path.
- Language stays **behavioral** and **channel-aware** where the product has distinct surfaces.

---

## Build

Produce **both** **`acceptance-criteria.md`** and **`acceptance-criteria.txt`** artifacts (same coverage), following **`templates/acceptance-criteria.md`** and **`templates/acceptance-criteria.txt`** respectively. See **Steps → Use every template file** — delivering a single format is incorrect unless the user explicitly requested only one. Match the bar under **Validate** below. Structure follows **WHEN/THEN/AND/BUT** and **atomic** deltas as above; keep discovery to **story-level** AC unless a later workflow adds or edits **scenarios**.

---

## Validate

Review **both** the **`.md`** and **`.txt`** and the story graph for:

- **Structure** — WHEN/THEN/AND/BUT used appropriately; **Given** not used inside `acceptance_criteria`.
- **Behavioral** language and **channel-specific** detail where CLI vs Panel differ.
- **Atomic** AC (no duplicated base WHEN/THEN blocks).
- **Actor** alternation and **AND** chaining for sequential reactions.
- **Verb–noun** names for epics/sub-epics/stories (shared bar with **abd-story-mapping**; this skill includes the **verb–noun** scanner).

Revise until a product owner, a tester, and a developer can agree on what “done” means for the story.

Run mechanical scanners via **execute_rules** as described in **Steps**.

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

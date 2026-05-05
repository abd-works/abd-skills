---
name: abd-author-practice-skill
description: >-
  Turn collected hub evidence into a finished practice skill: clear instructions and
  checkable do-and-don't norms that stay true to what you retrieved.
---
# abd-author-practice-skill

## Purpose

Teams need **practice skills** that people and agents can follow without improvising or drifting away from what the sources actually say. This authoring skill helps you **finish** such a package after you have already chosen what to keep from the hub: the teaching on the skill page reads clearly, and the norms on the outputs are explicit enough to pass or fail. It guides you from that evidence to aligned prose and checks. **Prerequisites**, **Build**, and **Not in this pass** on this page carry retrieval, bundling, and scanner wiring when you need those steps.

## When to use

- You **already gathered** the hub material for a practice and want to **produce the skill** itself—not run more searches.
- The practice is still a **rough draft** and you want it **finished**: readable instructions and **explicit** what-to-do / what-not-to-do norms.
- You care that the **finished guidance matches** what you collected, without invented process or hand-waving.

## Not in this pass

Wiring **Python scanners** on the **target** package belongs in a **later** pass, and only after **`scanners/*.py`** exist for any **`scanner:`** you add to rules.

## Prerequisites

- **Target:** `agilebydesign-skills/skills/<skill-name>/` (the practice package you are finishing, not this authoring skill).
- **`inputs/abd-answers-retrieval.md`** — every **Kept chunk** has a verbatim fenced **body** plus **Relevance**, query, rank, and source (see **abd-query-practice-sources**); legacy summary-only tables are not enough.
- **`SKILL.md`** — may be missing or still full of **`{{PLACEHOLDER}}`** until you finish authoring; if it is missing, start from **`templates/SKILL_template.md`** in this skill (see **Build**, item 1).

## Core concepts (for the target package)

### Practice skill

A **practice skill** is the packaged method—the artifact readers open when they want to perform this practice. It should let a person or agent follow the method **without inventing steps** and recognize **when** this practice is the right tool. Open with purpose and fit, then carry the method through procedures, examples, promised outputs when the practice has them, and a clear validation mindset. Keep mechanics and file paths out of that opening voice; they belong in later parts of the same document. **Purpose** on the target page should be **one** short paragraph about **why** the practice exists and what it helps people do, not a runbook for paths and tooling (bundled **Opening sections give outcomes not package mechanics**).

### Rules

**Normative rules** exist so the practice does not dissolve into taste and improvisation. They answer: *would we accept this concrete output as “good enough” for this method?* Without that shared bar, every run of an agent (or every reviewer) reinvents quality, outputs stop being comparable, and the package quietly drifts away from what the sources actually support. Rules are how you make **quality legible** and **repeatable**.

**Build** in **`SKILL.md`** carries **step order** and the main teaching voice. **Rules** under **`rules/*.md`** judge **real artifacts** — a filled template, a section of a file, a pattern in text — with explicit **pass** and **fail**. Same package, two jobs: **Build** walks the method; **rules** say whether the outputs meet the bar.

Each rule should read like a **small spec**: what must hold for **pass**, what counts as **fail**, with enough concrete examples that nobody has to guess. Hub-backed lines trace to **`inputs/abd-answers-retrieval.md`** when provenance matters. The full shape is in the bundled **Target rule files are checkable specs for named artifacts**; per-bullet examples are required by **Rule DOs and DON'Ts must each have examples**.

**Where it shows up on disk:** the **target** practice keeps those checks in **`rules/*.md`**. When you author with **abd-author-practice-skill**, the bundled habits at the end of this file also cover **how** to name rule files and open them (**Rules named after valid or invalid state**, **Rules open with plain pass-and-fail prose**) on top of that target shape. The **`rules/*.md`** that ship **inside this authoring skill** must stay **practice-agnostic**; anything that only fits one method (one map’s prefixes, one board layout, one hypothesis shape) belongs under **`skills/<that-practice>/rules/`** and that practice’s **`templates/`**, not here.

### Template

A **template** is a fixed output shape the practice promises—usually a file under **`templates/`**—that practitioners complete when they apply the method. It should make deliverables **comparable**, **complete**, and **easy to find**, and the skill should name every template shape it expects without ambiguity. When the skill names a template, either ship that file (filled or sensibly minimal), defer it in the skill text with a stated reason, or remove it from what the skill promises so scope stays honest. The starter **`SKILL_template.md`** in **abd-author-practice-skill** is a **parameterized seed**: it keeps **`{{PLACEHOLDER}}`** slots until you replace them and includes a short **filled example** (fictional practice) for tone; delete that example section from the copied **`SKILL.md`** once the real opening is written.

### Sections and rules

**`SKILL.md`** carries **teaching and workflow order**. The **Core concepts** block (or the skill’s main idea section) is the **meaning layer**: how the parts of the practice relate — goals, actors, behaviours, options, metrics, phasing, and similar — in plain language. **`rules/*.md`** are the **check layer** on real artifacts: pass/fail on outputs (phrasing, shape, trace, assumptions, and the like) — see bundled **Target rule files are checkable specs for named artifacts**. **Build** sequences the work; **rules** define acceptable output. The same split appears in skills such as **abd-story-mapping** and **abd-specification-by-example**.

## Build

Work on **one** practice under **`skills/<skill-name>/`**. The **quality bar** for that package is the bundled rules at the end of this file. Follow these items **in order**; they spell out the same work as the quick reference below, but in full sentences.

When you **maintain `abd-author-practice-skill`**, keep its bundled **`rules/`** generic for **any** practice; move or add method-specific checks only on the **target** skill under **`skills/<skill-name>/`** (see **Core concepts**, **Rules**, **Author-kit scope**).

1. **Create a starter skill page when the target has none yet.** If **`SKILL.md`** is not there, copy **`templates/SKILL_template.md`** from **abd-author-practice-skill** into the target folder, create empty **`rules/`**, **`templates/`**, and **`ide-files/`**, and set the YAML **`name`** and **`description`**. The file you copy is a **skeleton plus one filled example block** (fictional practice) for tone; remove that example section after your real **Purpose** and **When to use** are in place. Immediately after the frontmatter, add the **Manual:** line that points at **`./manual/index.html`**, and keep the **`<!-- execute_rules:bundle_rules:begin/end -->`** markers at the end of the file with nothing between them until real **`rules/*.md`** exist and you have run the bundle script. Also scaffold **`ide-files/`** and the deployable IDE files there (see step 8). If **`SKILL.md`** already exists, skip this step.

2. **Read the bundled rules as the contract for the target.** Scroll to the rule block at the bottom of **this** file. Those **DO** / **DO NOT** / **Examples** are what “done” means for how the **target** practice should read and how its **`rules/*.md`** should behave.

3. **Map hub evidence to the right parts of the target skill page.** Use the **Relevance** tag on each **Kept chunk** in **`inputs/abd-answers-retrieval.md`**: treat **`core_concept`** and **`glossary`** chunks as fuel for opening sections; **`procedure`** and **`rule`** for how-to and **Validate**-style checks; **`example`** for examples and template hints; **`diagram_ref`** for manual or figure notes. Do not add **`scanners/*.py`** in this pass.

4. **Rewrite the target `SKILL.md` for human readers.** Replace placeholder voice with plain **Purpose** and **When to use**, then procedures and examples. Where you claim something is hub-backed, cite retrieval row and source when that helps a reviewer. Either fill every **`{{PLACEHOLDER}}`**, defer it in writing with a reason, or narrow what the skill promises.

5. **Author `rules/*.md` on the target as output validators.** Each file targets a **named artifact**; every **DO** must be **decidable** from that artifact without extra context. Keep **step order** in **Build** in **`SKILL.md`**, not in rules. Every normative file needs **`## DO`**, **`## DO NOT`**, per-bullet **Example (pass)** / **Example (fail)** as in the bundled **Rule DOs and DON'Ts must each have examples**, plus enough condition text to mark pass vs fail. Point **`Source:`** at **`inputs/abd-answers-retrieval.md`** only for **hub-backed** lines; do not fake hub sources for chat-only norms. Add **`scanner:`** in front matter only if **`scanners/<stem>-scanner.py`** already exists on that package (see bundled **Target rule files are checkable specs for named artifacts**).

6. **Bundle the target skill so the inlined rules match disk.** From the **agilebydesign-skills** repository root, run **`bundle_rules_into_skill_md.py`** with **`--skill-root skills/<skill-name>`** so **`SKILL.md`** on the target reflects every change under **`rules/`**.

7. **Inspect the package instead of rewriting it from scratch.** Walk the **Validate** checklist in this file against the **target** folder, fix drift and weak spots, and stop when a careful reviewer would accept the package—unless new evidence forces a larger rewrite.

8. **Scaffold deployable IDE files** under **`ide-files/`** in the target skill root. Every skill should include:

   - **`ide-files/<skill-name>.mdc`** — Cursor rule (always-on). YAML frontmatter with `description:` and `alwaysApply: true`, then a short instruction that tells the agent when and how to use this skill.
   - **`ide-files/<skill-name>.instructions.md`** — VS Code instruction: the **exact same markdown body** as the `.mdc` file (everything after the closing `---` of the frontmatter) with **no** YAML header. Copy-paste the body; do not paraphrase. The **`mdc-instructions-parity`** scanner fails if they drift.
   - **`ide-files/<skill-name>.prompt.md`** — Slash command for both IDEs (short “run this skill” invocation). YAML frontmatter with `description:` only; body is **not** required to match the `.mdc` body.

9. **Deploy the skill outputs to the target project.** Run **`Deploy-SkillOutputs.ps1`** from this skill's `scripts/` to link the authored skill's IDE files into the target project:

   ```powershell
   .\agents\abd-practice-skill-builder\skills\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/<skill-name> -ProjectRoot <target-project> -Force
   ```

   `-IDE` defaults to **`Cursor`** (`.mdc` → **`.cursor/rules/`**, `.prompt.md` → **`.cursor/commands/`**, plus the **`~/.cursor/skills/`** junction). Add **`-IDE Both`** when **`<target-project>`** should also get **`.vscode/`** and **`.github/prompts/`**.

10. **Check `.mdc` / `.instructions.md` parity on the target.** From the **agilebydesign-skills** repo root, run **`run_scanners.py`** with **`--skill-root`** pointing at **this authoring skill** and **`--workspace`** as an **absolute** path to the target skill root (relative paths resolve against the authoring skill folder and will not work):

   ```bash
   python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
     --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill \
     --workspace /absolute/path/to/agilebydesign-skills/skills/<skill-name>
   ```

### Quick reference

- **Target root:** **`agilebydesign-skills/skills/<skill-name>/`**
- **Starter template:** **`skills/abd-practice-skill-builder/abd-author-practice-skill/templates/SKILL_template.md`**
- **Terse order:** seed **`SKILL.md`** if needed; read bundled rules; map retrieval by relevance; fill **`SKILL.md`**; write **`rules/*.md`**; run **`python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/<skill-name>`**; run **Validate** checklist.

## Validate

**Goal:** Inspect the **target** package as a reviewer (see bundled **Validate section is inspection not rewrite**).

Checklist for the **target** **`skills/<skill-name>/`**:

- **Readable English** — **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, and the rest of the target **`SKILL.md`** use **clear, grammatical prose** for humans, not only a polished opening followed by rough notes; paths and commands appear where expected, with enough sentence context that the page teaches the method (bundled **Clear English in every skill section**).
- **Purpose is outcome not mechanics** — **Purpose** is **one** short paragraph about **why** the practice exists and what it helps people do; **Purpose** and other **opening** teaching blocks do **not** front-load paths, **`Manual:`**, **`execute-skill-using-skills-rules`** markers, template-copy steps, or agent pipeline detail before that outcome is clear (bundled **Opening sections give outcomes not package mechanics**).
- **Concepts before notation** — **Core concepts** (and similar teaching blocks) explain **ideas and relationships** first; **diagram symbols, file line-prefix serialisation, and template positioning** (where something sits in an output file) live in **templates**, **Agent Instructions**, **Build**, **Validate**, and **`rules/*.md`**, not as the main way the method is introduced. The target **Core concepts** do **not** explain package structure (meaning layer vs check layer, “where teaching lives”) — that stays in **abd-author-practice-skill** (bundled **Core sections teach ideas before file prefixes and diagram notation**, **Sections and rules**).
- **YAML** — **`description`** is a **one-line outcome**, not a repeat of the file pipeline.
- **Placeholders** — no **`{{PLACEHOLDER}}`** unless the engagement **explicitly** defers that slice.
- **Evidence** — what you call **hub-backed** ties to **`inputs/abd-answers-retrieval.md`**; chat/engagement norms are not forced to; gaps are **documented**, not invented.
- **Templates** — every file the **target** **SKILL.md** promises under **`templates/`** is **filled**, **stubbed with a stated reason**, or **removed from the promise**; each promised template includes **at least one audience-appropriate filled example**, not only headings and placeholders (bundled **Templates include ideal filled examples for the audience**), unless **`SKILL.md`** explicitly defers that template as drill-only or stubbed.
- **Rule file shape** — target **`rules/*.md`** that are normative follow the bundled **Target rule files are checkable specs for named artifacts** (decidable **DO** / **DO NOT**, per-bullet examples, **Source** when hub-backed); **Build** in **`SKILL.md`** remains the step-order doc.
- **Rules and bundle** — **`rules/*.md`** match **execute-skill-using-skills-rules** shape; **`bundle_rules_into_skill_md.py`** was run on the **target** root so the bundle block matches disk; **`scanner:`** only where the script exists (bundled **SKILL.md bundle matches rules/*.md files; scanner stem matches Python filename**).
- **Teaching is positive, anti-patterns live in rules** — the target **`SKILL.md`** does **not** have "What this skill is not," "Anti-patterns," or "Common mistakes" sections; things to avoid are enforced as **`## DO NOT`** bullets in **`rules/*.md`** where they can be checked against artifacts (bundled **Anti-patterns belong in rules, not skill teaching**).
- **Validate section** — the **target** **SKILL.md** **Validate** list matches what that skill **actually** ships (templates, markers, citations).

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Anti-patterns belong in rules, not skill teaching

The **target** **`SKILL.md`** teaching voice (**Purpose**, **When to use**, **Core concepts**, **Build**) should tell practitioners **what to do** and **how to think**. Sections that list what the skill does **not** do — "What this skill is not," "Anti-patterns," "Common mistakes," "Don'ts" — belong in **`rules/*.md`** as **`## DO NOT`** bullets where they can be checked against real artifacts. Passing means the teaching voice is positive and forward; anti-patterns are enforced through rules. Failing means the skill page spends teaching space listing negatives that duplicate or should be rules.

#### DO

- Teach the method positively in **`SKILL.md`**: what to do, how to think, what to produce.

  **Example (pass):** "Write 1–2 paragraphs of flowing prose that define the abstraction." — teaches the positive action.

- Put anti-patterns, forbidden formats, and "don't do X" guidance in **`rules/*.md`** as **`## DO NOT`** bullets with concrete examples.

  **Example (pass):** `rules/no-jargon-added.md` has a `## DO NOT` bullet: "Add `Intent:` lines to any term or KA." — checkable against an artifact.

#### DO NOT

- Add a "What this skill is not" or "Anti-patterns" or "Common mistakes" section to the skill's main teaching voice.

  **Example (fail):** **`SKILL.md`** has a `### What this skill is not` section with three bullets listing things to avoid — these are rules, not teaching.

- Duplicate rule content as negative prose in teaching sections when a **`rules/*.md`** file already covers that check.

  **Example (fail):** **`SKILL.md`** says "It does **not** make class-level commitments" in the teaching voice while `rules/no-class-level-commitments.md` already enforces this — the skill page repeats the rule as prose instead of teaching the method.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Clear English in every skill section

**Scanner:** Manual review

The **target** **`SKILL.md`** should read in **clear, grammatical English** from start to finish: **Purpose**, **When to use**, **Core concepts**, **Build**, **Validate**, and other teaching blocks use full sentences and a colleague-level voice. Paths and commands belong where readers expect them, with a line or two of prose so the page teaches instead of dumping scripts. YAML **`description`** stays one short outcome line. Failure is a polished opening followed by brittle note fragments, a **Purpose** that is only file operations when readers wanted the practice, or a **description** that repeats the whole **Build** pipeline.

#### DO

- Write **every** narrative section in **direct, grammatical prose** — **Core concepts** and procedures included, not only **Purpose** / **When to use**.

  **Example (pass):** **Build** step 1: “If **`SKILL.md`** is missing, copy the starter template, add **`Manual:`**, and create empty **`rules/`** and **`templates/`**.” — full sentence.

- Keep **Purpose** and **When to use** as the short *why* and *when*; **When to use** uses real triggers (for example evidence already gathered, need a finished package).

  **Example (pass):** **When to use:** “You already have **`abd-answers-retrieval.md`** and need **`SKILL.md`** plus **`rules/`** finished for reviewers.”

- For **abd-author-practice-skill** itself, **Purpose** may state plainly that this step finishes the target page and **`rules/`** — that **is** the user-facing outcome here.

  **Example (pass):** “This skill authors the target **`rules/*.md`** and finishes **`SKILL.md`** from retrieval.”

- Keep YAML **`description`** to **one line** about the outcome, not every path touched.

  **Example (pass):** `description: Finish a practice skill package from hub retrieval evidence.`

- Put commands in **Prerequisites** / **Build** / **Validate** with a short intro sentence so lists are not orphaned.

  **Example (pass):** “From repo root, bundle rules after edits:” then the **`python ... bundle_rules...`** line.

- Use **clear phrases** in **Agent Instructions** table cells; terse is fine, broken grammar is not.

  **Example (pass):** “Read **`inputs/abd-answers-retrieval.md`** before editing **`SKILL.md`**.”

- Put provenance in **`Source:`** on **rules** or a **Sources:** note — not long “from the training / tightened for…” meta in body prose.

  **Example (pass):** Body says what the practice **is**; **`rules/foo.md`** ends a bullet with **Source:** Kept chunk #3.

#### DO NOT

- Polish **Purpose** only while **Core concepts** or **Build** read like a rough internal checklist with no real sentences.

  **Example (fail):** **Purpose** is two paragraphs; **Build** is “1. copy 2. bundle 3. done” with no connecting text.

- Open the **target practice** with **Purpose** that is only an IT runbook when readers expect the **practice** itself.

  **Example (fail):** Story-mapping skill: “**Purpose:** Copy **`SKILL.md`** and run **`bundle_rules...`**” as the first line.

- Paste the full **Build** pipeline into **`description`**.

  **Example (fail):** **`description`** lists six file paths and two shell commands — belongs in **Build** only.

- Pad teaching with provenance throat-clearing (“training-aligned”, “tightened for this notation”) instead of substance; put audit trail on **rules**.

  **Example (fail):** **Core concepts** paragraph 1 explains where wording came from; still no explanation of the method.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Core sections teach ideas before file prefixes and diagram notation

**Scanner:** Manual review

**Purpose** and **Core concepts** on the **target** **`SKILL.md`** should explain **what things mean and how they relate** — outcomes, who is involved, behaviour, options — in plain language first. **Prefix tags**, **ASCII tree layout**, **diagram geometry**, and **which file line holds what** belong in **templates**, **Agent Instructions**, **Build**, **Validate**, and **`rules/*.md`**, not as the main front-door to the method. You fail when **Core concepts** opens as a symbol legend or tells people which **`FOO:`** line to use before the ideas exist.

#### DO

- Teach **relationships** in plain language (for example broader outcomes decompose into finer ones; actors attach to the outcome in focus; behaviours and options hang under those).

  **Example (pass):** “Goals form a hierarchy from organisation-level outcomes down to impacts you can observe in behaviour.” — no `GOAL:` prefix in **Core concepts**.

- Put **exact markers**, **column names**, **diagram shape**, and **canvas placement** only in **templates**, **Agent Instructions**, **Build** / **Validate**, and **rules** that judge outputs.

  **Example (pass):** **`templates/impact-map.md`** shows `GOAL:` lines; **Core concepts** says “goals sit at the top of the map” without copying the prefix block.

- Keep **Core concepts** examples **conceptual** (outcome + proof, behaviour + proxy); **templates** show row/field layout.

  **Example (pass):** “An impact is observable behaviour change; a trailing metric is how you know it moved.” — template shows **`IMPACT:`** / **`TRAILING_METRIC:`** lines.

- When the hub uses a picture, translate to **concepts** in **`SKILL.md`**; cite figures in **manual** / **references** without turning the skill into a symbol glossary.

  **Example (pass):** “The training figure shows three levels of outcome; see **manual** figure 2.” — not a fenced block of every glyph.

#### DO NOT

- Use **Core concepts** mainly to rehearse **prefix tags**, **tree ASCII**, **indent rules**, or **spatial layout** when plain language could state relationships first.

  **Example (fail):** First screen of **Core concepts** is a fenced block of `EPIC:` / `STORY:` lines and “indent means subordinate” before “what an epic is”.

- Put **template positioning** in **Core concepts** (“use the `FOO:` line”, “in column 3 of the table”).

  **Example (fail):** “Core concepts” says “put the metric on **`TRAILING_METRIC:`** next to **`GOAL:`**” — belongs in **template** / **Agent Instructions**.

- Add **package-structure meta** to the **target** **Core concepts** (“meaning layer vs check layer”, “where teaching lives”) — that is **abd-author-practice-skill** guidance only.

  **Example (fail):** Target **Core concepts** explains how **`rules/`** differ from **Build** for package authors — practitioners need the method, not package anatomy.

- Train readers on **notation** before they know **what each node type means** in the real world.

  **Example (fail):** “Learn these seven prefixes” before “what is an actor vs an outcome”.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: `.mdc` body matches `.instructions.md` (VS Code parity)

On the **target** skill package, every **Cursor rule** ( **`*.mdc`** ) lives under **`ide-files/`** next to **`SKILL.md`** (legacy: skill root only if **`ide-files/`** is absent). Each **`.mdc`** must have a **paired** **`<same-stem>.instructions.md`** in the **same folder** so VS Code gets the **same** always-on text. The **markdown body** of the **`.mdc`** (everything **after** the YAML frontmatter block) must be **byte-for-byte the same** as the **entire** **`.instructions.md`** file after **normalization** (line endings → LF, trim trailing spaces per line, trim leading/trailing blank lines). The **`.prompt.md`** slash-command file is **deliberately different** — it is a short invocation, not the rule body — and is **not** compared to the **`.mdc`**. Failure is a missing pair, or mismatched bodies between **`.mdc`** and **`.instructions.md`**.

#### DO

- Keep **`<stem>.instructions.md`** as the **exact same prose** as **`<stem>.mdc`** without the `---` … `---` header (same headings, bullets, and paths). Edit one, then mirror the other, or edit **`.mdc`** and copy the body to **`.instructions.md`**.

  **Example (pass):** **`foo.mdc`** has frontmatter plus “# Run foo …” and three bullets; **`foo.instructions.md`** is only “# Run foo …” and those three bullets — identical after normalization.

- Run **`mdc-instructions-parity-scanner`** on the **target** skill root when validating ( **`--skill-root`** = **abd-author-practice-skill**, **`--workspace`** = **`skills/<target>/`** ).

  **Example (pass):** `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill --workspace C:/dev/agilebydesign-skills/skills/correct_output` reports **PASS** for **mdc-instructions-parity**.

  **Example (fail):** `...\run_scanners.py ... --workspace skills/correct_output` from a shell whose cwd is not the repo root — the path resolves under the authoring skill and is wrong; use an **absolute** `--workspace`.

#### DO NOT

- Change **`.mdc`** body text without updating **`.instructions.md`** to match (or the reverse).

  **Example (fail):** **`correct-output.mdc`** adds a fourth bullet; **`correct-output.instructions.md`** still has three bullets — scanner reports mismatch.

- Treat **`.prompt.md`** as the rule twin of **`.mdc`** — it is the **command** payload, not the always-on instruction file.

  **Example (fail):** Deleting **`.instructions.md`** because “**`.prompt.md`** is enough” — VS Code always-on parity is missing.

**Source:** deployable IDE file convention (abd-author-practice-skill **Build** step 8–9).

### Rule: Opening sections give outcomes not package mechanics

**Scanner:** Manual review

**Purpose**, **When to use**, and the first teaching blocks on a **`SKILL.md`** should read like **why the packaged method matters**, **who it helps**, and **what becomes possible** when the practice is done well. They stay in **human outcome language**. **Package mechanics** — repo paths, **`Manual:`**, **`execute-skill-using-skills-rules`** markers, which template to copy, bundling commands, retrieval filenames, scanner wiring, or “how an agent runs this skill” — belong in **Prerequisites**, **Build**, **Validate**, **Agent Instructions**, or **`rules/*.md`**, not in the opening voice. Failure is a **Purpose** that reads like a runbook or file checklist before the reader knows **why** the practice exists.

#### DO

- Write **Purpose** as **one** short paragraph (or at most two if the practice truly needs a problem/solution split) that answers **why** this skill exists, **what** finishing it helps people do, and **how** the skill supports that — without naming concrete paths or tooling steps.

  **Example (pass):** “This skill helps teams agree on thin vertical slices so delivery order matches risk and learning. It packages that thinking so facilitators and agents can run the same method and produce comparable maps.” — outcome only.

- Keep **When to use** as **triggers in plain language** (situations readers recognize), not a recap of **Build** or folder layout.

  **Example (pass):** “You have a story map and need to name the first shippable slice.” — no paths.

- Put **file names**, **copy steps**, **bundle commands**, and **what this skill does not include** (retrieval, scanners) in **Prerequisites**, **Build**, or **Not in this pass**.

  **Example (pass):** **Purpose** stays outcome-only; **Build** item 1 says “If **`SKILL.md`** is missing, copy from **`templates/SKILL_template.md`**…”

#### DO NOT

- Open **Purpose** with retrieval paths, **`inputs/...`**, **`rules/*.md`**, **`Manual:`**, **`execute-skill-using-skills-rules`**, or “start from **`templates/...`**” before stating **why** the practice matters.

  **Example (fail):** “You use this skill after hub evidence is in **`inputs/abd-answers-retrieval.md`**. It authors **`rules/*.md`** and finishes **`SKILL.md`**…” as the **whole** purpose — mechanics first, no **why**.

- Use **Purpose** to explain **agent choreography** or **another skill’s** pipeline (“load X then run Y”) when that is not the **substance** of the practice itself.

  **Example (fail):** “**Purpose:** Invoke **abd-query-practice-sources** then run **`bundle_rules_into_skill_md.py`** with **`--skill-root`**…” — operator steps, not the method’s value.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Rule DOs and DON'Ts must each have examples

**Scanner:** Manual review

Under **`## DO`**, every bullet must be followed by at least one **Example (pass):** with enough quoted or paraphrased content to show the shape, not a one-word stub. Under **`## DO NOT`**, every bullet must be followed by at least one **Example (fail):** the same way, in normal markdown (bullet then example lines). When several bullets share one vague example at the bottom, or examples do not map to a specific bullet, the rule fails.

#### DO

- After **each** **`## DO`** bullet, add **Example (pass):** with a concrete fragment, path, or multi-line quote so someone can imitate it.

  **Example (pass):** Bullet: “**DO** include a filled example in each promised template.”  
  **Example (pass):** In **`templates/story-map.md`**, an **Example** section shows a full mini map with real epic titles and user tasks, not only `{{EPIC}}` tokens — enough depth that a complex generation has a clear target.

- After **each** **`## DO NOT`** bullet, add **Example (fail):** showing the violation with the same level of detail.

  **Example (pass):** Correct pairing of a **DO NOT** bullet with a concrete **Example (fail):**

  - **DO NOT** ship a template that is only headings and placeholders.

    **Example (fail):** **`templates/foo.md`** has **## Instructions**, **## Fields**, and fifteen lines of **`{{PLACEHOLDER}}`** but **no** subsection where one row is filled with plausible prose — nothing to copy for tone or depth.

#### DO NOT

- Attach **one** **Pass** / **Fail** pair at the end that does not clearly illustrate **each** bullet above.

  **Example (fail):** Three **DO** bullets about templates, retrieval, and **Validate**; only **Pass:** “Opening reads well” — leaves the other bullets without an example.

- Use **Example (fail):** that repeats the bullet with no sample text.

  **Example (fail):** Bullet: “**DO NOT** omit examples.” **Example (fail):** “When examples are missing.” — not a showable artifact.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Rules named after valid or invalid state

**Scanner:** Manual review

Each normative check lives in its **own file** under **`rules/`**, and that file’s **name** is the **`*.md` basename** in **kebab-case** (everything before **`.md`**). That **filename** must read like the **outcome or state** you guard — what “good” means or what bad state you forbid — so someone can guess the check before opening the file. This rule is **about those rule markdown filenames**, not about prose inside **`SKILL.md`**. Naming fails when the basename is a vague quality label with **no** object (**`skill-valid-grammar`**), or when it names **only** a tool or folder (**`rules-files-and-bundle`**, **`execute-rules-steps`**) instead of the **verified outcome**.

#### DO

- Name **`rules/<basename>.md`** after the **valid state** you want (or the **invalid** one you forbid), so **`basename`** reads like **`clear-english-on-every-skill-section`** — **what** must hold.

  **Example (pass):** **`rules/clear-english-throughout-skill-page.md`** — the pass condition is in the **filename**.

- Make **`# Rule:`** in that **`.md`** file match the same idea in normal English (title aligns with **`basename`**).

  **Example (pass):** File **`rules/templates-include-ideal-filled-examples-for-audience.md`**, title **`# Rule: Templates include ideal filled examples for the audience`**.

#### DO NOT

- Use **`rules/<basename>.md`** names like **`skill-valid-grammar`** or **`valid-structure`** where **grammar** / **structure** has **no scope** (which artifact).

  **Example (fail):** **`rules/skill-valid-grammar.md`** — valid grammar **on what file or section**?

- Use a **basename** that only names plumbing (**`rules-and-bundle`**, **`files-and-bundle`**, **`misc-wiring`**) when the rule is really about a **checkable outcome** (then the **`.md`** name should say that outcome).

  **Example (fail):** **`rules/rules-files-and-bundle.md`** for “inlined **SKILL.md** matches **`rules/*.md`** and **`scanner:`** matches **`scanners/<stem>-scanner.py`**” — the **filename** should say **that**, e.g. **`skill-md-bundle-matches-rules-md-files-scanner-stem-matches-py-filename.md`**.

- Name the file after **only** a script or CLI when the rule is about an **artifact condition**; the **`rules/*.md`** name should describe the **pass/fail on disk**, not the command you ran.

  **Example (fail):** **`rules/run-bundle-script.md`** when the real check is **bundle content matches **`rules/naming.md`**, etc.**

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Rules open with plain pass-and-fail prose

**Scanner:** Manual review

A normative rule should stand on its own: right after the scanner line, use **ordinary prose** (one or two short paragraphs) to say **what passing looks like** and **what failing looks like** for a **named artifact**, without separate **Valid:** / **Invalid:** headings. Then **`## DO`** holds at least one checkable **pass** condition and **`## DO NOT`** at least one **fail** condition; more bullets are fine. The file must not be only a pointer to another rule for those conditions. If the opening is all “see elsewhere” or the bullets need workshop memory instead of file text, the rule fails.

#### DO

- Open with prose paragraphs that state pass and fail in plain language so a reviewer knows the bar before **`## DO`**.

  **Example (pass):** First paragraph: “After a rule edit, **`SKILL.md`**’s bundle block matches **`rules/*.md` on disk.” Second paragraph: “Failure is an inlined rule that still shows old wording, or a **`scanner:`** with no script.”

- Give **at least one** **`## DO`** bullet with a checkable condition (file, section, marker, pattern).

  **Example (pass):** “**DO** run **`bundle_rules_into_skill_md.py`** on the skill root after any change under **`rules/`**.”

- Give **at least one** **`## DO NOT`** bullet with a concrete failure mode.

  **Example (pass):** “**DO NOT** set **`scanner: foo`** when **`scanners/foo-scanner.py`** does not exist.”

#### DO NOT

- Replace the whole rule with cross-references so nobody can pass/fail from **this** file alone.

  **Example (fail):** “Mechanics for **`execute-skill-using-skills-rules`**: filenames, bundling, **`scanner:`**. For **DO**, **DO NOT**, **Examples**, see **Target rule files are checkable specs for named artifacts**.” — no local conditions in **this** file.

- Write **DO** bullets that need workshop context or memory — not decidable from the artifact.

  **Example (fail):** “**DO** ensure the team agreed in the room” — not checkable on a saved file.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: SKILL.md bundle matches rules/*.md files; scanner stem matches Python filename

**Scanner:** Manual review

On the **target** package, each **normative rule** is a **file** under **`rules/`** named **`something.md`**. After you edit any of those **`.md`** files, **`SKILL.md`** must be bundled so the inlined HTML block between **`execute_rules:bundle_rules`** markers contains the **same** text as the **`rules/<same-stem>.md`** file on disk — that is a **filename-to-content sync** check, not a vague “bundle” nod. In rule YAML, **`scanner: <stem>`** is allowed **only** if the **file** **`scanners/<stem>-scanner.py`** exists (same **stem** in both the field and the **Python filename**). Failure is stale inlined text, a **`scanner:`** stem with no matching **`.py`** file, or one **`scanner:`** stem pretending to cover unrelated **`rules/*.md`** topics.

#### DO

- After you change any **`rules/<name>.md`** on the **target** package, run **`bundle_rules_into_skill_md.py`** with **`--skill-root`** set to that skill’s root so the **inlined** copy in **`SKILL.md`** matches that **`.md`** file’s current contents.

  **Example (pass):** You edit **`skills/foo/rules/naming.md`**, run `python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/foo`, open **`skills/foo/SKILL.md`**, search for the **### Rule** heading that corresponds to **`naming.md`**, the inlined **DO** text matches **`rules/naming.md`**.

- Set **`scanner: <stem>`** in the **rule file’s YAML** only when **`scanners/<stem>-scanner.py`** exists on that package (**stem** repeated exactly in the **scanner Python filename**).

  **Example (pass):** **`rules/titles.md`** has frontmatter **`scanner: titles`** and the file **`scanners/titles-scanner.py`** is present beside **`rules/`**.

- Keep **one** **`rules/<topic>.md`** per validation concern; when a scanner exists, align **`scanner:`** **stem** with the **topic** and the **`scanners/<stem>-scanner.py`** **filename**.

  **Example (pass):** **`rules/story-title-shape.md`** owns title-shape checks; **`scanner: story-title-shape`** and **`scanners/story-title-shape-scanner.py`** use the same stem.

#### DO NOT

- Declare **`scanner: layout`** in **`rules/layout.md`** (or any rule) when **`scanners/layout-scanner.py`** is missing — the **YAML stem** must name a real **`.py`** file.

  **Example (fail):** **`rules/layout.md`** has **`scanner: layout`** but there is no **`layout-scanner.py`** under **`scanners/`**.

- Leave **`SKILL.md`** with an inlined rule that does not match the current **`rules/<stem>.md`** file after an edit (no re-bundle).

  **Example (fail):** **`rules/evidence.md`** on disk adds a **DO NOT** bullet, but **`SKILL.md`** still inlines the old text without that bullet.

**Source:** `skills/execute-skill-using-skills-rules` target layout convention.

### Rule: Target rule files are checkable specs for named artifacts

**Scanner:** Manual review

A **`rules/*.md`** on the **target** skill names a **named output** (file, section, marker pattern) and states **pass** conditions a reviewer can apply from text alone. It has **`## DO`** and **`## DO NOT`** with decidable bullets, each with **Example (pass)** / **Example (fail)** as required by **Rule DOs and DON'Ts must each have examples**. Hub-backed bullets need **`Source:`** to **`inputs/abd-answers-retrieval.md`**. **Build** in **`SKILL.md`** owns step order. You fail when the file is workshop facilitation, a pointer-only stub, **DO** lines that need “you had to be there”, fake hub **Source:**, or when **`rules/`** replace **Build** as the numbered how-to list.

#### DO

- Treat each **`rules/*.md`** as a **spec for judging one kind of artifact**, not a second copy of the whole **`SKILL.md`** story.

  **Example (pass):** **`rules/story-title-shape.md`** applies only to story titles in **`story-map.md`** / **`story-map.txt`**; it does not repeat the full story-mapping method.

- Make **every** **`## DO`** bullet **decidable** from the named file or string (no “team felt aligned”).

  **Example (pass):** “**DO** Every story title is verb–noun” — open **`story-map.md`**, scan titles, mark pass/fail.

- Put **`Source:`** on hub-backed bullets pointing to **Kept chunk #** (or row) in **`inputs/abd-answers-retrieval.md`**. Use **`Source:** Engagement** or omit for chat-only norms — do not invent hub rows.

  **Example (pass):** “**DO** Assumptions list includes owner and review date **Source:** Kept chunk #4 …”

- Prefer **one validation concern per file**; name the file after the check (**`naming.md`**, **`story-title-shape.md`**), not after a random **`SKILL.md`** heading.

  **Example (pass):** **`rules/acceptance-criteria-format.md`** only checks AC line format; ordering of work stays in **Build**.

#### DO NOT

- Use **`rules/*.md`** as the **primary step sequence** for the practice; **Build** in **`SKILL.md`** owns order.

  **Example (fail):** **`rules/how-to.md`** with **DO** “Step 1 run retrieval, Step 2 author SKILL” — belongs in **Build**, not **`rules/`**.

- Ship a normative rule with **no** **`## DO NOT`**, or with **DO** items that do not attach to any **named** file or pattern.

  **Example (fail):** “Stories should be good” — no **DO NOT**, no artifact, no way to score an output.

- Label a bullet as from the hub **without** a retrieval row that supports it.

  **Example (fail):** “**DO** Use Patton’s exact workshop timings **Source:** hub” — no chunk in **`inputs/`** says that.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).

### Rule: Templates include ideal filled examples for the audience

**Scanner:** Manual review

Each **target** **`templates/`** file that **`SKILL.md`** promises should ship **at least one** worked example — a filled block, rows, or mini-sample — with enough **tone and depth** for **who reads that output** (sponsor, team session, ticket tool, as the practice says). Drill-only or stub templates must be **called out** in **`SKILL.md`**. You fail when a promised template is only headings and **`{{PLACEHOLDER}}`**, or when **`SKILL.md`** talks about quality but the template never shows a finished-looking fragment of that format.

#### DO

- For each promised **`templates/`** file, include **at least one** filled example that matches the **audience** for that deliverable.

  **Example (pass):** **`templates/impact-map-hypotheses.md`** ends with an **Example** section: full hypothesis lines with realistic metrics, not only `{{impact_1_metric}}`.

- Say in **Instructions** or **`SKILL.md`** **who the example is for** when that is not obvious.

  **Example (pass):** “**Example** (sponsor readout): …” at the top of the example block.

- If a template is **drill-only** or **stubbed**, state that in **`SKILL.md`** like any other deferral.

  **Example (pass):** “**templates/drill-blank.md** is intentionally empty for classroom use; not used for delivery packages.”

#### DO NOT

- Ship a promised template whose body is **only** scaffolding: headings, blank tables, placeholders, **no** completed sample.

  **Example (fail):** **`templates/bar.md`** is **## Fields** plus twenty `{{FIELD_N}}` lines and zero filled rows.

- Rely on **`SKILL.md`** alone for quality bar when the template never shows a **finished** fragment of that format.

  **Example (fail):** **`SKILL.md`** says “write clear hypotheses” but **`templates/hypotheses.md`** has no example paragraph a reader could mirror.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder); theme **G** in **`progress/corrections-log.md`**.

### Rule: Validate section is inspection not rewrite

**Scanner:** Manual review

The **target** **`SKILL.md`** **Validate** section should read like a **critic checklist**: each line can be checked against **`SKILL.md`**, **`rules/`**, **`templates/`**, and **`inputs/`** as the skill actually promises. You close gaps and fix drift; you do not treat **Validate** as the place to rip up **Build** and re-sequence the whole method unless new evidence demands it. Failure is generic **Validate** bullets that ignore promised templates and scanners, or using the pass mainly to redesign workflow, or leaving hub claims in **`SKILL.md`** that contradict **`inputs/abd-answers-retrieval.md`** with no fix and no **Deferred** note.

#### DO

- Read **`SKILL.md`** and **`rules/*.md`** **as a critic**: each rule’s **DO** / **DO NOT** / examples should let you mark a concrete artifact pass or fail.

  **Example (pass):** Open **`rules/naming.md`**, pick **`story-map.md`** from **`templates/`**, verify titles match **DO** / **DO NOT**.

- Walk the **target** **Validate** section line by line; add missing checks when **`SKILL.md`** promises templates, markers, or citations **Validate** never mentions.

  **Example (pass):** Skill promises four **`templates/`** files; **Validate** lists all four plus “each has filled example” if that is required.

- Confirm **no** leftover **`{{PLACEHOLDER}}`** unless **`SKILL.md`** explicitly defers that slice.

  **Example (pass):** Grep **`{{PLACEHOLDER}}`** on target **`SKILL.md`**; only absent or explained in a **Deferred** note.

- Confirm **at least one** **`rules/*.md`** when **`SKILL.md`** has **`execute_rules:bundle_rules`** markers.

  **Example (pass):** Bundle markers present; **`rules/`** has **`naming.md`** (or another normative file).

#### DO NOT

- Treat **Validate** as optional boilerplate that does not match shipped templates, **scanner:** hooks, or retrieval claims.

  **Example (fail):** **Validate** says “check quality” while the skill promises **`scanners/`** and four templates — list does not mention them.

- Use the inspection pass mainly to **re-sequence** work; **Build** owns order.

  **Example (fail):** Rewriting **Build** steps 1–7 during **Validate** without a retrieval or scope change driving it.

- Leave **hub-backed** **`SKILL.md`** claims that contradict **`inputs/abd-answers-retrieval.md`** with no fix and no **Deferred** note.

  **Example (fail):** **Purpose** cites a method the hub chunks do not describe; no gap logged.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
<!-- execute_rules:bundle_rules:end -->

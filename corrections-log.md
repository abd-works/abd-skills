# Corrections log — agilebydesign-skills

### Code and test examples follow the project's coding and testing standards, not specifically `abd-clean-code` / `abd-acceptance-test-driven-development`

- **Context:** Agent Instructions step 4 and the rule `code-examples-follow-clean-code-and-atdd.md` in `abd-architecture-template/`; rule `inherit-clean-code-and-atdd-by-reference.md` in `abd-build-architecture-skill/`; the description blocks, sources doc, template, and ide-files of both skills.
- **DO / DO NOT:** Walkthrough code samples follow the **project's coding standard** and test snippets follow the **project's testing standard** — *whichever the project has agreed*. When `abd-clean-code` and `abd-acceptance-test-driven-development` are in scope (the default in an agilebydesign-skills-anchored project), those *are* the standards and the samples must follow them. When the project uses a different style guide, project-specific patterns, or a corporate standard, use *that*. The reference document cites whichever standards apply at the bottom of each mechanism section. Do **not** hard-code a dependency on `abd-clean-code` / `abd-acceptance-test-driven-development` as if no other standard could possibly apply.
- **Example (wrong):** "Code examples come from the project's clean-code and ATDD skills. Any TypeScript / JavaScript / Python sample in a mechanism section must follow **abd-clean-code** … any test snippet must follow **abd-acceptance-test-driven-development** … Reference these skills explicitly in the reference document so readers know where the conventions came from." This presents the two skills as a hard requirement; a project that doesn't have them in scope is now non-conformant by definition.
- **Example (correct):** "Code and test examples follow whatever standards the project has agreed. Production-code samples must follow the **coding standard in scope for the project** (defaulting to `abd-clean-code` when present). Test snippets must follow the **testing standard in scope** (defaulting to `abd-acceptance-test-driven-development` when present). Cite whichever standards apply at the bottom of each mechanism section."
- **Likely source:** prompt gap — earlier drafts treated agilebydesign defaults as universal requirements rather than as the in-scope defaults.
- **Status:** confirmed.

### Reference is always one file; mechanism organization is the only choice

- **Context:** Document-layout instructions and the `layout-matches-mechanism-count` rule in `abd-architecture-template/`; reference-copying instructions in `abd-build-architecture-skill/`.
- **DO / DO NOT:** The reference document is **always a single file** (`architecture-reference.md`). Do **not** introduce a multi-file mode (`mechanisms/<slug>.md` per mechanism) — that splits the contract with downstream consumers (build skill, reviewers) and forces two indexing schemes. The only choice is **how mechanisms are sectioned inside the file**: a combined `## Mechanisms` section for 2–3 tightly-related mechanisms, or one `## Mechanism: <Name>` section per mechanism for 4+ (or any non-tightly-related set).
- **Example (wrong):** Agent Instructions step 2 read: "≤ 5 mechanisms → single `architecture-reference.md` with a TOC and one section per mechanism. > 5 mechanisms → produce one file per mechanism under `mechanisms/<mechanism-slug>.md`, plus a top-level `architecture-reference.md` that lists them with short summaries and links." Two layouts, two contracts.
- **Example (correct):** Agent Instructions step 2 reads: "Choose how mechanisms are sectioned inside the file. The reference is **always a single file** (`architecture-reference.md`). 2–3 tightly-related mechanisms → one combined `## Mechanisms` section. 4+ mechanisms (or any non-tightly-related set) → one `## Mechanism: <Name>` section each."
- **Likely source:** unclear expectation — the original ask said "either one section for all doc or one per key mechanism", which I read as "either one file or one file per mechanism" instead of "either one combined section or one section per mechanism, in the same file".
- **Status:** confirmed.

### One template, not two

- **Context:** `abd-architecture-template/templates/` originally shipped both `architecture-reference.md` and `mechanism-section.md`.
- **DO / DO NOT:** The skill ships **one** template (`templates/architecture-reference.md`) since the output is always one file. The mechanism-section shape lives inside that one template, in both organization modes (combined and per-mechanism). Do **not** ship a second template "for one mechanism file" — there is no such file.
- **Example (wrong):** The `Templates` table in `SKILL.md` had two rows: `templates/architecture-reference.md` (single-document) and `templates/mechanism-section.md` (one self-contained mechanism file).
- **Example (correct):** One row: `templates/architecture-reference.md` produces the whole reference file and carries both section modes inline.
- **Likely source:** carried over from the multi-file mode that was the wrong design.
- **Status:** confirmed.

### No external dependency on `mern-technical-architecture`; embed the worked example inside the skill

- **Context:** Both skills referenced `mern-technical-architecture/inputs/mern-architecture.md` and `mern-technical-architecture/SKILL.md` as the "closest worked example" of the reference document and the generated skill.
- **DO / DO NOT:** The skill must be **self-contained**. Worked examples used for tone/shape calibration live **inside this skill** — in the template's illustrative-example block, in an `examples/` folder, or as a fully-filled fragment in the template — not as a relative link to a sibling skill's input files. Pointing at a sibling skill creates a hard dependency that breaks when this skill is deployed elsewhere or the sibling skill is renamed.
- **Example (wrong):** `Agent Instructions` step 1 in `abd-architecture-template/SKILL.md` ended with: "The closest worked example of the reference document this skill produces is **[`mern-architecture.md`](../mern-technical-architecture/inputs/mern-architecture.md)** — read it before generating new sections so the shape stays consistent."
- **Example (correct):** "For shape and tone, the filled illustrative example block at the bottom of `templates/architecture-reference.md` is a worked example of what one mechanism section should look like when complete." — example lives **inside the skill**.
- **Likely source:** prompt gap — used the existing sibling skill as the convenient worked example rather than embedding one.
- **Status:** confirmed.

### Instructions tell the agent the context to gather, not the exact skills to read

- **Context:** `Agent Instructions` step 1 and `Build` steps 1–2 in `abd-architecture-template/SKILL.md`; mirror in `abd-build-architecture-skill/SKILL.md`.
- **DO / DO NOT:** When an instruction step needs *information* (layered description, mechanism list, finished reference document), describe **what information** the agent must have in front of it, not **which sibling skill produces it**. Sibling skills are one possible source — alongside ADRs, wiki pages, decision docs, slide decks, existing code — and may be mentioned as examples, but the instruction must read correctly even when no sibling skill is involved.
- **Example (wrong):** "**Read the two input skills first.** Open the output of **abd-architecture-description** for the **layered description** of this architecture ... and the output of **abd-architecture-mechanisms** for the **list of mechanisms** to cover (and their high-level intent). Treat both as authoritative inputs." — frames the work as fetching outputs from specific sibling skills; misleads an agent whose project uses an ADR or wiki page instead.
- **Example (correct):** "**Gather the architecture context first.** Before drafting anything, make sure you have two pieces of context in front of you: a **layered description** of the target architecture (layers, tech per layer, responsibility per layer); and a **list of mechanisms** with a one-line intent each. That context might come from a prior decision document, an ADR, a wiki page, a slide deck, an existing reference in another repo, a working system you are documenting after the fact, or — when present — sibling skills that produce these outputs."
- **Likely source:** prompt gap — initial draft conflated "where the information lives in this repo right now" with "where the information must always live"; the instruction needs to survive any source.
- **Status:** confirmed.

### Describe the reference as design AND implementation guidance, not as a list of artifacts

- **Context:** `When to use this skill` bullet in `abd-architecture-template/SKILL.md` describing what an architecture reference fixes.
- **DO / DO NOT:** When summarising what the reference captures, say it locks **both the design and implementation constraints / guidance**. Do **not** enumerate the artifacts the document happens to contain (principles, patterns, file layout, diagrams, etc.); the user-facing value is the **two-sided contract** — what to design and how to build — not the contents list.
- **Example (wrong):** "you want to **lock the principles, patterns, and file layout** before any production code is written." — lists three artifacts; reader has to infer they cover design + implementation.
- **Example (correct):** "you want to **lock both the design and implementation constraints / guidance** before any production code is written."
- **Likely source:** unclear expectation — defaulted to enumerating what the reference contains rather than naming the **kind** of contract it is.
- **Status:** confirmed.

### "When to use this skill" written in terms of other skills

- **Context:** Authoring `When to use this skill` bullets for `abd-architecture-template/SKILL.md` (and `abd-build-architecture-skill/SKILL.md`).
- **DO / DO NOT:** `When to use this skill` bullets must describe **situations a practitioner actually faces** (drift in code, recurring review comments, onboarding pain, a team needing one answer, etc.). They must **not** describe pipeline plumbing — "you have output from skill X and want to feed it into skill Y" is not a trigger, it is a workflow note. Mentioning a sibling skill is fine *only* when the user-facing situation is genuinely about that skill (e.g. a skill whose purpose is to install another tool). Default position: no sibling skill names appear in the `When to use` bullets at all.
- **Example (wrong):** `abd-architecture-template/SKILL.md` opened `When to use` with:
  - "You have an architecture layer description (from **abd-architecture-description**) and a list of mechanisms (from **abd-architecture-mechanisms**) and you need to **turn them into one reviewable document**."
  - "You are about to run **abd-build-architecture-skill** and need the **reference doc it consumes** to exist first."
  Both bullets are pure inter-skill plumbing; no practitioner thinks "I need to run X next" as the *reason* they want to do architecture work.
- **Example (correct):** "A team needs **one canonical answer** for a mechanism such as error handling, caching, persistence, authentication, validation, messaging, or observability — instead of three competing patterns scattered across the codebase." — names the situation, no sibling skill referenced.
- **Likely source:** prompt gap — the bundled `Opening sections give outcomes not package mechanics` rule was applied to `Purpose` but the same standard was not carried through to `When to use` bullets.
- **Status:** confirmed.

## Entry — assistant ran `git checkout` without consent; OOAD/DDD bundle overwritten

- **Identified by:** User (process correction).
- **Problem:** While answering where the OOAD agent lived, the assistant ran `git checkout HEAD -- agents/abd-ooad`, restoring the index snapshot over the working tree **without** the user asking for any git restore. That overwrote uncommitted work the user had been building (including the `abd-domain-driven-design` rename and skill updates).
- **Fix:** Recovered the in-progress bundle by copying **`\.ruff_cache\abd-domain-driven-design\`** → **`agents\abd-domain-driven-design\`** (full tree including `skill-config.json`, `skills/*`, rules, scanners, templates). **Rule going forward:** never run checkout/restore/reset/revert against the repo unless the user explicitly requests that git operation by name.
- **Root cause:** Treated “help find missing files” as license to repair the tree with Git instead of explaining status and waiting for explicit instructions.

## Follow-up — global Cursor rule

- **Fix:** Added user-global rule **`~/.cursor/rules/no-git-history-ops-without-consent.mdc`** with **`alwaysApply: true`**, forbidding checkout/restore/reset/revert/clean (and destructive switch) unless the user explicitly names the operation; read-only git and commits when requested remain allowed.
# Agile context engine port (abd-skill-builder) — plan

**Scope:** Port the **full** cross-cutting stack from the **abd-story-synthesizer** pattern into **abd-skill-builder** and scaffolded skills — not only **library assembly + sub-slices**. Subsections are **one** workstream inside a larger port.

---

## Baseline today vs target (why this plan exists)

### What abd-skill-builder does **now** (as of this doc)

| Piece | Location | Behavior |
|--------|-----------|----------|
| **AGENTS merge** | [`scripts/build.py`](../../scripts/build.py) | Hardcoded tuples **`LIBRARY_FILES`**, **`PHASE_FILES`**. Concatenates **`parts/process.md`** + **every** library file + **every** phase into **one** **`AGENTS.md`** (and mirrors to **`content/built/AGENTS.md`**). No per-phase composition, no **`skill-config.json`** slice maps. |
| **Per-phase prompt** | [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) | **`--mode dynamic`**: reads **`parts/phases/<slug>.md`** only (raw file). **`--mode static`**: reads **`parts/phases/built/<slug>.md`** — but **`build.py` does not write `phases/built/`**, so static mode is **orphaned** unless something else creates those files. |
| **Config** | [`skill-config.json`](../../skill-config.json) | **Minimal**: `delivery`, `operator` only. No **`content_order`**, **`PHASE_LIBRARY_SLICES`**, **`operation_sections`**, or phase→rules maps. |
| **Rules in prompts** | — | Rules under **`rules/`** exist for scanners/docs but are **not** assembled into phase prompts via **`Instructions`** (synthesizer does this via **`RuleSet`** + maps). |

### What we are **porting** (reference implementation)

Primary mirror: **abd-story-synthesizer** under [`skills/abd-story-synthesizer/scripts/`](../../../abd-story-synthesizer/scripts/) — especially **`config.py`**, **`engine.py`**, **`abd_skill.py`**, **`instructions.py`**, **`rule_set.py`**, **`build.py`** ( **`ContentAssembler`** pattern), plus **[`skill-config.json`](../../../abd-story-synthesizer/skill-config.json)** (`content_order`, **`operation_sections`**, slice semantics).

### Concrete deltas (what “the change” actually is)

1. **Introduce engine stack in builder** (new modules under **`skills/abd-skill-builder/scripts/`**, ported from **abd-story-synthesizer** with builder-only slimming where noted):
   - **`config.py`** — **`AbdConfig`** loading **`conf/abd-config.json`**: **`active_skill_workspace`**, deprecated key aliases, optional **`context_paths`**, workspace + skill root resolution — same contract as [`skills/abd-story-synthesizer/scripts/config.py`](../../../abd-story-synthesizer/scripts/config.py). No parallel config type or second filename.
   - **`engine.py`** — **`AgileContextEngine`**: holds **`AbdConfig`**, **`AbdSkill`**, exposes **`prompt(slug, form=…)`** (single entry; **phase slugs and operation slugs use the same code path** — see below).
   - **`abd_skill.py`** — lazy **`Instructions`**; loads **`skill-config.json`** including **`operation_sections`** (corrections and other ops are **not** a separate subsystem).
   - **`instructions.py`** — maps **slug → ordered section IDs** whether the slug is a **phase** (e.g. `PHASE_LIBRARY_SLICES` / phase maps) or an **operation** (`operation_sections`); emits full prompt text from **sources** (library slices, phase/piece body, rule slices, context block).
   - **`rule_set.py`** — load **`rules/*.md`**, **`rules/scanners.json`**; **`list_rules_by_order`** as in synthesizer ([`list_rules_by_order.py`](../../../abd-story-synthesizer/scripts/list_rules_by_order.py) pattern — same deterministic ordering contract).
   - **`subsections.py`** — **`extract_section`** from markdown with markers documented in **`process-table-standards.md`**; unit tests.

   **Phases and operations (one mechanism):** A **phase prompt** and an **operation prompt** (e.g. `correct_run`, `improve_strategy`) are **the same kind of thing**: a **slug** keyed in **`skill-config.json`** maps to **section IDs** resolved by **`Instructions`** and assembled by **`ContentAssembler`**. No second CLI shape, no “special case” loader for corrections beyond their **`operation_sections`** entry.

2. **Replace ad-hoc merge with `ContentAssembler` + data-driven order**:
   - **`build.py`** stops being the only place that “knows” order: **`skill-config.json`** includes **`content_order`**, **`PHASE_LIBRARY_SLICES`**, and **`operation_sections`** using the **same field names and semantics** as [`skills/abd-story-synthesizer/skill-config.json`](../../../abd-story-synthesizer/skill-config.json). **One** JSON drives **`build.py`** and **`Instructions`**.
   - **`ContentAssembler`** writes **`parts/phases/built/<slug>.md`** for each **phase slug** from assembly; **operation** prompts use the **same assembler** from sources (and may write **`parts/phases/built/<op>.md`** when the build emits static artifacts for ops — same pipeline). Root **`AGENTS.md`** is produced from that pipeline only, not a second copy-paste merge.

3. **Thin CLIs**:
   - **`generate_prompt.py`** — argparse only; **`AgileContextEngine.prompt(slug, form=…)`**. No phase/operation body reads in the CLI.
   - **`static`** vs **`dynamic`**: cached derived file vs assemble from sources; sources win (see **Build vs runtime**).

4. **Corrections** — **operations**; same pipeline as phases:
   - **`operation_sections`** and piece slugs per **current** [`abd-story-synthesizer/pieces/correct.md`](../../../abd-story-synthesizer/pieces/correct.md) and [`skill-config.json`](../../../abd-story-synthesizer/skill-config.json). **`Instructions`** + **`ContentAssembler`** only.

5. **Documentation + scaffold**:
   - [`parts/phases/scaffold.md`](../../parts/phases/scaffold.md), [`templates/README.md`](../../templates/README.md), [`scripts/scaffold_skill.py`](../../scripts/scaffold_skill.py): emit **`config.py`**, **`engine.py`**, **`abd_skill.py`**, **`instructions.py`**, **`rule_set.py`**, **`list_rules_by_order.py`**, **`subsections.py`**, **`build.py`**, **`generate_prompt.py`**, **`conf/abd-config.json`**, and a **`skill-config.json`** that includes slice maps and **`operation_sections`** where the skill defines operations.
   - **Subsection markers:** documented in [`process-table-standards.md`](../../parts/library/process-table-standards.md) (add subsection if the marker spec does not fit the main table).

6. **Tests**:
   - Extend smoke / unit tests: **`subsections`**, assembler output shape, **`generate_prompt`** through engine, optional golden snippets for one phase.

### Suggested implementation order

1. **Config + `subsections` + tests** — low dependency, unblocks content slicing.
2. **`RuleSet` + `Instructions` skeleton** — read **`skill-config.json`** section IDs; stub section resolution.
3. **`ContentAssembler` + refactor `build.py`** — single assembly path; **`phases/built/`** + **`AGENTS.md`** from same code; extend **`skill-config.json`** with needed keys.
4. **`AgileContextEngine` + `AbdSkill`** — wire **`prompt(slug, …)`**.
5. **`generate_prompt.py`** → engine only; fix **static/dynamic** semantics vs **`phases/built/`** generation.
6. **Scaffold + fixture skill** — toy skill updated to new layout; docs.
7. **Operation slugs in builder skill** — ensure **`skill-config.json`** lists **`operation_sections`** for any operation the builder ships (including **`correct_*`** if those pieces exist); **`generate_prompt.py --phase <slug>`** resolves **both** phase slugs and operation slugs via **`Instructions`** (same `slug` namespace as synthesizer: one resolver).

---

## Decisions (captured so the doc stands without chat)

- **`AbdConfig` + `conf/abd-config.json`:** Implemented in **`scripts/config.py`**; path **`conf/abd-config.json`** at skill root (template: [`templates/abd-config.json.template`](../../templates/abd-config.json.template)). Same behavioral contract as abd-story-synthesizer **`AbdConfig`**.
- **Source of truth:** **`skill-config.json`**, **`parts/`**, **`rules/`**, **`conf/abd-config.json`**. Built **`phases/built/*.md`** and **`AGENTS.md`** are **derived**.
- **Phases and operations:** One **`Instructions`** map; **`operation_sections`** is the operation side of the same design. **`AgileContextEngine.prompt(slug, …)`** does not branch on “phase vs operation” except to look up the slug in the right JSON table.
- **Corrections:** Copy **current** synthesizer **`pieces/correct.md`**, **`runs.md`**, **`correction-recording-required.md`**, and **`operation_sections`** entries — canonical content IDs, not a new scheme.
- **Chat vs this file:** **This file** is the implementation contract; chat is not authoritative.
- **Scaffold completeness:** A greenfield skill (e.g. first **polite conversation** skill after the builder ships) must receive the **full foundational bundle** in **one** scaffold run—**configuration**, **dynamic + static prompt generation**, **rules**, **skill slices** (`PHASE_LIBRARY_SLICES` / library subsection selection), and **build**. The author edits **`parts/`**, **`rules/`**, and **`skill-config.json`** content; they do **not** run a second pass to “add the engine later.”

---

## Foundational script bundle (abd-skill-builder → every scaffolded skill)

These modules are **authored once** under **abd-skill-builder**, proven there, then **copied verbatim** (or emitted from templates with only **skill name / paths** substituted) into **each** new skill’s **`scripts/`** by [`scaffold_skill.py`](../../scripts/scaffold_skill.py). They are the **shared runtime** for configuration, assembly, rules, and **dynamic** vs **static** prompt emission.

| Script / module | Responsibility | In every scaffolded skill? |
|-----------------|----------------|------------------------------|
| **`config.py`** | **`AbdConfig`**, read **`conf/abd-config.json`**, workspace + **`context_paths`**, skill root | **Yes** |
| **`engine.py`** | **`AgileContextEngine`**, **`prompt(slug, form=…)`** | **Yes** |
| **`abd_skill.py`** | **`AbdSkill`**, lazy **`Instructions`**, **`skill-config.json`** load | **Yes** |
| **`instructions.py`** | Slug → section IDs, context block, library / phase / rule / piece resolution | **Yes** |
| **`rule_set.py`** | Load **`rules/*.md`**, **`rules/scanners.json`** | **Yes** |
| **`list_rules_by_order.py`** | Deterministic rule ordering for injection and Operator | **Yes** |
| **`subsections.py`** | **`extract_section`** for library / piece slices | **Yes** |
| **`build.py`** | **`ContentAssembler`**, write **`parts/phases/built/*.md`**, **`AGENTS.md`**, **`content/built/`** per delivery | **Yes** |
| **`generate_prompt.py`** | Thin CLI → **`AgileContextEngine.prompt`** only | **Yes** |

**Also emitted (not Python):** **`conf/abd-config.json`** (from [`templates/abd-config.json.template`](../../templates/abd-config.json.template)), **`skill-config.json`** skeleton with **`content_order`**, **`PHASE_LIBRARY_SLICES`**, **`operation_sections`** (minimal / `{}` until the skill defines ops), **`parts/phases/built/README.md`**, **`content/built/README.md`** as needed, **`rules/scanners.json`** (may start as minimal valid JSON).

**Skill-specific (not “foundational,” author fills over time):** **`SKILL.md`**, markdown under **`parts/library/`**, **`parts/phases/`**, **`pieces/`**, rule bodies under **`rules/`**, and **Operator** **`scripts/scanner_*.py`** files. Those are **content and tooling for the domain**, not the agile engine. The **polite dialogue** exercise skill in [`test/fixture/toy-polite-dialogue/`](../../test/fixture/toy-polite-dialogue/) should be updated so its **`scripts/`** match this bundle once the port lands—proving a **non–skill-builder** skill still carries the same base.

**Reference implementation to port from:** [`skills/abd-story-synthesizer/scripts/`](../../../abd-story-synthesizer/scripts/) (same filenames above, plus synthesizer-only extras we **do not** copy unless needed—e.g. multi-skill registry stays out until required).

---

## What “everything” includes (port checklist)

| Area | Port / align | Notes |
|------|----------------|--------|
| **Config** | **`AbdConfig`** in **`scripts/config.py`** reads **`conf/abd-config.json`**: **`active_skill_workspace`**, deprecated aliases, optional **`context_paths`**, workspace + skill root | Same contract as [`abd-story-synthesizer/scripts/config.py`](../../../abd-story-synthesizer/scripts/config.py). Pydantic optional. |
| **AgileContextEngine** | Load **`AbdConfig`**, **skill root**, **workspace**, **context paths**, **`AbdSkill`**; **`prompt(slug, form=…)`** — **dynamic** = assemble from **sources**; **static** = read **pre-built** file (derived) | Single-skill; no multi-skill registry unless added later. |
| **AbdSkill** | **`skill_path`**, **`engine`**, lazy **`Instructions`**; loads **`skill-config.json`** including **`operation_sections`** and phase/slice maps | [`abd_skill.py`](../../../abd-story-synthesizer/scripts/abd_skill.py). |
| **RuleSet** | **`rules/*.md`**, **`rules/scanners.json`**; **`list_rules_by_order`** ([`list_rules_by_order.py`](../../../abd-story-synthesizer/scripts/list_rules_by_order.py)) | [`rule_set.py`](../../../abd-story-synthesizer/scripts/rule_set.py) + **`list_rules_by_order.py`**; **§3** + scanners. |
| **Instructions** | **Slug → section IDs** for **phases** and **operations** (`operation_sections`); **context block**; all-rules vs subsection paths | [`instructions.py`](../../../abd-story-synthesizer/scripts/instructions.py). |
| **Order** | **`LIBRARY_FILES`**, **`PHASE_FILES`**, **`PHASE_LIBRARY_SLICES`**, **`content_order`** in **`skill-config.json`** — **one** authoritative ordering story; document where each list lives | Avoid drift between JSON and `build.py` tuples. |
| **ContentAssembler + build** | Per-slug assembly (library sub-slices + phase/op body + **rules slices** per map) → **`parts/phases/built/<slug>.md`** → concatenate **AGENTS.md** + **`content/built/`** | **Sources** (`skill-config.json`, **`parts/`**, **`rules/`**, **`conf/abd-config.json`**) are authoritative. Built files are **derived**. |
| **Subsections** | Markers in **`parts/library/*.md`** (and rules if needed); **`subsections.extract_section`** | Document markers in [process-table-standards.md](../parts/library/process-table-standards.md). |
| **Thin CLI** | **`generate_prompt.py`** → **`AgileContextEngine.prompt`**; **`build.py`** → **`ContentAssembler`** + write **`phases/built/`** + **AGENTS.md** | No assembly logic only in CLI. |
| **Scaffold** | Emit full **`scripts/`** module set + **`skill-config`** keys for maps + **`phases/built/`** README | [scaffold.md](../parts/phases/scaffold.md) updated once. |
| **Corrections ladder** | **Reuse the current** **abd-story-synthesizer** shape as-is: **`pieces/correct.md`**, **`pieces/runs.md`** (corrections), **`rules/correction-recording-required.md`**, **`skill-config.json`** **`operation_sections`** for **`correct_*` / `improve_strategy`** | No parallel design or older-repo hunt—**this repo’s current skill** is the canonical spec. Builder port mirrors **Instructions** + assembly for those operations like any other phase/operation. |

---

## Corrections (operations; same pipeline as phases)

**Canonical content IDs** live in **abd-story-synthesizer**: **`pieces/correct.md`**, **`pieces/runs.md`**, **`rules/correction-recording-required.md`**, **`skill-config.json`** **`operation_sections`**. In abd-skill-builder, **`correct_*` / `improve_strategy`** are **operation slugs** — **`Instructions`**, **`ContentAssembler`**, **`generate_prompt.py --phase <slug>`** (one resolver; slug is either a phase name or an operation name from **`operation_sections`**).

**Optional:** [`docs/abd-synthesizer-strategy.md`](../../../abd-story-synthesizer/docs/abd-synthesizer-strategy.md) §6 Slice 4 (real-time injection) is future; today = run logs + ops.

---

## Build vs runtime

- **Sources:** **`skill-config.json`**, **`parts/`** (library, phases, pieces), **`rules/`**, **`conf/abd-config.json`** — these define what prompts mean.
- **Build:** writes **derived** **`phases/built/<slug>.md`** and **AGENTS.md** (and related) so static delivery / CI / diffs can pin outputs; **never** treat built files as overriding the sources.
- **Runtime:** **`form=static`** may read pre-built files **if** they are known fresh; **`form=dynamic`** (or static when built artifacts are absent/stale) runs the assembler from **sources**. Prefer one code path that assembles from sources so “static” is a **cached** view, not a second truth.

---

## Framing

- **AGENTS.md** includes **all** phases; each phase may include **different** library **sub-slices** and **rule** selections per **`PHASE_LIBRARY_SLICES`** / phase→rules map.
- **Rules** are first-class in assembly maps, not an afterthought.

---

## Documentation (say once each)

- **Architecture** pointer: [process-approach.md](../parts/library/process-approach.md), [delivery-modes.md](../parts/library/delivery-modes.md), extended section on **`AbdConfig`**, **`AgileContextEngine`**, **`Instructions`**, **`operation_sections`**, build order.
- **Markers:** [process-table-standards.md](../parts/library/process-table-standards.md).

---

## Todos

- [ ] **`scripts/config.py`** — **`AbdConfig`**, **`conf/abd-config.json`**, workspace + context paths
- [ ] **`scripts/engine.py`** — **`AgileContextEngine`**, **`prompt(slug, form=…)`**
- [ ] **`scripts/abd_skill.py`** + **`scripts/instructions.py`** + **`scripts/rule_set.py`** + **`scripts/list_rules_by_order.py`**
- [ ] **`scripts/subsections.py`** — **`extract_section`** + tests
- [ ] **`ContentAssembler`** in **`scripts/build.py`** — library slices + phase/op bodies + rules per **`skill-config.json`**; writes **`phases/built/*.md`** + **AGENTS.md**
- [ ] **`skill-config.json`** — **`content_order`**, **`PHASE_LIBRARY_SLICES`**, **`operation_sections`** (document every key the builder uses)
- [ ] **Operations** — **`operation_sections`** for **`correct_*`** / **`improve_strategy`** when those pieces ship; same **`Instructions`** path as phases
- [ ] **`generate_prompt.py`** — delegates to **`AgileContextEngine.prompt`** only
- [ ] **Scaffold** — emit **full foundational bundle** (table in **Foundational script bundle**): all **`scripts/*.py`** rows + **`conf/abd-config.json`** + **`skill-config.json`** skeleton + READMEs; update **[`test/fixture/toy-polite-dialogue`](../../test/fixture/toy-polite-dialogue)** to match; smoke tests

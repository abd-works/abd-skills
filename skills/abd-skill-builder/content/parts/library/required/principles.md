These **principles** state how the abd-skill-builder pattern is meant to be operated.

1. **Phase-scoped context** — Do not rely on one giant instruction dump. Assemble prompts for the **named phase** only from `content/parts/phases/` and `content/parts/library/` (and inlined rules). Flat skills that grow without phases invite command drift.
2. **Rules plus scanners** — Serious rules live under **`rules/*.md`**: **normative prose** the model follows, and—when you need enforcement beyond review—a **scanner** (`scripts/...py`) declared in **`rules/scanners.json`** (**`rule_scanner_bindings`**: which script applies to which rule). **`python scripts/base/build.py`** runs **`build.build_pipeline`** after merge so scanners **read the tree on disk** (paths, layout, config, declared bindings) and **exit non-zero** when something violates what the prose promises; **`build.scanners`** should list the same scripts so local runs and **CI** apply the same gate. Prose without checks drifts; checks without prose confuse intent.
3. **Process and checklists** — `content/parts/process.md` orders phases; each phase file owns procedure, inputs/outputs, and a **markdown checklist** so the first unchecked item is the resume point.
4. **Composable parts** — **Library** = cross-cutting norms; **phases** = procedure per step; **built/** = pre-merged slices in static mode. Fix **sources** under `content/parts/` and `rules/`; never patch `AGENTS.md` or `content/built/` by hand to “fix” quality.
5. **Templates as contracts** — Use `templates/` (or scaffold equivalents) so generated artifacts have a **stable shape** for humans and scripts.
6. **Scripts and tests** — Repeatable work lives in `scripts/`; scripts should have tests in `test/`. If an operation is manual twice, it belongs in a script.


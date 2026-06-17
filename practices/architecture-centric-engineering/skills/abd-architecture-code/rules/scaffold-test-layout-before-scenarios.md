# Rule: Scaffold test layout before scenarios

When **`<spec-root>`** (the architecture spec path resolved in step 0) defines **Testing Architecture**, declare and create the full test file tree **before** writing scenario methods or production code. Authority order:

1. **`<spec-root>/architecture-specification.md`** — Testing Architecture section  
2. **`<spec-root>/rules/`** — test layout rules (tier count, naming)  
3. **`<spec-root>/templates/tests/`** — parameterized paths to instantiate  
4. **`<spec-root>/example/tests/`** — worked example when templates need a concrete shape  

Not story titles. Not agent memory of another stack. Not repo drift unless it matches items 1–4.

## DO

- Resolve **`<spec-root>`** first (user path, story-map `architecture-spec`, or project `docs/architecture/specification/<name>/`). Every layout decision reads from that directory.

- Derive the test inventory from the **lowest story artifact** **`<spec-root>`** maps to a file (often lowest-level sub-epic in `story-graph.json`) — not from individual story or scenario names.

  **Example (pass):** After reading `<spec-root>/Testing Architecture`, three sub-epics in scope → three file units × each mandatory tier × helper set defined in `<spec-root>/templates/tests/`.

- Instantiate empty scaffolds from **`<spec-root>/templates/tests/`** **before** the first RED scenario; substitute `{epicSlug}`, `{subEpicSlug}`, and other placeholders the templates define.

- When templates are thin, mirror **`<spec-root>/example/tests/`** file names and folder depth exactly — still under the resolved spec, not a different project.

- Use existing project tests only **after** verifying they match **`<spec-root>/rules/`**; reconcile drift before adding scenarios.

- Run **`<spec-root>`** scanners (when present) after scaffolding and again before declaring done.

## DO NOT

- Hardcode MERN, hero-vtt, or any stack in generated paths when **`<spec-root>`** is something else.

- Name test files after **stories** or **scenarios** when **`<spec-root>`** maps a higher artifact → file.

  **Example (fail):** Files like `validate-*_server.test.ts` / `enqueue-*_server.test.ts` when the spec maps **sub-epic → file** — fragments one unit across many files.

- Create only some tiers for a file unit when **`<spec-root>/rules/`** mandates all tiers for that unit.

- Follow **`abd-story-acceptance-test`** "host project conventions" when they contradict **`<spec-root>`**.

- Split helpers per story when **`<spec-root>`** defines one helper set per file unit.

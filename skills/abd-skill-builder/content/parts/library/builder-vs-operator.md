# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), runs **scanners** from **`skill-config.json`**. It does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.

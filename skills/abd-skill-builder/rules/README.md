# Rules

- **`content-placement.md`** — where normative bodies live (`content/parts/library/` vs `docs/` vs `rules/`).
- **`scanners.json`** — optional **`rule_scanner_bindings`** (which script enforces which rule) plus tooling-friendly **`scanners`** list. **Post-merge execution order** for **`build.py`** lives in **`skill-config.json` → `operator.build_pipeline`** (see **`parts/library/rules-and-automated-checks.md`** in **abd-skill-builder**).

Governance rules here are **not** auto-merged into **`AGENTS.md`** unless you add them to **`scripts/build.py`**.

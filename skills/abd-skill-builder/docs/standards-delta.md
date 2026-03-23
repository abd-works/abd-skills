# Standards delta — `abd-skill-builder`

**Purpose:** Inventory this skill against [`../content/parts/library/skill-repo-standards.md`](../content/parts/library/skill-repo-standards.md) and [`../content/parts/library/skill-standards-section-3.md`](../content/parts/library/skill-standards-section-3.md) (§3). Use it before migration fixes: **no silent full rewrites** — pick **Fix IDs** to implement.

**Date:** 2026-03-21 (REM pass); **2026-03-22** — `docs/` trimmed to this file only; delivery merge order moved to **`README.md`**; checklist copies only under skill/workspace **`docs/`**.

**Scope:** `skills/abd-skill-builder/` only.

---

## Minimal valid skill fixture (`toy-polite-dialogue`)

The **multi-phase greet → introduce → converse → close** example is the **canonical minimal valid skill** for this repo. It lives only under **`abd-skill-builder`**:

| Item | Path (inside this skill) |
| --- | --- |
| **Toy skill (polite dialogue)** | `test/fixture/toy-polite-dialogue/` |
| **Phases** | `content/parts/phases/greet.md`, `introduce.md`, `converse.md`, `close.md` |

**`agentic-skill-builder`** tests and CLI examples resolve this path from the **monorepo root** (`skills/abd-skill-builder/test/fixture/toy-polite-dialogue`). **Follow-up:** pytest/snapshot tests that assert **`build.py`** matches expected output for this fixture (optional).

---

## Summary table


| ID      | Area                                      | Current state                                                                                                    | Expected (standards)                                                                                                                                                              | Severity                                                   |
| ------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **D1**  | `skill-config.json` — **delivery**        | **Resolved:** `delivery.mode` **`static_built`**, `modes` listed                                                                 | `delivery.mode`: `**static_built`** or `runtime_injection`; document paths / merge / equivalence                                                                                  | —                                                       |
| **D2**  | `**content/built/`**                      | **Resolved:** **`scripts/build.py`** writes **`content/built/AGENTS.md`** + **`README.md`** (same merge as root)                                                                    | When `static_built`: pre-merged slices under `content/built/`; lookup in skill **`README.md`**                                                                                        | —                                                       |
| **D3**  | **Delivery lookup doc**                   | **Resolved:** **`README.md`** (*Delivery & merge order*)                                                                               | Single place naming paths, merge order, equivalence to runtime                                                                                                                    | —                                                     |
| **D4**  | **Authoring checklist**         | **Resolved:** canonical **`parts/library/authoring-checklist.md`**; workspace copy is **`docs/skill-plan.md`** § **Authoring checklist** (scaffold injects) | Work checklist in **`docs/skill-plan.md`** per skill you edit                                                                                                | —                                                     |
| **D5**  | **`builder-vs-operator.md`** | **Resolved:** body in **`content/parts/library/builder-vs-operator.md`**; **`docs/`** stubs removed (non-runtime only)               | —               | —                                                       |
| **D6**  | `**conf/`**                               | **Resolved:** **`conf/README.md`**, **`conf/abd-config.json`** (minimal template)                                                  | Optional `conf/README.md`; `**conf/abd-config.json**` when workspace routing is used — present for template parity                                                                 | —                                                        |
| **D7**  | **`test/` + pytest**                      | **Resolved:** **`requirements-dev.txt`**, **`test/test_build_smoke.py`**, **`test/README.md`** updated | `python -m pytest test/`                                                                 | —                                                                                                                      |
| **D8**  | `**build.py` vs `process.md`**            | **Resolved:** `build.py` merges **library** (ordered) + **phases** in order: **`workspace-and-config`**, **`plan-script-build`**, **`plan-migrate`**, **`scaffold`**, **`migrate`**, **`fill-scaffold-parts`** after `process.md` | —             | —                                                     |
| **D9**  | **Version field**                         | **Resolved:** top-level **`version`**: `0.1.0` in **`skill-config.json`**                                                                 | Checklist recommends explicit `version`                                                                                                                                | —                                                        |
| **D10** | **Static commit story**                   | **Resolved:** **`README.md`** — team may commit **`content/built/`** or regenerate in CI                                                                                     | README: team policy for committing `content/built/` when `static_built`                                                                                     | —                                                     |


---

## Detail by area

### Delivery & `content/built/` (D1, D2, D3, D10)

- **`skill-config.json`** declares **`delivery.mode`**: **`static_built`**.
- **`scripts/build.py`** writes **`AGENTS.md`**, **`content/built/AGENTS.md`**, **`content/built/README.md`**.
- **`README.md`** documents merge order and commit policy.

### Documentation & references (D4, D5)

- **Authoring checklist:** canonical **`content/parts/library/authoring-checklist.md`**; **`docs/authoring-checklist.md`** is a per-skill / workspace copy — not **`abd-skill-builder/docs/`**.
- **Builder vs Operator:** **`content/parts/library/builder-vs-operator.md`** only (no **`docs/`** duplicate).

### Conf & workspace (D6)

- **`conf/README.md`** and minimal **`conf/abd-config.json`** align with scaffold templates.

### Tests & fixtures (D7)

- **`test/test_build_smoke.py`** runs **`build.py`** and asserts root vs **`content/built/AGENTS.md`** match.
- **`test/fixture/toy-polite-dialogue/`** remains the reviewed minimal skill example.

### Build script vs process table (D8)

- **`build.py`** merges **`process.md`**, the **library** bundle, then **phases** in **`PHASE_FILES`** order (starting with **`workspace-and-config`**) into **`AGENTS.md`** (see **`scripts/build.py`**).

---

## Suggested fix batches


| Batch                | Fix IDs         | Notes                                                                                 |
| -------------------- | --------------- | ------------------------------------------------------------------------------------- |
| **A — Docs unblock** | D5, D4          | Restores working links; checklist copy                                                |
| **B — Delivery**     | D1, D2, D3, D10 | `static_built`, implement `content/built/` emission in `build.py`, `README.md` |
| **C — Align build**  | D8, D9          | `build.py` ↔ `process.md`; optional `version`                                         |
| **D — Tests**        | D7              | After fixture review                                                                  |

**Status:** Batches A–D addressed for **`abd-skill-builder`** (REM pass).

---

## References

- **[`../content/parts/phases/plan-migrate.md`](../content/parts/phases/plan-migrate.md)** (**1b**) — inventory + delta; **[`../content/parts/phases/migrate.md`](../content/parts/phases/migrate.md)** (**2b**) — execute.
- **[`../parts/library/authoring-checklist.md`](../parts/library/authoring-checklist.md)** — full checklist norms ( **## Authoring checklist** in **`<skill>/docs/skill-plan.md`** when tracking work).
- Minimal valid skill: **`test/fixture/toy-polite-dialogue/`** (this skill).

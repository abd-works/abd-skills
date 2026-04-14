# Rules and scanners

*Leaf **execute_rules** skill (single narrative: layout, commands, workflow): [`skills/execute_rules/SKILL.md`](../../../../skills/execute_rules/SKILL.md). This file is the **longer** merge-order / vocabulary reference for **AGENTS.md**.*

Rules are ordinary markdown files under `rules/`. They spell out what authors and the model are supposed to do. Scanners are optional Python scripts that check your outputs against those expectations. Lists of scanners in `skill-config.json` are tooling configuration (“run these scripts”), not the rules themselves—don’t confuse the two.

The **execute_rules** skill (under **`skills/execute_rules/`** in **abd-skill-builder**) is how you work on another skill from outside that package: refresh **Bundled rules** in **`SKILL.md`**, inspect **`rules/`**, list scanners, and run scanners. Nothing “runs” the rule markdown like an engine—authors and models read it.

**`--skill-root`** = the **skill directory** (has **`rules/`**, **`SKILL.md`**, etc.). **`--workspace`** = the **output** you’re validating (folder or file). Run scripts from the **abd-skill-builder** repo root with **`python skills/execute_rules/scripts/<script>.py --skill-root …`**.

In the rest of this doc, “active skill” means that skill directory.

---

## Rule files (markdown only)

| Piece | Role |
| --- | --- |
| **`<skill-root>/rules/<stem>.md`** | Human-readable expectations: scope, DO/DON'T, examples. **Source of truth** for bundled prose — do not hand-edit the **Bundled rules** block in **`SKILL.md`**. |
| **`scanner:`** in that file’s YAML frontmatter | Optional. **Stem or basename only** — no paths. The check script **always** lives at **`<skill-root>/scripts/scanners/<stem>-scanner.py`**. In frontmatter you usually set **`scanner: <stem>`** (e.g. **`check_links`** → **`check_links-scanner.py`**); you can also set the full basename **`check_links-scanner.py`**. **`list_scanner_scripts`** (in **execute_rules** **`scanner_paths.py`**) collects these (sorted by rule filename), then unions with any other **`scripts/scanners/*.py`** files (discovery). **`merge_scanner_paths`** is a backward-compatible alias for **`list_scanner_scripts`**. |

Prefer one concern per file.

---

## **`skills/execute_rules/scripts/`** (canonical CLIs)

All rule bundling, rule listing, scanner listing, and scanner execution for a **target skill** live here—not under **`scripts/base/`** on the skill package.

| Script | What it does |
| --- | --- |
| **`bundle_rules_into_skill_md.py`** | Reads **`rules/*.md`**, writes the **Bundled rules** section in **`SKILL.md`** between **`<!-- execute_rules:bundle_rules:begin/end -->`**. Args: **`--skill-root`**, **`--skill-md`**, **`--dry-run`**. |
| **`rule_inventory.py`** | **`skill-config.json`** / **`rules/`** / **`rules/scanners.json`** summary. **`--by-order`** + **`--tag`**: table **`order | rule_id | title`**. **`--list-scanners`**: print merged scanner paths (one per line), same set **`run_scanners.py`** would run. Args: **`--skill-root`**. |
| **`run_scanners.py`** | For each path from **`list_scanner_scripts`**: **`python <scanner> --workspace <path>`**. Non-zero if any scanner fails or a script path is missing. |
| **`scanner_paths.py`** | Library module: **`list_scanner_scripts`**, **`resolve_build_pipeline`**, **`skill_build_cfg`**, etc. Imported by **`run_scanners.py`** and **build_skill** diagnostics; **`scripts/base/build.py`** on the target skill **inlines** the same behavior so scaffolds stay self-contained without shipping this file under **`scripts/base/`**. |

---

## **`scripts/base/`** (inside the skill package)

Python modules for **merge** and **workspace** only: assembling **`content/parts/`** into **`AGENTS.md`** / **`content/built/`** / **`phases/built/`**, resolving **`SKILL_ROOT`**, **`skill-config.json`** helpers. **`skill_root.py`** assumes the skill root is **two levels up** from **`scripts/base/<script>.py`**; tools accept **`--skill-root`** where relevant.

| File | Role |
| --- | --- |
| **`build.py`** | Skill-package **merge** (**`content/parts/`** → **`AGENTS.md`**, optional **`content/built/`**, **`phases/built/`**). After merge: runs **`build.build_pipeline`** when non-empty; **otherwise** the same merged scanner list as **`run_scanners`** (logic inlined; mirrors **`resolve_build_pipeline`** in **execute_rules** **`scanner_paths.py`**). |
| **Other modules** | **`skill_root.py`**, **`instructions.py`**, **`skill.py`**, **`set_workspace.py`**, **`rules.py`**, **`markers.py`**, **`config.py`**, **`workspace_checklists.py`** — see **`scripts/base/README.md`** in abd-skill-builder. |

**Do not** add **`scanner_paths.py`**, **`run_scanners.py`**, or rule-order CLIs here — use **execute_rules** scripts from the **builder** repo.

---

## **`build.build_pipeline`** vs **`run_scanners`**

- **`scripts/base/build.py`** uses **`resolve_build_pipeline`** (inlined): if **`build.build_pipeline`** is **non-empty**, that ordered list runs after the merge; if **empty**, it falls back to the merged scanner set (same as **`list_scanner_scripts`**).
- **`run_scanners.py`** **always** uses **`list_scanner_scripts` only** — it does **not** run **`build.build_pipeline`** unless those scripts are also picked up via rule **`scanner:`** frontmatter or **`scripts/scanners/`** discovery.

---

## What not to do

- Do not treat green scanners as enough — still read **rule intent** and **`SKILL.md`**.
- Do not describe checks **only** in prose — set **`scanner:`** in the rule’s frontmatter and/or add **`scripts/scanners/*.py`** so **`run_scanners.py`** can run them.

---

## Typical flow (active skill)

1. Edit **`rules/*.md`** and narrative parts of **`SKILL.md`**.
2. **Build / refresh bundled rules** (from **abd-skill-builder** root): **`python skills/execute_rules/scripts/bundle_rules_into_skill_md.py --skill-root <active-skill-root>`**.
3. **Run scanners:** **`python skills/execute_rules/scripts/run_scanners.py --skill-root <skill-dir> --workspace <output-dir-or-file>`**.

---

## Scaffolded packages

Greenfield layouts ship a **`skill-config.json`** **`build`** block as needed — that is **content/config** on the target skill.

Full **`scripts/base/`** file list and roles: **`agents/abd-skill-builder/scripts/base/README.md`**.

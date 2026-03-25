**AI quality — normative rules, scanners, and review.** This shard is injected under `**## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as `**## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring `**content/parts/`**, `**rules/**`, `**skill-config.json**`, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under `**scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green `**python scripts/build.py`** as enough while `**AGENTS.md**` still disagrees with `**content/parts/**` or `**phase_rules**` omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with `**library/`** norms, run `**python scripts/build.py**` (and `**operator.scanners**` when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate Output guided by rules

While generating or editing skill artifacts:

- Apply `**rules/*.md`** inlined into this bundle (and related `**library/**` docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:


| Mechanism                     | What it does                                                                                                                                                                                        |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `**python scripts/build.py`** | Merges **process** + per-phase bundles into `**AGENTS.md`** and `**content/built/**`, then runs `**operator.build_pipeline**` (e.g. `**scripts/scanner_skill_builder_layout.py**`) when configured. |
| `**rules/scanners.json**`     | Declares **rule → scanner** bindings when your skill uses them; align with `**operator.scanners`**.                                                                                                 |


**Example (wrong):** Hand-editing `**AGENTS.md`** while `**build.py**` is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no `**rule_scanner_bindings`** or `**build_pipeline**` step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep `**skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (AI then Human)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between `**SKILL.md`**, `**process.md**`, and `**phases/**` even when the tree validates?



Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:


| Field                    | Content                                                                         |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Rule**                 | Rule id or `rules/<file>.md` name                                               |
| **Example (wrong)**      | What was done incorrectly                                                       |
| **Example (correct)**    | What it should be                                                               |
| **Scanner or validator** | If applicable — see `**rules/scanners.json`** and `**operator.build_pipeline**` |
| **Likely source**        | One of: prompt gap · rule not read · edge case · automation gap                 |


---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under `**content/parts/`**, `**rules/**`, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under `**scripts/`** and is wired through `**skill-config.json**` (`**build.py**`, `**build_pipeline**`, `**operator.scanners**`) as documented in `**library/rules-and-automated-checks.md**`.

**Example (wrong):** Patching `**AGENTS.md`** directly to “pass” review while `**process.md**` is unchanged.

**Example (correct):** Edit `**content/parts/`** (or `**rules/**`), run `**python scripts/build.py**`, commit regenerated `**AGENTS.md**` / `**content/built/**` when using `**static_built**`.
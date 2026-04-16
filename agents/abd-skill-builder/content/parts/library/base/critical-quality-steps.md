*Leaf **execute_rules** skill (commands, templates, quality workflow as Steps 1–4): [`skills/execute_rules/SKILL.md`](../../../../skills/execute_rules/SKILL.md). This file is the **library** slice merged into **AGENTS.md** / phases — phrased in **layers** for **`content/parts/`** and **`build.py`**.*

Rules improve skill quality in two ways: they guide the model while authoring artifacts, and they set expectations that can be checked mechanically or by review.

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring `**content/parts/`**, `**rules/`**, `**skill-config.json**`, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a scanner under `**scanners/**`, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green `**python scripts/base/build.py`** as enough while `**AGENTS.md`** still disagrees with `**content/parts/**` or `**phase_rules**` omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with `**library/`** norms; when this package **merges `AGENTS.md` / `built/`**, run `**python scripts/base/build.py`** (and from **abd-skill-builder** root **`python skills/execute_rules/scripts/run_scanners.py --skill-root <this-skill> --workspace …`** when you want an explicit scanner pass), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate output guided by rules

While generating or editing skill artifacts:

- Apply `**rules/*.md`** inlined into this bundle (and related `**library/`** docs).
- Prefer **DO / DON'T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:


| Mechanism | What it does |
| --- | --- |
| `**python scripts/base/build.py**` | **Batch merge:** process + per-phase bundles into `**AGENTS.md**` and `**content/built/**` (when used), then **`build.build_pipeline`** if set, **otherwise** the **merged scanner set** from **`scanner:`** frontmatter + **`scanners/*-scanner.py`** (see **`rules-and-scanners.md`**). Omit merge if your workflow does not ship **`AGENTS.md`**. |
| `**python skills/execute_rules/scripts/run_scanners.py**` | From **abd-skill-builder** root: runs that **same merged set** for **`--skill-root`**; pass **`--workspace`** (defaults to skill root). Missing scripts reported **`[MISSING]`**; summary at end. |
| `**rules/scanners.json**` | Declares **rule → scanner** bindings; optional flat **`scanners`** list. See **`rules-and-scanners.md`** for merge order vs **`build.py`**. |


**Example (wrong):** Hand-editing `**AGENTS.md**` while `**build.py**` is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or script on disk in the merged set.

**Example (correct):** Fix issues reported by scanners, re-run **build** / **`run_scanners`**, keep `**skill-config.json**` paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (AI then human)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between `**SKILL.md**`, `**process.md**`, and `**phases/**` even when the tree validates?

---

## Layer 4 — Corrections log

When a problem is found during review, **do not touch skill sources yet**. Log the problem and iterate on the output until the right answer is confirmed. Only then is the log entry complete.

**Where:** Create the log under **`active_skill_workspace`** from **`skill-config.json`** (the engagement / project tree — see **`library/workspace-config.md`**), **not** under the skill install directory. Examples: **`docs/corrections-log.md`**, **`.skill-builder/corrections-log.md`**. Same relative resolution idea as other workspace outputs.

**Field table, markdown skeleton, copy-paste entry, process table:** canonical copy lives in the **execute_rules** skill — [**`skills/execute_rules/templates/corrections-log.md`**](../../../../skills/execute_rules/templates/corrections-log.md). Do not duplicate that table here.

A **corrections log** holds one entry per problem. If the **same guidance has been violated before**, add a second example to the existing entry rather than creating a new one.

**Example (wrong):** Recording a correction and immediately editing `**content/parts/**` to fix it before the correct output has been confirmed.

**Example (correct):** Log the problem, re-generate and iterate until the output is right, then fill in "Example (correct)" and mark the entry done.

---

## Loop 1 — Correct the output

Iterate on the generated output until it is right. **Do not change skill sources during this loop.**

1. **Identify** — Note the problem; open the corrections log.
2. **Log** — Add a DO / DO NOT entry with "Example (wrong)" filled in. Leave "Example (correct)" blank.
3. **Re-generate** — Produce the output again, applying the DO / DO NOT rule explicitly.
4. **Review** — Does the new output satisfy the rule? If not, refine the statement and repeat from step 3.
5. **Confirm** — When the output is right, fill in "Example (correct)" and mark the entry done. The phase is now approved.

---

## Loop 2 — Fix the skill

Run this loop only after Loop 1 is complete for all phases — or when explicitly told "let's fix the skill."

1. **Review the log** — Read all completed corrections log entries together. Look across all issues as a set before proposing any fix.
2. **Determine root cause** — Identify the underlying cause(s) shared across one or more issues. A pattern of related issues likely has a single root cause (e.g. a missing rule, a gap in the prompt, an ambiguous instruction). Group issues by root cause before proposing changes.
3. **Propose improvements** — Suggest a set of changes to `**content/parts/**`, `**rules/**`, or config that address the root causes. Consider all issues together — a single rule change may resolve several. Do not make changes yet; get agreement on the proposal first.
4. **Fix sources** — Once the proposal is agreed, apply the changes. Do not fix the assembled pieces directly — fix the parts.
5. **Re-run build** — Run `**python scripts/base/build.py**` and **`skills/execute_rules/scripts/run_scanners.py`** (from **abd-skill-builder** root, with **`--skill-root`**) when applicable; confirm clean output. The fixes are now live — the corrections are promoted by virtue of being built.
6. **Clear the log** — Remove all resolved entries from the corrections log.

**Example (wrong):** Jumping to fixing `**content/parts/**` mid-review before the correct output is confirmed.

**Example (correct):** Finish Loop 1 (output confirmed right, log entry complete), then run Loop 2 (agree on root cause and improvements, fix sources, build, clear the log).

---

## Do not fix the assembled pieces directly — fix the parts

`**AGENTS.md**` and `**content/built/**` are generated. Fixing them directly is futile — the next build overwrites the change. Fix `**content/parts/**` and `**rules/**`; then build.

**Example (wrong):** Patching `**AGENTS.md**` directly to "pass" review while `**process.md**` is unchanged.

**Example (correct):** Edit `**content/parts/**` (or `**rules/**`), run `**python scripts/base/build.py**`, commit the regenerated output.

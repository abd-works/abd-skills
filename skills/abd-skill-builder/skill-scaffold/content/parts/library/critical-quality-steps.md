Rules improve skill quality in two ways: they guide the model while authoring artifacts, and they set expectations that can be checked mechanically or by review.

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring `content/parts/`, `rules/`, `skill-config.json`, and other skill artifacts. (2) **Checkable expectations** — where this skill ships a scanner under `scripts/scanners/`, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green `python scripts/build.py` as enough while `AGENTS.md` still disagrees with `content/parts/` or `phase_rules` omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with `library/` norms, run `python scripts/build.py` (and the scanners in `conf/abd-config.json` when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate Output guided by rules

While generating or editing skill artifacts:

- Apply `rules/*.md` inlined into this bundle (and related `library/` docs).
- Prefer **DO / DON'T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --- | --- |
| `python scripts/build.py` | Merges **process** + per-phase bundles into `AGENTS.md` and `content/built/`, then runs `operator.build_pipeline` entries when configured. |
| `conf/abd-config.json` → `rule_scanner_bindings` | Declares **rule → scanner** bindings; align with `operator.scanners`. |
| `python scripts/run_scanners.py` | Runs all scanners listed in `conf/abd-config.json → scanners[]` and reports pass/fail. |

**Example (wrong):** Hand-editing `AGENTS.md` while `build.py` is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no `rule_scanner_bindings` or `build_pipeline` step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep `skill-config.json` paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (AI then Human)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between `SKILL.md`, `process.md`, and `phases/` even when the tree validates?

## Layer 4 — Corrections log

When a problem is found during review, **do not touch skill sources yet**. Log the problem and iterate on the output until the right answer is confirmed. Only then is the log entry complete.

A **corrections log** file (e.g. `docs/corrections-log.md`) holds all entries. Add one entry per problem:

| Field | Content |
| ---- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **DO / DO NOT** | The rule as it should be stated |
| **Example (wrong)** | What the output actually did |
| **Example (correct)** | What it should have done — fill in only once the correct output is confirmed |
| **Scanner or validator** | If applicable — see `conf/abd-config.json → rule_scanner_bindings` and `operator.build_pipeline` |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

If the **same guidance has been violated before**, add a second example to the existing entry rather than creating a new one.

**Example (wrong):** Recording a correction and immediately editing `content/parts/` to fix it before the correct output has been confirmed.

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
3. **Propose improvements** — Suggest a set of changes to `content/parts/`, `rules/`, or config that address the root causes. Consider all issues together — a single rule change may resolve several. Do not make changes yet; get agreement on the proposal first.
4. **Fix sources** — Once the proposal is agreed, apply the changes. Do not fix the assembled pieces directly — fix the parts.
5. **Re-run build** — Run `python scripts/build.py` and any applicable scanners; confirm clean output. The fixes are now live — the corrections are promoted by virtue of being built.
6. **Clear the log** — Remove all resolved entries from the corrections log.

**Example (wrong):** Jumping to fixing `content/parts/` mid-review before the correct output is confirmed.

**Example (correct):** Finish Loop 1 (output confirmed right, log entry complete), then run Loop 2 (agree on root cause and improvements, fix sources, build, clear the log).

---

## Do not fix the assembled pieces directly — fix the parts

`AGENTS.md` and `content/built/` are generated. Fixing them directly is futile — the next build overwrites the change. Fix `content/parts/` and `rules/`; then build.

**Example (wrong):** Patching `AGENTS.md` directly to "pass" review while `process.md` is unchanged.

**Example (correct):** Edit `content/parts/` (or `rules/`), run `python scripts/build.py`, commit the regenerated output.

# Eval solution — practice skills

## Solution in one sentence

**Promote every confirmed correction into rerunnable fixtures; on each fixture run scanner (when the rule has one) then AI verdict on the matching rule — so the skill package improves from real failures and stays fixed across future sessions.**

---

## Problem

Practice skills already have rules, scanners, session correction logs, and a `fix-skill` pass. What they lack is **regression memory**: when a rule or scanner changes, nothing reruns the failures that taught us the rule in the first place.

Logs record good and bad examples. They do not **guard** against the same mistake coming back.

---

## Solution

Add an **eval layer** to each practice skill that adopts it:

1. **During session** — correction loop unchanged: log wrong → fix artifact → log correct on confirm.
2. **On confirm** — **promote** `Example (wrong)` and `Example (correct)` into that skill’s `eval/fixtures/`.
3. **Register expectation** — append a case to that skill’s `eval/cases.json` (rule, context, scanner expectation, AI verdict expectation).
4. **Before/after fix-skill** — run eval for that skill; source changes must keep relevant cases green.
5. **Recurring failures** — `Likely source: automation gap` → add or tighten scanner as a **pre-filter**; AI still judges the rule.

The model does not learn. **The skill package learns** — rules, scanners, templates, and instructions harden from production corrections.

---

## Closed loop

```text
Wrong output
  → log Example (wrong)
  → fix artifact
  → log Example (correct), Status: confirmed
  → PROMOTE to eval/fixtures/fail + eval/fixtures/pass (under the skill)
  → append eval/cases.json (rule, context, expectations)
  → post-session: theme log → fix-skill
  → run eval for that skill (must be green)
  → next session runs against improved skill package
```

**Promotion** is the hinge.

---

## Fixture layout — one area or separate per skill?

**Answer: separate per skill; one shared runner.**

| Approach | Verdict |
| --- | --- |
| **Single repo `eval/fixtures/` tagged by skill** | Avoid. Fixtures drift away from `rules/`, `scanners/`, and correction logs. Hard to own and review. |
| **`eval/` inside each skill package** | **Yes.** Fixture lives next to the rule and scanner it exercises. Promotion from `skill-errors-log.md` is local. |
| **Central `docs/eval/` or `common/eval/`** | Optional **index only** — manifest of which skills have eval, how to run all, aggregate reports. Not where fixtures are stored. |

```text
practices/<family>/skills/<skill-name>/
  rules/
  scanners/                    # optional per rule — pre-filter, not final judge
  skill-errors-log.md
  eval/
    cases.json
    fixtures/
      pass/<case-slug>/
      fail/<case-slug>/
    report.md                  # generated; gitignore

common/eval/                   # optional later
  index.json                   # pointers to skill eval roots
  run-all.sh                   # runs every skill with eval/
```

**Rule:** fixtures are **skill-local**. The repo provides **one runner** that accepts `--skill-root` or `--all`.

---

## How a case runs — scanner then AI (not “structural vs semantic”)

**Misinterpretation to reject:** “Structural rules get scanners; semantic rules get AI.” Most rules are not purely structural.

**Correct model — per rule, per fixture:**

```text
1. Scanner (if rule has one)
      → cheap signal, candidate issues, “look here”
      → may be heuristic (e.g. class size) not proof
2. AI verdict on matching rules/<rule>.md
      → PASS / FAIL with reason
      → authority for whether the rule is satisfied
```

| Rule type | Scanner | AI verdict |
| --- | --- | --- |
| Decidable without judgment (e.g. every term in `**Terms**` has a `###` heading) | Can be sufficient alone | Optional confirm |
| Heuristic / partial (e.g. single responsibility per class) | Flags suspects; cannot know | **Required** — reads rule + artifact |
| Judgment-only (e.g. thin-sliced enough) | None or weak hints | **Required** |
| Context-dependent (greenfield vs reverse-engineer existing app) | Same | **Required** with context in case metadata |

**Example — single responsibility per class:** mechanics might guess (too many methods, mixed concerns in one file). Scanner does **not** pass the rule. Scanner narrows; AI applies `rules/single-responsibility-per-class.md` and emits PASS/FAIL.

**Live validate and eval validate use the same sequence:** scanner pass (if any) → AI per-rule verdict. Eval freezes the artifact; validate runs on fresh generation.

**Do not** write pure-mechanics scanners for every rule. Many rules should be **AI-only in eval**, with scanners added only when a cheap pre-filter pays off.

---

## Context-specific rules and fixtures

Many rules only apply in some engagements. Cases must carry **context**, not assume one global pass/fail.

```json
{
  "id": "fail/domain-spec-brownfield-mixed-concerns",
  "skill": "abd-domain-specification",
  "rule": "single-responsibility-per-class",
  "context": {
    "system": "brownfield",
    "mode": "reverse-engineer-existing-app"
  },
  "workspace": "fixtures/fail/brownfield-mixed-concerns",
  "scanner": { "optional": "class-shape-heuristic-scanner", "must_violate": false },
  "ai_verdict": "FAIL"
}
```

```json
{
  "id": "pass/domain-spec-greenfield-clean",
  "rule": "single-responsibility-per-class",
  "context": {
    "system": "greenfield",
    "mode": "from-scratch"
  },
  "workspace": "fixtures/pass/greenfield-clean",
  "scanner": { "expect_zero_violations": true },
  "ai_verdict": "PASS"
}
```

**Runner behaviour:** when executing eval for a skill, filter cases by `context` profile (or run full suite in CI). A brownfield case does not fail a greenfield-only engagement — it is simply **out of scope** for that run.

Align with engagement mode docs (e.g. `practices/story-driven-delivery/reference/new-vs-existing-system.md`): fixture promotion records which context the correction came from.

---

## How many fixtures? (not “~10 per skill”)

There is **no arbitrary cap**. Ten was a planning placeholder — discard it.

| Principle | Meaning |
| --- | --- |
| **One case per confirmed failure mode** | Each promotion from a correction log entry = one case (fail + pass pair when both exist). Corpus grows with real work, not upfront authoring. |
| **Not one fixture per rule** | Rules overlap; one fixture often exercises several rules. Track `rules_exercised: []` on each case. |
| **Coverage over time** | Goal: every rule that has ever failed in production eventually has ≥1 case — through promotion, not day-one fabrication. |
| **CI may sample** | Full suite on skill-package changes; smoke subset on every commit if suite gets large. |

**Scale:** a skill with 40 rules might have 5 cases after month one and 80 cases after a year of promoted corrections. That is expected.

---

## How often eval runs

| When | What runs | Mandatory? |
| --- | --- | --- |
| **Every live generation** | `run_scanners.py` + AI per-rule verdict on output | Yes — existing validate workflow |
| **On confirmed correction → before fix-skill** | Eval for affected skill (at least new case + related cases) | Yes |
| **After fix-skill edits** | Full eval for that skill | Yes — must be green before merge |
| **PR / CI touching `rules/`, `scanners/`, `SKILL.md`, `eval/`** | Full eval for changed skills | Yes when eval exists |
| **End of every CDD session** | No — too heavy; session uses live validate only | No |
| **Nightly / weekly** | `run_skill_eval --all` aggregate report | Optional |

**Summary:** eval is **regression on the skill package**, not on every chat turn. Live validate is **every turn**; eval is **on promotion and on skill changes**.

---

## `cases.json` shape (revised)

```json
{
  "skill": "abd-domain-language",
  "cases": [
    {
      "id": "italic-coverage-001",
      "rules": ["domain-terms-italicized-in-prose-and-bullets"],
      "context": { "system": "greenfield" },
      "workspace": "fixtures/fail/unitalicized-terms",
      "scanner": { "must_violate": ["domain-terms-coverage-scanner"] },
      "ai_verdict": "FAIL",
      "source": "skill-errors-log.md#entry-italic-coverage"
    },
    {
      "id": "minimal-ka-001",
      "rules": ["domain-terms-italicized-in-prose-and-bullets", "verb-led-behavior-bullets"],
      "context": { "system": "greenfield" },
      "workspace": "fixtures/pass/minimal-ka",
      "scanner": { "expect_zero_violations": true },
      "ai_verdict": "PASS"
    }
  ]
}
```

---

## Repo scripts (to build)

| Script | Job |
| --- | --- |
| `promote_correction_to_eval.py` | Confirmed log entry → fixtures + case row (with rule, context) |
| `run_skill_eval.py` | Per case: run scanner expectations → AI verdict on listed rules → report; `--context` filter |
| `run_skill_eval.py --all` | Walk `common/eval/index.json` or discover `**/eval/cases.json` |

Wire `fix-skill` step 0: run eval for that skill; re-run until green.

---

## Promotion rules

| When | Do |
| --- | --- |
| `Status: confirmed` + recurring or `automation gap` | Promote; tag context; link rule(s); set scanner expectation if scanner exists |
| Same rule fails in 2+ sessions | Promote if not already covered |
| One-off typo | Do not promote |
| CDD correction marked reusable | Promote to target skill with context |
| `fix-skill` changes rules/scanners/eval | Run full skill eval |

---

## Skill types

### Deliverable skills (pilot first)

`abd-domain-language`, `abd-story-mapping`, `abd-secure-code`, etc. — **first pilot:** `abd-domain-language`.

### Orchestrator (CDD) — second wave

Session journal / checklist fixtures; same scanner→AI pattern where rules exist; defer until deliverable pilot proves promotion.

---

## Rollout

| Phase | What |
| --- | --- |
| **0** | Agree this doc; pilot `abd-domain-language` |
| **1** | Manual promotion of 1–2 real corrections with rule + context tags |
| **2** | `promote_correction_to_eval.py` + `run_skill_eval.py` (scanner then AI) |
| **3** | CI on skill-package changes |
| **4** | CDD + central index if needed |

---

## What this is not

- Not “scanners = structural, AI = semantic” — **scanner then AI on the matching rule**
- Not pure-mechanics scanners for every rule
- Not model training
- Not a fixture count cap
- Not the same as deploy / `npx skills add`
- Not a substitute for live validate on every generation

---

## References

| Piece | Path |
| --- | --- |
| Correction process | `common/instructions/log-and-fix-skill-errors.instructions.md` |
| Fix skill | `common/prompts/fix-skill.prompt.md` |
| Validate workflow | `common/skill-workflow.md` |
| Scanner driver | `common/scripts/run_scanners.py` |
| Secure-code fixture pattern | `stages/engineering/abd-secure-code/test/` |
| Greenfield vs brownfield | `practices/story-driven-delivery/reference/new-vs-existing-system.md` |
| Planning notes | `docs/eval-loop-planning.md` |

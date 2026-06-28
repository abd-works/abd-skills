# Eval solution — practice skills

## Solution in one sentence

**Promote every confirmed correction into rerunnable fixtures; on each fixture run scanner (when the rule has one) then AI verdict on the matching rule — so each real failure permanently upgrades the skill package and improvement compounds across sessions.**

---

## Problem

Practice skills already have rules, scanners, session correction logs, and a `fix-skill` pass. What they lack is **durable improvement**: confirmed corrections fix one artifact once, but the lesson does not reliably harden into the skill package for the next engagement.

Logs record good and bad examples. They do not **compound** — nothing ensures today's correction becomes tomorrow's default behaviour.

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

**Summary:** eval is **proof that skill-package improvements stick**, not on every chat turn. Live validate is **every turn**; eval is **on promotion and on skill changes** — rerunnable cases are how you know a fix-skill pass actually made the system better.

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
| `promote_correction_to_eval.py` | Confirmed log entry → fixtures + case row (with rule, context, pipeline metadata) |
| `run_skill_eval.py` | Per case: run scanner expectations → AI verdict on listed rules → report; `--context` filter |
| `run_skill_eval.py --all` | Walk `common/eval/index.json` or discover `**/eval/cases.json` |
| `aggregate_corrections.py` | Walk all skill `eval/cases.json` → merge into `common/eval/index.json` |
| `analyze_themes.py` | Frequency analysis + optional embedding cluster on `index.json` → `common/eval/themes.md` |

Wire `fix-skill` step 0: run eval for that skill; re-run until green.

---

## Cross-skill trend detection

### The pipeline reality

Skills are not isolated. Output of one skill is input for the next. Errors propagate downstream before they are caught.

```
Context
  └─ abd-domain-glossary
       └─ abd-domain-language
            └─ abd-domain-model
                 └─ abd-domain-specification
                      └─ abd-domain-code

       └─ abd-story-mapping
            └─ abd-story-acceptance-criteria
                 └─ abd-story-specification
                      └─ abd-story-acceptance-test

       └─ abd-architecture-outline
            └─ abd-architecture-blueprint
                 └─ abd-architecture-specification
                      └─ abd-architecture-code
```

A correction logged against `abd-domain-specification` may not belong there. The real failure may be upstream.

### Two failure modes per-skill logs collapse into one

| Mode | What the log shows | What actually happened | Wrong action |
| --- | --- | --- | --- |
| **Intrinsic** | Skill B correction | Skill B's rules or instructions are wrong | Fix skill B ✓ |
| **Inherited** | Skill B correction | Skill A output was wrong; B consumed it faithfully | Fix skill B — wrong skill ✗ |
| **Cross-stage theme** | Same error in B, D, F | Shared concept never resolved at source | Fix each skill separately ✗ |
| **Cross-package theme** | DDD error + ARC error | Same structural mistake across two families | Nobody notices the pattern ✗ |

`upstream_clean: true/false` on each promoted case is the root cause flag. If false, the correction is likely a symptom.

### Extended `cases.json` schema — pipeline fields

Add these fields at promotion time. Cost is low; missing them later is expensive.

```json
{
  "id": "domain-lang-italic-001",
  "skill": "abd-domain-language",
  "stage": "discovery",
  "package": "domain-driven-design",
  "rule": "domain-terms-italicized-in-prose",
  "upstream_skill": "abd-domain-glossary",
  "upstream_clean": true,
  "consumer_skills": ["abd-domain-model"],
  "theme": null,
  "source": "skill-errors-log.md#entry-2026-06-15",
  "session_date": "2026-06-15"
}
```

`theme` is `null` at promotion; set by `analyze_themes.py` after clustering.

### Cross-skill corpus layout

```text
common/
  eval/
    index.json          ← all promoted corrections across all skills and packages
    skill-graph.json    ← explicit dependency graph derived from stage definitions
    themes.md           ← generated theme report (gitignore or commit on demand)
```

`skill-graph.json` shape — one entry per skill:

```json
{
  "abd-domain-language": {
    "stage": "discovery",
    "package": "domain-driven-design",
    "consumes": ["abd-domain-glossary"],
    "produces_for": ["abd-domain-model", "abd-story-mapping"]
  }
}
```

This graph enables: *given a theme cluster, which node is the earliest common ancestor?* That is root cause attribution.

### Theme detection — two tiers

**Tier 1 — rule-name frequency (no LLM, build first):**
Aggregate `rule` field across `index.json`. A rule appearing across multiple skills and packages is a cross-skill signal even without semantic analysis.

**Tier 2 — semantic clustering (embeddings, add later):**
Embed the `Example (wrong)` text for each promoted case. Cluster. Name clusters. This finds themes that hit different rules but share the same root concept — e.g., "anemia" surfaces as `behavior-not-on-entity` in DDD, `thin-orchestration-violation` in ARC, and `acceptance-criteria-missing-domain-behavior` in SDD. Different rules; same upstream mistake.

Implementation: `openai.embeddings` + `sklearn KMeans` — approximately 40 lines. No framework required.

### What this changes about the LangChain question

| Capability needed for cross-skill trends | LangChain adds value? |
| --- | --- |
| Schema extension + promotion script | No — field additions |
| Cross-skill index aggregation | No — walk dirs, merge JSON |
| Skill graph traversal for root cause | No — plain graph traversal |
| Rule-name frequency trending | No — Counter over index.json |
| Semantic clustering of errors | Marginal — any embedding API + sklearn |
| Timeline trend (errors over time) | No — sort by `session_date` |
| Root cause attribution via graph | No — BFS/DFS on `skill-graph.json` |
| Dashboard / UI for trends | **LangSmith is relevant here** — without it, output is `themes.md` |

LangSmith becomes more justified for cross-skill trend visibility than for per-skill eval. It still puts correction data in a SaaS and still requires an account. Treat it as an optional ops layer once `analyze_themes.py` and the index exist, not a foundation decision.

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
| **1** | Manual promotion of 1–2 real corrections — include pipeline fields (`stage`, `package`, `upstream_skill`, `upstream_clean`, `session_date`) from the start |
| **2** | `promote_correction_to_eval.py` + `run_skill_eval.py` (scanner then AI) |
| **3** | `aggregate_corrections.py` → `common/eval/index.json`; author `skill-graph.json`; Tier 1 frequency analysis → `themes.md` |
| **4** | Tier 2 semantic clustering; root cause attribution via graph traversal |
| **5** | CI on skill-package changes |
| **6** | CDD + LangSmith observability layer if team size justifies it |

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

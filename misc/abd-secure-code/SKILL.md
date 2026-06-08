---
name: abd-secure-code
catalog_garden_tier: practice
catalog_garden_family: architecture-centric-engineering
catalog_garden_order: 65
catalogue_one_liner: >-
  OWASP-aligned secure coding rules and Python/Java/JavaScript scanners — write and prove security-sensitive production code before merge.
description: >-
  Generate and validate secure production code with OWASP-aligned rules and
  language-specific scanners for Python, Java, and JavaScript (Node.js and
  client-side). Use when implementing authentication, persistence, file
  handling, crypto, or user-rendered content; in the GREEN phase after
  acceptance tests; reviewing PRs for OWASP Top 10 categories; or when asked
  to fix injection, hash passwords, or run secure code scanners.
---
# abd-secure-code

## Purpose

Engineers ship features faster than attackers find gaps — but only when secure defaults are explicit, reviewable, and mechanically checkable. This skill packages Secure Code Warrior guidance into concrete coding rules and automated scanners so teams and agents can **write** security-sensitive code and **prove** it meets the same bar before merge.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** Production source files in the target language. Additionally, `secure-code-review-checklist.md` per slice.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — threat-informed defaults, parameterized data access, secrets/verifiers, fail-safe errors, language stacks, rule map, and context corpus.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/secure-code-review-checklist.md` | Per-slice checklist marking pass/fail per applicable rule |

**Generation steps:**
1. Confirm language — Python, Java, JavaScript/TypeScript, or combination. Default: detect from changed files.
2. Scope the change — list trust boundaries (HTTP input, files, third-party callbacks, admin-only fields).
3. Select rules — match story behavior to rule files using the OWASP theme table.
4. Author production code — apply DO patterns from each rule; avoid DO NOT anti-patterns.
5. Self-review (AI pass) — re-read output against each applicable rule before scanners.
6. Document residual risk — note rules marked n/a and manual-only controls.

### 3. Validate

Run the scanners per language:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-secure-code \
  --workspace <path-to-output> \
  --language python

python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-secure-code \
  --workspace <path-to-output> \
  --language javascript

python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-secure-code \
  --workspace <path-to-output> \
  --language java
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Applicable rules read** — production code matches DO / avoids DO NOT examples.
- **Scanners run** — per language in scope; all pass.
- **Checklist filled** — `templates/secure-code-review-checklist.md` completed for the slice.
- **Residual manual items documented** — CSP, rate limits, dependency CVEs noted (out of scanner scope).
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---

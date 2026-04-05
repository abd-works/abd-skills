---
id: "{{rule_id}}"
title: "Example rule (replace title)"
---

# Rule: {{rule_id}}

**Scanner:** `scripts/scanners/scanner_{{rule_id}}.py` — keep the rule id aligned with **`rules/scanners.json`** → **`rule_scanner_bindings`** and this file’s stem.

## Purpose

<!-- One sentence: what quality or invariant this rule protects. -->

## Scope

<!-- What artifacts, paths, or phases this rule applies to. -->

## Requirements

### Must

- <!-- Imperative, testable obligations. -->

### Should

- <!-- Strong recommendations; may be human-reviewed only. -->

## Examples

**Do**

- <!-- Allowed pattern or good output. -->

**Don’t**

- <!-- Forbidden pattern or failure mode. -->

## Done criteria

<!-- How you know the rule is satisfied (for humans; scanners implement checks here). -->

## See also

- **abd-skill-builder:** `content/parts/library/rules-and-scanners.md` — bindings, **`build_pipeline`**, **`scanners.json`**.

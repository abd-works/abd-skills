---
id: {{rule_id}}
title: {{Rule title — short, human-readable}}
scanner: {{rule_id}}
impact: HIGH | MEDIUM | LOW
---

## {{Rule title}}

<!-- What this rule requires. Write normative prose — the AI reads this. -->
{{rule_description}}

**DO** {{correct behaviour}}.

**DO NOT** {{anti-pattern}}.

This rule is enforced by `scripts/scanner_{{rule_id}}.py` (binding in `rules/scanners.json`).

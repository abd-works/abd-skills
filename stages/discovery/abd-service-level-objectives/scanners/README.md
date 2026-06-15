# Scanners — abd-service-level-objectives

No automated scanners are shipped yet. The bundled rules are enforced by manual review and the Validate checklist in `SKILL.md`.

Candidates for future automation:

| Rule | Possible scanner check |
|---|---|
| `slo-row-has-target-volume-and-percentage` | Each SLO table row contains a target value, an "at {volume}" phrase, and a percentage less than or equal to 100. |
| `slo-row-has-named-scope-and-nfr-category` | Scope cell matches `system\|parent epic:\|epic:\|story:` and Category cell matches one of the six canonical labels. |
| `error-budget-policy-has-concrete-actions` | Document contains a Section 6 / Error-budget policy table with thresholds at 50% / 25% / 0%. |
| `sla-is-looser-than-supporting-slo` | For each SLA row, the linked supporting SLO has a strictly tighter percentage. |

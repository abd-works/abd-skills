# Scanner Report — {{skill_name}}

**Workspace:** {{workspace}}
**Date:** {{timestamp}}

---

## Scanner Execution Status

### {{overall_status}} Overall Status: {{overall_text}}

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | {{executed_count}} | Scanners ran without errors |
| 🟩 Clean Rules | {{clean_count}} | No violations found |
| 🟨 Rules with Warnings | {{warning_count}} | Found {{total_warnings}} warning violation(s) |
| 🟥 Rules with Errors | {{error_count}} | Found {{total_errors}} error violation(s) |
| 🟥 Execution Failed | {{failed_count}} | Scanner crashed during execution |

**Total Rules:** {{total_rules}}
- **Rules with Scanners:** {{rules_with_scanners}}
  - 🟩 **Executed Successfully:** {{executed_count}}
  - 🟥 **Execution Failed:** {{failed_count}}

---

### 🟩 Successfully Executed Scanners

<!-- One line per scanner, sorted by violation count descending -->
- 🟥 **[Rule Name](#rule-name-violations)** - N violation(s) (ERRORS) - [View Details](#rule-name-violations)
  - Scanner: `scanners/rule-name-scanner.py`
- 🟨 **[Rule Name](#rule-name-violations)** - N violation(s) (WARNINGS) - [View Details](#rule-name-violations)
  - Scanner: `scanners/rule-name-scanner.py`
- 🟩 **[Rule Name](#rule-name)** - 0 violations (CLEAN)
  - Scanner: `scanners/rule-name-scanner.py`

---

### 🟥 Scanner Execution Failures

<!-- Only present when a scanner crashed -->
- 🟥 **[Rule Name](#rule-name)** - EXECUTION FAILED
  - Scanner Path: `scanners/rule-name-scanner.py`
  - Error: `AttributeError: 'str' object has no attribute 'get'`

---

## Violations

<!-- One section per failing rule, sorted errors first, then warnings -->

### <a id="rule-name-violations"></a>rule-name — N violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `epics[0].sub_epics[0].stories[0]` | Violation description here | error |
| 2 | `epics[0].sub_epics[0].stories[1]` | Violation description here | warning |

---

## Instructions

<!-- For skill maintainers — remove this section from generated reports -->

**Placeholders:**

| Placeholder | Value |
|-------------|-------|
| `{{skill_name}}` | Stem of `--skill-root` path (e.g. `abd-acceptance-criteria`) |
| `{{workspace}}` | Absolute path passed as `--workspace` |
| `{{timestamp}}` | ISO-8601 datetime of the run |
| `{{overall_status}}` | 🟩 / 🟨 / 🟥 emoji |
| `{{overall_text}}` | `ALL CLEAN` / `HEALTHY` / `GOOD - Minor Issues` / `NEEDS ATTENTION` / `CRITICAL ISSUES` |
| `{{executed_count}}` | Scanners that ran without crashing |
| `{{clean_count}}` | Scanners with 0 violations |
| `{{warning_count}}` | Scanners with only warnings |
| `{{error_count}}` | Scanners with at least one error-severity violation |
| `{{failed_count}}` | Scanners that raised an exception |
| `{{total_warnings}}` | Total warning violation count |
| `{{total_errors}}` | Total error violation count |
| `{{total_rules}}` | Total scanner count |
| `{{rules_with_scanners}}` | Scanners found (executed + failed) |

**Overall status logic:**
- 🟥 `CRITICAL ISSUES` — any scanner crashed
- 🟩 `ALL CLEAN` — 0 violations
- 🟩 `HEALTHY` — <150 violations, 0 error-severity rules
- 🟨 `GOOD - Minor Issues` — <200 violations, ≤5 error rules
- 🟨 `NEEDS ATTENTION` — any error-severity violations
- 🟨 `WARNINGS FOUND` — warnings only

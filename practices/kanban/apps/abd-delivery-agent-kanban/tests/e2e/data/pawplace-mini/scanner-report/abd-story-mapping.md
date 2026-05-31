# Scanner Report — abd-story-mapping

**Workspace:** C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-mini
**Date:** 2026-05-30 19:28:36

---

## Scanner Execution Status

### 🟨 Overall Status: GOOD - Minor Issues

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 5 | Scanners ran without errors |
| 🟩 Clean Rules | 2 | No violations found |
| 🟥 Rules with Errors | 3 | Found 8 error violation(s) |

**Total Rules:** 5
- **Rules with Scanners:** 5
  - 🟩 **Executed Successfully:** 5

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Small-And-Testable | 3 |
| 🟥 ERRORS | Verb-Noun-Format | 3 |
| 🟥 ERRORS | Active-Business-And-Behavioral-Language | 2 |
| 🟩 CLEAN | Outcome-Oriented-Language | 0 |
| 🟩 CLEAN | Scale-Story-Map-By-Domain | 0 |

---

## Violations

### 🟥 Small-And-Testable — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `View Store Map` | Story "View Store Map" appears to be an implementation operation — should be a step within a story that describes user/system outcome | error |
| 2 | `View Store List` | Story "View Store List" appears to be an implementation operation — should be a step within a story that describes user/system outcome | error |
| 3 | `Calculate Distance to Store` | Story "Calculate Distance to Store" appears to be an implementation operation — should be a step within a story that describes user/system outcome | error |

### 🟥 Verb-Noun-Format — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `epics[2].sub_epics[0].name` | Sub_epic name "Shopping Cart" uses gerund (-ing) form - use present tense verb (e.g., "Places Order" not "Placing Order") | error |
| 2 | `epics[2].sub_epics[1].name` | Sub_epic name "Checkout & Payment" contains actor prefix (e.g., "Customer") - use verb-noun format without actor | error |
| 3 | `epics[2].sub_epics[1].name` | Sub_epic name "Checkout & Payment" appears to be noun-only - use verb-noun format (e.g., "Places Order" not "Order Management") | error |

### 🟥 Active-Business-And-Behavioral-Language — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `epics[2].sub_epics[1].name` | Sub_epic name "Checkout & Payment" has actor "Checkout" in the name - actor should be in "users" field, not in name. Use Verb-Noun format: "& Payment" | error |
| 2 | `epics[2].sub_epics[2].name` | Sub_epic name "Store Fulfillment" uses capability noun - use active behavioral language (e.g., "Processes Payments" not "Payment Processing") | error |

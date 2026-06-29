# Scanner Report — abd-clean-code

**Workspace:** /workspace/practices/user-experience-design/skills/supporting/ux-ops
**Date:** 2026-06-29 07:25:27

---

## Scanner Execution Status

### 🟨 Overall Status: NEEDS ATTENTION

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 17 | Scanners ran without errors |
| 🟩 Clean Rules | 8 | No violations found |
| 🟥 Rules with Errors | 9 | Found 71 error violation(s) |

**Total Rules:** 17
- **Rules with Scanners:** 17
  - 🟩 **Executed Successfully:** 17

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Intention Revealing Names Scanner | 29 |
| 🟥 ERRORS | Separate Concerns Scanner | 18 |
| 🟥 ERRORS | Clear Parameters Scanner | 6 |
| 🟥 ERRORS | Function Size Scanner | 5 |
| 🟥 ERRORS | Property Encapsulation Code Scanner | 5 |
| 🟥 ERRORS | Function Single Responsibility Scanner | 3 |
| 🟥 ERRORS | Exception Handling Scanner | 2 |
| 🟥 ERRORS | Swallowed Exceptions Scanner | 2 |
| 🟥 ERRORS | Simplify Control Flow Scanner | 1 |
| 🟩 CLEAN | Abstraction Levels Scanner | 0 |
| 🟩 CLEAN | Consistent Naming Scanner | 0 |
| 🟩 CLEAN | Domain Language Code Scanner | 0 |
| 🟩 CLEAN | Duplication Scanner | 0 |
| 🟩 CLEAN | Explicit Dependencies Scanner | 0 |
| 🟩 CLEAN | Meaningful Context Scanner | 0 |
| 🟩 CLEAN | Single Responsibility Scanner | 0 |
| 🟩 CLEAN | Useless Comments Scanner | 0 |

---

## Violations

### 🟥 Intention Revealing Names Scanner — 29 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Single-letter name 'f' hides intention. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Name 'fo' is very short (2 chars). Use a descriptive name. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Single-letter name 'c' hides intention. | error |
| 4 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'h' hides intention. | error |
| 5 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'p' hides intention. | error |
| 6 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'r' hides intention. | error |
| 7 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 8 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'f' hides intention. | error |
| 9 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Name 'sh' is very short (2 chars). Use a descriptive name. | error |
| 10 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'w' hides intention. | error |
| 11 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 'f' hides intention. | error |
| 12 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Name 'fd' is very short (2 chars). Use a descriptive name. | error |
| 13 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 14 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Name 'fd' is very short (2 chars). Use a descriptive name. | error |
| 15 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 16 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Single-letter name 'p' hides intention. | error |
| 17 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Single-letter name 'p' hides intention. | error |
| 18 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Name 'rp' is very short (2 chars). Use a descriptive name. | error |
| 19 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Name 'fp' is very short (2 chars). Use a descriptive name. | error |
| 20 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Name 'cp' is very short (2 chars). Use a descriptive name. | error |
| 21 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Name 'sp' is very short (2 chars). Use a descriptive name. | error |
| 22 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'p' hides intention. | error |
| 23 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'f' hides intention. | error |
| 24 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'r' hides intention. | error |
| 25 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'c' hides intention. | error |
| 26 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Name 'sc' is very short (2 chars). Use a descriptive name. | error |
| 27 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'r' hides intention. | error |
| 28 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'c' hides intention. | error |
| 29 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Single-letter name 'r' hides intention. | error |

### 🟥 Separate Concerns Scanner — 18 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Function '_filter_screens' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Function 'filter_ux_graph_to_flow_names' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/graph_filters.py` | Function 'filter_ux_graph_to_screen_names' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 4 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function '_sha256_file' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 5 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function '_acquire_lock' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 6 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_search' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 7 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_filter' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 8 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_write' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 9 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function '_validate_regions' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 10 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function 'validate_ux_graph_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 11 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function 'load_ux_graph_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 12 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function 'save_ux_graph_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 13 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'screens' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 14 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'regions' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 15 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'from_json_file' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 16 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'flows' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 17 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'connections' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 18 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Function 'to_mockup_state_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |

### 🟥 Clear Parameters Scanner — 6 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Parameter 'data' in '_collect_screen_names' is vague. Use a domain-specific name. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Parameter 'data' in 'validate_ux_graph_dict' is vague. Use a domain-specific name. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Parameter 'data' in 'save_ux_graph_dict' is vague. Use a domain-specific name. | error |
| 4 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |
| 5 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |
| 6 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |

### 🟥 Function Size Scanner — 5 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function '_acquire_lock' is 39 lines (max 20). Extract helpers. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_write' is 28 lines (max 20). Extract helpers. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'main' is 39 lines (max 20). Extract helpers. | error |
| 4 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function '_validate_regions' is 21 lines (max 20). Extract helpers. | error |
| 5 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function 'validate_ux_graph_dict' is 59 lines (max 20). Extract helpers. | error |

### 🟥 Property Encapsulation Code Scanner — 5 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Public attribute 'self.data' in 'UxNode.__init__'. Prefix with '_' and expose via @property. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Public attribute 'self.flow_idx' in 'UxNode.__init__'. Prefix with '_' and expose via @property. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Public attribute 'self.screen_idx' in 'UxNode.__init__'. Prefix with '_' and expose via @property. | error |
| 4 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Public attribute 'self.region_idx' in 'Region.__init__'. Prefix with '_' and expose via @property. | error |
| 5 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_map.py` | Public attribute 'self.graph' in 'UxGraph.__init__'. Prefix with '_' and expose via @property. | error |

### 🟥 Function Single Responsibility Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function '_acquire_lock' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_search' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 3 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Function 'cmd_filter' mixes logging with computation. Separate the pure logic from observability concerns. | error |

### 🟥 Exception Handling Scanner — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |

### 🟥 Swallowed Exceptions Scanner — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |
| 2 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_cli.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |

### 🟥 Simplify Control Flow Scanner — 1 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts/ux_graph_file.py` | Function 'validate_ux_graph_dict' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |

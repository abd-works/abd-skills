# Scanner Report — abd-clean-code

**Workspace:** /workspace/practices/domain-driven-design/skills/supporting/domain-ops
**Date:** 2026-06-29 07:25:26

---

## Scanner Execution Status

### 🟨 Overall Status: NEEDS ATTENTION

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 17 | Scanners ran without errors |
| 🟩 Clean Rules | 9 | No violations found |
| 🟥 Rules with Errors | 8 | Found 83 error violation(s) |

**Total Rules:** 17
- **Rules with Scanners:** 17
  - 🟩 **Executed Successfully:** 17

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Intention Revealing Names Scanner | 27 |
| 🟥 ERRORS | Separate Concerns Scanner | 27 |
| 🟥 ERRORS | Function Size Scanner | 11 |
| 🟥 ERRORS | Property Encapsulation Code Scanner | 6 |
| 🟥 ERRORS | Clear Parameters Scanner | 5 |
| 🟥 ERRORS | Function Single Responsibility Scanner | 3 |
| 🟥 ERRORS | Exception Handling Scanner | 2 |
| 🟥 ERRORS | Swallowed Exceptions Scanner | 2 |
| 🟩 CLEAN | Abstraction Levels Scanner | 0 |
| 🟩 CLEAN | Consistent Naming Scanner | 0 |
| 🟩 CLEAN | Domain Language Code Scanner | 0 |
| 🟩 CLEAN | Duplication Scanner | 0 |
| 🟩 CLEAN | Explicit Dependencies Scanner | 0 |
| 🟩 CLEAN | Meaningful Context Scanner | 0 |
| 🟩 CLEAN | Simplify Control Flow Scanner | 0 |
| 🟩 CLEAN | Single Responsibility Scanner | 0 |
| 🟩 CLEAN | Useless Comments Scanner | 0 |

---

## Violations

### 🟥 Intention Revealing Names Scanner — 27 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'h' hides intention. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'p' hides intention. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'r' hides intention. | error |
| 4 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 5 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'f' hides intention. | error |
| 6 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Name 'sh' is very short (2 chars). Use a descriptive name. | error |
| 7 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'w' hides intention. | error |
| 8 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 'f' hides intention. | error |
| 9 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Name 'fd' is very short (2 chars). Use a descriptive name. | error |
| 10 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 11 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Name 'fd' is very short (2 chars). Use a descriptive name. | error |
| 12 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Single-letter name 's' hides intention. | error |
| 13 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Name 'ka' is very short (2 chars). Use a descriptive name. | error |
| 14 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Name 'bd' is very short (2 chars). Use a descriptive name. | error |
| 15 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Name 'dm' is very short (2 chars). Use a descriptive name. | error |
| 16 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Single-letter name 'p' hides intention. | error |
| 17 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Single-letter name 'p' hides intention. | error |
| 18 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 19 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Name 'bd' is very short (2 chars). Use a descriptive name. | error |
| 20 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Single-letter name 'p' hides intention. | error |
| 21 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Single-letter name 'f' hides intention. | error |
| 22 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Single-letter name 'p' hides intention. | error |
| 23 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Single-letter name 'o' hides intention. | error |
| 24 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Name 'ka' is very short (2 chars). Use a descriptive name. | error |
| 25 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Name 'ka' is very short (2 chars). Use a descriptive name. | error |
| 26 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Name 'bd' is very short (2 chars). Use a descriptive name. | error |
| 27 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Single-letter name 'm' hides intention. | error |

### 🟥 Separate Concerns Scanner — 27 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function '_sha256_file' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function '_acquire_lock' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_search' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 4 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_filter' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 5 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_write' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 6 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_interaction' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 7 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_member_list' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 8 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_relationships' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 9 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_class' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 10 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_key_abstraction' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 11 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_module' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 12 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function 'validate_domain_model_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 13 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function 'load_domain_model_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 14 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function 'save_domain_model_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 15 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'relationships' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 16 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'key_abstractions' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 17 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'boundary_classes' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 18 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'relationships' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 19 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'classes' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 20 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'properties' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 21 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'operations' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 22 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'from_json_file' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 23 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Function 'modules' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 24 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Function '_filter_class_list' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 25 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Function '_filter_key_abstraction' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 26 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Function 'filter_domain_model_to_module_names' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 27 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Function 'filter_domain_model_to_class_names' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |

### 🟥 Function Size Scanner — 11 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function '_acquire_lock' is 39 lines (max 20). Extract helpers. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_filter' is 21 lines (max 20). Extract helpers. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_write' is 28 lines (max 20). Extract helpers. | error |
| 4 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'main' is 39 lines (max 20). Extract helpers. | error |
| 5 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_interaction' is 31 lines (max 20). Extract helpers. | error |
| 6 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_member_list' is 26 lines (max 20). Extract helpers. | error |
| 7 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_relationships' is 28 lines (max 20). Extract helpers. | error |
| 8 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_key_abstraction' is 22 lines (max 20). Extract helpers. | error |
| 9 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function '_validate_module' is 37 lines (max 20). Extract helpers. | error |
| 10 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Function 'validate_domain_model_dict' is 34 lines (max 20). Extract helpers. | error |
| 11 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/graph_filters.py` | Function 'filter_domain_model_to_class_names' is 25 lines (max 20). Extract helpers. | error |

### 🟥 Property Encapsulation Code Scanner — 6 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.data' in 'DomainNode.__init__'. Prefix with '_' and expose via @property. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.module_idx' in 'DomainNode.__init__'. Prefix with '_' and expose via @property. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.ka_idx' in 'DomainNode.__init__'. Prefix with '_' and expose via @property. | error |
| 4 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.class_idx' in 'DomainNode.__init__'. Prefix with '_' and expose via @property. | error |
| 5 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.boundary' in 'DomainNode.__init__'. Prefix with '_' and expose via @property. | error |
| 6 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Public attribute 'self.domain_model' in 'DomainMap.__init__'. Prefix with '_' and expose via @property. | error |

### 🟥 Clear Parameters Scanner — 5 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Parameter 'data' in '_collect_class_names' is vague. Use a domain-specific name. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Parameter 'data' in 'validate_domain_model_dict' is vague. Use a domain-specific name. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_file.py` | Parameter 'data' in 'save_domain_model_dict' is vague. Use a domain-specific name. | error |
| 4 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |
| 5 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_map.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |

### 🟥 Function Single Responsibility Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function '_acquire_lock' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_search' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 3 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Function 'cmd_filter' mixes logging with computation. Separate the pure logic from observability concerns. | error |

### 🟥 Exception Handling Scanner — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |

### 🟥 Swallowed Exceptions Scanner — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |
| 2 | `/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts/domain_graph_cli.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |

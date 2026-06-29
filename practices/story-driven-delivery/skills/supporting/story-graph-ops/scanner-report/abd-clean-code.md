# Scanner Report — abd-clean-code

**Workspace:** /workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops
**Date:** 2026-06-29 07:43:08

---

## Scanner Execution Status

### 🟨 Overall Status: NEEDS ATTENTION

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 17 | Scanners ran without errors |
| 🟩 Clean Rules | 3 | No violations found |
| 🟥 Rules with Errors | 14 | Found 387 error violation(s) |

**Total Rules:** 17
- **Rules with Scanners:** 17
  - 🟩 **Executed Successfully:** 17

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Intention Revealing Names Scanner | 151 |
| 🟥 ERRORS | Function Size Scanner | 64 |
| 🟥 ERRORS | Separate Concerns Scanner | 56 |
| 🟥 ERRORS | Simplify Control Flow Scanner | 32 |
| 🟥 ERRORS | Property Encapsulation Code Scanner | 18 |
| 🟥 ERRORS | Useless Comments Scanner | 17 |
| 🟥 ERRORS | Clear Parameters Scanner | 13 |
| 🟥 ERRORS | Function Single Responsibility Scanner | 12 |
| 🟥 ERRORS | Single Responsibility Scanner | 9 |
| 🟥 ERRORS | Consistent Naming Scanner | 5 |
| 🟥 ERRORS | Exception Handling Scanner | 3 |
| 🟥 ERRORS | Explicit Dependencies Scanner | 3 |
| 🟥 ERRORS | Swallowed Exceptions Scanner | 3 |
| 🟥 ERRORS | Duplication Scanner | 1 |
| 🟩 CLEAN | Abstraction Levels Scanner | 0 |
| 🟩 CLEAN | Domain Language Code Scanner | 0 |
| 🟩 CLEAN | Meaningful Context Scanner | 0 |

---

## Violations

### 🟥 Intention Revealing Names Scanner — 151 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Single-letter name 'm' hides intention. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py` | Single-letter name 'v' hides intention. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Single-letter name 'm' hides intention. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/_utils_min.py` | Single-letter name 's' hides intention. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/_utils_min.py` | Single-letter name 's' hides intention. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/_utils_min.py` | Single-letter name 's' hides intention. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Single-letter name 'c' hides intention. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Single-letter name 'v' hides intention. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Single-letter name 'r' hides intention. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Single-letter name 'c' hides intention. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Single-letter name 'r' hides intention. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'ac' is very short (2 chars). Use a descriptive name. | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'p' hides intention. | error |
| 18 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'b' hides intention. | error |
| 19 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'ac' is very short (2 chars). Use a descriptive name. | error |
| 20 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 21 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 22 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 23 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 24 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 't' hides intention. | error |
| 25 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 26 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 27 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'ch' is very short (2 chars). Use a descriptive name. | error |
| 28 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 29 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'r' hides intention. | error |
| 30 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'dc' is very short (2 chars). Use a descriptive name. | error |
| 31 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'dc' is very short (2 chars). Use a descriptive name. | error |
| 32 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'b' hides intention. | error |
| 33 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'u' hides intention. | error |
| 34 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 35 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 36 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 37 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 38 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 39 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 40 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 41 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 42 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 43 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 44 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 45 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 46 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 47 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'info' is too generic. Use a domain-specific name. | error |
| 48 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'f' hides intention. | error |
| 49 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'cb' is very short (2 chars). Use a descriptive name. | error |
| 50 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 51 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 52 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 53 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 54 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'e' hides intention. | error |
| 55 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 56 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'item' is too generic. Use a domain-specific name. | error |
| 57 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 58 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 'u' hides intention. | error |
| 59 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 60 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Name 'info' is too generic. Use a domain-specific name. | error |
| 61 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 62 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Single-letter name 's' hides intention. | error |
| 63 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Single-letter name 's' hides intention. | error |
| 64 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Single-letter name 'e' hides intention. | error |
| 65 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Single-letter name 'e' hides intention. | error |
| 66 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'value' is too generic. Use a domain-specific name. | error |
| 67 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'value' is too generic. Use a domain-specific name. | error |
| 68 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'v' hides intention. | error |
| 69 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'f' hides intention. | error |
| 70 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'value' is too generic. Use a domain-specific name. | error |
| 71 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 's' hides intention. | error |
| 72 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'v' hides intention. | error |
| 73 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'f' hides intention. | error |
| 74 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'value' is too generic. Use a domain-specific name. | error |
| 75 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'sn' is very short (2 chars). Use a descriptive name. | error |
| 76 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'v' hides intention. | error |
| 77 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Name 'value' is too generic. Use a domain-specific name. | error |
| 78 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'f' hides intention. | error |
| 79 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 'v' hides intention. | error |
| 80 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Single-letter name 't' hides intention. | error |
| 81 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 't' hides intention. | error |
| 82 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Name 'nm' is very short (2 chars). Use a descriptive name. | error |
| 83 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Name 'tx' is very short (2 chars). Use a descriptive name. | error |
| 84 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'p' hides intention. | error |
| 85 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 's' hides intention. | error |
| 86 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'e' hides intention. | error |
| 87 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 's' hides intention. | error |
| 88 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 't' hides intention. | error |
| 89 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'c' hides intention. | error |
| 90 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 't' hides intention. | error |
| 91 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'c' hides intention. | error |
| 92 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'c' hides intention. | error |
| 93 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 's' hides intention. | error |
| 94 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 's' hides intention. | error |
| 95 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 's' hides intention. | error |
| 96 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Name 'ac' is very short (2 chars). Use a descriptive name. | error |
| 97 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Name 'ch' is very short (2 chars). Use a descriptive name. | error |
| 98 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 't' hides intention. | error |
| 99 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'c' hides intention. | error |
| 100 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Single-letter name 'c' hides intention. | error |
| 101 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Name 'ld' is very short (2 chars). Use a descriptive name. | error |
| 102 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 103 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 104 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 105 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 106 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 107 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 108 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 109 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 110 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 111 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 112 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 113 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'e' hides intention. | error |
| 114 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 115 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 116 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 117 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'r' hides intention. | error |
| 118 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'r' hides intention. | error |
| 119 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 120 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 121 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 122 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 123 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 124 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 125 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 126 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 127 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 128 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 129 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 130 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 131 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 132 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 133 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 134 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 135 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 136 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 137 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 138 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 139 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'm' hides intention. | error |
| 140 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'r' hides intention. | error |
| 141 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'r' hides intention. | error |
| 142 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 143 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 't' hides intention. | error |
| 144 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 't' hides intention. | error |
| 145 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 's' hides intention. | error |
| 146 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 147 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'v' hides intention. | error |
| 148 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Single-letter name 'c' hides intention. | error |
| 149 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_scanner.py` | Name 'ac' is very short (2 chars). Use a descriptive name. | error |
| 150 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_scanner.py` | Single-letter name 'v' hides intention. | error |
| 151 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_scanner_runner.py` | Name 'er' is very short (2 chars). Use a descriptive name. | error |

### 🟥 Function Size Scanner — 64 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Function 'main' is 50 lines (max 20). Extract helpers. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py` | Function 'parse' is 79 lines (max 20). Extract helpers. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Function 'parse_increments' is 26 lines (max 20). Extract helpers. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Function 'main' is 36 lines (max 20). Extract helpers. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/_utils_min.py` | Function 'find_matching_test_files' is 28 lines (max 20). Extract helpers. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'submit_instructions' is 30 lines (max 20). Extract helpers. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'rename' is 26 lines (max 20). Extract helpers. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'delete' is 46 lines (max 20). Extract helpers. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'move_to' is 192 lines (max 20). Extract helpers. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_resolve_target_from_string' is 67 lines (max 20). Extract helpers. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'move_after' is 79 lines (max 20). Extract helpers. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_validate_action_parameters' is 47 lines (max 20). Extract helpers. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryFile' is 31 lines (max 20). Extract helpers. | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_get_matching_test_files_for_story' is 22 lines (max 20). Extract helpers. | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openTest' is 61 lines (max 20). Extract helpers. | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openCode' is 93 lines (max 20). Extract helpers. | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_get_code_scopes' is 72 lines (max 20). Extract helpers. | error |
| 18 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_collect_scoped_imports' is 40 lines (max 20). Extract helpers. | error |
| 19 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_resolve_module_to_file' is 30 lines (max 20). Extract helpers. | error |
| 20 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openAll' is 54 lines (max 20). Extract helpers. | error |
| 21 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryGraph' is 48 lines (max 20). Extract helpers. | error |
| 22 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'create_child' is 26 lines (max 20). Extract helpers. | error |
| 23 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' is 21 lines (max 20). Extract helpers. | error |
| 24 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'behavior_needed' is 27 lines (max 20). Extract helpers. | error |
| 25 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'create_child' is 56 lines (max 20). Extract helpers. | error |
| 26 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'behavior_needed' is 22 lines (max 20). Extract helpers. | error |
| 27 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'behaviors_needed' is 22 lines (max 20). Extract helpers. | error |
| 28 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'all_scenarios_have_tests' is 45 lines (max 20). Extract helpers. | error |
| 29 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'create_child' is 27 lines (max 20). Extract helpers. | error |
| 30 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' is 32 lines (max 20). Extract helpers. | error |
| 31 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'behavior_needed' is 42 lines (max 20). Extract helpers. | error |
| 32 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'reorder' is 21 lines (max 20). Extract helpers. | error |
| 33 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_bot' is 41 lines (max 20). Extract helpers. | error |
| 34 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'submit_increment_instructions' is 31 lines (max 20). Extract helpers. | error |
| 35 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'copy_increment_stories_json' is 22 lines (max 20). Extract helpers. | error |
| 36 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'filter_by_name' is 42 lines (max 20). Extract helpers. | error |
| 37 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'create_epic' is 48 lines (max 20). Extract helpers. | error |
| 38 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'delete_epic' is 43 lines (max 20). Extract helpers. | error |
| 39 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_story_to_dict' is 22 lines (max 20). Extract helpers. | error |
| 40 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_scenario_to_dict' is 29 lines (max 20). Extract helpers. | error |
| 41 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_generate_test_code_for_scenario' is 25 lines (max 20). Extract helpers. | error |
| 42 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_generate_trace_for_scenario' is 48 lines (max 20). Extract helpers. | error |
| 43 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_calculate_story_file_link' is 25 lines (max 20). Extract helpers. | error |
| 44 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function 'compare_pair_children' is 60 lines (max 20). Extract helpers. | error |
| 45 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function '_compare_node_lists' is 107 lines (max 20). Extract helpers. | error |
| 46 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function 'diff_hierarchy_epics' is 29 lines (max 20). Extract helpers. | error |
| 47 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function '_story_names_from_increments' is 24 lines (max 20). Extract helpers. | error |
| 48 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_story_graph' is 131 lines (max 20). Extract helpers. | error |
| 49 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'from_dict' is 32 lines (max 20). Extract helpers. | error |
| 50 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'load' is 31 lines (max 20). Extract helpers. | error |
| 51 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_sub_epic' is 63 lines (max 20). Extract helpers. | error |
| 52 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function 'update_from_report' is 34 lines (max 20). Extract helpers. | error |
| 53 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_new_nodes' is 45 lines (max 20). Extract helpers. | error |
| 54 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_story_users_changes' is 29 lines (max 20). Extract helpers. | error |
| 55 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_ac_moves' is 25 lines (max 20). Extract helpers. | error |
| 56 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_ac_changes' is 72 lines (max 20). Extract helpers. | error |
| 57 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_sub_epic_moves' is 28 lines (max 20). Extract helpers. | error |
| 58 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function '__init__' is 21 lines (max 20). Extract helpers. | error |
| 59 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'reconcile_ac_moves' is 36 lines (max 20). Extract helpers. | error |
| 60 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'has_changes' is 24 lines (max 20). Extract helpers. | error |
| 61 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'reconcile_moves' is 107 lines (max 20). Extract helpers. | error |
| 62 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function '_collect_stories_under_removed' is 31 lines (max 20). Extract helpers. | error |
| 63 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'to_dict' is 94 lines (max 20). Extract helpers. | error |
| 64 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'from_dict' is 78 lines (max 20). Extract helpers. | error |

### 🟥 Separate Concerns Scanner — 56 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Function 'parse_acceptance_criteria' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Function 'inject_acceptance_criteria' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Function 'main' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py` | Function 'parse' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Function 'parse_increments' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Function 'main' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/_utils_min.py` | Function '_find_ast_node_line' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_log' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'submit_instructions' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'delete' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_validate_action_parameters' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openTest' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openCode' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openAll' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryGraph' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 18 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 19 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 20 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 21 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 22 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'examples_columns' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 23 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'examples_rows' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 24 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'has_examples' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 25 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 26 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 27 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'stories_in_order' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 28 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'rename_story_reference' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 29 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'add' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 30 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'rename' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 31 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'add_story_to' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 32 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'remove_story_from' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 33 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'reorder_story_in' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 34 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_bot' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 35 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_json_file' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 36 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'save' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 37 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'submit_increment_instructions' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 38 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_scenario_to_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 39 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_generate_test_code_for_scenario' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 40 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_generate_trace_for_scenario' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 41 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_step_text' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 42 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function '_compare_node_lists' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 43 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function '_story_names_from_increments' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 44 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_story_graph' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 45 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 46 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'save' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 47 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'load' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 48 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_sub_epic' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 49 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_reorder_increments_from_report' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 50 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_remove_story_from_increment' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 51 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_increment_lane_moves' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 52 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_increments_without_removed_names' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 53 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_ac_changes' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 54 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'reconcile_moves' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 55 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'from_dict' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |
| 56 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_scanner.py` | Function '_get_ac_text' mixes I/O with computation. Split into a pure function and an I/O wrapper. | error |

### 🟥 Simplify Control Flow Scanner — 32 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_story_map_to_story_graph.py` | Function 'parse' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_scope_command_for_node' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_parse_steps_from_data' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'move_to' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_resolve_target_from_string' has nesting depth 7 (max 3). Use guard clauses or early returns. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'move_after' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_validate_action_parameters' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryFile' has nesting depth 6 (max 3). Use guard clauses or early returns. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openTest' has nesting depth 7 (max 3). Use guard clauses or early returns. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openCode' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_get_code_scopes' has nesting depth 6 (max 3). Use guard clauses or early returns. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_collect_scoped_imports' has nesting depth 8 (max 3). Use guard clauses or early returns. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openAll' has nesting depth 6 (max 3). Use guard clauses or early returns. | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryGraph' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'children' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'has_stories' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'create_child' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 18 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'submit_increment_instructions' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 19 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'filter_by_name' has nesting depth 9 (max 3). Use guard clauses or early returns. | error |
| 20 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'find_node' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 21 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_generate_trace_for_scenario' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 22 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function '_compare_node_lists' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 23 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function '_story_names_from_increments' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 24 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_story_graph' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 25 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'filter_sub_epic' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 26 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_increment_lane_moves' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 27 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_story_users_changes' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 28 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_find_story_for_ac' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 29 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_ac_changes' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 30 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_remove_epic_from_map' has nesting depth 4 (max 3). Use guard clauses or early returns. | error |
| 31 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function 'reconcile_moves' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |
| 32 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Function '_collect_stories_under_removed' has nesting depth 5 (max 3). Use guard clauses or early returns. | error |

### 🟥 Property Encapsulation Code Scanner — 18 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py` | Public attribute 'self.data' in 'DomainConceptNode.__init__'. Prefix with '_' and expose via @property. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py` | Public attribute 'self.epic_idx' in 'DomainConceptNode.__init__'. Prefix with '_' and expose via @property. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py` | Public attribute 'self.sub_epic_path' in 'DomainConceptNode.__init__'. Prefix with '_' and expose via @property. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py` | Public attribute 'self.concept_idx' in 'DomainConceptNode.__init__'. Prefix with '_' and expose via @property. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method '_get_available_actions' returns mutable internal 'self._registered_actions' directly. Return a copy. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_sub_epics' in 'Epic' takes no args beyond self — use @property. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_stories' in 'Epic' takes no args beyond self — use @property. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_sub_epics' in 'SubEpic' takes no args beyond self — use @property. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_stories' in 'SubEpic' takes no args beyond self — use @property. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_sub_epics' in 'Story' takes no args beyond self — use @property. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_stories' in 'Story' takes no args beyond self — use @property. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Public attribute 'self.story_graph' in 'StoryMap.__init__'. Prefix with '_' and expose via @property. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_all_nodes' in 'StoryMap' takes no args beyond self — use @property. | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_all_acceptance_criteria' in 'StoryMap' takes no args beyond self — use @property. | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Method 'get_increments' in 'StoryMap' takes no args beyond self — use @property. | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Public attribute 'self.workspace_directory' in 'StoryGraphScope.__init__'. Prefix with '_' and expose via @property. | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Public attribute 'self.bot_paths' in 'StoryGraphScope.__init__'. Prefix with '_' and expose via @property. | error |
| 18 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Public attribute 'self.type' in 'StoryGraphScope.__init__'. Prefix with '_' and expose via @property. | error |

### 🟥 Useless Comments Scanner — 17 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Handle Story deletion from StoryGroup' | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Handle CLI parameter alias' | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Create a new StoryGroup' | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get absolute paths' | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Handle already-quoted paths from parameter parsing (e.g., ' | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Handle Epic nodes (no _parent, managed by StoryMap)' | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Handle other node types (SubEpic, Story, etc.)' | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get story files' | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get test files' | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get exploration docs (for sub-epics)' | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get inferred code files' | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# return the most advanced (lowest index) behavior' | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get test_file from parent sub-epic' | error |
| 14 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Get test_file from parent sub-epic (Story's parent is Stor' | error |
| 15 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Create Epic instance' | error |
| 16 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Comment narrates code instead of explaining why: '# Set sequential_order based on position in list' | error |
| 17 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Commented-out code detected. Remove or use version control. | error |

### 🟥 Clear Parameters Scanner — 13 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/domain_concept_node.py` | Parameter 'data' in '__init__' is vague. Use a domain-specific name. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/domain.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_diff.py` | Function '_compare_node_lists' has 9 parameters (max 5). Group related params into an object. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |
| 13 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Parameter 'data' in 'from_dict' is vague. Use a domain-specific name. | error |

### 🟥 Function Single Responsibility Scanner — 12 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_acceptance_criteria_to_story_graph.py` | Function 'main' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/md_thin_slice_to_story_graph.py` | Function 'main' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'delete' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '_validate_action_parameters' mixes validation with I/O. Validate in a separate function. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'add' mixes validation with I/O. Validate in a separate function. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'rename' mixes validation with I/O. Validate in a separate function. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'add_story_to' mixes validation with I/O. Validate in a separate function. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'remove_story_from' mixes validation with I/O. Validate in a separate function. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'reorder_story_in' mixes validation with I/O. Validate in a separate function. | error |
| 10 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'from_bot' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 11 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Function 'load' mixes logging with computation. Separate the pure logic from observability concerns. | error |
| 12 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Function '_apply_ac_changes' mixes logging with computation. Separate the pure logic from observability concerns. | error |

### 🟥 Single Responsibility Scanner — 9 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'StoryNode' has 22 public methods (max 10). Split responsibilities. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'StoryNode' mixes I/O and calculation methods. Separate into distinct classes. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'Epic' has 13 public methods (max 10). Split responsibilities. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'SubEpic' has 16 public methods (max 10). Split responsibilities. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'Story' has 21 public methods (max 10). Split responsibilities. | error |
| 6 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'IncrementCollection' has 15 public methods (max 10). Split responsibilities. | error |
| 7 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Class 'StoryMap' has 36 public methods (max 10). Split responsibilities. | error |
| 8 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Class 'StoryGraphScope' has 14 public methods (max 10). Split responsibilities. | error |
| 9 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Class 'UpdateReport' has 43 public methods (max 10). Split responsibilities. | error |

### 🟥 Consistent Naming Scanner — 5 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryFile' uses camelCase while the file majority uses the other convention. Be consistent. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openTest' uses camelCase while the file majority uses the other convention. Be consistent. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openCode' uses camelCase while the file majority uses the other convention. Be consistent. | error |
| 4 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openAll' uses camelCase while the file majority uses the other convention. Be consistent. | error |
| 5 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function 'openStoryGraph' uses camelCase while the file majority uses the other convention. Be consistent. | error |

### 🟥 Exception Handling Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Exception swallowed silently with 'pass'. Log or re-raise. | error |

### 🟥 Explicit Dependencies Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Hidden dependency 'EpicsCollection()' constructed inside __init__ in 'StoryMap'. Inject via constructor parameter instead. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_graph_scope.py` | Hidden dependency 'Path()' constructed inside __init__ in 'StoryGraphScope'. Inject via constructor parameter instead. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/update_report.py` | Hidden dependency 'LargeDeletions()' constructed inside __init__ in 'UpdateReport'. Inject via constructor parameter instead. | error |

### 🟥 Swallowed Exceptions Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |
| 2 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |
| 3 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/story_map_updater.py` | Exception swallowed with 'pass'. Log, re-raise, or handle it. | error |

### 🟥 Duplication Scanner — 1 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py` | Function '__getitem__' has the same body as '__getitem__' (/workspace/practices/story-driven-delivery/skills/supporting/story-graph-ops/scripts/story_graph_ops/nodes.py:1414). Extract shared logic. | error |

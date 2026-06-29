# run-1 violations — abd-skills-domain-model.drawio

**Source model:** `abd-skills-domain-model.md`  
**Diagram:** `abd-skills-domain-model.drawio`  
**Date:** 2026-06-28  
**Status:** RESOLVED — all scanners pass

---

## Root cause

The CLI (`drawio_domain_cli.py`) auto-routes every edge with no explicit anchors.
When a class has both an **inheritance** and an **association** edge to the same target,
DrawIO's orthogonal router places both on the *same* path, producing `edge_on_edge_overlap`
and `shared_anchor` violations.

Additionally, when many children all inherit from the same parent (e.g. seven classes
→ `StoryNode`), all approach vertical columns cluster within 12 px of each other because
the checker's `mid_x = (exit.x + entry.x) / 2` formula maps similar fractions to similar
x values.

There were no `edge_crosses_class` violations after this generation.

---

## Violations found (initial scan)

### StoryGraph

| # | Rule | Edge | Detail |
|---|------|------|--------|
| 1 | `edge_on_edge_overlap` | `Epic->StoryNode` inh + assoc | Both auto-routed to same vertical |
| 2 | `edge_on_edge_overlap` | `SubEpic->StoryNode` inh + assoc | Same issue |
| 3 | `edge_on_edge_overlap` | `StoryGroup->StoryNode` inh + assoc | Same issue |
| 4 | `edge_on_edge_overlap` | `StoryGroup->StoryNode` inh overlaps `Scenario->StoryNode` assoc | Parallel horizontals 6 px apart |
| 5 | `edge_on_edge_overlap` | `Scenario->StoryNode` inh overlaps `StoryGraphCli->Epic` assoc | Both ran up at x≈635–645 |
| 6 | `shared_anchor` | `StoryNode` bottom — multiple edges | All 7+ inheritance edges used same default entry |

### DomainGraph

| # | Rule | Edge | Detail |
|---|------|------|--------|
| 7 | `edge_on_edge_overlap` | `DomainNode->CPNode` inh overlaps `DCN->DomainNode` assoc | Both at x=910 |
| 8 | `edge_on_edge_overlap` | `DomainModule->DomainNode` inh + assoc | Both at x=874 |
| 9 | `edge_on_edge_overlap` | `KeyAbstractionNode->DomainNode` inh + assoc | Both at x=1040 |
| 10 | `edge_on_edge_overlap` | `DCN->DomainNode` inh + assoc | Approach verticals 8 px apart |
| 11 | `shared_anchor` | `DomainNode` entry — DomainModule + DCN | Same entry fraction |

### UxGraph

| # | Rule | Edge | Detail |
|---|------|------|--------|
| 12 | `edge_on_edge_overlap` | `Screen->UxNode` inh + assoc | Both auto-routed to same vertical |

---

## Fix applied — `fix_overlaps_v2.py`

**Principle:** assign every edge explicit `exitX/exitY/entryX/entryY` anchors and
one or two waypoints that pin the approach vertical column to a unique x value
with ≥ 26 px separation between adjacent columns.

### StoryGraph — StoryNode approach column allocation

All entry columns are ≥ 26 px apart. Edges routed via the gap between row 2
(y ≤ 516) and row 3 (y ≥ 676). Scenario routed from the RIGHT side to avoid
the left-corridor used by `StoryGraphCli→Epic`.

| Edge | Type | Approach x | Gap y |
|------|------|-----------|-------|
| `Story->StoryNode` | inh | 680 | 564 |
| `Epic->StoryNode` | inh | 719 | 556 |
| `SubEpic->StoryNode` | inh | 758 | 610 |
| `StoryGroup->StoryNode` | inh | 784 | 580 |
| `Step->StoryNode` | inh | 810 | 556 |
| `Example->StoryNode` | inh | 836 | 524 |
| `Epic->StoryNode` | assoc | 849 | 556 |
| `SubEpic->StoryNode` | assoc | 888 | 626 |
| `StoryGroup->StoryNode` | assoc | 914 | 596 |
| `Scenario->StoryNode` | inh | right x=940 | 540 |
| `Scenario->StoryNode` | assoc | right x=927 | 450 |

### DomainGraph — pair separations

| Pair | inh channel | assoc channel | Sep |
|------|-------------|--------------|-----|
| `DomainGraph->CPG` | vert x=498 | — (single edge) | — |
| `DomainNode->CPNode` | vert x=858 | — (single edge) | — |
| `DomainModule->DomainNode` | corner x=871 | corner x=949 | 78 px |
| `KAN->DomainNode` | right corridor x=1260, y=358 | right corridor x=1300, y=374 | 40/16 px |
| `DCN->DomainNode` | horiz y=286 → x=910 | horiz y=300 → x=730→left | 14 px y |

### UxGraph

| Pair | inh channel | assoc channel | Sep |
|------|-------------|--------------|-----|
| `Screen->UxNode` | vert x≈519 | vert x≈623 | 104 px |

---

## Final audit result

```
=== Page: StoryGraph — PASS ===   No issues found.
=== Page: DomainGraph — PASS ===  No issues found.
=== Page: UxGraph     — PASS ===  No issues found.
(all other pages also PASS)

Definitive violations: 0
All violations resolved. ✓
```

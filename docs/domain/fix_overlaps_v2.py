"""
Fix all remaining edge_on_edge_overlap + shared_anchor violations.

KEY INSIGHT from checker (_compute_edge_segments_ex):
  - No waypoints + orthogonal → uses mid_x=(p1.x+p2.x)/2 for the vertical column.
    So even setting explicit exitX/entryX without waypoints → SAME mid_x for
    all same-pair edges.
  - With waypoints → last waypoint's x IS the approach vertical column.
  - Proximity threshold: two parallel segments <12px apart and >8px shared extent
    → flagged as overlap.

FIX STRATEGY:
  Every edge to StoryNode gets ONE or TWO waypoints at a unique (x, y) so the
  final approach vertical column is exactly known and ≥26px from all others.

  STORYGRAPH approach x allocation (all at StoryNode bottom y=452):
    Story inh   → x=680   (entryX=0.05)
    Epic inh    → x=719   (entryX=0.20)
    SubEpic inh → x=758   (entryX=0.35)
    StGrp inh   → x=784   (entryX=0.45)
    Step inh    → x=810   (entryX=0.55)
    Example inh → x=836   (entryX=0.65)
    Epic assoc  → x=849   (entryX=0.70)
    SubEpic ass → x=888   (entryX=0.85)
    StGrp assoc → x=914   (entryX=0.95)
    Scenario inh/assoc → enter from RIGHT side (different channel)

  STORYGRAPH gap y allocation (all in gap 452..676 or 1350→452):
    Distinct y per group so no horizontal at similar y overlaps.

Pages: StoryGraph, DomainGraph, UxGraph.
"""

import sys

sys.path.insert(
    0,
    r'C:\dev\abd-skills\practices\domain-driven-design\skills\supporting'
    r'\drawio-domain-sync\scripts',
)

from drawio_tools import (
    load_drawio, save_drawio, get_page,
    get_all_classes, get_all_edges,
    find_cell_by_name, find_cell_by_id,
    set_edge_anchors, add_edge_waypoints,
    audit_diagram_report,
)

DIAGRAM = r'C:\dev\abd-skills\docs\domain\abd-skills-domain-model.drawio'
_tree, mxfile = load_drawio(DIAGRAM)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def clear_waypoints(cell):
    geo = cell.find('mxGeometry')
    if geo is not None:
        for arr in geo.findall('Array'):
            geo.remove(arr)


def fix_edge(root, src_name, tgt_name, etype_substr,
             exit_x, exit_y, entry_x, entry_y, waypoints=None):
    """Locate the specific edge and apply anchors + waypoints."""
    src_id = find_cell_by_name(root, src_name).get('id')
    tgt_id = find_cell_by_name(root, tgt_name).get('id')
    found = False
    for eid, etype, s, t in get_all_edges(root):
        if s == src_id and t == tgt_id and etype_substr in etype:
            cell = find_cell_by_id(root, eid)
            clear_waypoints(cell)
            set_edge_anchors(cell,
                             exit_x=exit_x, exit_y=exit_y,
                             entry_x=entry_x, entry_y=entry_y)
            if waypoints:
                add_edge_waypoints(cell, waypoints)
            found = True
            break
    if not found:
        print(f'  WARNING: edge not found: {src_name}->{tgt_name} [{etype_substr}]',
              file=sys.stderr)


# ─────────────────────────────────────────────────────────────────────────────
# STORYGRAPH
# ─────────────────────────────────────────────────────────────────────────────

_, sg_root = get_page(mxfile, 'StoryGraph')
print('=== StoryGraph ===')

# StoryGraph → CPG  (existing fix — refresh)
# StoryGraph: x=285, w=260. CPG: x=829, w=260.
# exit bottom-center (0.5,1) at (415,826); entry top-center (0.5,0) at (959,60).
# waypoint (960,826) steers clear of all classes.
fix_edge(sg_root, 'StoryGraph', 'ContextPerspectiveGraph', 'inheritance',
         exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0,
         waypoints=[(960, 826)])
print('  StoryGraph->CPG  exit-bottom→(960,826)→CPG-top')

# ── StoryNode approaches ────────────────────────────────────────────────────
# All classes below StoryNode (y=334-452) reach it via vertical approach
# columns spaced 26px apart. Edges from row3 (y=676) go up through gap y=452..676.
# Edges from row4+ (Story y=938) route around Increment (x=130-390,y=880-1014).
#
# Approach x allocation (from StoryNode left to right):
#   x=680 Story inh (entryX=0.05)
#   x=719 Epic inh  (entryX=0.20)
#   x=758 SubEpic inh (entryX=0.35)
#   x=784 StGrp inh  (entryX=0.45)
#   x=810 Step inh   (entryX=0.55)
#   x=836 Example inh(entryX=0.65)
#   x=849 Epic assoc (entryX=0.70)
#   x=888 SubEpic ass(entryX=0.85)
#   x=914 StGrp assoc(entryX=0.95)
#   Scenario inh/assoc → RIGHT side of StoryNode

# Story → StoryNode inheritance
# Story: x=-160, w=260. Exit top(0.05) at (-147,938).
# Route: go straight up (avoiding Increment x=130-390 by staying at x=-147),
#        then hop right at y=564 to approach x=680.
# Expansion: (-147,938)→(-147,564)→(680,564)→(680,452) [all axis-aligned].
fix_edge(sg_root, 'Story', 'StoryNode', 'inheritance',
         exit_x=0.05, exit_y=0.0, entry_x=0.05, entry_y=1.0,
         waypoints=[(-147, 564), (680, 564)])
print('  Story->StoryNode  inh: x=-147↑→y=564→x=680↑→StoryNode(0.05)')

# Epic → StoryNode  (inh + assoc)
# Epic: x=645, w=260. Force verticals at x=719 (inh) and x=849 (assoc).
# Single waypoint mid-gap steers clear of any auto-routing artifacts.
# Expansion: (exit,676)→(target_x,676)→(target_x,556)→(target_x,452).
fix_edge(sg_root, 'Epic', 'StoryNode', 'inheritance',
         exit_x=0.2, exit_y=0.0, entry_x=0.2, entry_y=1.0,
         waypoints=[(719, 556)])
fix_edge(sg_root, 'Epic', 'StoryNode', 'association',
         exit_x=0.7, exit_y=0.0, entry_x=0.7, entry_y=1.0,
         waypoints=[(849, 556)])
print('  Epic->StoryNode  inh x=719, assoc x=849  (gap y=556)')

# SubEpic → StoryNode
# SubEpic: x=1005, w=260. Route via gap y=610 (inh) / y=626 (assoc).
# Two waypoints: exit-vertical then gap-horizontal, final vertical at target_x.
fix_edge(sg_root, 'SubEpic', 'StoryNode', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.35, entry_y=1.0,
         waypoints=[(1083, 610), (758, 610)])
fix_edge(sg_root, 'SubEpic', 'StoryNode', 'association',
         exit_x=0.7, exit_y=0.0, entry_x=0.85, entry_y=1.0,
         waypoints=[(1187, 626), (888, 626)])
print('  SubEpic->StoryNode  inh x=758 y=610, assoc x=888 y=626')

# StoryGroup → StoryNode
# StoryGroup: x=1365, w=260. Gap y=580 (inh) / y=596 (assoc).
fix_edge(sg_root, 'StoryGroup', 'StoryNode', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.45, entry_y=1.0,
         waypoints=[(1443, 580), (784, 580)])
fix_edge(sg_root, 'StoryGroup', 'StoryNode', 'association',
         exit_x=0.7, exit_y=0.0, entry_x=0.95, entry_y=1.0,
         waypoints=[(1547, 596), (914, 596)])
print('  StoryGroup->StoryNode  inh x=784 y=580, assoc x=914 y=596')

# Step → StoryNode inheritance
# Step: x=1725, w=260. Route via gap y=556.
# Exit from top at x=1868, drop to y=556, slide left to x=810, drop to StoryNode.
fix_edge(sg_root, 'Step', 'StoryNode', 'inheritance',
         exit_x=0.55, exit_y=0.0, entry_x=0.55, entry_y=1.0,
         waypoints=[(1868, 556), (810, 556)])
print('  Step->StoryNode  inh x=810 y=556')

# Example → StoryNode inheritance
# Example: x=2085, w=260. Route via gap y=524.
fix_edge(sg_root, 'Example', 'StoryNode', 'inheritance',
         exit_x=0.65, exit_y=0.0, entry_x=0.65, entry_y=1.0,
         waypoints=[(2254, 524), (836, 524)])
print('  Example->StoryNode  inh x=836 y=524')

# Scenario → StoryNode  (route via RIGHT side — avoids StoryGraphCli→Epic corridor)
# Scenario: x=1190, w=260, top=1350.
# Corridor x=1281 (between SubEpic.right=1265 and StoryGroup.left=1365).
# inh:  goes up at x=1281, hops to x=940, turns to StoryNode.right at y=369.
#   Expansion wp2→entry: (940,540)→(927,369) prev_dir="h" → vert first:
#     corner=(940,369). → (940,540)→(940,369)→(927,369). Vertical x=940 (≥12 from x=927). ✓
# assoc: goes up at x=1320, single wp at y=450, then L-turn to StoryNode.right at y=393.
#   Expansion wp→entry: (1320,450)→(927,393) prev_dir="v" → horiz first:
#     corner=(927,450). → (1320,450)→(927,450)→(927,393). Vertical x=927. |940-927|=13≥12. ✓
fix_edge(sg_root, 'Scenario', 'StoryNode', 'inheritance',
         exit_x=0.35, exit_y=0.0, entry_x=1.0, entry_y=0.3,
         waypoints=[(1281, 540), (940, 540)])
fix_edge(sg_root, 'Scenario', 'StoryNode', 'association',
         exit_x=0.5, exit_y=0.0, entry_x=1.0, entry_y=0.5,
         waypoints=[(1320, 450)])
print('  Scenario->StoryNode  inh via x=1281→940→right(0.3), assoc via x=1320→right(0.5)')


# ─────────────────────────────────────────────────────────────────────────────
# DOMAINGRAPH
# ─────────────────────────────────────────────────────────────────────────────

_, dg_root = get_page(mxfile, 'DomainGraph')
print('\n=== DomainGraph ===')

# DomainGraph → CPG  (single inheritance edge, no association)
# Both directly above each other (same x column). Stagger to x=498.
fix_edge(dg_root, 'DomainGraph', 'ContextPerspectiveGraph', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.3, entry_y=1.0)
print('  DomainGraph->CPG  inh: vertical x=498')

# DomainNode → CPNode  (single inheritance edge, no association)
# Move off x=910 (used by DCN→DN routes) → vertical at x=858.
fix_edge(dg_root, 'DomainNode', 'ContextPerspectiveNode', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.3, entry_y=1.0)
print('  DomainNode->CPNode  inh: vertical x=858')

# DomainModule → DomainNode  (inh + assoc, row 3→2)
# DomainModule top=724; DomainNode bottom=414.
# Stagger L-shaped routes: inh corner at x=871, assoc corner at x=949.
# Both go: exit top → horizontal at y=724 (row3 top) → vertical down to entry bottom.
fix_edge(dg_root, 'DomainModule', 'DomainNode', 'inheritance',
         exit_x=0.35, exit_y=0.0, entry_x=0.35, entry_y=1.0)
fix_edge(dg_root, 'DomainModule', 'DomainNode', 'association',
         exit_x=0.65, exit_y=0.0, entry_x=0.65, entry_y=1.0)
print('  DomainModule->DomainNode  inh x=871, assoc x=949')

# KeyAbstractionNode → DomainNode  (inh + assoc)
# KAN: x=974, w=260, top=724; DomainNode: x=780-1040, bottom=414.
# inh: exit top(0.1)=(1000,724) → RIGHT corridor at x=1260 → enter DomainNode.right at y=358.
#   wp1=(1260,724): same y as exit → axis-aligned horizontal.
#   wp2=(1260,358): same x as wp1 → axis-aligned vertical.
#   wp2→entry=(1040,358): same y → axis-aligned horizontal. CLEAN.
# assoc: exit right(1.0,0.5)=(1234,767) → far-right corridor x=1300 → enter right at y=374.
#   wp1=(1300,767): same y → horizontal. wp2=(1300,374): vertical.
#   wp2→entry=(1040,374): same y → horizontal. CLEAN.
# inh horizontal at y=358, assoc horizontal at y=374 → 16px > 12 ✓
# inh vertical x=1260, assoc vertical x=1300 → 40px ✓
# AVOIDS DomainModule (x=614-874) entirely (corridor is x=1040-1300).
fix_edge(dg_root, 'KeyAbstractionNode', 'DomainNode', 'inheritance',
         exit_x=0.1, exit_y=0.0, entry_x=1.0, entry_y=0.3,
         waypoints=[(1260, 724), (1260, 358)])
fix_edge(dg_root, 'KeyAbstractionNode', 'DomainNode', 'association',
         exit_x=1.0, exit_y=0.5, entry_x=1.0, entry_y=0.5,
         waypoints=[(1300, 767), (1300, 374)])
print('  KAN->DomainNode  inh: top→x=1260 corridor→right(y=358)')
print('  KAN->DomainNode  assoc: right→x=1300 corridor→right(y=374)')

# DomainConceptNode → DomainNode  (inh + assoc)
# DCN: x=254, w=260, top=724; DomainNode: x=780-1040, bottom=414 / left=780.
# Left corridor: x=320-420 (between DomainGraphCli.right=320 and DomainGraph.left=420).
#
# inh: exit top(0.3)=(332,724) → up at x=332 to y=286 → right to x=910 → down to DN bottom(0.5,1)=(910,414).
#   All segments axis-aligned. Horizontal at y=286 (gap row1-row2, all clear). ✓
#   Entry (0.5,1) gives unique anchor (DomainModule uses 0.35, no collision). ✓
# assoc: exit top(0.39)≈(355,724) → up at x=355 to y=300 → right to x=730 → down to y=374
#         → right to DN left(0,0.5)=(780,374).
#   x=355 vs x=332: 23px > 12 ✓. Horizontals y=286 vs y=300: 14px > 12 ✓.
#   Vertical x=730 is in corridor DomainGraph.right=680 → DomainNode.left=780.
#   All clear.
fix_edge(dg_root, 'DomainConceptNode', 'DomainNode', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.5, entry_y=1.0,
         waypoints=[(332, 286), (910, 286)])
fix_edge(dg_root, 'DomainConceptNode', 'DomainNode', 'association',
         exit_x=0.39, exit_y=0.0, entry_x=0.0, entry_y=0.5,
         waypoints=[(355, 300), (730, 300), (730, 374)])
print('  DCN->DomainNode  inh: (332,286)→(910,286)→DN-bottom(0.5)')
print('  DCN->DomainNode  assoc: (355,300)→(730,300)→(730,374)→DN-left(0.5)')


# ─────────────────────────────────────────────────────────────────────────────
# UXGRAPH
# ─────────────────────────────────────────────────────────────────────────────

_, ux_root = get_page(mxfile, 'UxGraph')
print('\n=== UxGraph ===')

# Screen → UxNode  (inh + assoc)
# Screen: x=420, w=260, top=574; UxNode: x=463, w=260, bottom=414.
# Stagger to separate verticals: inh x=541, assoc x=645 (104px apart).
fix_edge(ux_root, 'Screen', 'UxNode', 'inheritance',
         exit_x=0.3, exit_y=0.0, entry_x=0.3, entry_y=1.0)
fix_edge(ux_root, 'Screen', 'UxNode', 'association',
         exit_x=0.7, exit_y=0.0, entry_x=0.7, entry_y=1.0)
print('  Screen->UxNode  inh mid-x=(498+541)/2≈519→vert, assoc≈623 (104px apart)')


# ─────────────────────────────────────────────────────────────────────────────
# Save & audit
# ─────────────────────────────────────────────────────────────────────────────

save_drawio(DIAGRAM, mxfile)
print(f'\nSaved: {DIAGRAM}')

report = audit_diagram_report(DIAGRAM)
print('\n' + report)

violations = [ln for ln in report.splitlines()
              if ('[edge_crosses_class]' in ln and '(approx)' not in ln)
              or '[edge_on_edge_overlap]' in ln]

print(f'\nDefinitive violations: {len(violations)}')
if violations:
    print('Remaining:')
    for ln in violations:
        print('  ' + ln)
    sys.exit(1)
else:
    print('All violations resolved. ✓')

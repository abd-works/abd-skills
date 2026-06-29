"""
Fix definitive edge_crosses_class violations in abd-skills-domain-model.drawio.

Key insight about _compute_edge_segments_ex expansion:
  prev_dir='v'  → next diagonal bends VERTICAL first  (corner = (ax, by))
  prev_dir='h'  → next diagonal bends HORIZONTAL first (corner = (bx, ay))
  prev_dir=None → horizontal first (corner = (bx, ay))

Violations to fix
-----------------

StoryGraph page — StoryGraph->ContextPerspectiveGraph (inheritance-orthogonal)
  Original exit/entry: top-center (415,676) → bottom-center (959,170)
  Approx mid_x=687 path: horizontal at y=676 passes through Epic (x=645–905)
  Fix:
    Exit from BOTTOM center (exitY=1): (415, 826)
    Entry at TOP center (entryY=0):   (959,  60)
    Waypoint: (960, 826)
  Expanded path:
    (415,826)→(960,826)  horizontal at y=826 — below Epic bottom=762  ✓
    (960,826)→(959,826)  1-px horizontal expansion (source area)        ✓
    (959,826)→(959,  60) vertical at x=959 — right of StoryNode (927),
                          right of ContextPerspectiveNode (729),
                          CPG is target → skipped                       ✓

DomainGraph page — DomainConceptNode->DomainNode (association)
  Original: exit top (414,724), entry left-low (780,402)
  Approx mid_x=597: vertical at x=597 passes through DomainGraph (x=420–680)
  Fix:
    Keep exit anchor: exitX=0.617, exitY=0   → (414, 724)
    Change entry to TOP center: entryX=0.5, entryY=0 → (910, 334)
    Waypoints: (340, 300) then (910, 300)
  Expanded path (all pure axis-aligned — no diagonal expansion):
    (414,724)→(340,724)  horizontal left (source area)                   ✓
    (340,724)→(340,300)  vertical up at x=340, in corridor DomainGraphCli
                          right=320 < 340 < 420 DomainGraph left          ✓
    (340,300)→(910,300)  horizontal at y=300 — above DomainGraph top=334 ✓
    (910,300)→(910,334)  vertical — DomainNode target, skipped           ✓

DomainGraph page — DomainConceptNode->DomainNode (inheritance-orthogonal)
  Same corridor as association, but with shifted exit (exitX=0.3 → x=332)
  so the two edges no longer share an anchor point.
  Entry changed to BOTTOM center: entryX=0.5, entryY=1 → (910, 414)
  Waypoints: (332, 300) then (910, 300)
  Expanded path (all pure axis-aligned):
    (332,724)→(332,300)  vertical up at x=332, corridor 320–420          ✓
    (332,300)→(910,300)  horizontal at y=300                             ✓
    (910,300)→(910,414)  vertical — DomainNode target, skipped           ✓
"""

import sys
sys.path.insert(
    0,
    r'C:\dev\abd-skills\practices\domain-driven-design\skills\supporting'
    r'\drawio-domain-sync\scripts',
)

from drawio_tools import (
    load_drawio, save_drawio, get_page,
    find_cell_by_name, find_cell_by_id,
    get_all_edges, set_edge_anchors, add_edge_waypoints,
    audit_diagram_report,
)

DIAGRAM = r'C:\dev\abd-skills\docs\domain\abd-skills-domain-model.drawio'

_tree, mxfile = load_drawio(DIAGRAM)


# ─────────────────────────────────────────────────────────────────────────────
# StoryGraph page
# ─────────────────────────────────────────────────────────────────────────────
_, sg_root = get_page(mxfile, 'StoryGraph')

sg_id  = find_cell_by_name(sg_root, 'StoryGraph').get('id')
cpg_id = find_cell_by_name(sg_root, 'ContextPerspectiveGraph').get('id')

for eid, etype, src, tgt in get_all_edges(sg_root):
    if src == sg_id and tgt == cpg_id and 'inheritance' in etype:
        edge = find_cell_by_id(sg_root, eid)
        # Route: exit bottom → go right past all row-3 classes → up x=959
        # (right of StoryNode x=927, right of CPG node x=729) → enter CPG top
        set_edge_anchors(edge, exit_x=0.5, exit_y=1.0,
                         entry_x=0.5, entry_y=0.0)
        add_edge_waypoints(edge, [(960, 826)])
        print(f'  StoryGraph: rerouted {etype} edge {eid} via bottom→(960,826)→CPG-top')


# ─────────────────────────────────────────────────────────────────────────────
# DomainGraph page
# ─────────────────────────────────────────────────────────────────────────────
_, dg_root = get_page(mxfile, 'DomainGraph')

dcn_id = find_cell_by_name(dg_root, 'DomainConceptNode').get('id')
dn_id  = find_cell_by_name(dg_root, 'DomainNode').get('id')

for eid, etype, src, tgt in get_all_edges(dg_root):
    if src == dcn_id and tgt == dn_id:
        edge = find_cell_by_id(dg_root, eid)
        if etype == 'association':
            # Keep exit at top (exitX=0.617 → x=414).
            # Change entry to TOP of DomainNode (entryY=0 → y=334).
            # Waypoints thread through the corridor x=320–420, above DomainGraph.
            set_edge_anchors(edge, exit_x=0.617, exit_y=0.0,
                             entry_x=0.5, entry_y=0.0)
            add_edge_waypoints(edge, [(340, 300), (910, 300)])
            print(f'  DomainGraph: rerouted {etype} edge {eid} via (340,300)→(910,300)→top')
        elif 'inheritance' in etype:
            # Shift exit left (exitX=0.3 → x=332) to separate anchors from
            # the association edge above.  Enter at BOTTOM of DomainNode.
            # Same corridor, slightly different x.
            set_edge_anchors(edge, exit_x=0.3, exit_y=0.0,
                             entry_x=0.5, entry_y=1.0)
            add_edge_waypoints(edge, [(332, 300), (910, 300)])
            print(f'  DomainGraph: rerouted {etype} edge {eid} via (332,300)→(910,300)→bottom')


# ─────────────────────────────────────────────────────────────────────────────
# Save & audit
# ─────────────────────────────────────────────────────────────────────────────
save_drawio(DIAGRAM, mxfile)
print(f'\nSaved: {DIAGRAM}')

report = audit_diagram_report(DIAGRAM)
print('\n' + report)

definitive = [
    ln for ln in report.splitlines()
    if '[edge_crosses_class]' in ln and '(approx)' not in ln
]
if definitive:
    print('\nStill has definitive violations:', file=sys.stderr)
    for ln in definitive:
        print('  ' + ln, file=sys.stderr)
    sys.exit(1)
else:
    print('\nAll definitive edge_crosses_class violations resolved. ✓')

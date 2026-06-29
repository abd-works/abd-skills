# drawio-domain-sync iterative improvement — SUMMARY

Goal: bring CLI-generated diagram of `abd-skills-domain-model.md` to a clean
audit, focusing on the `AbdSkill` page (with `AiChatAgent` and
`Context-Driven Delivery` tracked as a regression guard).

## Final result — run-4 PASSES all three pages

| Page                       | run-1 | run-2 | run-3 | run-4   |
| -------------------------- | ----- | ----- | ----- | ------- |
| AbdSkill — crossings       | 2     | 2     | 0     | **0** ✅ |
| AbdSkill — overlaps        | 1     | 1     | 3     | **0** ✅ |
| AiChatAgent — crossings    | 0     | 0     | 0     | **0** ✅ |
| AiChatAgent — overlaps     | 3     | 3     | 1     | **0** ✅ |
| CDD — crossings            | 1     | 1     | 0     | **0** ✅ |
| CDD — overlaps             | 1     | 1     | 0     | **0** ✅ |

Hierarchy-flow violations: 0 in all runs (rule "base above derived" satisfied
throughout).

## Skill changes made during iteration

### New rules (run-2)

- `rules/class-diagram-edges-do-not-cross-classes.md`
- `rules/class-diagram-edges-do-not-overlap-other-edges.md`

### New scanners (run-2)

- `scanners/edges_do_not_cross_classes.py` — wraps
  `drawio_tools.check_edges_crossing_classes`.
- `scanners/edges_do_not_overlap_edges.py` — wraps
  `drawio_tools.check_edge_on_edge_overlaps`.

### CLI engine changes (runs 3 and 4)

In `scripts/drawio_domain_cli.py`:

1. **Obstacle-avoiding U-shape router** (run-3)
   - Replaced the previous single-waypoint dog-leg picker with an axis-aligned
     U-shape generator that produces 2- and 3-waypoint candidates around
     blocker rectangles, with multiple offset lanes per side.
   - Replaced the straight-line "candidate doesn't cross obstacle" filter
     with `_path_crossings`, which matches the audit's interpretation:
     - source→first-waypoint expanded H-V-H,
     - inner waypoint-to-waypoint segments treated as straight lines.
   - Added lane awareness: when picking a detour, candidates that overlap
     any other edge's already-routed segments are deprioritised. For paths
     with no waypoints, the other edge's segments are computed as H-V-H to
     match drawio's auto-routing.
   - Added a second post-pass that re-routes any edge whose final path
     overlaps another edge, choosing a different lane when possible.
   - `_stagger_target_approach` stays as a final stub-staggering safety net.

2. **Side reassignment** (run-4)
   - After `_dominant_side`, a second pass moves association/composition/
     aggregation edges off any side that already carries inheritance
     traffic. The new side is the perpendicular side that points toward
     the target.
   - This is what unblocked the last three overlaps on the AbdSkill page:
     `AbdSkill → Reference`, `PracticeSkill → Reference`, and
     `PracticeSkill → Practice` all moved off their parents' crowded
     bottom rows.

### Other notes

- The hand-curated `evals/abd-skills-domain-model-good.drawio` is NOT a
  strict gold standard. Running the same audit against it reports 4
  `edge_crosses_class (approx)` violations and 3 `hierarchy_flow`
  violations (it draws derived above base, opposite to the rule the skill
  enforces). Run-4 strictly passes the audit; the good ref does not.

- All four iterations kept the deployed copy in
  `c:\dev\paradise-mobile\.cursor\skills\drawio-domain-sync\` in sync with
  the source under
  `c:\dev\abd-skills\practices\domain-driven-design\skills\supporting\drawio-domain-sync\`.

## Stop condition reached

The iterative goal — clean audit for the AbdSkill page (and no regression
on the other two pages) — is met at run-4. No further runs scheduled.

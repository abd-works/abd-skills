# eval — Agentic Repair Loop

---

## Execution model — always run as a background sub-agent

The repair loop is a multi-step, iterative process. It must be launched as a
**non-blocking background sub-agent** so that the main conversation can continue
uninterrupted while the loop runs.

**How to launch:**

```
Task tool — subagent_type: generalPurpose, run_in_background: true
```

The prompt must include:
- The absolute path to the diagram file
- The entry point (A or B) and the violation or user complaint verbatim
- Any reference files (good/bad examples, target coordinates) the agent needs
- A clear instruction: do NOT rebuild from spec; apply surgical fixes only
- Which page(s) to touch and which to leave alone

The parent agent ends its turn immediately after launching. The sub-agent
notifies on completion.

---

## Entry points — choose the right one before starting

### Entry A — scanners/rules already found the problem

`audit_diagram_report()` returned violations. The loop is runnable immediately.
Proceed directly to **Step 1**.

### Entry B — the user found the problem (scanners passed)

The diagram looks clean to the tools but the user sees something wrong.

**You cannot run the repair loop until the tools see the same problem.**

Do this first:

1. **Understand the user's complaint exactly.** Ask for specifics if needed
   (which page, which edge, what is wrong visually).
2. **Identify the gap.** Read the relevant scanner(s) and rule(s) in
   `scanners/` and `rules/`. Determine why they missed it — wrong threshold,
   missing geometry case, rule not codified, etc.
3. **Fix the scanner or rule** until `audit_diagram_report()` flags the same
   problem the user described. This may require:
   - Tightening a proximity/overlap threshold in a scanner
   - Adding a new check to `validate_layout()` in `drawio_tools.py`
   - Writing a new scanner file
   - Adding a new rule `.md` to `rules/`
4. **Verify the scanner now catches it.** Run `audit_diagram_report()` — it
   must report a violation on the specific case the user raised.
5. **Capture a fail fixture** for this new scanner/rule gap (see Step 3 below)
   so it becomes a permanent regression test.

Only once the scanner/rule reliably detects the problem, proceed to **Step 1**
and run the repair loop as normal.

> **Key principle:** never attempt to fix the diagram without a verifiable
> error signal. If you can't reproduce the failure programmatically, you have
> no way to know when you've fixed it.

---

## 1. Archive and create the eval folder

The eval folder lives **next to the generated diagram**:

```
<diagram-dir>/evals/
```

If `evals/` already exists from a prior session, rename it before starting:

```
evals/        →  evals-1/
evals-1/      →  evals-2/    (if both exist)
...
```

Then create a fresh run folder:

```
evals/run-1/
```

Subsequent fix attempts in the same session become `run-2`, `run-3`, etc.

---

## 2. Write violations.md

Create `evals/run-<n>/violations.md`. Include, for every definitive violation:

| Field        | Content |
|--------------|---------|
| Rule         | filename from `rules/` |
| Page         | which diagram tab |
| Edge type    | inheritance / association / composition / … |
| Source class | name + anchor coords |
| Target class | name + anchor coords |
| Violator     | class name + bounding box |
| Category     | `edge_crosses_class`, `edge_on_edge_overlap`, `shared_anchor` |
| Root cause   | why the CLI routed it this way |
| Fix applied  | anchor changes + waypoints used |

Non-blocking warnings (approx / cosmetic) may be listed separately but do not
block the loop.

---

## 3. Capture fail fixtures

For each failing page, extract a **single-page `.drawio`** and save it as a
fixture:

```
eval/fail/<slug>/diagram.drawio
```

Where `<slug>` describes the violation (e.g.
`story-graph-inheritance-crosses-epic`).

Update `eval/cases.json` with the new fixture entry:

```json
"fail/<slug>": {
  "date": "<YYYY-MM-DD>",
  "situation": "<one sentence>",
  "rules": [
    { "rule": "<rule-file>", "scanner": "<scanner-file>", "expect": "violate" },
    ...
  ]
}
```

---

## 4. Apply the fix

For routing violations, the most reliable approach is a bespoke Python fix
script that calls `drawio_tools` directly:

```python
from drawio_tools import (
    load_drawio, save_drawio, get_page,
    find_cell_by_name, find_cell_by_id, get_all_edges,
    set_edge_anchors, add_edge_waypoints,
    audit_diagram_report,
)
# ...
set_edge_anchors(edge, exit_x=..., exit_y=..., entry_x=..., entry_y=...)
add_edge_waypoints(edge, [(x1, y1), (x2, y2)])
```

**Key insight for orthogonal edge routing:**

The checker (`_compute_edge_segments_ex`) expands orthogonal edges using the
**previous segment direction** to decide corner orientation:

- `prev_dir = 'v'` → next bend is **vertical first** → corner at `(ax, by)`
- `prev_dir = 'h'` or `None` → next bend is **horizontal first** → corner at `(bx, ay)`

A 5-pixel margin is added to all class bounding boxes during intersection
tests. Plan waypoints so every segment runs through a clear corridor.

**Three reliable escape corridors:**

1. **Bottom-then-right:** Exit bottom, waypoint below all row classes, travel
   right then up to target.
2. **Left corridor:** Exit top, waypoint to the left of the leftmost blocker
   class, travel up then right to target.
3. **Right corridor:** Exit top/bottom, waypoint to the right of the rightmost
   class on the row, travel up/down then across.

---

## 5. Run the audit

After each fix attempt, run:

```python
report = audit_diagram_report(DIAGRAM)
print(report)
```

Save the output (or a `violations.md` diff) in `evals/run-<n>/`.

If violations remain, increment to `run-<n+1>` and repeat from step 2.

---

## 6. Capture pass fixtures

Once a page is clean, extract the single-page `.drawio` and save it as:

```
eval/pass/<slug>/diagram.drawio
```

Update `eval/cases.json` with the pass entry. The pass fixture becomes a
**regression sentinel** — future CLI changes must not break it.

---

## 7. Propagate CLI improvements

If the fix reveals a systematic routing problem in the CLI (not a one-off
layout quirk), improve `drawio_domain_cli.py` so future generated diagrams
don't have the same issue. Document the change in `evals/SUMMARY.md`.

---

## File map

| Path | Purpose |
|------|---------|
| `<diagram-dir>/evals/run-<n>/violations.md` | Per-run violation report |
| `<diagram-dir>/evals/SUMMARY.md` | Cross-run summary once stable |
| `eval/fail/<slug>/diagram.drawio` | Single-page fail fixture |
| `eval/pass/<slug>/diagram.drawio` | Single-page pass fixture |
| `eval/cases.json` | Fixture registry with expected scanner results |

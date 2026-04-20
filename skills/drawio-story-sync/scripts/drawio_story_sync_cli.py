#!/usr/bin/env python3
"""CLI for story DrawIO render and layout (**drawio-story-sync** + **story-graph-ops**).

Put **this** ``scripts`` directory and **story-graph-ops** ``scripts`` on ``PYTHONPATH``,
or run from this repo layout where the sibling skill exists (paths are added automatically).

Example (PowerShell):

```text
$env:PYTHONPATH = "C:\\dev\\agilebydesign-skills\\skills\\drawio-story-sync\\scripts;C:\\dev\\agilebydesign-skills\\skills\\story-graph-ops\\scripts"
cd C:\\dev\\agilebydesign-skills\\skills\\drawio-story-sync\\scripts
python drawio_story_sync_cli.py render --mode outline --graph C:\\tmp\\story-graph.json --out C:\\tmp\\story-map.drawio
```
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

_MODES = {
    'outline': 'render-outline',
    'story-map': 'render-outline',
    'exploration': 'render-exploration',
    'acceptance-criteria': 'render-exploration',
    'increments': 'render-increments',
    'thin-slices': 'render-increments',
    'prioritization': 'render-increments',
}


def _ensure_story_graph_ops_path() -> None:
    """Sibling ``story-graph-ops/scripts`` (same layout as ``story_io_synchronizer``)."""
    ops = _SCRIPT_DIR.parent / 'story-graph-ops' / 'scripts'
    if ops.is_dir() and str(ops) not in sys.path:
        sys.path.insert(0, str(ops))


def cmd_render(args: argparse.Namespace) -> int:
    _ensure_story_graph_ops_path()
    from drawio_story_sync.story_io_synchronizer import DrawIOSynchronizer

    mode = (args.mode or 'outline').lower().replace('_', '-')
    renderer = _MODES.get(mode)
    if not renderer:
        print(f"Unknown mode {args.mode!r}. Use: {', '.join(sorted(set(_MODES)))}", file=sys.stderr)
        return 2

    sync = DrawIOSynchronizer()
    kw = {}
    if args.scope:
        kw['scope'] = args.scope
    sync.render(args.graph, args.out, renderer_command=renderer, **kw)
    print(json.dumps({'status': 'ok', 'output': str(args.out), 'mode': mode, 'renderer_command': renderer}))
    return 0


def cmd_save_layout(args: argparse.Namespace) -> int:
    _ensure_story_graph_ops_path()
    from drawio_story_sync.story_io_synchronizer import DrawIOSynchronizer

    r = DrawIOSynchronizer().save_layout(args.drawio)
    print(json.dumps(r))
    return 0 if r.get('status') == 'success' else 1


def cmd_apply_report(args: argparse.Namespace) -> int:
    """Apply ``*-update-report.json`` to ``story-graph.json`` using **story_graph_ops** (no DrawIO)."""
    _ensure_story_graph_ops_path()
    from story_graph_ops.nodes import StoryMap
    from story_graph_ops.update_report import UpdateReport

    report_path = Path(args.report)
    graph_path = Path(args.graph)
    if not report_path.is_file():
        print(f"Missing report: {report_path}", file=sys.stderr)
        return 2
    if not graph_path.is_file():
        print(f"Missing graph: {graph_path}", file=sys.stderr)
        return 2

    report = UpdateReport.from_dict(json.loads(report_path.read_text(encoding='utf-8')))
    story_map = StoryMap.from_json_file(graph_path)
    story_map.apply_update_report(report)
    if not getattr(args, 'dry_run', False):
        story_map.save()
    print(json.dumps({'status': 'ok', 'graph_path': str(graph_path), 'dry_run': bool(getattr(args, 'dry_run', False))}))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    _ensure_story_graph_ops_path()
    from drawio_story_sync.drawio_story_map import DrawIOStoryMap
    from story_graph_ops.nodes import StoryMap

    diagram = Path(args.drawio)
    graph = Path(args.graph)
    if not diagram.is_file():
        print(f"Missing diagram: {diagram}", file=sys.stderr)
        return 2
    drawio_map = DrawIOStoryMap.load(diagram)
    from drawio_story_sync.story_io_synchronizer import DrawIOSynchronizer, load_story_graph_json

    DrawIOSynchronizer().save_layout(diagram)

    original = StoryMap(load_story_graph_json(graph))
    if args.scope:
        filtered = original.filter_by_name(args.scope)
        if filtered is not None:
            original = filtered

    extracted_path = diagram.parent / f"{diagram.stem}-extracted.json"
    drawio_map.save_as_json(extracted_path)
    report = drawio_map.generate_update_report(original)
    out = Path(args.report_out) if args.report_out else diagram.parent / f"{diagram.stem}-update-report.json"
    report.save(out)
    print(json.dumps({'status': 'ok', 'report_path': str(out), 'extracted_path': str(extracted_path)}))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description='DrawIO story map render / sync helpers')
    sub = p.add_subparsers(dest='cmd', required=True)

    r = sub.add_parser('render', help='Render story-graph.json to .drawio')
    r.add_argument('--mode', default='outline', help='outline | exploration | increments (+ aliases)')
    r.add_argument('--graph', type=Path, required=True, help='Path to story-graph.json')
    r.add_argument('--out', type=Path, required=True, help='Output .drawio path')
    r.add_argument('--scope', help='Optional story/epic/sub-epic name to filter graph')
    r.set_defaults(func=cmd_render)

    s = sub.add_parser('save-layout', help='Write *-layout.json next to a .drawio')
    s.add_argument('--drawio', type=Path, required=True)
    s.set_defaults(func=cmd_save_layout)

    g = sub.add_parser('report', help='Extract diagram, diff vs story graph, write update report JSON')
    g.add_argument('--drawio', type=Path, required=True)
    g.add_argument('--graph', type=Path, required=True)
    g.add_argument('--report-out', type=Path, help='Defaults to <stem>-update-report.json beside diagram')
    g.add_argument('--scope', help='Optional filter on original story map')
    g.set_defaults(func=cmd_report)

    a = sub.add_parser(
        'apply-report',
        help='Apply update-report JSON to story-graph.json (story_graph_ops; no diagram read)',
    )
    a.add_argument('--graph', type=Path, required=True, help='Path to story-graph.json to update')
    a.add_argument('--report', type=Path, required=True, help='Path to *-update-report.json')
    a.add_argument('--dry-run', action='store_true', help='Apply in memory only; do not write graph')
    a.set_defaults(func=cmd_apply_report)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == '__main__':
    raise SystemExit(main())

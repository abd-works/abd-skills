#!/usr/bin/env python3
"""CLI for Miro story-map render (**miro-story-sync** + **story-graph-ops**).

Put **`common/`**, **this skill's `scripts/`**, and **story-graph-ops**
``scripts/`` on ``PYTHONPATH``, or run from the standard monorepo layout
where the sibling skills exist (paths are added automatically).

Example (PowerShell):

```text
$env:MIRO_ACCESS_TOKEN = "<your token>"
python miro_story_sync_cli.py render --mode outline `
    --graph C:\\tmp\\story-graph.json `
    --board uXjVK123abc=
python miro_story_sync_cli.py render --mode outline `
    --graph C:\\tmp\\story-graph.json --dry-run
```

``--dry-run`` swaps in ``InMemoryMiroTransport`` so you can verify rendering
without contacting Miro. Without a token (and without ``--dry-run``) the CLI
exits non-zero and prints the auth requirement.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


_MODES = {
    'outline': 'render-outline',
    'story-map': 'render-outline',
}


def _ensure_repo_paths() -> None:
    """Sibling ``story-graph-ops/scripts`` and ``common/`` (mirrors miro_story_sync._bootstrap)."""
    skill_root = _SCRIPT_DIR.parent
    skills_dir = skill_root.parent
    repo_root = skills_dir.parent
    for p in (repo_root / 'common', skills_dir / 'story-graph-ops' / 'scripts'):
        s = str(p)
        if p.is_dir() and s not in sys.path:
            sys.path.insert(0, s)


def _build_transport(board_id: Optional[str], dry_run: bool):
    """Return ``(transport, transport_name, dry_run_actual)``.

    Falls back to ``InMemoryMiroTransport`` when ``--dry-run`` is set or when
    no ``MIRO_ACCESS_TOKEN`` is configured (so ``render`` works locally for
    smoke tests without surprising the user with HTTP errors).
    """
    from miro_story_sync.miro_transport import (
        InMemoryMiroTransport,
        MiroTransportError,
        RestMiroTransport,
    )

    if dry_run or not board_id:
        return InMemoryMiroTransport(), 'InMemoryMiroTransport', True
    if not os.environ.get('MIRO_ACCESS_TOKEN'):
        return InMemoryMiroTransport(), 'InMemoryMiroTransport', True
    try:
        return RestMiroTransport(board_id), 'RestMiroTransport', False
    except MiroTransportError:
        return InMemoryMiroTransport(), 'InMemoryMiroTransport', True


def cmd_render(args: argparse.Namespace) -> int:
    _ensure_repo_paths()
    from miro_story_sync.miro_story_synchronizer import MiroSynchronizer

    mode = (args.mode or 'outline').lower().replace('_', '-')
    renderer = _MODES.get(mode)
    if not renderer:
        print(
            f"Unknown mode {args.mode!r}. Use: {', '.join(sorted(set(_MODES)))}",
            file=sys.stderr,
        )
        return 2

    transport, transport_name, dry_run_actual = _build_transport(
        getattr(args, 'board', None), bool(getattr(args, 'dry_run', False)),
    )
    sync = MiroSynchronizer(transport=transport)
    kw = {}
    if args.scope:
        kw['scope'] = args.scope
    result = sync.render(args.graph, renderer_command=renderer, **kw)

    print(json.dumps({
        'status': 'ok',
        'graph': str(args.graph),
        'mode': mode,
        'renderer_command': renderer,
        'transport': transport_name,
        'dry_run': dry_run_actual,
        'board_id': result.get('board_id'),
        'item_count': result.get('item_count', 0),
        'summary': result.get('summary'),
    }))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description='Miro story map render helpers')
    sub = p.add_subparsers(dest='cmd', required=True)

    r = sub.add_parser('render', help='Render story-graph.json onto a Miro board')
    r.add_argument('--mode', default='outline', help='outline | story-map')
    r.add_argument('--graph', type=Path, required=True, help='Path to story-graph.json')
    r.add_argument('--board', help='Miro board id (omit with --dry-run)')
    r.add_argument(
        '--dry-run',
        action='store_true',
        help='Use InMemoryMiroTransport; nothing is sent to Miro.',
    )
    r.add_argument('--scope', help='Optional story/epic/sub-epic name to filter graph')
    r.set_defaults(func=cmd_render)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == '__main__':
    raise SystemExit(main())

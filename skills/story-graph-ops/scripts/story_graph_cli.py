#!/usr/bin/env python3
"""CLI for reading, searching, filtering, and writing ``story-graph.json`` without agile_bots.

Add ``…/story-graph-ops/scripts`` and ``…/execute_using_rules/scripts`` to PYTHONPATH, then:

  python story_graph_cli.py read --file path/to/story-graph.json
  python story_graph_cli.py names --file path/to/story-graph.json
  python story_graph_cli.py search --file ... --substring "Login"
  python story_graph_cli.py filter --file ... --stories "A","B" > subset.json
  python story_graph_cli.py write --file out.json < input.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

# Allow running from repo without install: parent directory is on PYTHONPATH
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


def _load_graph(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        print(f"[error] not a file: {path}", file=sys.stderr)
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def _collect_story_names(data: Dict[str, Any]) -> List[str]:
    from story_map import Story, StoryMap

    sm = StoryMap(data)
    names: List[str] = []
    for epic in sm.epics():
        for node in sm.walk(epic):
            if isinstance(node, Story) and node.name:
                names.append(node.name)
    return names


def cmd_read(args: argparse.Namespace) -> int:
    data = _load_graph(Path(args.file))
    if args.pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))
    return 0


def cmd_names(args: argparse.Namespace) -> int:
    data = _load_graph(Path(args.file))
    for n in _collect_story_names(data):
        print(n)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    data = _load_graph(Path(args.file))
    sub = (args.substring or "").lower()
    hits = [n for n in _collect_story_names(data) if sub in n.lower()]
    for n in hits:
        print(n)
    return 0 if hits else 1


def cmd_filter(args: argparse.Namespace) -> int:
    from graph_filters import filter_story_graph_to_story_names

    data = _load_graph(Path(args.file))
    raw = args.stories or ""
    names: Set[str] = {s.strip() for s in raw.split(",") if s.strip()}
    out = filter_story_graph_to_story_names(data, names)
    if args.pretty:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False))
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path}", file=sys.stderr)
    return 0


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="story_graph_cli", description="Story graph file operations")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("read", help="Print JSON story graph")
    r.add_argument("--file", required=True, help="Path to story-graph.json")
    r.add_argument("--pretty", action="store_true", help="Indent JSON")
    r.set_defaults(func=cmd_read)

    n = sub.add_parser("names", help="List story names (flat)")
    n.add_argument("--file", required=True)
    n.set_defaults(func=cmd_names)

    s = sub.add_parser("search", help="List story names containing substring (case-insensitive)")
    s.add_argument("--file", required=True)
    s.add_argument("--substring", required=True)
    s.set_defaults(func=cmd_search)

    f = sub.add_parser("filter", help="Emit graph subset containing only named stories")
    f.add_argument("--file", required=True)
    f.add_argument("--stories", required=True, help="Comma-separated story names")
    f.add_argument("--pretty", action="store_true")
    f.set_defaults(func=cmd_filter)

    w = sub.add_parser("write", help="Write JSON from stdin (-) or --input file")
    w.add_argument("--file", required=True, help="Output path")
    w.add_argument("--input", default="-", help="Input JSON path or - for stdin")
    w.set_defaults(func=cmd_write)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

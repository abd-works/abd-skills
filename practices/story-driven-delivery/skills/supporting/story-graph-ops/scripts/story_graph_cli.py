#!/usr/bin/env python3
"""CLI for reading, searching, filtering, and writing ``story-graph.json``."""
from __future__ import annotations

import argparse
import graph_path_bootstrap  # noqa: F401
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

from graph_cli_commands import (
    run_filter_command,
    run_names_command,
    run_read_command,
    run_search_command,
    run_sha_command,
    run_write_command,
)
from graph_cli_subparsers import (
    add_names_parser,
    add_read_parser,
    add_search_parser,
    add_sha_parser,
    add_write_parser,
)

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


def _load_graph(path: Path) -> Dict[str, Any]:
    from story_graph_file import load_story_graph_dict

    if not path.is_file():
        print(f"[error] not a file: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        return load_story_graph_dict(path)
    except (ValueError, TypeError) as exc:
        print(f"[error] validation failed: {exc}", file=sys.stderr)
        sys.exit(1)


def _collect_story_names(story_graph: Dict[str, Any]) -> List[str]:
    from story_map import Story, StoryMap

    story_map = StoryMap(story_graph)
    names: List[str] = []
    for epic in story_map.epics():
        for node in story_map.walk(epic):
            if isinstance(node, Story) and node.name:
                names.append(node.name)
    return names


def _apply_story_filter(story_graph: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    from graph_filters import filter_story_graph_to_story_names

    raw_names = args.stories or ""
    story_names: Set[str] = {name.strip() for name in raw_names.split(",") if name.strip()}
    if not story_names:
        raise ValueError("filter requires --stories with at least one name")
    return filter_story_graph_to_story_names(story_graph, story_names)


def cmd_read(args: argparse.Namespace) -> int:
    return run_read_command(args, _load_graph)


def cmd_names(args: argparse.Namespace) -> int:
    return run_names_command(args, _load_graph, _collect_story_names)


def cmd_search(args: argparse.Namespace) -> int:
    return run_search_command(args, _load_graph, _collect_story_names)


def cmd_filter(args: argparse.Namespace) -> int:
    return run_filter_command(
        args,
        _load_graph,
        _apply_story_filter,
        missing_filter_message="filter requires --stories",
    )


def cmd_sha(args: argparse.Namespace) -> int:
    return run_sha_command(args)


def cmd_write(args: argparse.Namespace) -> int:
    from story_graph_file import save_story_graph_dict

    return run_write_command(args, save_story_graph_dict)


def _register_filter_parser(sub: argparse._SubParsersAction) -> None:
    filter_parser = sub.add_parser("filter", help="Emit graph subset containing only named stories")
    filter_parser.add_argument("--file", required=True)
    filter_parser.add_argument("--stories", required=True, help="Comma-separated story names")
    filter_parser.add_argument("--pretty", action="store_true")
    filter_parser.set_defaults(func=cmd_filter)


def _register_subparsers(sub: argparse._SubParsersAction) -> None:
    add_read_parser(sub, command_handler=cmd_read, help_text="Print JSON story graph")
    add_names_parser(sub, command_handler=cmd_names, help_text="List story names (flat)")
    add_search_parser(
        sub,
        command_handler=cmd_search,
        help_text="List story names containing substring (case-insensitive)",
    )
    _register_filter_parser(sub)
    add_sha_parser(
        sub,
        command_handler=cmd_sha,
        help_text="Print SHA-256 of the file content (capture at read time for --expect-sha on write)",
    )
    add_write_parser(sub, command_handler=cmd_write, help_text="Write JSON from stdin (-) or --input file")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="story_graph_cli", description="Story graph file operations")
    sub = parser.add_subparsers(dest="cmd", required=True)
    _register_subparsers(sub)
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

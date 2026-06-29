#!/usr/bin/env python3
"""CLI for reading, searching, filtering, and writing ``ux-graph.json``."""
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


def _load_and_validate(path: Path) -> Dict[str, Any]:
    from ux_graph_file import load_ux_graph_dict

    if not path.is_file():
        print(f"[error] not a file: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        return load_ux_graph_dict(path)
    except (ValueError, TypeError) as exc:
        print(f"[error] validation failed: {exc}", file=sys.stderr)
        sys.exit(1)


def _list_screen_names(ux_graph: Dict[str, Any]) -> List[str]:
    from ux_map import UxGraph

    return UxGraph(ux_graph).screen_names()


def _apply_ux_filter(ux_graph: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    from graph_filters import filter_ux_graph_to_flow_names, filter_ux_graph_to_screen_names

    if args.flows:
        flow_names: Set[str] = {name.strip() for name in args.flows.split(",") if name.strip()}
        return filter_ux_graph_to_flow_names(ux_graph, flow_names)
    if args.screens:
        screen_names = {name.strip() for name in args.screens.split(",") if name.strip()}
        return filter_ux_graph_to_screen_names(ux_graph, screen_names)
    raise ValueError("filter requires --flows or --screens")


def cmd_read(args: argparse.Namespace) -> int:
    return run_read_command(args, _load_and_validate)


def cmd_names(args: argparse.Namespace) -> int:
    return run_names_command(args, _load_and_validate, _list_screen_names)


def cmd_search(args: argparse.Namespace) -> int:
    return run_search_command(args, _load_and_validate, _list_screen_names)


def cmd_filter(args: argparse.Namespace) -> int:
    return run_filter_command(
        args,
        _load_and_validate,
        _apply_ux_filter,
        missing_filter_message="filter requires --flows or --screens",
    )


def cmd_sha(args: argparse.Namespace) -> int:
    return run_sha_command(args)


def cmd_write(args: argparse.Namespace) -> int:
    from ux_graph_file import save_ux_graph_dict

    return run_write_command(args, save_ux_graph_dict)


def _register_filter_parser(sub: argparse._SubParsersAction) -> None:
    filter_parser = sub.add_parser("filter", help="Emit graph subset by flow or screen names")
    filter_parser.add_argument("--file", required=True)
    filter_parser.add_argument("--flows", default=None, help="Comma-separated flow names")
    filter_parser.add_argument("--screens", default=None, help="Comma-separated screen names")
    filter_parser.add_argument("--pretty", action="store_true")
    filter_parser.set_defaults(func=cmd_filter)


def _register_subparsers(sub: argparse._SubParsersAction) -> None:
    add_read_parser(sub, command_handler=cmd_read)
    add_names_parser(sub, command_handler=cmd_names, help_text="List screen names (flat)")
    add_search_parser(sub, command_handler=cmd_search, help_text="List screen names containing substring")
    _register_filter_parser(sub)
    add_sha_parser(sub, command_handler=cmd_sha, help_text="Print SHA-256 of file content")
    add_write_parser(sub, command_handler=cmd_write, help_text="Validate and write JSON from stdin or --input")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ux_graph_cli", description="UX graph file operations")
    sub = parser.add_subparsers(dest="cmd", required=True)
    _register_subparsers(sub)
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

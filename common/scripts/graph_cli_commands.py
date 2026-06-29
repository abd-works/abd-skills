"""Shared CLI command bodies for graph-ops skills."""
from __future__ import annotations

import sys
from argparse import Namespace
from pathlib import Path
from typing import Any, Callable, Dict

from graph_ops_common import (
    acquire_write_lock,
    names_matching_substring,
    parse_json_text,
    read_json_text_file,
    release_write_lock,
    sha256_file,
    write_json_text_file,
)

LoadGraph = Callable[[Path], Dict[str, Any]]
SaveGraph = Callable[[Path, Dict[str, Any]], None]
NameListFn = Callable[[Dict[str, Any]], list[str]]


def emit_json(graph: Dict[str, Any], *, pretty: bool) -> None:
    import json

    if pretty:
        print(json.dumps(graph, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(graph, ensure_ascii=False))


def run_read_command(args: Namespace, loader: LoadGraph) -> int:
    graph = loader(Path(args.file))
    emit_json(graph, pretty=bool(args.pretty))
    return 0


def run_names_command(args: Namespace, loader: LoadGraph, list_names: NameListFn) -> int:
    graph = loader(Path(args.file))
    for name in list_names(graph):
        print(name)
    return 0


def run_search_command(args: Namespace, loader: LoadGraph, list_names: NameListFn) -> int:
    graph = loader(Path(args.file))
    hits = names_matching_substring(list_names(graph), args.substring)
    for name in hits:
        print(name)
    return 0 if hits else 1


def run_sha_command(args: Namespace) -> int:
    target = Path(args.file)
    if not target.is_file():
        print(f"[error] not a file: {target}", file=sys.stderr)
        return 2
    print(sha256_file(target))
    return 0


def run_write_command(args: Namespace, saver: SaveGraph) -> int:
    target = Path(args.file)
    if args.input == "-":
        graph = parse_json_text(sys.stdin.read())
    else:
        graph = read_json_text_file(Path(args.input))

    lock = None if args.no_lock else acquire_write_lock(target, force=bool(args.force))
    try:
        if target.is_file() and args.expect_sha and not args.force:
            current = sha256_file(target)
            if current != args.expect_sha:
                print(
                    f"[error] concurrent write refused: --expect-sha mismatch. "
                    f"expected={args.expect_sha} current={current}.",
                    file=sys.stderr,
                )
                return 3
        saver(target, graph)
        print(f"wrote {target}", file=sys.stderr)
        return 0
    except (ValueError, TypeError) as exc:
        print(f"[error] validation failed: {exc}", file=sys.stderr)
        return 1
    finally:
        release_write_lock(lock)


def save_validated_graph(target: Path, graph: Dict[str, Any], validator: Callable[[Dict[str, Any]], None]) -> None:
    validator(graph)
    write_json_text_file(target, graph)


def load_validated_graph(target: Path, validator: Callable[[Dict[str, Any]], None]) -> Dict[str, Any]:
    graph = read_json_text_file(target)
    validator(graph)
    return graph


FilterFn = Callable[[Dict[str, Any], Namespace], Dict[str, Any]]


def run_filter_command(
    args: Namespace,
    loader: LoadGraph,
    apply_filter: FilterFn,
    *,
    missing_filter_message: str,
) -> int:
    graph = loader(Path(args.file))
    try:
        filtered = apply_filter(graph, args)
    except ValueError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 2
    emit_json(filtered, pretty=bool(args.pretty))
    return 0

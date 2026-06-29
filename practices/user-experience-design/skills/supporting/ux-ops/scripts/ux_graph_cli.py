#!/usr/bin/env python3
"""CLI for reading, searching, filtering, and writing ``ux-graph.json``.

Add ``…/ux-ops/scripts`` to PYTHONPATH, then:

  python ux_graph_cli.py read --file path/to/ux-graph.json
  python ux_graph_cli.py names --file path/to/ux-graph.json
  python ux_graph_cli.py search --file ... --substring "Search"
  python ux_graph_cli.py filter --file ... --flows "Shop in store"
  python ux_graph_cli.py filter --file ... --screens "Search Results","Product Detail"
  python ux_graph_cli.py sha --file path/to/ux-graph.json
  python ux_graph_cli.py write --file out.json < input.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

_STALE_LOCK_SECONDS = 300


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _lock_path_for(target: Path) -> Path:
    return target.with_name(target.name + ".lock")


def _read_lock(lock: Path) -> Dict[str, Any]:
    try:
        return json.loads(lock.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _acquire_lock(target: Path, force: bool) -> Path | None:
    lock = _lock_path_for(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({
        "pid": os.getpid(),
        "acquired_at": time.time(),
        "host": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "",
    }).encode("utf-8")
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        existing = _read_lock(lock)
        age = time.time() - float(existing.get("acquired_at", 0) or 0)
        if age > _STALE_LOCK_SECONDS or force:
            try:
                lock.unlink()
            except FileNotFoundError:
                pass
            try:
                fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                print(
                    f"[error] could not acquire lock {lock} "
                    f"(held by pid={existing.get('pid')}, age={int(age)}s).",
                    file=sys.stderr,
                )
                sys.exit(4)
        else:
            print(
                f"[error] concurrent write refused: lock {lock} is held by "
                f"pid={existing.get('pid')} (age={int(age)}s).",
                file=sys.stderr,
            )
            sys.exit(4)
    try:
        os.write(fd, payload)
    finally:
        os.close(fd)
    return lock


def _release_lock(lock: Path | None) -> None:
    if lock is None:
        return
    try:
        lock.unlink()
    except FileNotFoundError:
        pass


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


def _collect_screen_names(data: Dict[str, Any]) -> List[str]:
    from ux_map import UxGraph

    return UxGraph(data).screen_names()


def cmd_read(args: argparse.Namespace) -> int:
    data = _load_and_validate(Path(args.file))
    if args.pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))
    return 0


def cmd_names(args: argparse.Namespace) -> int:
    data = _load_and_validate(Path(args.file))
    for name in _collect_screen_names(data):
        print(name)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    data = _load_and_validate(Path(args.file))
    sub = (args.substring or "").lower()
    hits = [n for n in _collect_screen_names(data) if sub in n.lower()]
    for name in hits:
        print(name)
    return 0 if hits else 1


def cmd_filter(args: argparse.Namespace) -> int:
    from graph_filters import filter_ux_graph_to_flow_names, filter_ux_graph_to_screen_names

    data = _load_and_validate(Path(args.file))
    if args.flows:
        names: Set[str] = {s.strip() for s in args.flows.split(",") if s.strip()}
        out = filter_ux_graph_to_flow_names(data, names)
    elif args.screens:
        names = {s.strip() for s in args.screens.split(",") if s.strip()}
        out = filter_ux_graph_to_screen_names(data, names)
    else:
        print("[error] filter requires --flows or --screens", file=sys.stderr)
        return 2
    if args.pretty:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False))
    return 0


def cmd_sha(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"[error] not a file: {path}", file=sys.stderr)
        return 2
    print(_sha256_file(path))
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    from ux_graph_file import save_ux_graph_dict

    path = Path(args.file)
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    lock = None if args.no_lock else _acquire_lock(path, force=args.force)
    try:
        if path.is_file() and args.expect_sha and not args.force:
            current = _sha256_file(path)
            if current != args.expect_sha:
                print(
                    f"[error] concurrent write refused: --expect-sha mismatch. "
                    f"expected={args.expect_sha} current={current}.",
                    file=sys.stderr,
                )
                return 3
        save_ux_graph_dict(path, data)
        print(f"wrote {path}", file=sys.stderr)
        return 0
    except (ValueError, TypeError) as exc:
        print(f"[error] validation failed: {exc}", file=sys.stderr)
        return 1
    finally:
        _release_lock(lock)


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ux_graph_cli", description="UX graph file operations")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("read", help="Load, validate, and print JSON")
    r.add_argument("--file", required=True)
    r.add_argument("--pretty", action="store_true")
    r.set_defaults(func=cmd_read)

    n = sub.add_parser("names", help="List screen names (flat)")
    n.add_argument("--file", required=True)
    n.set_defaults(func=cmd_names)

    s = sub.add_parser("search", help="List screen names containing substring")
    s.add_argument("--file", required=True)
    s.add_argument("--substring", required=True)
    s.set_defaults(func=cmd_search)

    f = sub.add_parser("filter", help="Emit graph subset by flow or screen names")
    f.add_argument("--file", required=True)
    f.add_argument("--flows", default=None, help="Comma-separated flow names")
    f.add_argument("--screens", default=None, help="Comma-separated screen names")
    f.add_argument("--pretty", action="store_true")
    f.set_defaults(func=cmd_filter)

    sh = sub.add_parser("sha", help="Print SHA-256 of file content")
    sh.add_argument("--file", required=True)
    sh.set_defaults(func=cmd_sha)

    w = sub.add_parser("write", help="Validate and write JSON from stdin or --input")
    w.add_argument("--file", required=True)
    w.add_argument("--input", default="-")
    w.add_argument("--expect-sha", dest="expect_sha", default=None)
    w.add_argument("--no-lock", dest="no_lock", action="store_true")
    w.add_argument("--force", action="store_true")
    w.set_defaults(func=cmd_write)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

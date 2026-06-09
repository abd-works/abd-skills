#!/usr/bin/env python3
"""CLI for reading, searching, filtering, and writing ``story-graph.json`` without agile_bots.

Add ``…/story-graph-ops/scripts`` and ``…/execute-skill-using-skills-rules/scripts`` to PYTHONPATH, then:

  python story_graph_cli.py read --file path/to/story-graph.json
  python story_graph_cli.py names --file path/to/story-graph.json
  python story_graph_cli.py search --file ... --substring "Login"
  python story_graph_cli.py filter --file ... --stories "A","B" > subset.json
  python story_graph_cli.py sha --file path/to/story-graph.json
  python story_graph_cli.py write --file out.json < input.json
  python story_graph_cli.py write --file out.json --input in.json --expect-sha <hex>

Concurrency / parallel-run safety:

  - ``write`` takes an exclusive advisory lock at ``<file>.lock`` for the
    duration of the write. If another process holds the lock, the write is
    refused (exit 4). Stale locks (>300s) are auto-cleaned.
  - ``write`` also supports ``--expect-sha <hex>``: if the target file's
    current content hash does not match, the write is refused (exit 3).
    Capture the hash at read time with ``sha`` and pass it back on write.
  - ``--force`` on ``write`` bypasses both checks. Use only for recovery.
  - ``--no-lock`` skips the advisory lock (rarely needed; not recommended).

These safeguards backstop the planning-level rule that **parallel runs must
not edit the same slice of ``story-graph.json`` at the same time** (see
``SKILL.md`` → "Parallel runs and concurrent writes").
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

# Allow running from repo without install: parent directory is on PYTHONPATH
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# --- concurrency helpers ----------------------------------------------------- #

_STALE_LOCK_SECONDS = 300  # 5 minutes


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
    """Create an exclusive lock file next to *target*. Return its path, or None on failure.

    Returns the lock path on success. Raises SystemExit(4) if another live lock is held
    and ``force`` is false.
    """
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
            # Stale or forced: remove and retry once.
            try:
                lock.unlink()
            except FileNotFoundError:
                pass
            try:
                fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                print(
                    f"[error] could not acquire lock {lock} "
                    f"(held by pid={existing.get('pid')}, age={int(age)}s). "
                    "Another writer is active; retry later or pass --force.",
                    file=sys.stderr,
                )
                sys.exit(4)
        else:
            print(
                f"[error] concurrent write refused: lock {lock} is held by "
                f"pid={existing.get('pid')} (age={int(age)}s). "
                "Parallel runs must not edit the same graph file. "
                "Wait for the other writer, or pass --force if you are recovering a stale lock.",
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


def cmd_sha(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"[error] not a file: {path}", file=sys.stderr)
        return 2
    print(_sha256_file(path))
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)

    lock = None if args.no_lock else _acquire_lock(path, force=args.force)
    try:
        # Optimistic concurrency: if the caller captured a sha at read time and the
        # file changed since, refuse rather than clobber another writer's edit.
        if path.is_file() and args.expect_sha and not args.force:
            current = _sha256_file(path)
            if current != args.expect_sha:
                print(
                    f"[error] concurrent write refused: --expect-sha mismatch. "
                    f"expected={args.expect_sha} current={current}. "
                    "Re-read the file, merge your changes against the current content, "
                    "and retry. Pass --force only if you intend to clobber.",
                    file=sys.stderr,
                )
                return 3

        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        path.write_text(text, encoding="utf-8")
        print(f"wrote {path}", file=sys.stderr)
        return 0
    finally:
        _release_lock(lock)


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

    sh = sub.add_parser(
        "sha",
        help="Print SHA-256 of the file content (capture this at read time for --expect-sha on write)",
    )
    sh.add_argument("--file", required=True)
    sh.set_defaults(func=cmd_sha)

    w = sub.add_parser("write", help="Write JSON from stdin (-) or --input file")
    w.add_argument("--file", required=True, help="Output path")
    w.add_argument("--input", default="-", help="Input JSON path or - for stdin")
    w.add_argument(
        "--expect-sha",
        dest="expect_sha",
        default=None,
        help="Refuse the write (exit 3) if the target file's current SHA-256 differs.",
    )
    w.add_argument(
        "--no-lock",
        dest="no_lock",
        action="store_true",
        help="Skip the advisory lock at <file>.lock (not recommended).",
    )
    w.add_argument(
        "--force",
        action="store_true",
        help="Override both the advisory lock and --expect-sha checks. Use only for recovery.",
    )
    w.set_defaults(func=cmd_write)

    args = p.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

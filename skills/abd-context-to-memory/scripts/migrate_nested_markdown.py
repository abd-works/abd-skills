"""
Move legacy nested ``<topic>/.../markdown/file.md`` to ``<topic>/markdown/.../file.md``.

Skips ``memory/`` and ``assets/``. Aborts on destination conflicts unless --force.

Usage:
  python migrate_nested_markdown.py <topic_root> [--dry-run] [--force]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SKIP_TOP = frozenset({"memory", "assets"})


def dest_for_file(topic_root: Path, src: Path) -> Path | None:
    """Return destination path, or None if this file should not be moved."""
    try:
        rel = src.relative_to(topic_root)
    except ValueError:
        return None
    parts = list(rel.parts)
    if not parts:
        return None
    if parts[0].casefold() in SKIP_TOP:
        return None
    try:
        i = next(i for i, p in enumerate(parts) if p.casefold() == "markdown")
    except StopIteration:
        return None
    new_parts = parts[:i] + parts[i + 1 :]
    if not new_parts:
        return None
    return topic_root / "markdown" / Path(*new_parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic_root", type=Path, help="Topic folder (e.g. .../Agile Thinking)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    parser.add_argument("--force", action="store_true", help="Overwrite existing destinations")
    args = parser.parse_args()
    topic_root = args.topic_root.expanduser().resolve()
    if not topic_root.is_dir():
        print(f"Not a directory: {topic_root}", file=sys.stderr)
        sys.exit(1)

    moves: list[tuple[Path, Path]] = []
    for src in sorted(topic_root.rglob("*")):
        if not src.is_file():
            continue
        dest = dest_for_file(topic_root, src)
        if dest is None:
            continue
        if dest == src:
            continue
        moves.append((src, dest))

    conflicts: list[tuple[Path, Path]] = []
    for src, dest in moves:
        if dest.exists() and dest.resolve() != src.resolve():
            conflicts.append((src, dest))

    if conflicts and not args.force:
        print("Destination conflicts (use --force to overwrite):", file=sys.stderr)
        for src, dest in conflicts[:30]:
            print(f"  {src} -> {dest} (exists)", file=sys.stderr)
        if len(conflicts) > 30:
            print(f"  ... and {len(conflicts) - 30} more", file=sys.stderr)
        sys.exit(2)

    for src, dest in moves:
        print(f"{'DRY ' if args.dry_run else ''}{src} -> {dest}")
        if args.dry_run:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and dest.resolve() != src.resolve():
            dest.unlink()
        shutil.move(str(src), str(dest))

    if not args.dry_run and moves:
        # Remove empty nested markdown dirs (deepest first; longest path first)
        md_dirs = sorted(
            {p for p in topic_root.rglob("markdown") if p.is_dir()},
            key=lambda p: (len(p.parts), len(str(p))),
            reverse=True,
        )
        for d in md_dirs:
            if d == topic_root / "markdown":
                continue
            try:
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
                    print(f"Removed empty: {d}")
            except OSError:
                pass

    print(f"\nDone: {len(moves)} file(s).")


if __name__ == "__main__":
    main()

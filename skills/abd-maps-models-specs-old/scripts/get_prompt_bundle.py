#!/usr/bin/env python3
"""Load a prompt bundle for an AI step and print it to stdout.

Two modes:

1. **Full bundle** (`--operation <slug>`): `process.md` + `domain.md` + `story-map.md` +
   `context.md` + one `parts/steps/built/<slug>.md` — same sources as `AGENTS.md`, but only
   the step you are running. Implemented in `build_agents.assemble_prompt_bundle`.

2. **Single file** (`--built-step`, `--file`, stdin): one markdown file only.

Intended flow: the agent runs this script, reads stdout, and executes the instructions.

Usage::

    python scripts/get_prompt_bundle.py --operation modules-epics-scaffold-breadth
    python scripts/get_prompt_bundle.py --list-operations
    python scripts/get_prompt_bundle.py --built-step modules-epics-scaffold-breadth
    python scripts/get_prompt_bundle.py --file path/to/prompt.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_DIR = Path(__file__).resolve().parent.parent
_BUILT_DIR = _SKILL_DIR / "parts" / "steps" / "built"

sys.path.insert(0, str(_SCRIPT_DIR))
from build_agents import ai_step_slugs, assemble_prompt_bundle  # noqa: E402


def _load_single_file(args: argparse.Namespace) -> str:
    if args.built_step:
        p = _BUILT_DIR / f"{args.built_step}.md"
        if not p.is_file():
            print(f"abd-maps-models-specs: built step not found: {p}", file=sys.stderr)
            sys.exit(1)
        return p.read_text(encoding="utf-8")
    if args.file:
        fp = Path(args.file).resolve()
        if not fp.is_file():
            print(f"abd-maps-models-specs: file not found: {fp}", file=sys.stderr)
            sys.exit(1)
        return fp.read_text(encoding="utf-8")
    if args.stdin or (not sys.stdin.isatty()):
        return sys.stdin.read()
    print(
        "Usage: --operation <slug> | --list-operations | --built-step | --file | pipe stdin.\n"
        "  python scripts/get_prompt_bundle.py --operation modules-epics-scaffold-breadth\n"
        "  python scripts/get_prompt_bundle.py --built-step modules-epics-scaffold-breadth\n"
        "  python scripts/get_prompt_bundle.py --file path.md\n"
        "  type x.md | python scripts/get_prompt_bundle.py",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description="Print a prompt bundle to stdout (for AI steps).")
    ap.add_argument(
        "--operation",
        "-o",
        metavar="SLUG",
        help="Full bundle: shared parts + parts/steps/built/<SLUG>.md (see --list-operations).",
    )
    ap.add_argument(
        "--list-operations",
        action="store_true",
        help="Print known operation slugs (one per line) and exit.",
    )
    ap.add_argument(
        "--built-step",
        metavar="NAME",
        help=f"Single file only: parts/steps/built/{{NAME}}.md (under {_BUILT_DIR})",
    )
    ap.add_argument("--file", "-f", help="Single file: load prompt text from this path")
    ap.add_argument(
        "--stdin",
        action="store_true",
        help="Read prompt from stdin (default when stdin is not a TTY)",
    )
    ap.add_argument(
        "--quiet-meta",
        action="store_true",
        help="Do not print a one-line size note to stderr on success.",
    )
    args = ap.parse_args()

    if args.list_operations:
        for slug in ai_step_slugs():
            print(slug)
        return

    if args.operation:
        try:
            text = assemble_prompt_bundle(_SKILL_DIR, args.operation.strip())
        except (ValueError, FileNotFoundError) as e:
            print(f"abd-maps-models-specs: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = _load_single_file(args)

    if not text.strip():
        print("abd-maps-models-specs: prompt is empty", file=sys.stderr)
        sys.exit(1)

    if not args.quiet_meta:
        print(f"chars={len(text)}", file=sys.stderr)

    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()

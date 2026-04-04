#!/usr/bin/env python3
"""Copy shared DrawIO modules from src/drawio into skill script dirs with a generated header."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# (canonical_path relative to repo root, destination path relative to repo root)
VENDOR_FILES: list[tuple[str, str]] = [
    ("src/drawio/drawio_tools.py", "skills/abd-story-synthesizer/scripts/drawio_tools.py"),
    ("src/drawio/layout_plan.py", "skills/abd-story-synthesizer/scripts/layout_plan.py"),
    ("src/drawio/model_to_drawio.py", "skills/abd-story-synthesizer/scripts/model_to_drawio.py"),
    ("src/drawio/drawio_class_cli.py", "skills/abd-story-synthesizer/scripts/drawio_class_cli.py"),
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _generated_header(*, src_rel: str) -> str:
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        "# " + "=" * 77,
        "# GENERATED FILE — DO NOT EDIT MANUALLY",
        f"# Canonical source: {src_rel}",
        "# Regenerate from repo root: python scripts/sync_drawio_vendor.py",
        f"# Generated at: {ts}",
        "# " + "=" * 77,
        "",
    ]
    return "\n".join(lines)


def _prepend_generated(body: str, *, src_rel: str) -> str:
    header = _generated_header(src_rel=src_rel)
    text = body.lstrip("\ufeff")
    if text.startswith("#!"):
        nl = text.find("\n")
        if nl == -1:
            return header + text
        first_line = text[: nl + 1]
        rest = text[nl + 1 :]
        return first_line + header + rest
    return header + text


# Opening/closing banner lines are "# ===...===", with variable-length lines of metadata between.
_GEN_BLOCK_RE = re.compile(
    r"^# ={10,}\r?\n(?:# [^\r\n]*\r?\n)*?# ={10,}\r?\n(?:\r?\n)?",
    re.MULTILINE,
)


def _strip_generated_vendor_prefix(text: str) -> str:
    """Remove the generated banner from a vendored file; preserve an optional shebang."""
    t = text.lstrip("\ufeff")
    shebang = ""
    if t.startswith("#!"):
        nl = t.find("\n")
        if nl != -1:
            shebang = t[: nl + 1]
            t = t[nl + 1 :]
    m = _GEN_BLOCK_RE.match(t)
    if not m:
        return shebang + t
    return shebang + t[m.end() :]


def _norm_newlines(s: str) -> str:
    return s.replace("\r\n", "\n")


def check_all() -> int:
    """Verify vendored files match canonical sources (ignores generated timestamps)."""
    root = _repo_root()
    failed = False
    for src_rel, dest_rel in VENDOR_FILES:
        src = root.joinpath(*src_rel.split("/"))
        dest = root.joinpath(*dest_rel.split("/"))
        if not src.is_file():
            print(f"ERROR: missing canonical file: {src}", file=sys.stderr)
            failed = True
            continue
        if not dest.is_file():
            print(f"ERROR: missing vendored file (run sync): {dest}", file=sys.stderr)
            failed = True
            continue
        expected = _norm_newlines(src.read_text(encoding="utf-8"))
        actual = _norm_newlines(dest.read_text(encoding="utf-8"))
        stripped = _norm_newlines(_strip_generated_vendor_prefix(actual))
        if stripped != expected:
            print(
                f"ERROR: drift {dest_rel} != {src_rel} — run: python scripts/sync_drawio_vendor.py",
                file=sys.stderr,
            )
            failed = True
        else:
            print(f"OK {dest_rel}")
    return 1 if failed else 0


def sync_all(*, dry_run: bool) -> int:
    root = _repo_root()
    for src_rel, dest_rel in VENDOR_FILES:
        src = root.joinpath(*src_rel.split("/"))
        dest = root.joinpath(*dest_rel.split("/"))
        if not src.is_file():
            print(f"ERROR: missing canonical file: {src}", file=sys.stderr)
            return 1
        body = src.read_text(encoding="utf-8")
        out = _prepend_generated(body, src_rel=src_rel)
        if dry_run:
            print(f"Would write {dest} ({len(out)} bytes)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8", newline="\n")
        print(f"Wrote {dest}")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description="Vendor DrawIO shared modules into skill script directories.")
    p.add_argument("--dry-run", action="store_true", help="Print targets only; do not write files.")
    p.add_argument(
        "--check",
        action="store_true",
        help="Verify vendored files match src/drawio (exit 1 if out of sync).",
    )
    args = p.parse_args()
    if args.check:
        raise SystemExit(check_all())
    raise SystemExit(sync_all(dry_run=args.dry_run))


if __name__ == "__main__":
    main()

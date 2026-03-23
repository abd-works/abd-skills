"""
Convert evidence sources to canonical Markdown (context markdown phase; after set workspace).

Same conversion engine as **abd-context-to-memory** (`convert_to_markdown.py`): Microsoft
MarkItDown. Writes `<stem>.md` next to each source file under the **skill workspace** root
(the directory that contains `solution.conf`, from `conf/abd-config.json` →
`active_skill_workspace`).

Documented workflow (from skill package root; see context-markdown.md):

  --file <path>   Use when manifest_sources[] is not set up yet or the file is not listed;
                  convert one path (workspace-relative unless absolute).

  --manifest      Use when manifest_sources[] already lists inputs; convert every supported
                  non-.md entry (skip .md, missing, unsupported).

Optional: `--no-provenance`.

See **content/parts/phases/context-markdown.md** (exact commands). For RAG/memory pipelines
(SharePoint links, chunk-to-memory layout), use **abd-context-to-memory** instead.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print(
        'Missing MarkItDown (expected with a complete skill environment). '
        'See scripts/requirements-convert.txt only if you are wiring deps manually.',
        file=sys.stderr,
    )
    sys.exit(1)

# Workspace + manifest resolution (fails fast with a clear message if unset)
from _config import resolved_manifest_sources, workspace_root

SUPPORTED = {
    ".pdf",
    ".pptx",
    ".docx",
    ".xlsx",
    ".xls",
    ".html",
    ".htm",
    ".txt",
    ".csv",
    ".json",
    ".xml",
}

_md = MarkItDown()


def _resolve_under_workspace(workspace: Path, user_path: str) -> Path:
    p = Path(user_path)
    if not p.is_absolute():
        p = (workspace / p).resolve()
    return p


def convert_one(
    src: Path,
    *,
    workspace: Path,
    provenance: bool = True,
) -> Path:
    """Convert one file; write markdown beside the source. Returns output path."""
    if not src.is_file():
        raise FileNotFoundError(src)
    suf = src.suffix.lower()
    if suf not in SUPPORTED:
        raise ValueError(f"unsupported format {suf!r}; supported: {sorted(SUPPORTED)}")
    text = _md.convert(str(src)).text_content
    if provenance:
        try:
            rel = src.resolve().relative_to(workspace.resolve())
            text = f"<!-- Source: {rel.as_posix()} -->\n\n" + text
        except ValueError:
            text = f"<!-- Source: {src} -->\n\n" + text
    out = src.parent / (src.stem + ".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


def _cmd_file(workspace: Path, path: str, provenance: bool) -> int:
    src = _resolve_under_workspace(workspace, path)
    try:
        out = convert_one(src, workspace=workspace, provenance=provenance)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    kb = out.stat().st_size // 1024
    print(f"Wrote {out} ({kb} KB)")
    return 0


def _cmd_manifest(workspace: Path, provenance: bool) -> int:
    entries = resolved_manifest_sources()
    if not entries:
        print("No manifest_sources in solution.conf (or empty list).", file=sys.stderr)
        return 1
    ok, skipped, fail = 0, 0, 0
    for abs_path, _role, rel_posix in entries:
        suf = abs_path.suffix.lower()
        if suf == ".md":
            print(f"skip (already markdown): {rel_posix}")
            skipped += 1
            continue
        if not abs_path.is_file():
            print(f"skip (missing): {rel_posix}", file=sys.stderr)
            skipped += 1
            continue
        if suf not in SUPPORTED:
            print(f"skip (unsupported {suf}): {rel_posix}", file=sys.stderr)
            skipped += 1
            continue
        out = abs_path.parent / (abs_path.stem + ".md")
        print(f"convert: {rel_posix} -> {out.name} ... ", end="", flush=True)
        try:
            convert_one(abs_path, workspace=workspace, provenance=provenance)
            print("OK")
            ok += 1
        except (OSError, ValueError) as e:
            print(f"FAIL ({e})")
            fail += 1
    print(f"\nDone: {ok} converted, {skipped} skipped, {fail} failed.")
    return 0 if fail == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", metavar="PATH", help="single source file (workspace-relative or absolute)")
    g.add_argument(
        "--manifest",
        action="store_true",
        help="convert supported non-.md files listed in solution.conf manifest_sources",
    )
    parser.add_argument(
        "--no-provenance",
        action="store_true",
        help="omit <!-- Source: ... --> prefix",
    )
    args = parser.parse_args()
    try:
        ws = workspace_root()
    except SystemExit:
        return 1
    provenance = not args.no_provenance
    if args.file:
        return _cmd_file(ws, args.file, provenance)
    return _cmd_manifest(ws, provenance)


if __name__ == "__main__":
    raise SystemExit(main())

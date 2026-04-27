"""
Rewrite ``<!-- Source: path | url -->`` in pipeline markdown and chunked ``.md`` files.

- Normalizes ``source/...`` → ``data/assets/...``
- Normalizes bare ``abd-answers-memory-pipeline/...`` → ``data/assets/abd-answers-memory-pipeline/...``; maps pipeline ``markdown/*.md`` to sibling originals (e.g. ``.pptx``) when present
- Deduplicates multiple consecutive Source comments (keeps best: ``data/assets/...`` + non-``.md`` when possible)
- Refreshes SharePoint URL via ``get_sharepoint_open_doc_url_for_file`` when the asset exists under ``data/assets/``
- For files under ``chunked/``, applies ``chunked_source_path_to_asset_binary``: strips ``.../abd-answers-memory-pipeline/markdown/`` so ``Source`` points at ``data/assets/<topic>/...`` with a binary extension (URL or on-disk sibling). Does **not** refresh SharePoint URLs on that pass (URLs already target the original file).

Run from repo or this directory::

  python repair_source_comments.py
  python repair_source_comments.py --dry-run
  python repair_source_comments.py --markdown-only
  python repair_source_comments.py --chunked-only
  python repair_source_comments.py --chunked-only --quiet --progress-every 100 --log repair.log

Requires ``sharepoint_mapping.json`` with ``open_doc_base`` and optional ``file_open_urls`` for full fidelity.

Progress: prints ``[repair_source_comments] scanned i/n, rewritten k`` every ``--progress-every`` files (stderr, flushed). Use ``--quiet`` to hide per-file ``updated:`` lines on large trees.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from _config import ASSETS, PIPELINE_CHUNKED, PIPELINE_MARKDOWN, REPO_ROOT, ensure_root
from chunked_source_asset import chunked_source_path_to_asset_binary
from onedrive_to_sharepoint import get_sharepoint_open_doc_url_for_file

ensure_root()

SOURCE_BLOCK = re.compile(
    r"<!--\s*Source:\s*([^|]+?)\s*\|\s*([^>]+?)\s*-->",
    re.DOTALL,
)

_CHUNK_LOC_SUFFIX = re.compile(r",\s*(slide|section)\s+(\d+)\s*$", re.IGNORECASE)

_PIPELINE_MD_PREFIX = "data/assets/abd-answers-memory-pipeline/markdown/"


def _split_chunk_location(path_part: str) -> tuple[str, str | None]:
    """Split ``data/assets/.../x.md, slide 1`` → base path + ``, slide 1``."""
    s = path_part.strip()
    m = _CHUNK_LOC_SUFFIX.search(s)
    if not m:
        return s, None
    base = s[: m.start()].strip()
    loc = f", {m.group(1).lower()} {m.group(2)}"
    return base, loc


def _normalize_path_part(p: str) -> str:
    """Repo-relative paths; bare ``abd-answers-memory-pipeline/...`` → ``data/assets/abd-answers-memory-pipeline/...``."""
    s = p.strip().replace("\\", "/")
    if s.startswith("source/"):
        return "data/assets/" + s[len("source/") :]
    if s.startswith("data/assets/"):
        return s
    if s.startswith("abd-answers-memory-pipeline/"):
        return "data/assets/" + s
    return s


def _try_sibling_binary_for_md(repo_path: str) -> str:
    if not repo_path.startswith("data/assets/") or not repo_path.lower().endswith(".md"):
        return repo_path
    inner = repo_path[len("data/assets/") :]
    base = (ASSETS / inner).resolve()
    if not base.is_file():
        return repo_path
    parent, stem = base.parent, base.stem
    for ext in (".pptx", ".ppt", ".pdf", ".docx", ".xlsx", ".xls"):
        cand = parent / f"{stem}{ext}"
        if cand.is_file():
            try:
                rel = cand.resolve().relative_to(ASSETS.resolve())
                return f"data/assets/{rel.as_posix()}"
            except ValueError:
                break
    return repo_path


def _pipeline_mirror_md_to_original_asset(repo_path: str) -> str:
    if not repo_path.startswith(_PIPELINE_MD_PREFIX) or not repo_path.lower().endswith(".md"):
        return repo_path
    inner = repo_path[len(_PIPELINE_MD_PREFIX) :]
    stem = Path(inner).stem
    parent = Path(inner).parent
    for ext in (".pptx", ".ppt", ".pdf", ".docx", ".xlsx", ".xls"):
        cand = ASSETS / parent / f"{stem}{ext}"
        if cand.is_file():
            try:
                rel = cand.resolve().relative_to(ASSETS.resolve())
                return f"data/assets/{rel.as_posix()}"
            except ValueError:
                break
    return _try_sibling_binary_for_md(repo_path)


def _resolve_asset_path(path_part: str) -> Path | None:
    """``data/assets/...`` → absolute path if file exists (ignores ``, slide N`` suffix)."""
    base, _ = _split_chunk_location(path_part)
    norm = _normalize_path_part(base)
    norm = _pipeline_mirror_md_to_original_asset(norm)
    norm = _try_sibling_binary_for_md(norm)
    if not norm.startswith("data/assets/"):
        return None
    rel = norm[len("data/assets/") :]
    abs_path = (ASSETS / Path(rel)).resolve()
    return abs_path if abs_path.is_file() else None


def _pick_best_path(paths: list[str]) -> str:
    """Choose best ``data/assets/...`` path; preserve ``, slide N`` from the last path that has one.

    Prefer a non-``.md`` path (original binary beside the converted mirror). Mirror→binary
    resolution matches ``chunk_markdown._pipeline_mirror_md_to_original_asset`` (originals
    often live at ``data/assets/<topic>/...`` rather than under ``.../markdown/``).
    """
    loc: str | None = None
    for p in reversed(paths):
        _, l = _split_chunk_location(_normalize_path_part(p))
        if l:
            loc = l
            break

    bases: list[str] = []
    for p in paths:
        base, _ = _split_chunk_location(_normalize_path_part(p))
        bases.append(_normalize_path_part(base))

    def _upgrade(b: str) -> str:
        n = _pipeline_mirror_md_to_original_asset(b)
        n = _try_sibling_binary_for_md(n)
        return n

    upgraded = [_upgrade(b) for b in bases]
    for n in upgraded:
        if n.startswith("data/assets/") and not n.lower().endswith(".md"):
            return n + (loc or "")
    for n in upgraded:
        if n.startswith("data/assets/"):
            return n + (loc or "")
    if upgraded:
        return upgraded[0] + (loc or "")
    return ""


def _is_under_chunked(file_path: Path) -> bool:
    try:
        file_path.resolve().relative_to(PIPELINE_CHUNKED.resolve())
        return True
    except ValueError:
        return False


def _rewrite_body(text: str, *, apply_chunked_asset_binary: bool = False) -> tuple[str, bool]:
    matches = list(SOURCE_BLOCK.finditer(text))
    if not matches:
        return text, False

    paths = [m.group(1) for m in matches]
    path_part = _pick_best_path(paths)
    url_part = matches[-1].group(2).strip()

    if apply_chunked_asset_binary:
        path_part = chunked_source_path_to_asset_binary(path_part, url_part)

    # Chunked pass: only .md→binary extension; do not refresh SharePoint URLs (avoids rewriting every file).
    if not apply_chunked_asset_binary:
        abs_asset = _resolve_asset_path(path_part)
        if abs_asset is not None:
            new_url = get_sharepoint_open_doc_url_for_file(abs_asset)
            if new_url:
                url_part = new_url

    new_comment = f"<!-- Source: {path_part} | {url_part} -->"
    # Remove all old Source blocks; prepend single comment to non-empty body.
    stripped = SOURCE_BLOCK.sub("", text).lstrip("\n")
    out = new_comment + "\n\n" + stripped if stripped.strip() else new_comment + "\n"
    changed = out != text
    return out, changed


def _walk_md_roots(roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*.md"):
            if "images" in p.parts:
                continue
            out.append(p)
    return sorted(out)


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Print counts only; do not write files")
    ap.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only process pipeline markdown/ mirror (not chunked/)",
    )
    ap.add_argument(
        "--chunked-only",
        action="store_true",
        help="Only process pipeline chunked/ output",
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print each updated/would-update path (still print progress and summary)",
    )
    ap.add_argument(
        "--progress-every",
        type=int,
        default=50,
        metavar="N",
        help="Log progress every N files scanned (0 disables). Default: 50",
    )
    ap.add_argument(
        "--log",
        type=Path,
        metavar="FILE",
        help="Append timestamped progress lines to this file (UTF-8)",
    )
    args = ap.parse_args()

    if args.markdown_only and args.chunked_only:
        print("--markdown-only and --chunked-only are mutually exclusive", file=sys.stderr)
        sys.exit(2)

    roots: list[Path]
    if args.markdown_only:
        roots = [PIPELINE_MARKDOWN]
    elif args.chunked_only:
        roots = [PIPELINE_CHUNKED]
    else:
        roots = [PIPELINE_MARKDOWN, PIPELINE_CHUNKED]
    files = _walk_md_roots(roots)
    changed = 0
    scanned = 0
    t0 = time.perf_counter()
    log_fp = None
    if args.log is not None:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        log_fp = args.log.open("a", encoding="utf-8")

    def _progress_note() -> str:
        elapsed = time.perf_counter() - t0
        return (
            f"[repair_source_comments] scanned {scanned}/{len(files)}, "
            f"rewritten {changed}, {elapsed:.1f}s elapsed"
        )

    def _emit_progress(force: bool = False) -> None:
        if args.progress_every <= 0 and not force:
            return
        if not force and scanned % args.progress_every != 0:
            return
        line = _progress_note()
        print(line, file=sys.stderr, flush=True)
        if log_fp is not None:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            log_fp.write(f"{ts} {line}\n")
            log_fp.flush()

    print(
        f"[repair_source_comments] starting: {len(files)} files, "
        f"progress every {args.progress_every if args.progress_every > 0 else 'disabled'} files",
        file=sys.stderr,
        flush=True,
    )
    if log_fp is not None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        log_fp.write(
            f"{ts} [repair_source_comments] starting: {len(files)} files "
            f"(progress every {args.progress_every if args.progress_every > 0 else 'disabled'})\n"
        )
        log_fp.flush()

    try:
        for f in files:
            scanned += 1
            _emit_progress()
            try:
                text = f.read_text(encoding="utf-8")
            except OSError as e:
                print(f"SKIP read {f}: {e}", file=sys.stderr, flush=True)
                continue
            except UnicodeDecodeError as e:
                print(f"SKIP read (not UTF-8) {f.relative_to(REPO_ROOT)}: {e}", file=sys.stderr, flush=True)
                continue
            new_text, did = _rewrite_body(
                text,
                apply_chunked_asset_binary=_is_under_chunked(f),
            )
            if not did:
                continue
            if args.dry_run:
                changed += 1
                if not args.quiet:
                    print(f"would update: {f.relative_to(REPO_ROOT)}", flush=True)
            else:
                try:
                    f.write_text(new_text, encoding="utf-8")
                    changed += 1
                    if not args.quiet:
                        print(f"updated: {f.relative_to(REPO_ROOT)}", flush=True)
                except OSError as e:
                    print(f"SKIP write {f.relative_to(REPO_ROOT)}: {e}", file=sys.stderr, flush=True)

        _emit_progress(force=True)
        done = f"Done. Files matched: {len(files)}, files rewritten: {changed}"
        print(done, flush=True)
        print(done, file=sys.stderr, flush=True)
        if log_fp is not None:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            log_fp.write(f"{ts} {done}\n")
            log_fp.flush()
    finally:
        if log_fp is not None:
            log_fp.close()


if __name__ == "__main__":
    main()

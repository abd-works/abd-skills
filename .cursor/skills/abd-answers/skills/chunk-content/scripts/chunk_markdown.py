"""
Chunk converted markdown into smaller pieces for agent memory.

Fork of abd-context-to-memory ``chunk_markdown.py``. **Destinations:** default chunked output is
``<assets>/abd-answers-memory-pipeline/chunked/`` mirroring paths under the markdown folder.

Resolve ``--path`` in order:
  1. ``<pipeline>/markdown/<path>`` when that exists
  2. ``<assets>/<path>`` (source tree)

Chunk output always mirrors the pipeline layout: ``<pipeline>/chunked/<path under Assets>`` when the
input resolves under Assets (never ``data/assets/memory/<folder>/`` for that case).

Usage:
  python chunk_markdown.py --path <source_folder> [--memory <memory_name>]
  python chunk_markdown.py --path <source_folder> --output <output_dir>
  python chunk_markdown.py --path <source_folder> --update   # skip fresh chunks; delete orphaned chunk files
  python chunk_markdown.py --path <source_folder> --update --force   # rechunk everything
  python chunk_markdown.py --path <source_folder> --log-file <path>   # append START/END + tee (use one file per stage)

Run ``convert_to_markdown.py`` first so markdown exists under the pipeline mirror.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _config import (
    ASSETS,
    MEMORY,
    PIPELINE_CHUNKED,
    PIPELINE_MARKDOWN,
    PIPELINE_ROOT,
    ROOT,
    ensure_root,
    path_is_pinecone_rag_metadata_only,
)

ensure_root()

_scripts_chunk = Path(__file__).resolve().parent
if str(_scripts_chunk) not in sys.path:
    sys.path.insert(0, str(_scripts_chunk))
from _pipeline_logging import get_optional_log_file, pipeline_log_session
from _pipeline_update import chunk_manifest_path, delete_chunk_outputs_for_stem, load_json, save_json
from chunked_source_asset import chunked_source_path_to_asset_binary
MIN_CHUNK_LINES = 5


def _find_chunk_src_root(source_path: str) -> Path | None:
    p = Path(source_path)
    if p.is_absolute():
        return p if p.is_dir() else None
    rel = source_path.strip().replace("\\", "/").strip("/")
    candidates = [
        PIPELINE_MARKDOWN / rel if rel else PIPELINE_MARKDOWN,
        ASSETS / rel if rel else ASSETS,
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _chunk_base_for_output(
    src_root: Path,
    memory_name_override: str | None,
    output_override: str | None,
) -> tuple[Path, str]:
    if output_override:
        chunk_base = Path(output_override)
        if not chunk_base.is_absolute():
            chunk_base = Path.cwd() / chunk_base
        return chunk_base, str(chunk_base)

    if output_override is None:
        try:
            rel = src_root.resolve().relative_to(PIPELINE_MARKDOWN.resolve())
            if rel == Path("."):
                base = PIPELINE_CHUNKED
            else:
                base = PIPELINE_CHUNKED / rel
            return base, str(base)
        except ValueError:
            pass
        # --path pointed at ASSETS (e.g. markdown not created yet under pipeline): mirror chunked layout
        try:
            rel = src_root.resolve().relative_to(ASSETS.resolve())
            if rel == Path("."):
                base = PIPELINE_CHUNKED
            else:
                base = PIPELINE_CHUNKED / rel
            return base, str(base)
        except ValueError:
            pass

    memory_name = memory_name_override or src_root.name
    base = MEMORY / memory_name
    return base, f"markdown/{memory_name}/"


def _find_image_refs(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(<?([^)>]+)>?\)", text)


def _copy_images(refs: list[str], src_base: Path, dst_base: Path):
    import shutil

    for ref in refs:
        src = src_base / ref
        if not src.exists():
            continue
        dst = dst_base / ref
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(str(src), str(dst))


def _chunk_by_slides(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(<!-- Slide number: \d+ -->)", text)
    chunks, current_label, current_lines = [], "preamble", []

    for part in parts:
        m = re.match(r"<!-- Slide number: (\d+) -->", part)
        if m:
            if current_lines and "".join(current_lines).strip():
                chunks.append((current_label, "".join(current_lines)))
            current_label = f"slide_{int(m.group(1)):02d}"
            current_lines = [part]
        else:
            current_lines.append(part)

    if current_lines and "".join(current_lines).strip():
        chunks.append((current_label, "".join(current_lines)))
    return chunks


def _chunk_by_headings(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0

    for line in lines:
        if re.match(r"^#{1,2}\s", line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)

    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _chunk_by_section_markers(text: str) -> list[tuple[str, str]]:
    lines = text.split("\n")
    chunks, current_lines, chunk_idx = [], [], 0
    section_pat = re.compile(r"^CHAPTER\s+\d+\b", re.IGNORECASE)

    for line in lines:
        if section_pat.search(line) and len(current_lines) >= MIN_CHUNK_LINES:
            chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
            current_lines, chunk_idx = [], chunk_idx + 1
        current_lines.append(line)

    if current_lines:
        chunks.append((f"section_{chunk_idx:02d}", "\n".join(current_lines)))
    return chunks


def _has_markdown_headings(text: str) -> bool:
    return bool(re.search(r"^#{1,2}\s", text, re.MULTILINE))


def _is_slide_deck(text: str) -> bool:
    return bool(re.search(r"<!-- Slide number: \d+ -->", text))


def _is_chunked_output(path: Path) -> bool:
    return bool(re.search(r"__(?:slide|section|page)_\d+\.md$", path.name, re.IGNORECASE))


def _is_under_source_memory_tree(md_path: Path, src_root: Path) -> bool:
    try:
        rel = md_path.relative_to(src_root.resolve())
    except ValueError:
        return False
    if not rel.parts:
        return False
    return rel.parts[0].casefold() == "memory"


def _extract_source_ref(text: str) -> tuple[str | None, str | None]:
    m = re.search(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text)
    return (m.group(1).strip(), m.group(2).strip()) if m else (None, None)


def _normalize_source_path_from_comment(path_part: str) -> str:
    """Normalize legacy ``source/...`` and bare pipeline paths to repo-relative ``data/assets/...``."""
    p = path_part.strip().replace("\\", "/")
    if p.startswith("source/"):
        return "data/assets/" + p[len("source/") :]
    if p.startswith("data/assets/"):
        return p
    if p.startswith("abd-answers-memory-pipeline/"):
        return "data/assets/" + p
    return p


def _extract_best_source_ref(text: str) -> tuple[str | None, str | None]:
    """Prefer a ``data/assets/...`` path that points at an original asset (not ``.md`` mirror)."""
    found: list[tuple[str, str]] = []
    for m in re.finditer(r"<!--\s*Source:\s*([^|]+)\s*\|\s*([^>]+)\s*-->", text):
        found.append((m.group(1).strip(), m.group(2).strip()))
    for path_part, url in found:
        n = _normalize_source_path_from_comment(path_part)
        if n.startswith("data/assets/") and not n.lower().endswith(".md"):
            return n, url
    if found:
        p, u = found[0]
        return _normalize_source_path_from_comment(p), u
    return None, None


def _data_assets_repo_path_for_file_under_assets(md_path: Path) -> str | None:
    """``md_path`` under ``ASSETS`` → ``data/assets/<rel>`` (always include the prefix)."""
    try:
        rel = md_path.resolve().relative_to(ASSETS.resolve())
        return f"data/assets/{rel.as_posix()}"
    except ValueError:
        return None


def _try_sibling_binary_for_md(repo_path: str) -> str:
    """If ``repo_path`` is ``data/assets/.../Foo.md`` and ``Foo.pptx`` (etc.) exists beside it, use that path."""
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


_PIPELINE_MD_PREFIX = "data/assets/abd-answers-memory-pipeline/markdown/"


def _pipeline_mirror_md_to_original_asset(repo_path: str) -> str:
    """
    Converted markdown lives under ``.../abd-answers-memory-pipeline/markdown/<mirror>/Foo.md``;
    originals usually live at ``data/assets/<mirror>/Foo.pptx``.
    """
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


def _canonical_source_path_for_chunk(
    md_path: Path, comment_path: str | None, source_url: str | None
) -> tuple[str | None, str | None]:
    """Single repo-relative path for chunk ``Source:`` (``data/assets/...`` + original binary when possible)."""
    p: str | None = None
    if comment_path:
        p = _normalize_source_path_from_comment(comment_path.strip())
    if not p or not p.startswith("data/assets/"):
        p = _data_assets_repo_path_for_file_under_assets(md_path)
    if not p:
        return None, source_url
    p = _pipeline_mirror_md_to_original_asset(p)
    p = _try_sibling_binary_for_md(p)
    if p:
        p = chunked_source_path_to_asset_binary(p, source_url or "")
    return p, source_url


def _add_chunk_source_ref(content: str, source_path: str | None, source_url: str | None, location: str) -> str:
    if not source_path:
        return content
    loc = f", {location}" if location else ""
    url = f" | {source_url}" if source_url else ""
    return f"<!-- Source: {source_path}{loc}{url} -->\n\n" + content


def _chunk_outputs_max_mtime(chunk_root: Path, stem: str) -> float | None:
    mtimes: list[float] = []
    if not chunk_root.is_dir():
        return None
    for pattern in (f"{stem}.md", f"{stem}__*.md"):
        for p in chunk_root.glob(pattern):
            if p.is_file():
                mtimes.append(p.stat().st_mtime)
    return max(mtimes) if mtimes else None


def chunk_file(md_path: Path, conv_root: Path, chunk_root: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    stem = md_path.stem
    comment_path, source_url = _extract_best_source_ref(text)
    source_path, source_url = _canonical_source_path_for_chunk(md_path, comment_path, source_url)
    out_dir = chunk_root
    out_dir.mkdir(parents=True, exist_ok=True)

    if _is_slide_deck(text):
        chunks = _chunk_by_slides(text)
    elif text.count("\n") > 200:
        if _has_markdown_headings(text):
            chunks = _chunk_by_headings(text)
        else:
            chunks = _chunk_by_section_markers(text)
    else:
        chunks = [(stem, text)]

    def _loc(label: str) -> str:
        if label.startswith("slide_"):
            return f"slide {int(label.split('_')[1])}"
        if label.startswith("section_"):
            return f"section {int(label.split('_')[1]) + 1}"
        return ""

    written = 0
    for label, content in chunks:
        if not content.strip():
            continue
        content = _add_chunk_source_ref(content, source_path, source_url, _loc(label))
        out = out_dir / (f"{stem}__{label}.md" if len(chunks) > 1 else f"{stem}.md")
        out.write_text(content, encoding="utf-8")
        for ref in _find_image_refs(content):
            _copy_images([ref], conv_root, chunk_root)
        written += 1
    return written


def _run_path_mode(
    source_path: str,
    memory_name_override: str | None = None,
    output_override: str | None = None,
    *,
    update: bool = False,
    force: bool = False,
) -> None:
    src_root = _find_chunk_src_root(source_path)
    if src_root is None or not src_root.is_dir():
        print(f"Path not found: {source_path}")
        print(f"Try a folder under {PIPELINE_MARKDOWN} (pipeline markdown mirror) or {ASSETS}.")
        return

    chunk_base, dest = _chunk_base_for_output(src_root, memory_name_override, output_override)

    md_files = sorted(
        f
        for f in src_root.rglob("*.md")
        if "images" not in f.parts
        and not _is_chunked_output(f)
        and not _is_under_source_memory_tree(f, src_root)
        and not path_is_pinecone_rag_metadata_only(f)
    )
    if not md_files:
        print(f"No markdown in {src_root}")
        print("Run convert_to_markdown.py --memory <path> first.")
        return

    scope_key = str(src_root.resolve())
    manifest_path = chunk_manifest_path(PIPELINE_ROOT)
    expected_md: dict[str, float] = {}
    for md in md_files:
        try:
            mk = md.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            mk = str(md.resolve())
        expected_md[mk] = md.stat().st_mtime

    if update:
        data = load_json(manifest_path, {"version": 1, "scopes": {}})
        scopes = data.setdefault("scopes", {})
        old = scopes.get(scope_key, {})
        if isinstance(old, dict):
            to_remove = set(old) - set(expected_md)
            for md_key in sorted(to_remove):
                try:
                    md_abs = ROOT / md_key
                except OSError:
                    continue
                stem = Path(md_key).stem
                try:
                    rel_parent = md_abs.parent.relative_to(src_root.resolve())
                except ValueError:
                    rel_parent = Path(".")
                chunk_root = chunk_base / rel_parent
                n = delete_chunk_outputs_for_stem(chunk_root, stem)
                if n:
                    print(f"  [update] removed {n} orphan chunk file(s) for {md_key}")

    print(f"Source: {src_root}  ({len(md_files)} files) -> {dest}\n")
    total = 0
    for i, f in enumerate(md_files, 1):
        conv_root = f.parent
        rel_parent = f.parent.relative_to(src_root)
        chunk_root = chunk_base / rel_parent
        rel = f.relative_to(src_root)
        label = str(rel) if rel != Path(".") else f.name
        print(f"  [{i}/{len(md_files)}] {label} ... ", end="", flush=True)
        stem = f.stem
        if force:
            delete_chunk_outputs_for_stem(chunk_root, stem)
        elif update:
            mx = _chunk_outputs_max_mtime(chunk_root, stem)
            if mx is not None and mx >= f.stat().st_mtime:
                print("SKIP (up to date)")
                continue
            if mx is not None:
                delete_chunk_outputs_for_stem(chunk_root, stem)
        try:
            n = chunk_file(f, conv_root, chunk_root)
            total += n
            print(f"OK  ({n} chunks)")
        except Exception as e:
            print(f"FAIL  {e}")
    if update:
        data = load_json(manifest_path, {"version": 1, "scopes": {}})
        data.setdefault("scopes", {})[scope_key] = {k: expected_md[k] for k in sorted(expected_md)}
        data["version"] = 1
        save_json(manifest_path, data)
    print(f"\nDone: {total} chunks.")


def _get_arg(flag: str) -> str | None:
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return None


def _main_impl():
    path_arg = _get_arg("--path")
    memory_arg = _get_arg("--memory")
    output_arg = _get_arg("--output")
    upd = "--update" in sys.argv
    force = "--force" in sys.argv
    if path_arg:
        _run_path_mode(
            path_arg,
            memory_name_override=memory_arg,
            output_override=output_arg,
            update=upd,
            force=force,
        )
        return
    if memory_arg:
        _run_path_mode(memory_arg, update=upd, force=force)
        return
    print(
        "Usage: python chunk_markdown.py --path <source_folder> "
        "[--memory <name> | --output <dir>] [--update] [--force] [--log-file <path>]"
    )


def main():
    log_path = get_optional_log_file()
    if log_path:
        with pipeline_log_session(log_path, "chunk_markdown", sys.argv):
            _main_impl()
    else:
        _main_impl()


if __name__ == "__main__":
    main()

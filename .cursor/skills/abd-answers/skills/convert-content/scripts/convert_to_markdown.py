"""
Convert source files to markdown for agent memory (abd-answers pipeline).

Fork of abd-context-to-memory ``convert_to_markdown.py``. **Destinations:** writes converted
``.md`` under ``<assets>/abd-answers-memory-pipeline/markdown/`` mirroring paths under the rest of ``assets/``,
instead of next to each source file. Existing ``.md`` under the source tree are copied into the
same mirror.

Usage:
  python convert_to_markdown.py --memory <source_path>   # folder: all supported files
  python convert_to_markdown.py --memory <source_path> --sharepoint-base <url>
  python convert_to_markdown.py --memory <source_path> --resume-from-log <pipeline-full.log>
  python convert_to_markdown.py --memory <source_path> --update   # skip up-to-date; delete mirror orphans
  python convert_to_markdown.py --memory <source_path> --update --force   # reconvert & resync all
  python convert_to_markdown.py --file <file_path>      # single file only

``--resume-from-log``: reads ``[n/total] ... OK`` lines from the log (UTF-8; UTF-16 LE with BOM
for legacy PowerShell ``Tee-Object`` logs), takes the **maximum** ``n``, and skips the first ``n`` files
(same sorted order as a full run). A restarted run that logged ``[1/total]`` again does not
erase earlier progress in the same file.

Configure OneDrive→SharePoint in ``scripts/source-convert/sharepoint_mapping.json``.

Requires: pip install "markitdown[all]"

**PDF dev / smoke test:** ``PDF_POSTPROCESS_MAX_LINES=5000`` — only the first N lines of the raw
extract are post-processed (faster iteration); unset for the full book.

**Progress lines:** only the suffix after ``...`` counts: ``OK``, ``FAIL``, or ``SKIP (up to date)``.
Other text on stderr (e.g. pdfminer font warnings) is not a per-file failure unless that file's line shows ``FAIL``.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

try:
    from markitdown import MarkItDown, StreamInfo
    from markitdown.converters import DocxConverter, PptxConverter, XlsConverter, XlsxConverter
except ImportError:
    print('Missing dependency. Run: pip install "markitdown[all]"')
    sys.exit(1)

# pdfminer (used by MarkItDown for PDFs) emits a WARNING per bad FontBBox in font descriptors.
# Conversion still succeeds; the noise drowns out real progress in tee'd logs.
logging.getLogger("pdfminer").setLevel(logging.ERROR)

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
try:
    from onedrive_to_sharepoint import (
        get_sharepoint_base_for_path,
        get_sharepoint_open_doc_url_for_file,
        get_sharepoint_url_for_file,
        path_is_onedrive,
        extract_onedrive_prefix,
    )
except ImportError:
    def get_sharepoint_base_for_path(p):
        return (None, "")

    def get_sharepoint_open_doc_url_for_file(p):
        return None

    def get_sharepoint_url_for_file(p, b, q):
        return ""

    def path_is_onedrive(p):
        return False

    def extract_onedrive_prefix(p):
        return None


from _config import (
    ASSETS,
    PIPELINE_MARKDOWN,
    PIPELINE_ROOT,
    ROOT,
    ensure_root,
    path_is_pinecone_rag_metadata_only,
    resolve_repo_data_assets_root,
)

ensure_root()

from _pipeline_logging import (
    configure_stdio_utf8,
    get_optional_log_file,
    pipeline_log_session,
    safe_print,
)
from _pipeline_update import convert_manifest_path, load_json, save_json

from pdf_markdown_post import postprocess_pdf_markdown


def _maybe_truncate_pdf_extract_lines(text: str) -> str:
    """If ``PDF_POSTPROCESS_MAX_LINES`` is a positive integer, keep only the first N lines."""
    raw = os.environ.get("PDF_POSTPROCESS_MAX_LINES", "").strip()
    if not raw.isdigit():
        return text
    n = int(raw)
    if n <= 0:
        return text
    lines = text.splitlines()
    if len(lines) <= n:
        return text
    body = "\n".join(lines[:n])
    if text.endswith("\n") or body:
        body += "\n"
    return (
        f"<!-- excerpt: first {n} lines of raw extract only — "
        f"PDF_POSTPROCESS_MAX_LINES (unset env for full book) -->\n\n"
    ) + body


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


def _patch_pptx_chart_never_returns_none() -> None:
    """markitdown: _convert_chart_to_markdown can return None on some ValueError branches; get_shape_content does += and crashes."""
    try:
        from markitdown.converters._pptx_converter import PptxConverter
    except ImportError:
        return
    _orig = PptxConverter._convert_chart_to_markdown

    def _safe(self, chart):  # type: ignore[no-untyped-def]
        out = _orig(self, chart)
        return out if out is not None else "\n\n*[chart could not be exported]*\n\n"

    PptxConverter._convert_chart_to_markdown = _safe  # type: ignore[method-assign]


_patch_pptx_chart_never_returns_none()


def _data_assets_path_part_for_source(
    src: Path,
    memory_name: str | None,
    logical_rel: Path | None,
    src_base: Path | None,
) -> str | None:
    """Repo-relative path string for HTML comments: ``data/assets/...`` (abd-answers root)."""
    try:
        rel = src.resolve().relative_to(ASSETS.resolve())
        return f"data/assets/{rel.as_posix()}"
    except ValueError:
        pass
    if logical_rel is not None:
        rel_posix = logical_rel.as_posix()
    elif src_base is not None:
        try:
            rel_posix = src.relative_to(src_base).as_posix()
        except (ValueError, OSError):
            return None
    else:
        return None
    if "/" in rel_posix:
        return f"data/assets/{rel_posix}"
    if memory_name:
        return f"data/assets/{memory_name}/{rel_posix}"
    return f"data/assets/{rel_posix}"


# MarkItDown routes through Magika; when a file's bytes don't match its extension (cloud-only
# placeholders, partial sync, corruption), Magika adds a second "guess" (e.g. PDF). After
# PptxConverter fails, PdfConverter then runs and errors with misleading PDFSyntaxError
# ("No /Root object"). Call OOXML converters directly with a single StreamInfo so we never
# fall through to PdfConverter for `.pptx` / `.docx` / `.xlsx` / `.xls`.
_OOXML_CONVERTERS = {
    ".pptx": PptxConverter(),
    ".docx": DocxConverter(),
    ".xlsx": XlsxConverter(),
    ".xls": XlsConverter(),
}


def _convert_src_to_markdown_text(src: Path) -> str:
    ext = src.suffix.lower()
    conv = _OOXML_CONVERTERS.get(ext)
    if conv is not None:
        with open(src, "rb") as fh:
            info = StreamInfo(extension=ext, filename=src.name, local_path=str(src))
            return conv.convert(fh, info).text_content
    return _md.convert(str(src)).text_content


DEFAULT_SHAREPOINT_QUERY = "csf=1&web=1"

_onedrive_warned_prefixes: set[str] = set()

_SKILL_ROOT = _scripts_dir


def _print_onedrive_mapping_instructions(prefix: str) -> None:
    config_path = _SKILL_ROOT / "sharepoint_mapping.json"
    add_script = _scripts_dir / "add_sharepoint_mapping.py"
    try:
        script_rel = add_script.relative_to(ROOT)
    except ValueError:
        script_rel = add_script
    print("\n" + "=" * 70)
    print("WARNING: Source is in OneDrive but no SharePoint mapping is configured.")
    safe_print(f"  OneDrive folder: {prefix}")
    print("  Links in the generated markdown will use local paths (not shareable).")
    print()
    print("To add shareable SharePoint links:")
    print("  1. Open any file from this OneDrive folder in SharePoint/OneDrive web.")
    print("  2. Copy the URL from the browser address bar.")
    print("  3. Add the mapping (paste your URL; script will derive the base):")
    print(f'     python {script_rel} --prefix "{prefix}" --base "<paste_url_here>"')
    print()
    print("  Or with a file path (prefix is auto-detected):")
    print(f'     python {script_rel} --path "<file_in_onedrive>" --base "<paste_url_here>"')
    print()
    print(f"  Or edit {config_path} and add an entry to the mappings array.")
    print("=" * 70 + "\n")


def convert_one(
    src: Path,
    out_dir: Path,
    source_ref: bool = True,
    src_base: Path | None = None,
    sharepoint_base: str | None = None,
    sharepoint_query: str | None = None,
    memory_name: str | None = None,
    logical_rel: Path | None = None,
) -> Path:
    """Convert one file to markdown. Returns output path."""
    out_dir.mkdir(parents=True, exist_ok=True)

    text = _convert_src_to_markdown_text(src)
    if src.suffix.lower() == ".pdf":
        text = _maybe_truncate_pdf_extract_lines(text)
        text = postprocess_pdf_markdown(text, pdf_path=src)

    if sharepoint_base is None:
        od_base, od_query = get_sharepoint_base_for_path(src)
        if od_base:
            sharepoint_base = od_base
            sharepoint_query = sharepoint_query or od_query
        elif path_is_onedrive(src):
            prefix = extract_onedrive_prefix(src)
            if prefix and prefix not in _onedrive_warned_prefixes:
                _onedrive_warned_prefixes.add(prefix)
                _print_onedrive_mapping_instructions(prefix)

    if source_ref:
        added = False
        path_part = _data_assets_path_part_for_source(
            src, memory_name, logical_rel, src_base
        )
        if path_part:
            q = sharepoint_query or DEFAULT_SHAREPOINT_QUERY
            url_part = get_sharepoint_open_doc_url_for_file(src) or ""
            if not url_part and sharepoint_base:
                url_part = get_sharepoint_url_for_file(src, sharepoint_base, q)
            if not url_part and sharepoint_base:
                try:
                    rel_a = src.resolve().relative_to(ASSETS.resolve())
                    encoded = quote(rel_a.as_posix(), safe="/")
                    url_part = f"{sharepoint_base.rstrip('/')}/{encoded}?{q}"
                except ValueError:
                    pass
            if url_part:
                text = f"<!-- Source: {path_part} | {url_part} -->\n\n" + text
                added = True
            else:
                try:
                    rel_a = src.resolve().relative_to(ASSETS.resolve())
                    local_uri = (ASSETS / rel_a).as_uri()
                except ValueError:
                    local_uri = src.resolve().as_uri()
                text = f"<!-- Source: {path_part} | {local_uri} -->\n\n" + text
                added = True
        if not added and sharepoint_base:
            url_part = get_sharepoint_open_doc_url_for_file(src) or get_sharepoint_url_for_file(
                src, sharepoint_base, sharepoint_query or DEFAULT_SHAREPOINT_QUERY
            )
            if url_part:
                pp = path_part or (src.name if not src_base else str(src.relative_to(src.parent)))
                text = f"<!-- Source: {pp} | {url_part} -->\n\n" + text
                added = True
        if not added:
            try:
                rel = src.relative_to(ASSETS)
                path_part = f"data/assets/{rel.as_posix()}"
                url = (ASSETS / rel).as_uri()
                text = f"<!-- Source: {path_part} | {url} -->\n\n" + text
            except (ValueError, OSError):
                try:
                    rel = src.relative_to(ROOT)
                    path_part = f"data/assets/{rel.as_posix()}"
                    url = (ASSETS / rel).as_uri() if (ASSETS / rel).exists() else (ROOT / rel).as_uri()
                    text = f"<!-- Source: {path_part} | {url} -->\n\n" + text
                except (ValueError, OSError):
                    pass

    out = out_dir / (src.stem + ".md")
    out.write_text(text, encoding="utf-8")
    return out


_SKIP_WALK_DIRS = frozenset({"abd-answers-memory-pipeline", ".git", "__pycache__", "node_modules"})

# Pipeline log lines: "  [1479/12592] path\\file.pptx ... OK  (12 KB)"
# Do not anchor with ^ only — PowerShell Tee-Object often writes UTF-16 LE; match the bracket run.
_LOG_LINE_OK = re.compile(
    r"\[(\d+)/(\d+)\][^\r\n]*?\.\.\.\s+OK\b",
)


def _read_log_text(log_path: Path) -> str | None:
    """
    Read log text. Prefer UTF-8 (pipeline ``--log-file``); support UTF-16 BOM legacy;
    tolerate invalid bytes in mixed/corrupt tails via ``errors=replace``.
    """
    try:
        raw = log_path.read_bytes()
    except OSError:
        return None
    if not raw:
        return ""
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16-le", errors="replace")
    if raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16-be", errors="replace")
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig", errors="replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return raw.decode("utf-16-le", errors="replace")
        except UnicodeDecodeError:
            return raw.decode("utf-8", errors="replace")


def parse_resume_start_index_from_log(log_path: Path) -> int | None:
    """
    Read a pipeline log (e.g. data/pipeline-full.log) and find the last successful
    convert line. Files are processed in sorted order; the bracket number n means
    the n-th file finished OK, so the next file to process is at 0-based index n.

    Returns None if no OK line is found or the file is missing.
    """
    if not log_path.is_file():
        return None
    text = _read_log_text(log_path)
    if not text:
        return None
    matches = list(_LOG_LINE_OK.finditer(text))
    if not matches:
        return None
    # [n/total] ... OK: n is the completed file ordinal. Use max(n) so a failed resume that
    # restarted at [1/total] does not erase progress from an earlier run in the same log.
    last_n = max(int(m.group(1)) for m in matches)
    return last_n


def _walk_with_logical_path(
    root: Path, logical_prefix: Path, followlinks: bool = True
) -> list[tuple[Path, Path]]:
    out: list[tuple[Path, Path]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=followlinks):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_WALK_DIRS and not d.startswith(".")]
        dp = Path(dirpath)
        try:
            rel = dp.relative_to(root)
        except ValueError:
            rel = Path(logical_prefix.name)
        logical_rel = logical_prefix / rel if rel != Path(".") else logical_prefix
        for name in filenames:
            p = dp / name
            if p.suffix.lower() in SUPPORTED:
                try:
                    if p.is_file():
                        out.append((p, logical_rel / name))
                except OSError:
                    pass
    return out


def _out_dir_for_pipeline(logical_rel: Path) -> Path:
    parent = logical_rel.parent
    if parent == Path("."):
        return PIPELINE_MARKDOWN
    return PIPELINE_MARKDOWN / parent


def _mirror_rel_for_standalone_md(md_path: Path, src_full: Path) -> Path:
    """Path under ``PIPELINE_MARKDOWN`` mirroring ``data/assets/...`` (hub vs repo-safe)."""
    repo_assets = resolve_repo_data_assets_root().resolve()
    for base in (repo_assets, ASSETS.resolve()):
        try:
            return md_path.resolve().relative_to(base)
        except ValueError:
            continue
    return md_path.relative_to(src_full)


def _markdown_mirror_rel_for_convert(f: Path, logical_rel: Path) -> str:
    out_dir = _out_dir_for_pipeline(logical_rel)
    out_md = out_dir / (f.stem + ".md")
    return out_md.resolve().relative_to(PIPELINE_MARKDOWN.resolve()).as_posix()


def _expected_standalone_md_mirror(src_full: Path) -> dict[str, float]:
    """Pipeline markdown mirror relpaths (posix) -> source mtime for standalone ``.md`` copies."""
    out: dict[str, float] = {}
    for md_path in src_full.rglob("*.md"):
        if "abd-answers-memory-pipeline" in md_path.parts:
            continue
        if path_is_pinecone_rag_metadata_only(md_path):
            continue
        try:
            rel = _mirror_rel_for_standalone_md(md_path, src_full)
        except ValueError:
            continue
        dst = PIPELINE_MARKDOWN / rel
        key = dst.resolve().relative_to(PIPELINE_MARKDOWN.resolve()).as_posix()
        out[key] = md_path.stat().st_mtime
    return out


def _merge_expected_convert(files: list[tuple[Path, Path]], src_full: Path) -> dict[str, float]:
    expected: dict[str, float] = {}
    for f, lr in files:
        key = _markdown_mirror_rel_for_convert(f, lr)
        expected[key] = f.stat().st_mtime
    for k, m in _expected_standalone_md_mirror(src_full).items():
        expected[k] = m
    return expected


def _sync_markdown_files_from_source(src_full: Path, *, update: bool = False, force: bool = False) -> None:
    """Copy standalone ``.md`` from source tree into the pipeline markdown mirror."""
    paths = sorted(
        md_path
        for md_path in src_full.rglob("*.md")
        if "abd-answers-memory-pipeline" not in md_path.parts
        and not path_is_pinecone_rag_metadata_only(md_path)
    )
    for md_path in paths:
        # Mirror under PIPELINE_MARKDOWN using the same layout as data/assets (not only
        # relative to --memory scope), so root-level .md in a scoped folder land at
        # markdown/01 Agile Practices/.../file.md, not markdown/file.md.
        try:
            rel = _mirror_rel_for_standalone_md(md_path, src_full)
        except ValueError:
            continue
        dst = PIPELINE_MARKDOWN / rel
        label = rel.as_posix()
        mirror_newer = dst.is_file() and dst.stat().st_mtime >= md_path.stat().st_mtime
        if mirror_newer and not force:
            if update:
                safe_print(f"  [md] {label} ... SKIP (mirror up to date)", flush=True)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md_path, dst)
        kb = dst.stat().st_size // 1024
        safe_print(f"  [md] {label} ... OK  ({kb} KB)", flush=True)


def _run_file_mode(file_path: str) -> None:
    p = Path(file_path)
    if not p.is_absolute():
        for base in (ASSETS, ROOT):
            candidate = base / file_path
            if candidate.is_file():
                p = candidate
                break
    if not p.is_file():
        print(f"File not found: {file_path}")
        return

    if p.suffix.lower() == ".md":
        try:
            rel = p.relative_to(ASSETS.resolve())
            out_dir = PIPELINE_MARKDOWN / rel.parent
        except ValueError:
            out_dir = PIPELINE_MARKDOWN
        out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / p.name
        shutil.copy2(p, dst)
        print(f"Markdown: {p.name} -> {dst}\nDone (copied to pipeline markdown mirror)")
        return

    if p.suffix.lower() not in SUPPORTED:
        print(f"Unsupported format: {p.suffix}. Supported: {sorted(SUPPORTED)}")
        return

    try:
        rel = p.relative_to(ASSETS.resolve())
        out_dir = PIPELINE_MARKDOWN / rel.parent
    except ValueError:
        out_dir = PIPELINE_MARKDOWN
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"File: {p.name} -> {out_dir}/\n")
    try:
        memory_name = p.parent.name if p.parent != Path(".") else p.stem
        logical_rel = Path(p.name)
        out = convert_one(
            p,
            out_dir,
            memory_name=memory_name,
            logical_rel=logical_rel,
        )
        kb = out.stat().st_size // 1024
        print(f"Done: 1 file converted ({kb} KB)")
    except (Exception, BaseException) as e:
        reason = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
        print(f"FAIL  {reason}")
        print(f"  >>> CONVERSION FAILED: {p}")


def _run_memory_mode(
    memory_path: str,
    sharepoint_base: str | None = None,
    sharepoint_query: str | None = None,
    subfolders: list[str] | None = None,
    memory_name_override: str | None = None,
    resume_from_log: Path | None = None,
    *,
    update: bool = False,
    force: bool = False,
) -> None:
    """Convert folder; write markdown under ``abd-answers-memory-pipeline/markdown/`` (mirrored)."""
    p = Path(memory_path)
    if p.is_absolute():
        src_full = p
    else:
        under_assets = ASSETS / memory_path
        under_root = ROOT / memory_path
        if under_assets.exists():
            src_full = under_assets
        elif under_root.exists():
            src_full = under_root
        else:
            safe_print(f"Path not found: {memory_path}")
            if "data/assets" in memory_path.replace("\\", "/").lower():
                safe_print(
                    "Hint: --memory is resolved under ASSETS (repo data/assets). "
                    "Use a path relative to that folder, e.g. "
                    "'06 Client Engagements/Inactive/MyClient' — not 'data/assets/06...'.",
                    file=sys.stderr,
                )
            return

    memory_name = memory_name_override or src_full.name

    # Anchor logical paths under ASSETS so files in the scope folder root mirror to
    # PIPELINE_MARKDOWN/<relative path under Assets>/... instead of the mirror root.
    try:
        logical_base = src_full.resolve().relative_to(ASSETS.resolve())
    except ValueError:
        logical_base = Path(".")

    folders_to_walk: list[tuple[Path, Path]] = []
    if subfolders:
        for sub in subfolders:
            sub_path = src_full / sub.strip()
            if sub_path.exists():
                folders_to_walk.append((sub_path, logical_base / Path(sub.strip())))
    if not folders_to_walk:
        folders_to_walk = [(src_full, logical_base)]

    files: list[tuple[Path, Path]] = []
    for walk_root, logical_prefix in folders_to_walk:
        files.extend(_walk_with_logical_path(walk_root, logical_prefix))
    files.sort(key=lambda x: str(x[1]))
    files = [(f, lr) for f, lr in files if not path_is_pinecone_rag_metadata_only(f)]

    # Standalone .md under the source tree are copied in _sync_markdown_files_from_source (not in SUPPORTED).
    # If the folder has only .md files, ``files`` is empty — we must still sync, not exit early.
    standalone_mirror_expected = _expected_standalone_md_mirror(src_full)
    if not files and not standalone_mirror_expected:
        safe_print(
            f"No convertible files (supported: {', '.join(sorted(SUPPORTED))}) "
            f"and no standalone .md under {src_full}"
        )
        return

    manifest_path = convert_manifest_path(PIPELINE_ROOT)
    scope_key = str(src_full.resolve())
    expected: dict[str, float]
    if update:
        expected = _merge_expected_convert(files, src_full)
        data = load_json(manifest_path, {"version": 1, "scopes": {}})
        scopes = data.setdefault("scopes", {})
        old = scopes.get(scope_key, {})
        if isinstance(old, dict):
            to_remove = set(old) - set(expected)
            for k in sorted(to_remove):
                target = PIPELINE_MARKDOWN / k
                if target.is_file():
                    try:
                        target.unlink()
                        safe_print(f"  [update] removed orphan mirror: {k}")
                    except OSError as e:
                        safe_print(f"  [update] could not remove {k}: {e}")

    start_idx = 0
    if resume_from_log is not None and files:
        parsed = parse_resume_start_index_from_log(resume_from_log)
        if parsed is None:
            safe_print(
                f"Warning: no '[n/total] ... OK' line found in {resume_from_log}; "
                "processing from the first file.\n"
            )
        else:
            start_idx = parsed
            if start_idx >= len(files):
                safe_print(
                    f"Resume from log: last OK implied start index {start_idx}, "
                    f"but only {len(files)} file(s) in the current scan — nothing to do."
                )
                return
            last_line = resume_from_log.resolve()
            safe_print(
                f"Resume from log {last_line}: skipped first {start_idx} file(s); "
                f"continuing at [{start_idx + 1}/{len(files)}].\n"
            )

    if files:
        safe_print(f"Source: {src_full}  ({len(files)} convertible files) -> {PIPELINE_MARKDOWN} (mirror)\n")
        safe_print(
            "Per-file result is only the line ending with: OK (...), FAIL (...), or SKIP (up to date).\n"
            "Messages from PDF/Office libraries on stderr are not failures unless the same file line shows FAIL.\n"
        )
    elif standalone_mirror_expected:
        safe_print(
            f"Source: {src_full}  (0 convertible files; {len(standalone_mirror_expected)} standalone .md) "
            f"-> {PIPELINE_MARKDOWN} (mirror)\n"
        )

    ok, fail = [], []
    slice_files = files[start_idx:]
    for i, (f, logical_rel) in enumerate(slice_files, start_idx + 1):
        out_dir = _out_dir_for_pipeline(logical_rel)
        out_dir.mkdir(parents=True, exist_ok=True)

        label = str(logical_rel) if logical_rel != Path(".") else f.name
        safe_print(f"  [{i}/{len(files)}] {label} ... ", end="", flush=True)
        out_md = out_dir / (f.stem + ".md")
        if (
            update
            and not force
            and out_md.is_file()
            and out_md.stat().st_mtime >= f.stat().st_mtime
        ):
            safe_print("SKIP (up to date)", flush=True)
            ok.append(label)
            continue
        try:
            convert_one(
                f,
                out_dir,
                sharepoint_base=sharepoint_base,
                sharepoint_query=sharepoint_query,
                memory_name=memory_name,
                logical_rel=logical_rel,
            )
            kb = out_md.stat().st_size // 1024
            safe_print(f"OK  ({kb} KB)", flush=True)
            ok.append(label)
        except (Exception, BaseException) as e:
            reason = f"{type(e).__name__}: {e}" if str(e) else type(e).__name__
            safe_print(f"FAIL  {reason}", flush=True)
            safe_print(f"    >>> CONVERSION FAILED (file {i}/{len(files)}): {label}", flush=True)
            fail.append((label, reason))

    safe_print("Syncing standalone .md files into markdown mirror...")
    _sync_markdown_files_from_source(src_full, update=update, force=force)

    if update:
        data = load_json(manifest_path, {"version": 1, "scopes": {}})
        data.setdefault("scopes", {})[scope_key] = {k: expected[k] for k in sorted(expected)}
        data["version"] = 1
        save_json(manifest_path, data)

    _print_memory_mode_summary(len(files), ok, fail)


def _print_memory_mode_summary(
    files_in_scan: int,
    ok: list[str],
    fail: list[tuple[str, str]],
) -> None:
    """Clear end-of-run summary: only FAIL entries are real conversion failures."""
    bar = "=" * 76
    n_ok = len(ok)
    n_fail = len(fail)
    n_processed = n_ok + n_fail
    safe_print(f"\n{bar}")
    safe_print("PIPELINE SUMMARY (convert_to_markdown)")
    safe_print(f"  Files matching scan: {files_in_scan}")
    safe_print(f"  Files processed this run: {n_processed}")
    safe_print(f"  Succeeded (OK or SKIP): {n_ok}")
    safe_print(f"  Failed (exception during convert): {n_fail}")
    if n_fail == 0:
        safe_print(
            "  No files failed. If an older log showed hundreds of 'FontBBox' lines, "
            "those were pdfminer warnings, not failed files."
        )
    else:
        safe_print("  Failed files — these are the only paths that did not convert:")
        for path, reason in fail:
            safe_print(f"    - {path}")
            safe_print(f"      {reason}")
    safe_print(bar + "\n")


def _main_impl():
    file_idx = next((i for i, a in enumerate(sys.argv) if a == "--file"), None)
    if file_idx is not None and file_idx + 1 < len(sys.argv):
        _run_file_mode(sys.argv[file_idx + 1])
        return

    memory_idx = next((i for i, a in enumerate(sys.argv) if a == "--memory"), None)
    if memory_idx is not None and memory_idx + 1 < len(sys.argv):
        sb_idx = next((i for i, a in enumerate(sys.argv) if a == "--sharepoint-base"), None)
        sq_idx = next((i for i, a in enumerate(sys.argv) if a == "--sharepoint-query"), None)
        f_idx = next((i for i, a in enumerate(sys.argv) if a == "--folders"), None)
        mn_idx = next((i for i, a in enumerate(sys.argv) if a == "--memory-name"), None)
        sb = sys.argv[sb_idx + 1] if sb_idx is not None and sb_idx + 1 < len(sys.argv) else None
        sq = sys.argv[sq_idx + 1] if sq_idx is not None and sq_idx + 1 < len(sys.argv) else None
        mn = sys.argv[mn_idx + 1] if mn_idx is not None and mn_idx + 1 < len(sys.argv) else None
        folders = []
        if f_idx is not None and f_idx + 1 < len(sys.argv):
            j = f_idx + 1
            while j < len(sys.argv) and not sys.argv[j].startswith("--"):
                folders.append(sys.argv[j])
                j += 1
        rl_idx = next((i for i, a in enumerate(sys.argv) if a == "--resume-from-log"), None)
        resume_log: Path | None = None
        if rl_idx is not None and rl_idx + 1 < len(sys.argv):
            resume_log = Path(sys.argv[rl_idx + 1])
        _run_memory_mode(
            sys.argv[memory_idx + 1],
            sharepoint_base=sb,
            sharepoint_query=sq,
            subfolders=folders or None,
            memory_name_override=mn,
            resume_from_log=resume_log,
            update="--update" in sys.argv,
            force="--force" in sys.argv,
        )
        return

    print("Usage:")
    print("  python convert_to_markdown.py --file <file_path>")
    print("  python convert_to_markdown.py --memory <source_path>")
    print("  python convert_to_markdown.py --memory <source_path> --sharepoint-base <url> [--sharepoint-query <query>]")
    print("  python convert_to_markdown.py --memory <source_path> --folders <sub1> <sub2> ...")
    print("  python convert_to_markdown.py --memory <source_path> --resume-from-log <path-to-convert.log>")
    print("  python convert_to_markdown.py --memory <source_path> --update [--force]")
    print("  [...] [--log-file <path>]   # tee stdout/stderr; one log file per pipeline stage")


def main():
    configure_stdio_utf8()
    log_path = get_optional_log_file()
    if log_path:
        with pipeline_log_session(log_path, "convert_to_markdown", sys.argv):
            _main_impl()
    else:
        _main_impl()


if __name__ == "__main__":
    main()

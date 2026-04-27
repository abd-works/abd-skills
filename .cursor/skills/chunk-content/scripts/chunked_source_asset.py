"""
Chunked ``Source:`` path → ``data/assets/<topic>/.../<stem>.<binary>``.

- Strips ``data/assets/abd-answers-memory-pipeline/markdown/`` so the path names the **asset**
  tree under ``data/assets/``, not the pipeline markdown mirror.
- Replaces trailing ``.md`` with the original binary extension (URL filename, then on-disk
  sibling in the topic folder or beside the pipeline ``.md``).
- Does **not** change SharePoint URLs; ``repair_source_comments`` skips URL refresh for chunked.

Preserves ``, slide N`` / ``, section N``.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

_CHUNK_LOC_SUFFIX = re.compile(r",\s*(slide|section)\s+(\d+)\s*$", re.IGNORECASE)

_PIPELINE_MD_PREFIX = "data/assets/abd-answers-memory-pipeline/markdown/"

_BINARY_EXTENSIONS: tuple[str, ...] = (
    ".pptx",
    ".ppt",
    ".ppsx",
    ".pdf",
    ".docx",
    ".doc",
    ".xlsx",
    ".xls",
)


def _split_chunk_location(path_part: str) -> tuple[str, str | None]:
    s = path_part.strip()
    m = _CHUNK_LOC_SUFFIX.search(s)
    if not m:
        return s, None
    base = s[: m.start()].strip()
    loc = f", {m.group(1).lower()} {m.group(2)}"
    return base, loc


def _normalize_path_part(p: str) -> str:
    s = p.strip().replace("\\", "/")
    if s.startswith("source/"):
        return "data/assets/" + s[len("source/") :]
    if s.startswith("data/assets/"):
        return s
    if s.startswith("abd-answers-memory-pipeline/"):
        return "data/assets/" + s
    return s


def _extension_from_url(url: str) -> str | None:
    if not (url and url.strip()):
        return None
    path = urlparse(url.strip()).path
    if not path:
        return None
    name = unquote(path.split("/")[-1].split("?")[0])
    if not name or "." not in name:
        return None
    suf = Path(name).suffix.lower()
    return suf if suf in _BINARY_EXTENSIONS else None


def _topic_rel_under_assets(base: str) -> str:
    """``06 .../file.md`` under ``data/assets/`` (drops pipeline ``markdown/`` prefix when present)."""
    b = _normalize_path_part(base)
    if b.startswith(_PIPELINE_MD_PREFIX):
        return b[len(_PIPELINE_MD_PREFIX) :]
    if b.startswith("data/assets/"):
        return b[len("data/assets/") :]
    return b


def _extension_from_disk(assets_root: Path, topic_parent: Path, stem: str) -> str | None:
    """Topic folder first, then beside pipeline markdown mirror for same stem."""
    for base in (
        assets_root / topic_parent,
        assets_root / "abd-answers-memory-pipeline" / "markdown" / topic_parent,
    ):
        if not base.is_dir():
            continue
        for ext in _BINARY_EXTENSIONS:
            cand = base / f"{stem}{ext}"
            if cand.is_file():
                return ext
    return None


def chunked_source_path_to_asset_binary(
    path_part: str,
    url_part: str,
    *,
    assets_root: Path | None = None,
) -> str:
    """
    If the path ends in ``.md``, map to ``data/assets/<topic>/.../<stem>.<binary>`` (strip
    pipeline ``markdown/`` segment). Otherwise return ``path_part`` unchanged.
    """
    if assets_root is None:
        from _config import ASSETS

        assets_root = ASSETS

    base, loc = _split_chunk_location(path_part)
    base = _normalize_path_part(base)
    if not base.startswith("data/assets/") or not base.lower().endswith(".md"):
        return path_part

    rel = _topic_rel_under_assets(base)
    p = Path(rel)
    stem = p.stem
    parent = p.parent

    ext = _extension_from_url(url_part)
    if ext is None:
        ext = _extension_from_disk(assets_root, parent, stem)
    if ext is None:
        ext = ".md"

    if parent.as_posix() in ("", "."):
        asset_rel = Path(f"{stem}{ext}")
    else:
        asset_rel = parent / f"{stem}{ext}"

    out = f"data/assets/{asset_rel.as_posix()}" + (loc or "")
    return out


__all__ = ["chunked_source_path_to_asset_binary"]

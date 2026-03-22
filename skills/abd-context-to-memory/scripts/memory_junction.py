"""
Create junctions after ingest.

**Named hub junction (primary):** Under the **local** hub root, links live in
``<hub>/<junctions_dir>/<source_folder_name>`` → ``<absolute path to source>/memory``.
``junctions_dir`` comes from ``content_memory_roots.json`` (default ``assets``) or
``CONTENT_MEMORY_JUNCTIONS_DIR``. That directory holds **only junctions** (plus README);
it is **not** the SharePoint ``Assets`` library. Chunked markdown and aggregate ``.rag``
are configured per hub (usually on SharePoint).

**Legacy:** `ensure_memory_junction` / `junction_link_path` — older layouts (optional).

Skip with env SKIP_MEMORY_JUNCTION=1 or --no-junction on index_memory.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from _config import junctions_dir_for_root

_WIN_INVALID = re.compile(r'[<>:"/\\|?*]')


def _safe_segment(name: str) -> str:
    s = _WIN_INVALID.sub("_", name).strip(" .")
    return s or "memory_link"


def ensure_named_source_junction(
    hub_root: Path,
    *,
    source_folder: Path,
    memory_dir: Path,
) -> bool:
    """
    Create ``hub_root/<junctions_dir>/<source_folder.name>`` -> memory_dir (junction/symlink).

    The junction parent is **local only**; targets are usually remote ``…/<topic>/memory`` trees.
    """
    if os.environ.get("SKIP_MEMORY_JUNCTION", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        return False
    hub = hub_root.resolve()
    target = memory_dir.resolve()
    if not target.is_dir():
        print(
            f"[junction] Skip: memory folder missing: {target}",
            file=sys.stderr,
        )
        return False
    name = _safe_segment(source_folder.name)
    jd = junctions_dir_for_root(hub)
    junction_parent = hub / jd
    link_path = (junction_parent / name).resolve()
    try:
        junction_parent.mkdir(parents=True, exist_ok=True)
        _create_junction(link_path, target)
        print(f"[junction] {link_path} -> {target}")
        return True
    except Exception as e:
        print(f"[junction] Failed: {e}", file=sys.stderr)
        return False


def _create_junction(link_path: Path, target: Path) -> None:
    if link_path.exists() or link_path.is_symlink():
        if link_path.is_dir():
            try:
                link_path.rmdir()
            except OSError as e:
                raise RuntimeError(
                    f"Cannot replace {link_path}: not an empty dir/junction ({e})"
                ) from e
        else:
            link_path.unlink()
    if not target.is_dir():
        raise RuntimeError(f"Junction target must exist and be a directory: {target}")
    if sys.platform == "win32":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link_path), str(target)],
            check=True,
        )
    else:
        link_path.symlink_to(target, target_is_directory=True)


def junction_link_path(workspace: Path, content_root: Path) -> Path:
    """Compute where the junction should live under workspace (legacy helper)."""
    ws = workspace.resolve()
    jd = junctions_dir_for_root(ws)
    parts = content_root.resolve().parts
    assets_idx = None
    for i, p in enumerate(parts):
        if p.casefold() == "assets":
            assets_idx = i
            break
    if assets_idx is not None:
        rel = parts[assets_idx + 1 :]
        sub = Path(*rel) if rel else Path("_memory")
        return (ws / jd / sub).resolve()
    leaf = _safe_segment(content_root.name)
    return (ws / f"chunked_{leaf}").resolve()


def ensure_memory_junction(
    content_root: Path,
    *,
    workspace: Path | None = None,
) -> bool:
    """
    Ensure workspace has a junction pointing at content_root/memory.
    Returns True on success; False on skip or failure (non-fatal).
    """
    if os.environ.get("SKIP_MEMORY_JUNCTION", "").strip().lower() in (
        "1",
        "true",
        "yes",
    ):
        return False
    ws = (workspace or Path.cwd()).resolve()
    memory_target = (content_root / "memory").resolve()
    if not memory_target.is_dir():
        print(
            f"[junction] Skip: memory folder missing: {memory_target}",
            file=sys.stderr,
        )
        return False
    link_path = junction_link_path(ws, content_root)
    try:
        link_path.parent.mkdir(parents=True, exist_ok=True)
        _create_junction(link_path, memory_target)
        print(f"[junction] {link_path} -> {memory_target}")
        return True
    except Exception as e:
        print(f"[junction] Failed: {e}", file=sys.stderr)
        return False

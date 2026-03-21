"""
Create junctions after ingest.

**Named hub junction (primary):** Under the memory hub root (e.g. abd_content),
`<hub>/<source_folder_name>` → `<absolute path to source>/memory` (chunked markdown).
Name matches the last segment of the source folder; invalid path characters are sanitized.

**Legacy:** `ensure_memory_junction` / `junction_link_path` — assets/... or chunked_* layout
(optional; not used by default index_memory flow).

Skip with env SKIP_MEMORY_JUNCTION=1 or --no-junction on index_memory.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

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
    Create hub_root/<source_folder.name> -> memory_dir (junction/symlink).
    source_folder is the memory source path passed to --path (used for the link name only).
    memory_dir is the actual chunked output folder (usually source_folder / "memory").
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
    link_path = (hub / name).resolve()
    try:
        hub.mkdir(parents=True, exist_ok=True)
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
    """Compute where the junction should live under workspace."""
    parts = content_root.resolve().parts
    assets_idx = None
    for i, p in enumerate(parts):
        if p.casefold() == "assets":
            assets_idx = i
            break
    if assets_idx is not None:
        rel = parts[assets_idx + 1 :]
        sub = Path(*rel) if rel else Path("_memory")
        return (workspace / "assets" / sub).resolve()
    leaf = _safe_segment(content_root.name)
    return (workspace / f"chunked_{leaf}").resolve()


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

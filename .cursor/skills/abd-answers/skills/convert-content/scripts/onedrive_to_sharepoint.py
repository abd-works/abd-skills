#!/usr/bin/env python3
"""
Resolve OneDrive path to SharePoint base URL for shareable links.

Fork of abd-context-to-memory ``onedrive_to_sharepoint.py``.
Config: ``sharepoint_mapping.json`` in this directory (``scripts/source-convert/``).
"""

import json
from pathlib import Path
from urllib.parse import quote

_SCRIPTS_DIR = Path(__file__).resolve().parent
CONFIG_PATH = _SCRIPTS_DIR / "sharepoint_mapping.json"


def _load_mappings() -> list[tuple[str, str, str]]:
    if not CONFIG_PATH.exists():
        return []
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        out = []
        for m in data.get("mappings", []):
            prefix = m.get("onedrive_prefix", "").strip()
            base = m.get("sharepoint_base", "").strip().rstrip("/")
            query = m.get("sharepoint_query", "csf=1&web=1")
            if prefix and base:
                out.append((prefix, base, query))
        return out
    except (json.JSONDecodeError, OSError):
        return []


def _load_mapping_dicts() -> list[dict]:
    if not CONFIG_PATH.exists():
        return []
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return [x for x in data.get("mappings", []) if isinstance(x, dict)]
    except (json.JSONDecodeError, OSError):
        return []


def path_is_onedrive(file_path: Path) -> bool:
    path_str = str(file_path.resolve()).replace("\\", "/")
    return "onedrive" in path_str.lower()


def extract_onedrive_prefix(file_path: Path) -> str | None:
    path_str = str(file_path.resolve()).replace("\\", "/")
    idx = path_str.lower().find("onedrive")
    if idx < 0:
        return None
    rest = path_str[idx:]
    end = rest.find("/")
    if end > 0:
        return rest[:end]
    return rest


def get_sharepoint_base_for_path(file_path: Path) -> tuple[str | None, str]:
    path_str = str(file_path.resolve())
    path_str = path_str.replace("\\", "/")
    mappings = _load_mappings()
    for prefix, base, query in mappings:
        if prefix in path_str:
            return base, query
    return None, ""


def get_sharepoint_url_for_file(file_path: Path, sharepoint_base: str, query: str) -> str:
    path_str = str(file_path.resolve())
    path_str = path_str.replace("\\", "/")
    mappings = _load_mappings()
    for prefix, base, _ in mappings:
        if prefix in path_str:
            idx = path_str.find(prefix)
            after_prefix = path_str[idx + len(prefix) :].lstrip("/\\")
            if "Shared Documents" in after_prefix or "Shared%20Documents" in after_prefix:
                for sep in ("Shared Documents/", "Shared Documents\\", "Shared%20Documents/", "Shared%20Documents\\"):
                    if sep in after_prefix:
                        after_prefix = after_prefix.split(sep, 1)[-1]
                        break
            encoded = quote(after_prefix, safe="/")
            return f"{base.rstrip('/')}/{encoded}?{query}"
    return ""


def _rel_after_shared_documents(path_str: str, prefix: str) -> str | None:
    """Path under Assets (e.g. ``01 Agile Practices/.../file.pptx``) from a OneDrive path."""
    idx = path_str.find(prefix)
    if idx < 0:
        return None
    after_prefix = path_str[idx + len(prefix) :].lstrip("/\\")
    for sep in ("Shared Documents/", "Shared Documents\\", "Shared%20Documents/", "Shared%20Documents\\"):
        if sep in after_prefix:
            after_prefix = after_prefix.split(sep, 1)[-1]
            break
    return after_prefix.replace("\\", "/")


def get_sharepoint_open_doc_url_for_file(file_path: Path) -> str | None:
    """
    Office Web App open URL (``Doc.aspx`` on ``ABDInternal`` or similar) when configured.

    Prefer per-file ``file_open_urls`` in ``sharepoint_mapping.json`` (key = path under
    ``Assets/``, posix, e.g. ``01 Agile Practices/1) Kanban/Foo.pptx``). Otherwise, if
    ``open_doc_base`` is set on the matching mapping, build
    ``{open_doc_base}?file={encoded_name}&action=edit&mobileredirect=true`` (no ``sourcedoc`` —
    add per-file URLs to ``file_open_urls`` when Office requires a document id).
    """
    try:
        from _config import ASSETS

        rel_key = file_path.resolve().relative_to(ASSETS.resolve()).as_posix()
    except (ImportError, ValueError, OSError):
        rel_key = None

    path_str = str(file_path.resolve()).replace("\\", "/")

    for m in _load_mapping_dicts():
        prefix = m.get("onedrive_prefix", "").strip()
        file_urls = m.get("file_open_urls") if isinstance(m.get("file_open_urls"), dict) else {}
        open_base = m.get("open_doc_base", "").strip()

        keys: list[str] = []
        if rel_key:
            keys.append(rel_key)
        if prefix and prefix in path_str:
            after = _rel_after_shared_documents(path_str, prefix)
            if after:
                keys.append(after)

        for k in keys:
            hit = file_urls.get(k) or file_urls.get(file_path.name)
            if isinstance(hit, str) and hit.strip():
                return hit.strip()

        if open_base and keys:
            fn = quote(file_path.name, safe="")
            sep = "&" if "?" in open_base else "?"
            return f"{open_base.rstrip('/')}{sep}file={fn}&action=edit&mobileredirect=true"
    return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python onedrive_to_sharepoint.py <file_path>")
        sys.exit(0)
    p = Path(sys.argv[1])
    base, query = get_sharepoint_base_for_path(p)
    if base:
        url = get_sharepoint_url_for_file(p, base, query)
        print(f"SharePoint base: {base}")
        print(f"Full URL: {url}")
    else:
        print("No mapping for this path. Add to sharepoint_mapping.json")

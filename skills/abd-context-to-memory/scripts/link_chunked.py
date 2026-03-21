#!/usr/bin/env python3
"""Create the chunked junction under a root. Uses memory_path from roots.json if not given.

Usage:
  python link_chunked.py --root <name> [--memory-path <path>] [--workspace <dir>]
"""

import json
import sys
from pathlib import Path

ROOTS_DIR = Path("roots")
MANIFEST = ROOTS_DIR / "roots.json"
CHUNKED_NAME = "chunked"


def get_workspace(workspace_arg: str | None) -> Path:
    if workspace_arg:
        return Path(workspace_arg).resolve()
    return Path.cwd()


def main() -> int:
    args = sys.argv[1:]
    root_idx = next((i for i, a in enumerate(args) if a == "--root"), None)
    path_idx = next((i for i, a in enumerate(args) if a == "--memory-path"), None)
    ws_idx = next((i for i, a in enumerate(args) if a == "--workspace"), None)

    if root_idx is None or root_idx + 1 >= len(args):
        print("Usage: python link_chunked.py --root <name> [--memory-path <path>] [--workspace <dir>]", file=sys.stderr)
        return 1

    name = args[root_idx + 1].strip()
    memory_path_arg = args[path_idx + 1].strip() if path_idx is not None and path_idx + 1 < len(args) else None
    workspace = args[ws_idx + 1] if ws_idx is not None and ws_idx + 1 < len(args) else None

    root_dir = get_workspace(workspace)
    roots_dir = root_dir / ROOTS_DIR
    manifest_path = root_dir / MANIFEST

    if memory_path_arg:
        target = Path(memory_path_arg).resolve()
    else:
        if not manifest_path.exists():
            print(f"No roots list at {manifest_path}. Use --memory-path or add the root first.", file=sys.stderr)
            return 1
        with open(manifest_path, encoding="utf-8") as f:
            data = json.load(f)
        roots = data.get("roots", [])
        entry = next((r for r in roots if r.get("name") == name), None)
        if not entry:
            print(f"Root '{name}' not in {manifest_path}. Add it first or pass --memory-path.", file=sys.stderr)
            return 1
        mp = entry.get("memory_path") or ""
        if not mp:
            print(f"Root '{name}' has no memory_path. Pass --memory-path or edit roots.json.", file=sys.stderr)
            return 1
        target = Path(mp).expanduser().resolve()

    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 1

    root_folder = roots_dir / name
    root_folder.mkdir(parents=True, exist_ok=True)
    link_path = root_folder / CHUNKED_NAME

    try:
        if link_path.exists():
            if link_path.is_dir():
                link_path.rmdir()
            else:
                link_path.unlink()
        if sys.platform == "win32":
            import subprocess
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link_path), str(target)], check=True)
        else:
            link_path.symlink_to(target)
        print(f"Junction: {link_path} -> {target}")
        return 0
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

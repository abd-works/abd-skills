#!/usr/bin/env python3
"""Add a new root: create roots/<name>/ and register it in roots/roots.json.

Usage:
  python add_root.py --name <name> [--memory-path <path>] [--workspace <dir>]

If --memory-path is given, also creates the chunked junction (calls link_chunked logic).
Run from workspace root, or pass --workspace.
"""

import json
import sys
from pathlib import Path

ROOTS_DIR = Path("roots")
MANIFEST = ROOTS_DIR / "roots.json"


def get_workspace(workspace_arg: str | None) -> Path:
    if workspace_arg:
        return Path(workspace_arg).resolve()
    return Path.cwd()


def ensure_manifest(roots_path: Path) -> list:
    if roots_path.exists():
        with open(roots_path, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("roots", [])
    roots_path.parent.mkdir(parents=True, exist_ok=True)
    return []


def main() -> int:
    args = sys.argv[1:]
    name_idx = next((i for i, a in enumerate(args) if a == "--name"), None)
    path_idx = next((i for i, a in enumerate(args) if a == "--memory-path"), None)
    ws_idx = next((i for i, a in enumerate(args) if a == "--workspace"), None)

    if name_idx is None or name_idx + 1 >= len(args):
        print("Usage: python add_root.py --name <name> [--memory-path <path>] [--workspace <dir>]", file=sys.stderr)
        return 1

    name = args[name_idx + 1].strip().lower().replace(" ", "_")
    memory_path = args[path_idx + 1].strip() if path_idx is not None and path_idx + 1 < len(args) else ""
    workspace = args[ws_idx + 1] if ws_idx is not None and ws_idx + 1 < len(args) else None

    root_dir = get_workspace(workspace)
    roots_dir = root_dir / ROOTS_DIR
    manifest_path = root_dir / MANIFEST

    roots = ensure_manifest(manifest_path)
    if any(r.get("name") == name for r in roots):
        print(f"Root '{name}' already exists in {manifest_path}", file=sys.stderr)
        return 1

    root_folder = roots_dir / name
    root_folder.mkdir(parents=True, exist_ok=True)

    roots.append({
        "name": name,
        "memory_path": memory_path,
        "chunked_junction": "chunked",
    })
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"roots": roots}, f, indent=2)

    print(f"Added root '{name}' at {root_folder}")
    print(f"Updated {manifest_path}")

    if memory_path:
        # Create junction
        link_path = root_folder / "chunked"
        target = Path(memory_path).resolve()
        if not target.exists():
            print(f"Warning: memory path does not exist yet: {target}", file=sys.stderr)
        else:
            try:
                _create_junction(link_path, target)
                print(f"Junction created: {link_path} -> {target}")
            except Exception as e:
                print(f"Could not create junction: {e}", file=sys.stderr)

    return 0


def _create_junction(link_path: Path, target: Path) -> None:
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


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Set or get the active skill workspace for abd-diagrams.

Usage:
  python set_workspace.py              -- prints active_skill_workspace from skill-config.json
  python set_workspace.py <path>       -- sets active_skill_workspace to <path> in skill-config.json

The skill-config.json file is stored at the skill package root (same directory as SKILL.md).
Paths are resolved and stored relative to skill_path when possible (to keep them portable),
otherwise as absolute paths.
"""

import json
import os
import sys
from pathlib import Path


def get_skill_path():
    """Return the skill package root (where SKILL.md and skill-config.json live)."""
    return Path(__file__).resolve().parent.parent.parent


def get_config_path():
    """Return the path to skill-config.json."""
    return get_skill_path() / "skill-config.json"


def load_config():
    """Load skill-config.json, or return default if missing."""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {
        "active_skill_workspace": ".",
        "known_skill_workspaces": []
    }


def save_config(config):
    """Save config to skill-config.json."""
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def resolve_path(path_str):
    """
    Resolve a path to absolute, then determine if it should be stored as relative or absolute.
    Returns the path to store in skill-config.json.
    """
    # Resolve to absolute path
    abs_path = Path(path_str).resolve()

    # Verify the directory exists
    if not abs_path.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {abs_path}")

    # Try to make it relative to skill_path for portability
    skill_path = get_skill_path()
    try:
        rel_path = abs_path.relative_to(skill_path)
        # If it's a simple relative path, return it
        if len(rel_path.parts) < 5:  # heuristic: keep it relative if not too deep
            return str(rel_path)
    except ValueError:
        # Can't make relative, use absolute
        pass

    return str(abs_path)


def main():
    """Main entry point."""
    skill_path = get_skill_path()
    config = load_config()

    if len(sys.argv) == 1:
        # Print current workspace
        active = config.get("active_skill_workspace", "(not set)")
        if active == ".":
            # Resolve "." to absolute for display
            active_abs = skill_path
        else:
            # Resolve relative to skill_path
            active_abs = skill_path / active if not Path(active).is_absolute() else Path(active)

        print(f"Active skill workspace: {active}")
        print(f"Resolved to: {active_abs.resolve()}")
        return 0

    elif len(sys.argv) == 2:
        # Set workspace
        new_workspace = sys.argv[1]
        try:
            resolved = resolve_path(new_workspace)
            config["active_skill_workspace"] = resolved
            save_config(config)
            print(f"Set active_skill_workspace to: {resolved}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    else:
        print("Usage: python set_workspace.py [<path>]", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Deploy the kanban package — thin wrapper around deploy_family_package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from deploy_family_package import deploy_family_package  # noqa: E402

DEFAULT_SOURCE = REPO_ROOT / "kanban"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Deploy the kanban/ family package into an engagement workspace.",
    )
    ap.add_argument("--to", required=True, type=Path, dest="workspace")
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--no-sync-source", action="store_true", help="No-op (compatibility)")
    ap.add_argument("--skip-ide", action="store_true")
    ap.add_argument(
        "--ide",
        choices=("cursor", "vscode", "github", "both"),
        default="cursor",
    )
    ns = ap.parse_args()
    return deploy_family_package(
        ns.workspace,
        ns.source,
        ide=ns.ide if ns.ide != "github" else "vscode",
        skip_ide=ns.skip_ide,
        remove_legacy=True,
    )


if __name__ == "__main__":
    raise SystemExit(main())

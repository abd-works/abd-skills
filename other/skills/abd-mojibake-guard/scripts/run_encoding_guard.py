#!/usr/bin/env python3
"""Run abd-skills encoding guard scripts from any cwd inside the repo."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _repo_root import abd_skills_repo_root


def _run_scanner(repo: Path, extra_args: list[str]) -> int:
    cmd = [sys.executable, str(repo / "scripts" / "scan_encoding.py"), *extra_args]
    return subprocess.call(cmd, cwd=repo)


def _run_deploy(repo: Path, mode: str, targets: list[str]) -> int:
    deploy = repo / "scripts" / "deploy-mojibake-guard.sh"
    if not deploy.is_file():
        print(f"Missing {deploy}", file=sys.stderr)
        return 1
    cmd = ["bash", str(deploy), mode, *targets]
    return subprocess.call(cmd, cwd=repo)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan, fix, or install mojibake guards (abd-mojibake-guard skill)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scan", help="Report encoding issues in tracked text files")
    fix_p = sub.add_parser("fix", help="Auto-fix mojibake, U+FFFD, and BOM in place")
    fix_p.add_argument(
        "--bom-only",
        action="store_true",
        help="Strip UTF-8 BOM only (passes --fix-bom to scan_encoding.py)",
    )
    sub.add_parser("check-staged", help="Fail if staged files have encoding issues (pre-commit)")
    install_p = sub.add_parser(
        "install-guard",
        help="Deploy CI workflow and/or pre-commit hook via deploy-mojibake-guard.sh",
    )
    install_p.add_argument(
        "--mode",
        choices=("all", "ci", "local"),
        default="all",
        help="Deploy CI workflow, local hook, or both (default: all)",
    )
    install_p.add_argument(
        "repo_roots",
        nargs="*",
        help="Git repo roots to guard (default: abd-skills repo only)",
    )

    args = parser.parse_args()
    repo = abd_skills_repo_root()

    if args.command == "scan":
        return _run_scanner(repo, [])
    if args.command == "fix":
        flag = "--fix-bom" if args.bom_only else "--fix"
        return _run_scanner(repo, [flag])
    if args.command == "check-staged":
        return _run_scanner(repo, ["--staged", "--check"])

    mode_flag = {"all": "--all", "ci": "--ci", "local": "--local"}[args.mode]
    targets = args.repo_roots or [str(repo)]
    return _run_deploy(repo, mode_flag, targets)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Git operations tool for delivery engagements.

Usage:
    python git_ops.py status  --workspace <path>
    python git_ops.py branch  --workspace <path> --name delivery/run-01
    python git_ops.py commit  --workspace <path> --message "slot-01: ..."
    python git_ops.py push    --workspace <path>
    python git_ops.py pr      --workspace <path> --title "Run 01" --base main
"""
import argparse, subprocess, sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def cmd_status(ws: Path) -> None:
    branch = run(["git", "branch", "--show-current"], ws)
    status = run(["git", "status", "--short"], ws)
    print(f"Branch : {branch}")
    print(f"Changes:\n{status or '  (clean)'}")


def cmd_branch(ws: Path, name: str) -> None:
    existing = run(["git", "branch", "--list", name], ws)
    if existing:
        run(["git", "checkout", name], ws)
        print(f"Switched to existing branch: {name}")
    else:
        run(["git", "checkout", "-b", name], ws)
        print(f"Created and switched to: {name}")


def cmd_commit(ws: Path, message: str) -> None:
    run(["git", "add", "-A"], ws)
    staged = run(["git", "diff", "--cached", "--name-only"], ws)
    if not staged:
        print("Nothing to commit.")
        return
    sha = run(["git", "commit", "-m", message], ws)
    short = run(["git", "rev-parse", "--short", "HEAD"], ws)
    print(f"Committed {short}: {message}")


def cmd_push(ws: Path) -> None:
    branch = run(["git", "branch", "--show-current"], ws)
    run(["git", "push", "--set-upstream", "origin", branch], ws)
    print(f"Pushed: {branch}")


def cmd_pr(ws: Path, title: str, base: str) -> None:
    try:
        result = subprocess.run(
            ["gh", "pr", "create", "--title", title, "--base", base, "--fill"],
            cwd=str(ws), capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"PR created: {result.stdout.strip()}")
        else:
            print(f"PR failed: {result.stderr.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print("gh CLI not found — create the PR manually.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["status", "branch", "commit", "push", "pr"])
    p.add_argument("--workspace", required=True)
    p.add_argument("--name", help="Branch name (for 'branch' command)")
    p.add_argument("--message", help="Commit message (for 'commit' command)")
    p.add_argument("--title", help="PR title (for 'pr' command)")
    p.add_argument("--base", default="main", help="Base branch for PR")
    args = p.parse_args()

    ws = Path(args.workspace)
    if not ws.exists():
        sys.exit(f"Workspace not found: {ws}")

    if args.command == "status":
        cmd_status(ws)
    elif args.command == "branch":
        if not args.name:
            sys.exit("--name required for 'branch' command")
        cmd_branch(ws, args.name)
    elif args.command == "commit":
        if not args.message:
            sys.exit("--message required for 'commit' command")
        cmd_commit(ws, args.message)
    elif args.command == "push":
        cmd_push(ws)
    elif args.command == "pr":
        if not args.title:
            sys.exit("--title required for 'pr' command")
        cmd_pr(ws, args.title, args.base)


if __name__ == "__main__":
    main()

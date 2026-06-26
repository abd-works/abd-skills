#!/usr/bin/env python3
"""
generate_manifest.py — Generate a deploy manifest for the skills repo.

The manifest records the source commit, timestamp, and a file inventory
with content hashes for every deployable file.

Usage:
    python3 scripts/generate_manifest.py                    # print manifest to stdout
    python3 scripts/generate_manifest.py -o manifest.json   # write to file
    python3 scripts/generate_manifest.py --deployed /path   # read deployed receipt
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "node_modules", "catalog", "retired", "temp-drawio", "tests"}

# File extensions that get deployed
DEPLOYABLE_EXTS = {
    ".md", ".mdc", ".json", ".py", ".sh", ".ps1", ".drawio", ".html", ".css", ".js", ".ts"
}


def get_version():
    """Read version from VERSION file."""
    version_file = os.path.join(REPO_ROOT, "VERSION")
    try:
        with open(version_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def get_commit_hash():
    """Get short commit hash of HEAD."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def get_commit_date():
    """Get ISO date of HEAD commit."""
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "HEAD"],
            cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def file_hash(path):
    """SHA-256 of file content, truncated to 16 chars."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def collect_packages():
    """Collect all package roots and their deployable files."""
    packages = {}

    for top in ("practices", "foundational", "stages"):
        top_path = os.path.join(REPO_ROOT, top)
        if not os.path.isdir(top_path):
            continue
        for entry in sorted(os.listdir(top_path)):
            pkg_path = os.path.join(top_path, entry)
            if not os.path.isdir(pkg_path):
                continue
            name = f"{top}/{entry}"
            files = collect_files(pkg_path)
            if files:
                packages[name] = files

    for flat in ("utilities", "others"):
        flat_path = os.path.join(REPO_ROOT, flat)
        if os.path.isdir(flat_path):
            files = collect_files(flat_path)
            if files:
                packages[flat] = files

    return packages


def collect_files(pkg_root):
    """Collect deployable files in a package, returning {relative_path: hash}."""
    files = {}
    for dirpath, dirnames, filenames in os.walk(pkg_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1]
            if ext not in DEPLOYABLE_EXTS:
                continue
            abs_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(abs_path, pkg_root)
            files[rel_path] = file_hash(abs_path)
    return files


def generate_manifest():
    """Generate the full manifest dict."""
    return {
        "version": 1,
        "repoVersion": get_version(),
        "commit": get_commit_hash(),
        "commitDate": get_commit_date(),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "packages": collect_packages(),
    }


def read_deployed_receipt(path):
    """Read a deployed receipt from a target workspace."""
    receipt_path = os.path.join(path, ".abd-deploy.json")
    if not os.path.isfile(receipt_path):
        return None
    with open(receipt_path, "r") as f:
        return json.load(f)


def compute_delta(source_manifest, deployed_receipt):
    """Compare source manifest with deployed receipt. Returns delta report."""
    if not deployed_receipt:
        return {"status": "fresh", "message": "No previous deploy found — full deploy."}

    src_commit = source_manifest["commit"]
    dst_commit = deployed_receipt.get("commit", "unknown")
    src_version = source_manifest.get("repoVersion", "unknown")
    dst_version = deployed_receipt.get("repoVersion", "unknown")

    if src_commit == dst_commit:
        return {
            "status": "current",
            "message": f"Already up to date at v{src_version} ({src_commit}).",
            "lastDeploy": deployed_receipt.get("deployedAt", "unknown"),
            "lastIde": deployed_receipt.get("ide", "unknown"),
            "version": src_version,
        }

    # File-level diff
    src_packages = source_manifest.get("packages", {})
    dst_packages = deployed_receipt.get("packages", {})

    changes = {"added": [], "modified": [], "deleted": []}

    all_pkg_names = set(src_packages.keys()) | set(dst_packages.keys())

    for pkg in sorted(all_pkg_names):
        src_files = src_packages.get(pkg, {})
        dst_files = dst_packages.get(pkg, {})

        if pkg not in dst_packages:
            changes["added"].extend(f"{pkg}/{f}" for f in sorted(src_files))
            continue
        if pkg not in src_packages:
            changes["deleted"].extend(f"{pkg}/{f}" for f in sorted(dst_files))
            continue

        all_files = set(src_files.keys()) | set(dst_files.keys())
        for f in sorted(all_files):
            full = f"{pkg}/{f}"
            if f not in dst_files:
                changes["added"].append(full)
            elif f not in src_files:
                changes["deleted"].append(full)
            elif src_files[f] != dst_files[f]:
                changes["modified"].append(full)

    total = sum(len(v) for v in changes.values())
    return {
        "status": "outdated",
        "message": f"Source v{src_version} ({src_commit}), deployed v{dst_version} ({dst_commit}). {total} file(s) changed.",
        "lastDeploy": deployed_receipt.get("deployedAt", "unknown"),
        "lastIde": deployed_receipt.get("ide", "unknown"),
        "version": src_version,
        "changes": changes,
    }


def write_deploy_receipt(deploy_root, ide, manifest):
    """Write a deploy receipt to the target workspace."""
    receipt = {
        "version": 1,
        "ide": ide,
        "repoVersion": manifest["repoVersion"],
        "commit": manifest["commit"],
        "commitDate": manifest["commitDate"],
        "deployedAt": datetime.now(timezone.utc).isoformat(),
        "packages": manifest["packages"],
    }
    receipt_path = os.path.join(deploy_root, ".abd-deploy.json")
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    return receipt_path


def main():
    parser = argparse.ArgumentParser(description="Generate skills deploy manifest")
    parser.add_argument("-o", "--output", help="Write manifest to file")
    parser.add_argument("--deployed", help="Read deployed receipt from path and show delta")
    parser.add_argument("--write-receipt", help="Write deploy receipt to target path")
    parser.add_argument("--ide", default="cursor", help="IDE for deploy receipt (cursor or vscode)")
    args = parser.parse_args()

    manifest = generate_manifest()

    if args.deployed:
        receipt = read_deployed_receipt(args.deployed)
        delta = compute_delta(manifest, receipt)
        print(json.dumps(delta, indent=2))
        if delta["status"] == "outdated":
            return 1
        return 0

    if args.write_receipt:
        path = write_deploy_receipt(args.write_receipt, args.ide, manifest)
        print(f"Deploy receipt written to {path}")
        return 0

    if args.output:
        with open(args.output, "w") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
        print(f"Manifest written to {args.output}")
    else:
        print(json.dumps(manifest, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())

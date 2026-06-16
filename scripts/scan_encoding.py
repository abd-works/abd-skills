#!/usr/bin/env python3
"""
scan_encoding.py — Guard against mojibake, U+FFFD replacement characters,
and UTF-8 BOM in .md / .mdc files.

Usage:
    python3 scripts/scan_encoding.py              # report all issues
    python3 scripts/scan_encoding.py --check      # exit 1 if any issues found (for CI/hooks)
    python3 scripts/scan_encoding.py --fix-bom    # strip BOM from files in-place
    python3 scripts/scan_encoding.py --fix        # fix all: mojibake, U+FFFD, BOM
    python3 scripts/scan_encoding.py --staged     # only scan git staged files (for pre-commit)
"""

import os
import sys
import subprocess
from collections import Counter

# ── Mojibake patterns ──────────────────────────────────────────────────────
# These are the byte sequences that appear when UTF-8 text is misread as
# Windows-1252 or ISO-8859-1 and then re-encoded as UTF-8 (double-encoding).

MOJIBAKE = {
    # ---- Windows-1252 mojibake (UTF-8 → cp1252 → UTF-8) ----
    "\u00e2\u20ac\u2014": "\u2014 (em-dash)",
    "\u00e2\u20ac\u201c": "\u201c (left double quote)",
    "\u00e2\u20ac\u201d": "\u201d (right double quote)",
    "\u00e2\u20ac\u2018": "\u2018 (left single quote)",
    "\u00e2\u20ac\u2019": "\u2019 (right single quote)",
    "\u00e2\u20ac\u2013": "\u2013 (en-dash)",
    "\u00e2\u20ac\u2022": "\u2022 (bullet)",
    "\u00e2\u20ac\u2026": "\u2026 (ellipsis)",
    "\u00c2\u00a0": "\u00a0 (non-breaking space)",
    "\u00c2\u00ae": "\u00ae (registered)",
    "\u00c2\u00a9": "\u00a9 (copyright)",
    "\u00c2\u00ad": "\u00ad (soft hyphen)",
    # ---- Latin-1 mojibake (UTF-8 → ISO-8859-1 → UTF-8) ----
    "\u00e2\u0080\u0093": "\u2013 (en-dash)",
    "\u00e2\u0080\u0094": "\u2014 (em-dash)",
    "\u00e2\u0080\u0098": "\u2018 (left single quote)",
    "\u00e2\u0080\u0099": "\u2019 (right single quote)",
    "\u00e2\u0080\u009c": "\u201c (left double quote)",
    "\u00e2\u0080\u009d": "\u201d (right double quote)",
    "\u00e2\u0080\u00a2": "\u2022 (bullet)",
    "\u00e2\u0080\u00a6": "\u2026 (ellipsis)",
}

REPLACEMENT = "\ufffd"  # U+FFFD

# ── Helpers ────────────────────────────────────────────────────────────────

def staged_md_files():
    """Return list of .md/.mdc files currently staged in git."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            text=True,
        )
        return [
            f for f in out.strip().splitlines()
            if f.endswith(".md") or f.endswith(".mdc")
        ]
    except subprocess.CalledProcessError:
        return []


def walk_md_files(root="."):
    """Walk the repo and yield .md/.mdc paths, skipping .git and node_modules."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for f in filenames:
            if f.endswith(".md") or f.endswith(".mdc"):
                yield os.path.join(dirpath, f)


def is_binary_preview_line(line):
    """Return True if a line is a binary file preview (not a real encoding issue)."""
    binary_markers = ("IHDR", "[Content_Types]", "P!\ufffd", ".png)", ".docx)", ".xlsx)")
    return any(marker in line for marker in binary_markers)


def scan_file(path):
    """Return a list of (description, count) tuples for issues found in a file."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except Exception:
        return []

    issues = []

    # U+FFFD replacement character (skip binary preview lines)
    lines = content.split("\n")
    fffd_count = sum(
        line.count(REPLACEMENT)
        for line in lines
        if "\ufffd" in line and not is_binary_preview_line(line)
    )
    if fffd_count:
        issues.append(("U+FFFD replacement char", fffd_count))

    # Mojibake patterns
    for pattern, desc in MOJIBAKE.items():
        n = content.count(pattern)
        if n:
            issues.append(("mojibake " + desc, n))

    # UTF-8 BOM
    if content.startswith("\ufeff"):
        issues.append(("UTF-8 BOM", 1))

    return issues


# Map each mojibake pattern to its correct Unicode character
MOJIBAKE_FIX = {
    "\u00e2\u20ac\u2014": "\u2014",  # — em-dash
    "\u00e2\u20ac\u201c": "\u201c",  # " left double quote
    "\u00e2\u20ac\u201d": "\u201d",  # " right double quote
    "\u00e2\u20ac\u2018": "\u2018",  # ' left single quote
    "\u00e2\u20ac\u2019": "\u2019",  # ' right single quote
    "\u00e2\u20ac\u2013": "\u2013",  # – en-dash
    "\u00e2\u20ac\u2022": "\u2022",  # • bullet
    "\u00e2\u20ac\u2026": "\u2026",  # … ellipsis
    "\u00c2\u00a0": "\u00a0",        # non-breaking space
    "\u00c2\u00ae": "\u00ae",        # ® registered
    "\u00c2\u00a9": "\u00a9",        # © copyright
    "\u00c2\u00ad": "\u00ad",        # soft hyphen
    "\u00e2\u0080\u0093": "\u2013",  # – en-dash (latin1 variant)
    "\u00e2\u0080\u0094": "\u2014",  # — em-dash (latin1 variant)
    "\u00e2\u0080\u0098": "\u2018",  # ' left single quote (latin1)
    "\u00e2\u0080\u0099": "\u2019",  # ' right single quote (latin1)
    "\u00e2\u0080\u009c": "\u201c",  # " left double quote (latin1)
    "\u00e2\u0080\u009d": "\u201d",  # " right double quote (latin1)
    "\u00e2\u0080\u00a2": "\u2022",  # • bullet (latin1)
    "\u00e2\u0080\u00a6": "\u2026",  # … ellipsis (latin1)
}


def fix_mojibake(content):
    """Replace mojibake patterns with correct Unicode. Returns (new_content, count)."""
    total = 0
    for bad, good in MOJIBAKE_FIX.items():
        n = content.count(bad)
        if n:
            content = content.replace(bad, good)
            total += n
    return content, total


def fix_fffd(content, path):
    """Replace U+FFFD with em-dash in markdown content. Skips binary preview lines.
    Returns (new_content, count)."""
    lines = content.split("\n")
    fixed = 0
    new_lines = []
    for line in lines:
        if "\ufffd" not in line:
            new_lines.append(line)
            continue
        # Skip lines that look like binary file previews (IHDR, P!, Content_Types)
        if any(marker in line for marker in ("IHDR", "[Content_Types]", "P!\ufffd")):
            new_lines.append(line)
            continue
        # Replace U+FFFD with em-dash (the overwhelmingly common case)
        new_lines.append(line.replace("\ufffd", "\u2014"))
        fixed += line.count("\ufffd")
    return "\n".join(new_lines), fixed


def strip_bom(path):
    """Remove UTF-8 BOM from a file in-place. Returns True if modified."""
    with open(path, "rb") as fh:
        raw = fh.read(3)
    if raw != b"\xef\xbb\xbf":
        return False
    with open(path, "rb") as fh:
        data = fh.read()
    with open(path, "wb") as fh:
        fh.write(data[3:])
    return True


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    args = set(sys.argv[1:])
    check_mode = "--check" in args
    fix_bom = "--fix-bom" in args
    fix_mode = "--fix" in args
    staged_only = "--staged" in args

    if staged_only:
        paths = [f for f in staged_md_files() if os.path.isfile(f)]
    else:
        paths = sorted(walk_md_files())

    results = {}
    for path in paths:
        issues = scan_file(path)
        if issues:
            results[path] = issues

    # ── BOM fix mode ──
    if fix_bom:
        fixed = 0
        for path in sorted(results):
            path_issues = results[path]
            has_bom = any("BOM" in desc for desc, _ in path_issues)
            if has_bom and strip_bom(path):
                fixed += 1
                print(f"  stripped BOM: {path}")
        print(f"\nStripped BOM from {fixed} file(s).")
        # Re-scan remaining (non-BOM) issues
        remaining = {}
        for path in sorted(results):
            issues = [i for i in scan_file(path) if "BOM" not in i[0]]
            if issues:
                remaining[path] = issues
        results = remaining

    # ── Full fix mode (mojibake + U+FFFD + BOM) ──
    if fix_mode:
        stats = {"mojibake": 0, "fffd": 0, "bom": 0, "files": 0}
        for path in sorted(results):
            with open(path, "r", encoding="utf-8") as fh:
                original = fh.read()
            content = original

            # Strip BOM
            if content.startswith("\ufeff"):
                content = content[1:]
                stats["bom"] += 1

            # Fix mojibake
            content, n = fix_mojibake(content)
            stats["mojibake"] += n

            # Fix U+FFFD
            content, n = fix_fffd(content, path)
            stats["fffd"] += n

            if content != original:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
                stats["files"] += 1
                print(f"  fixed: {path}")

        print(f"\n✅ Fixed {stats['files']} file(s):")
        print(f"   {stats['mojibake']} mojibake → correct Unicode")
        print(f"   {stats['fffd']} U+FFFD → em-dash")
        print(f"   {stats['bom']} BOM stripped")

        # Re-scan to show remaining
        remaining = {}
        for path in sorted(walk_md_files()):
            issues = scan_file(path)
            if issues:
                remaining[path] = issues
        if remaining:
            total = sum(sum(c for _, c in v) for v in remaining.values())
            print(f"\n⚠️  {total} issue(s) remain in {len(remaining)} file(s) (likely binary previews).")
        else:
            print("\n✅ All encoding issues resolved.")
        return 0

    # ── Report ──
    if not results:
        print("✅ No encoding issues found.")
        return 0

    total_issues = sum(sum(c for _, c in v) for v in results.values())
    print(f"⚠️  Encoding issues in {len(results)} file(s) ({total_issues} total):\n")

    for path in sorted(results):
        print(f"  {path}")
        for desc, count in results[path]:
            print(f"    {count}x  {desc}")
        print()

    # Summary
    type_counts = Counter()
    for issues in results.values():
        for desc, count in issues:
            type_counts[desc] += count
    print("── Summary ──")
    for desc, count in type_counts.most_common():
        print(f"  {count:>5}x  {desc}")

    if check_mode:
        print(f"\n❌ {total_issues} encoding issue(s) — failing.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

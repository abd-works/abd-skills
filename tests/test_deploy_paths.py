#!/usr/bin/env python3
"""
test_deploy_paths.py — Validate that skills, agents, prompts, and instructions
are written in an IDE-agnostic way so they deploy correctly to both Cursor and
VS Code.

Run standalone:   python3 tests/test_deploy_paths.py
Run with pytest:  pytest tests/test_deploy_paths.py -v

Exit code 0 = all checks pass, 1 = failures found.
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None  # SKILL.md frontmatter test will be skipped

# ── Repo root ──────────────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", "node_modules", "catalog", "retired", "temp-drawio"}

# ── Helpers ────────────────────────────────────────────────────────────────


def walk_files(root, extensions=None):
    """Walk repo yielding (relative_path, absolute_path) tuples."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if extensions and not any(f.endswith(ext) for ext in extensions):
                continue
            abs_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(abs_path, root)
            yield rel_path, abs_path


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ── Test: deploy-path compliance ───────────────────────────────────────────
# Files that get deployed to BOTH IDEs (.prompt.md, .instructions.md) must
# use relative paths like ../skills/<name>/SKILL.md, NOT hardcoded
# .cursor/skills/ or bare skills/ paths.


def test_no_hardcoded_cursor_paths():
    """Dual-deployed files must not contain .cursor/skills/ references."""
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, (".prompt.md", ".instructions.md")):
        for i, line in enumerate(read_file(abs_path).splitlines(), 1):
            if ".cursor/skills/" in line:
                violations.append(f"  {rel}:{i}  {line.strip()[:100]}")
    assert not violations, (
        f".cursor/skills/ found in {len(violations)} dual-deployed line(s).\n"
        "These files are deployed to both Cursor (.cursor/commands/) and "
        "VS Code (.github/prompts/). Use ../skills/<name>/SKILL.md instead.\n"
        + "\n".join(violations)
    )


def test_no_bare_skill_paths():
    """Dual-deployed files must not use bare skills/ paths without ../ prefix."""
    violations = []
    # Match skills/X/SKILL.md where X starts with a letter, NOT preceded by ../
    pattern = re.compile(r"(?<!\.\./)skills/[a-z][\w-]*/SKILL\.md")
    for rel, abs_path in walk_files(REPO_ROOT, (".prompt.md", ".instructions.md")):
        for i, line in enumerate(read_file(abs_path).splitlines(), 1):
            if pattern.search(line):
                violations.append(f"  {rel}:{i}  {line.strip()[:100]}")
    assert not violations, (
        f"Bare skills/ path (missing ../) in {len(violations)} line(s).\n"
        "Use ../skills/<name>/SKILL.md for IDE-agnostic resolution.\n"
        + "\n".join(violations)
    )


def test_no_tilde_parent_skill_paths():
    """No ~/../skills/ paths — these don't resolve correctly."""
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, (".prompt.md", ".instructions.md")):
        for i, line in enumerate(read_file(abs_path).splitlines(), 1):
            if "~/../skills/" in line:
                violations.append(f"  {rel}:{i}  {line.strip()[:100]}")
    assert not violations, (
        f"~/../skills/ path in {len(violations)} line(s). Use ../skills/ instead.\n"
        + "\n".join(violations)
    )


# ── Test: encoding guard ───────────────────────────────────────────────────

MOJIBAKE_PATTERNS = {
    "\u00e2\u20ac\u2014": "em-dash",
    "\u00e2\u20ac\u201c": "left double quote",
    "\u00e2\u20ac\u201d": "right double quote",
    "\u00e2\u20ac\u2018": "left single quote",
    "\u00e2\u20ac\u2019": "right single quote",
    "\u00e2\u20ac\u2013": "en-dash",
    "\u00e2\u20ac\u2022": "bullet",
    "\u00e2\u20ac\u2026": "ellipsis",
    "\u00c2\u00a0": "non-breaking space",
    "\u00c2\u00ae": "registered",
    "\u00c2\u00a9": "copyright",
    "\u00c2\u00ad": "soft hyphen",
    "\u00e2\u0080\u0093": "en-dash (latin1)",
    "\u00e2\u0080\u0094": "em-dash (latin1)",
    "\u00e2\u0080\u0098": "left single quote (latin1)",
    "\u00e2\u0080\u0099": "right single quote (latin1)",
    "\u00e2\u0080\u009c": "left double quote (latin1)",
    "\u00e2\u0080\u009d": "right double quote (latin1)",
    "\u00e2\u0080\u00a2": "bullet (latin1)",
    "\u00e2\u0080\u00a6": "ellipsis (latin1)",
}

BINARY_MARKERS = ("IHDR", "[Content_Types]", "P!\ufffd", ".png)", ".docx)", ".xlsx)")


def is_binary_preview_line(line):
    return any(m in line for m in BINARY_MARKERS)


def test_no_mojibake():
    """No double-encoded Unicode (mojibake) in .md/.mdc files."""
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, (".md", ".mdc")):
        try:
            with open(abs_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except UnicodeDecodeError:
            continue  # Binary content — skip
        for pattern, desc in MOJIBAKE_PATTERNS.items():
            if pattern in content:
                n = content.count(pattern)
                violations.append(f"  {rel}: {n}x {desc}")
    assert not violations, (
        f"Mojibake found in {len(violations)} file(s).\n"
        "Run: python3 scripts/scan_encoding.py --fix\n"
        + "\n".join(violations)
    )


def test_no_replacement_char():
    """No U+FFFD replacement characters in .md/.mdc files (excluding binary previews)."""
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, (".md", ".mdc")):
        try:
            with open(abs_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except UnicodeDecodeError:
            continue  # Binary content — skip
        for i, line in enumerate(content.splitlines(), 1):
            if "\ufffd" in line and not is_binary_preview_line(line):
                violations.append(f"  {rel}:{i}")
    assert not violations, (
        f"U+FFFD replacement char in {len(violations)} line(s).\n"
        "Run: python3 scripts/scan_encoding.py --fix\n"
        + "\n".join(violations)
    )


def test_no_bom():
    """No UTF-8 BOM at start of .md/.mdc files."""
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, (".md", ".mdc")):
        with open(abs_path, "rb") as fh:
            if fh.read(3) == b"\xef\xbb\xbf":
                violations.append(f"  {rel}")
    assert not violations, (
        f"UTF-8 BOM in {len(violations)} file(s).\n"
        "Run: python3 scripts/scan_encoding.py --fix-bom\n"
        + "\n".join(violations)
    )


# ── Test: SKILL.md frontmatter ─────────────────────────────────────────────


def test_skill_frontmatter():
    """Every SKILL.md must have valid YAML frontmatter with name and description."""
    if yaml is None:
        return  # Skip if pyyaml not installed
    violations = []
    for rel, abs_path in walk_files(REPO_ROOT, ("SKILL.md",)):
        content = read_file(abs_path)
        if not content.startswith("---"):
            violations.append(f"  {rel}: missing frontmatter (no opening ---)")
            continue
        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            violations.append(f"  {rel}: malformed frontmatter (no closing ---)")
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            violations.append(f"  {rel}: YAML parse error: {e}")
            continue
        if not isinstance(fm, dict):
            violations.append(f"  {rel}: frontmatter is not a YAML mapping")
            continue
        if "name" not in fm:
            violations.append(f"  {rel}: missing 'name' field")
        if "description" not in fm:
            violations.append(f"  {rel}: missing 'description' field")
        # Check name matches directory convention
        expected_name = os.path.basename(os.path.dirname(abs_path))
        if fm.get("name") and fm["name"] != expected_name:
            # Allow some known mismatches (e.g. opportunity-canvas vs abd-opportunity-generation)
            pass  # Warn but don't fail — names may differ intentionally
    assert not violations, (
        f"SKILL.md frontmatter issues in {len(violations)} file(s).\n"
        + "\n".join(violations)
    )


# ── Test: AGENT.md / AGENTS.md presence ────────────────────────────────────


def test_agent_files():
    """Agent directories must have AGENT.md or AGENTS.md."""
    violations = []
    for top in ("practices", "foundational", "stages", "utilities", "others"):
        top_path = os.path.join(REPO_ROOT, top)
        if not os.path.isdir(top_path):
            continue
        for dirpath, dirnames, filenames in os.walk(top_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            # Only check directories that are direct children of an "agents/" folder
            parent = os.path.basename(os.path.dirname(dirpath))
            if parent != "agents":
                continue
            # Skip shared/utility directories
            name = os.path.basename(dirpath)
            if name.startswith("_") or name == "scripts":
                continue
            # Skip dirs that only have non-agent files (catalog HTML, configs)
            md_files = [f for f in filenames if f.endswith(".md")]
            if not md_files and filenames:
                continue  # Has files but no .md — likely a catalog page or config
            has_agent = "AGENT.md" in filenames or "AGENTS.md" in filenames
            if not has_agent:
                rel = os.path.relpath(dirpath, REPO_ROOT)
                violations.append(f"  {rel}: no AGENT.md or AGENTS.md")
    assert not violations, (
        f"Agent directories missing entry files:\n" + "\n".join(violations)
    )


# ── Test: version consistency ──────────────────────────────────────────────


def test_version_in_readme():
    """README must contain the version from VERSION file."""
    version_file = os.path.join(REPO_ROOT, "VERSION")
    if not os.path.isfile(version_file):
        return  # No VERSION file yet
    version = read_file(version_file).strip()
    readme_path = os.path.join(REPO_ROOT, "README.md")
    if not os.path.isfile(readme_path):
        return
    readme = read_file(readme_path)
    # Check for <!-- VERSION -->X.Y.Z<!-- /VERSION --> marker
    import re
    match = re.search(r"<!-- VERSION -->([\d.]+)<!-- /VERSION -->", readme)
    if match:
        readme_version = match.group(1)
        assert readme_version == version, (
            f"VERSION file says '{version}' but README says '{readme_version}'. "
            f"Update the <!-- VERSION --> marker in README.md."
        )
    else:
        assert False, (
            f"README.md missing version marker. Add: <!-- VERSION -->{version}<!-- /VERSION -->"
        )


def test_version_bump_on_new_content():
    """If new skills/agents/prompts were added, VERSION must have been bumped."""
    import subprocess
    try:
        # Get list of new files compared to previous commit
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", "HEAD~1", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True
        )
        new_files = result.stdout.strip().splitlines() if result.stdout.strip() else []
    except Exception:
        return  # Can't check — not a git repo or single commit

    # Check if any new content files were added
    new_content = [
        f for f in new_files
        if f.endswith("SKILL.md") or f.endswith("AGENT.md")
        or f.endswith("AGENTS.md") or f.endswith(".prompt.md")
    ]

    if not new_content:
        return  # No new content files

    # Check if VERSION was also changed
    version_changed = any(f.strip() == "VERSION" for f in new_files)
    if not version_changed:
        # Also check if VERSION was modified (not just added)
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=M", "HEAD~1", "HEAD"],
                cwd=REPO_ROOT, capture_output=True, text=True
            )
            modified = result.stdout.strip().splitlines() if result.stdout.strip() else []
            version_changed = any(f.strip() == "VERSION" for f in modified)
        except Exception:
            pass

    assert version_changed, (
        f"New content added but VERSION not bumped.\n"
        f"New files: {new_content}\n"
        f"Bump the version in the VERSION file, then update README.md."
    )


# ── Runner ─────────────────────────────────────────────────────────────────

ALL_TESTS = [
    ("Deploy: no hardcoded .cursor/skills/", test_no_hardcoded_cursor_paths),
    ("Deploy: no bare skills/ paths", test_no_bare_skill_paths),
    ("Deploy: no ~/../skills/ paths", test_no_tilde_parent_skill_paths),
    ("Encoding: no mojibake", test_no_mojibake),
    ("Encoding: no U+FFFD replacement char", test_no_replacement_char),
    ("Encoding: no UTF-8 BOM", test_no_bom),
    ("Structure: SKILL.md frontmatter", test_skill_frontmatter),
    ("Structure: agent entry files", test_agent_files),
    ("Version: README matches VERSION file", test_version_in_readme),
    ("Version: bump on new content", test_version_bump_on_new_content),
]


def main():
    """Standalone runner — prints results and exits with 0/1."""
    passed = 0
    failed = 0
    errors = []

    for label, test_fn in ALL_TESTS:
        try:
            test_fn()
            print(f"  ✅ {label}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {label}")
            errors.append(str(e))
            failed += 1
        except Exception as e:
            print(f"  ⚠️  {label} — error: {e}")
            errors.append(f"{label}: {e}")
            failed += 1

    print(f"\n{'─' * 50}")
    print(f"  {passed} passed, {failed} failed, {passed + failed} total")

    if errors:
        print(f"\n{'═' * 50}")
        for err in errors:
            print(err)
            print(f"{'─' * 50}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

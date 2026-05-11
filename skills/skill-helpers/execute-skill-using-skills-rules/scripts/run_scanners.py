#!/usr/bin/env python3
"""Run every scanner script configured for a skill (execute-skill-using-skills-rules — canonical driver).

Always saves a Markdown violations report to <report_dir>/<skill-name>.md.
Default report_dir: <workspace>/scanner-report/ (created if absent).
Override with --report-dir.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Same directory as this file (…/execute-skill-using-skills-rules/scripts)
_SCRIPT_DIR = Path(__file__).resolve().parent
_STORY_GRAPH_OPS_SCRIPTS = _SCRIPT_DIR.parent.parent / "story-graph-ops" / "scripts"
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
if _STORY_GRAPH_OPS_SCRIPTS.is_dir() and str(_STORY_GRAPH_OPS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_STORY_GRAPH_OPS_SCRIPTS))

from scanner_paths import list_scanner_scripts  # noqa: E402


def _load_cfg(skill_root: Path) -> dict:
    p = skill_root / "skill-config.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Violation parsing — scanners print Python dict repr lines to stdout
# ---------------------------------------------------------------------------

def _parse_violations(output: str) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = ast.literal_eval(line)
            if isinstance(obj, dict) and "violation_message" in obj:
                violations.append(obj)
        except Exception:
            pass
    return violations


# ---------------------------------------------------------------------------
# Markdown report generation
# ---------------------------------------------------------------------------

def _overall_status(
    executed: list[dict], failed_scanners: list[str]
) -> tuple[str, str]:
    if failed_scanners:
        return ("🟥", "CRITICAL ISSUES")
    total = sum(r["violation_count"] for r in executed)
    errors = sum(1 for r in executed if r["has_errors"])
    if total == 0:
        return ("🟩", "ALL CLEAN")
    if total < 150 and errors == 0:
        return ("🟩", "HEALTHY")
    if total < 200 and errors <= 5:
        return ("🟨", "GOOD - Minor Issues")
    if errors > 0:
        return ("🟨", "NEEDS ATTENTION")
    return ("🟨", "WARNINGS FOUND")


def _rule_display(scanner_path: str) -> str:
    stem = Path(scanner_path).stem.replace("-scanner", "").replace("_", " ").title()
    return stem


def _anchor(scanner_path: str) -> str:
    return Path(scanner_path).stem.replace("-scanner", "").lower()


def _build_report(
    skill_name: str,
    workspace: str,
    executed: list[dict],
    failed_scanners: list[str],
    passed_scanners: list[str],
) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_emoji, status_text = _overall_status(executed, failed_scanners)

    total_violations = sum(r["violation_count"] for r in executed)
    clean = [r for r in executed if r["violation_count"] == 0]
    warned = [r for r in executed if r["has_warnings"] and not r["has_errors"]]
    errored = [r for r in executed if r["has_errors"]]
    total_warnings = sum(r["violation_count"] for r in warned)
    total_errors = sum(r["violation_count"] for r in errored)

    lines: list[str] = []
    lines += [
        f"# Scanner Report — {skill_name}",
        "",
        f"**Workspace:** {workspace}",
        f"**Date:** {ts}",
        "",
        "---",
        "",
        "## Scanner Execution Status",
        "",
        f"### {status_emoji} Overall Status: {status_text}",
        "",
        "| Status | Count | Description |",
        "|--------|-------|-------------|",
    ]
    if executed:
        lines.append(f"| 🟩 Executed Successfully | {len(executed)} | Scanners ran without errors |")
    if clean:
        lines.append(f"| 🟩 Clean Rules | {len(clean)} | No violations found |")
    if warned:
        lines.append(f"| 🟨 Rules with Warnings | {len(warned)} | Found {total_warnings} warning violation(s) |")
    if errored:
        lines.append(f"| 🟥 Rules with Errors | {len(errored)} | Found {total_errors} error violation(s) |")
    if failed_scanners:
        lines.append(f"| 🟥 Execution Failed | {len(failed_scanners)} | Scanner crashed during execution |")
    lines.append("")

    total_rules = len(executed) + len(failed_scanners)
    lines += [
        f"**Total Rules:** {total_rules}",
        f"- **Rules with Scanners:** {total_rules}",
        f"  - 🟩 **Executed Successfully:** {len(executed)}",
    ]
    if failed_scanners:
        lines.append(f"  - 🟥 **Execution Failed:** {len(failed_scanners)}")
    lines += ["", "---", ""]

    # Summary table — one row per scanner, no links
    lines += ["### Scanner Results", ""]
    all_scanners = sorted(executed, key=lambda r: (-r["violation_count"], r["scanner_path"]))
    lines += ["| Status | Rule | Violations |", "|--------|------|------------|"]
    for r in all_scanners:
        vc = r["violation_count"]
        display = _rule_display(r["scanner_path"])
        if r["has_errors"]:
            icon = "🟥"
            label = "ERRORS"
        elif r["has_warnings"]:
            icon = "🟨"
            label = "WARNINGS"
        else:
            icon = "🟩"
            label = "CLEAN"
        vtext = str(vc) if vc > 0 else "0"
        lines.append(f"| {icon} {label} | {display} | {vtext} |")
    for sp in failed_scanners:
        display = _rule_display(sp)
        lines.append(f"| 🟥 FAILED | {display} | — |")
    for sp in passed_scanners:
        display = _rule_display(sp)
        lines.append(f"| 🟩 CLEAN | {display} | 0 |")
    lines += ["", "---", ""]

    # Violations detail — one section per failing scanner
    failing = [r for r in all_scanners if r["violation_count"] > 0]
    if failing:
        lines += ["## Violations", ""]
        for r in failing:
            display = _rule_display(r["scanner_path"])
            vc = r["violation_count"]
            if r["has_errors"]:
                icon = "🟥"
            else:
                icon = "🟨"
            lines += [f"### {icon} {display} — {vc} violation(s)", ""]
            lines += ["| # | Location | Message | Severity |", "|---|----------|---------|----------|"]
            for i, v in enumerate(r["violations"], 1):
                loc = v.get("location") or ""
                msg = v.get("violation_message", "").replace("|", "\\|")
                sev = v.get("severity", "error")
                lines.append(f"| {i} | `{loc}` | {msg} | {sev} |")
            lines += [""]
    else:
        lines += ["## Violations", "", "_No violations found._", ""]

    if failed_scanners:
        lines += ["## Scanner Failures", ""]
        for sp in failed_scanners:
            display = _rule_display(sp)
            out = next((r.get("stderr", "") for r in executed if r.get("scanner_path") == sp), "")
            lines += [f"### {display}", "", f"Scanner: `{sp}`", ""]
            if out:
                lines += ["```", out[:2000], "```"]
            lines += [""]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _build_env(root: Path, language: str | None) -> dict:
    env = os.environ.copy()
    parts: list[str] = []
    if _STORY_GRAPH_OPS_SCRIPTS.is_dir():
        parts.append(str(_STORY_GRAPH_OPS_SCRIPTS))
    parts.append(str(_SCRIPT_DIR))
    skill_scripts = root / "scripts"
    if skill_scripts.is_dir():
        parts.append(str(skill_scripts))
    skill_scanners = root / "scanners"
    if skill_scanners.is_dir():
        parts.append(str(skill_scanners))
    if language:
        skill_lang_scanners = root / "scanners" / language
        if skill_lang_scanners.is_dir():
            parts.append(str(skill_lang_scanners))
    prev = env.get("PYTHONPATH", "")
    if prev:
        parts.append(prev)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="execute-skill-using-skills-rules: run scanners for --skill-root"
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        default=Path.cwd(),
        help="Skill root (directory with SKILL.md, rules/, scanners/*-scanner.py, …). Default: cwd.",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Path passed to each scanner as --workspace (default: --skill-root).",
    )
    parser.add_argument(
        "--language",
        default=None,
        metavar="LANG",
        help=(
            "Target language (e.g. 'python', 'javascript'). "
            "When given, scanners are resolved from scanners/<LANG>/ and that directory "
            "is added to PYTHONPATH so language base classes are importable."
        ),
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=None,
        help=(
            "Directory to write the Markdown violations report. "
            "Default: <workspace>/scanner-report/ (created if absent). "
            "Pass 'none' to suppress report saving."
        ),
    )
    args = parser.parse_args(argv)
    root = args.skill_root.resolve()
    workspace = args.workspace if args.workspace is not None else str(root)
    language: str | None = args.language

    cfg = _load_cfg(root)
    scanners = list_scanner_scripts(root, cfg, language=language)
    if not scanners:
        lang_info = f" for language '{language}'" if language else ""
        print(
            f"[INFO] No scanners found{lang_info} "
            f"(no scanner: in rules frontmatter and no scanners/*-scanner.py)"
        )
        return 0

    env = _build_env(root, language)
    executed_results: list[dict] = []
    failed_scanners: list[str] = []
    passed_scanners: list[str] = []

    # Find story-graph.json once and pass it explicitly to every scanner.
    ws_path = Path(workspace)
    story_graph_matches = sorted(ws_path.rglob("story-graph.json"))
    story_graph_path = str(story_graph_matches[0]) if story_graph_matches else None
    if story_graph_path:
        print(f"[GRAPH] {story_graph_path}")
    else:
        print("[GRAPH] story-graph.json not found in workspace")

    for scanner_path in scanners:
        script = root.joinpath(*scanner_path.split("/"))
        if not script.is_file():
            print(f"[MISSING] {scanner_path}")
            failed_scanners.append(scanner_path)
            continue

        cmd = [sys.executable, str(script), "--workspace", workspace]
        if story_graph_path:
            cmd += ["--story-graph", story_graph_path]

        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            env=env,
        )

        # Stream output to terminal
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)

        violations = _parse_violations(result.stderr)
        has_errors = any(v.get("severity", "error") == "error" for v in violations)
        has_warnings = any(v.get("severity") == "warning" for v in violations)

        if result.returncode == 0:
            passed_scanners.append(scanner_path)
            executed_results.append({
                "scanner_path": scanner_path,
                "violation_count": 0,
                "violations": [],
                "has_errors": False,
                "has_warnings": False,
                "returncode": 0,
            })
        elif result.returncode == 1:
            executed_results.append({
                "scanner_path": scanner_path,
                "violation_count": len(violations),
                "violations": violations,
                "has_errors": has_errors,
                "has_warnings": has_warnings,
                "returncode": 1,
            })
        else:
            # Crash / missing
            failed_scanners.append(scanner_path)
            executed_results.append({
                "scanner_path": scanner_path,
                "violation_count": 0,
                "violations": [],
                "has_errors": True,
                "has_warnings": False,
                "returncode": result.returncode,
                "stderr": result.stderr,
            })

    # --- Console summary ---
    print("\n--- Scanner summary ---")
    all_paths = [r["scanner_path"] for r in executed_results] + failed_scanners
    rc_map = {r["scanner_path"]: r["returncode"] for r in executed_results}
    seen: set[str] = set()
    for sp in scanners:
        if sp in seen:
            continue
        seen.add(sp)
        code = rc_map.get(sp, 2)
        status = "[PASS]" if code == 0 else "[FAIL]" if code == 1 else "[MISSING/CRASH]"
        print(f"  {status} {sp}")

    failed_count = sum(1 for r in executed_results if r["returncode"] != 0) + len(
        [sp for sp in failed_scanners if sp not in rc_map]
    )
    if failed_count:
        print(f"\n{failed_count} scanner(s) failed.")
    else:
        print(f"\nAll {len(scanners)} scanner(s) passed.")

    # --- Save report ---
    suppress = str(args.report_dir).lower() == "none" if args.report_dir else False
    if not suppress:
        if args.report_dir:
            report_dir = args.report_dir.resolve()
        else:
            report_dir = Path(workspace).resolve() / "scanner-report"
        report_dir.mkdir(parents=True, exist_ok=True)

        skill_name = root.name
        report_path = report_dir / f"{skill_name}.md"

        non_crashed_executed = [r for r in executed_results if r["returncode"] in (0, 1)]
        crashed = [r["scanner_path"] for r in executed_results if r["returncode"] not in (0, 1)]
        crashed += [sp for sp in failed_scanners if sp not in rc_map]

        report_md = _build_report(
            skill_name=skill_name,
            workspace=workspace,
            executed=non_crashed_executed,
            failed_scanners=crashed,
            passed_scanners=[],
        )
        report_path.write_text(report_md, encoding="utf-8")
        print(f"\n[REPORT] {report_path}")

    return 1 if failed_count else 0


if __name__ == "__main__":
    sys.exit(main())

"""Structural operator: compileall, build.py, declared scanners (plan §4.2)."""

from __future__ import annotations

import compileall
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_SKILL_MD = "SKILL.md"
_SKILL_CONFIG = "skill-config.json"
_SCANNERS_JSON = Path("rules") / "scanners.json"


def _load_skill_config(skill_root: Path) -> dict[str, Any]:
    p = skill_root / _SKILL_CONFIG
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _merge_scanner_paths(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    op = cfg.get("operator") or {}
    for rel in op.get("scanners") or []:
        s = str(rel).replace("\\", "/")
        if s not in seen:
            seen.add(s)
            out.append(s)
    sj = skill_root / _SCANNERS_JSON
    if sj.is_file():
        data = json.loads(sj.read_text(encoding="utf-8"))
        for b in data.get("rule_scanner_bindings") or []:
            rel = b.get("scanner")
            if not rel:
                continue
            s = str(rel).replace("\\", "/")
            if s not in seen:
                seen.add(s)
                out.append(s)
        for rel in data.get("scanners") or []:
            s = str(rel).replace("\\", "/")
            if s not in seen:
                seen.add(s)
                out.append(s)
    return out


def _verify_rule_scanner_bindings(skill_root: Path) -> list[dict[str, Any]]:
    """Ensure each rule_scanner_bindings entry points at existing rule + scanner files."""
    sj = skill_root / _SCANNERS_JSON
    if not sj.is_file():
        return []
    data = json.loads(sj.read_text(encoding="utf-8"))
    bindings = data.get("rule_scanner_bindings") or []
    if not bindings:
        return []
    rows: list[dict[str, Any]] = []
    for b in bindings:
        bid = b.get("id")
        rule_rel = b.get("rule")
        scan_rel = b.get("scanner")
        rule_ok = bool(rule_rel and (skill_root / str(rule_rel).replace("\\", "/")).is_file())
        scan_ok = bool(scan_rel and (skill_root / str(scan_rel).replace("\\", "/")).is_file())
        rows.append(
            {
                "id": bid,
                "rule": rule_rel,
                "scanner": scan_rel,
                "rule_exists": rule_ok,
                "scanner_exists": scan_ok,
            }
        )
    return rows


def _compileall_paths(skill_root: Path, cfg: dict[str, Any]) -> list[str]:
    op = cfg.get("operator") or {}
    raw = op.get("compileall_paths")
    if raw is None:
        scripts = skill_root / "scripts"
        return ["scripts"] if scripts.is_dir() else []
    return [str(x).replace("\\", "/") for x in raw]


def run_operator(skill_path: str | Path) -> dict[str, Any]:
    """
    Run compileall on configured paths, ``python scripts/build.py`` when configured,
    then each scanner script with the repo venv / current interpreter.

    Returns a report dict with ``ok: bool`` and ``checks: list`` of per-step records.
    """
    root = Path(skill_path).resolve()
    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    if not (root / _SKILL_MD).is_file():
        return {
            "ok": False,
            "skill_path": str(root),
            "errors": [f"missing {_SKILL_MD}"],
            "checks": [],
        }

    cfg = _load_skill_config(root)
    cwd = root

    binding_rows = _verify_rule_scanner_bindings(root)
    if binding_rows:
        bad = [r for r in binding_rows if not r.get("rule_exists") or not r.get("scanner_exists")]
        checks.append(
            {
                "step": "rule_scanner_bindings",
                "ok": len(bad) == 0,
                "bindings": binding_rows,
                "detail": None if not bad else f"missing files for {len(bad)} binding(s)",
            }
        )
        if bad:
            errors.append(
                "rule_scanner_bindings: "
                + "; ".join(
                    f"{r.get('id')}: rule={r.get('rule_exists')} scanner={r.get('scanner_exists')}"
                    for r in bad
                )
            )

    for rel in _compileall_paths(root, cfg):
        sub = (root / rel).resolve()
        if not sub.exists():
            checks.append({"step": "compileall", "path": rel, "ok": True, "detail": "skip (missing)"})
            continue
        ok = compileall.compile_dir(str(sub), quiet=1)
        checks.append(
            {
                "step": "compileall",
                "path": rel,
                "ok": bool(ok),
                "detail": "compile_dir returned truthy" if ok else "compile failures",
            }
        )
        if not ok:
            errors.append(f"compileall failed: {rel}")

    build_rel = (cfg.get("operator") or {}).get("build_script")
    if not build_rel:
        if (root / "scripts" / "build.py").is_file():
            build_rel = "scripts/build.py"
    if build_rel:
        script = root / build_rel
        if not script.is_file():
            checks.append({"step": "build", "script": build_rel, "ok": False, "detail": "missing file"})
            errors.append(f"build script not found: {build_rel}")
        else:
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(cwd),
                capture_output=True,
                text=True,
            )
            ok = proc.returncode == 0
            checks.append(
                {
                    "step": "build",
                    "script": build_rel,
                    "ok": ok,
                    "returncode": proc.returncode,
                    "stdout": (proc.stdout or "")[-4000:],
                    "stderr": (proc.stderr or "")[-4000:],
                }
            )
            if not ok:
                errors.append(f"build.py failed ({build_rel}) rc={proc.returncode}")

    for rel in _merge_scanner_paths(root, cfg):
        script = root / rel
        if not script.is_file():
            checks.append({"step": "scanner", "script": rel, "ok": False, "detail": "missing file"})
            errors.append(f"scanner not found: {rel}")
            continue
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(cwd),
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        checks.append(
            {
                "step": "scanner",
                "script": rel,
                "ok": ok,
                "returncode": proc.returncode,
                "stdout": (proc.stdout or "")[-2000:],
                "stderr": (proc.stderr or "")[-2000:],
            }
        )
        if not ok:
            errors.append(f"scanner failed: {rel} rc={proc.returncode}")

    return {
        "ok": len(errors) == 0,
        "skill_path": str(root),
        "errors": errors,
        "checks": checks,
    }

#!/usr/bin/env python3
"""Orchestrate pipeline phases by name. AI phases print instructions; code phases run scripts."""
import importlib
import subprocess
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_DIR / "scripts"))
from _config import (
    chunk_index_path as _chunk_index_path_fn,
    context_path as _context_path_fn,
    context_dir as _context_dir_fn,
    domain_dir as _domain_dir_fn,
    interaction_model_dir as _interaction_model_dir_fn,
    evidence_dir as _evidence_dir_fn,
    generated_dir as _generated_dir_fn,
    concept_signals_dir as _concept_signals_dir_fn,
    hypothesis_path as _hypothesis_path_fn,
    extraction_config_path as _extraction_config_path_fn,
    evidence_index_path as _evidence_index_path_fn,
    solution_model_path as _solution_model_path_fn,
    no_tree as _no_tree_fn,
)

_SCRIPTS_DIR = _SKILL_DIR / "scripts"
_PIECES_DIR = _SKILL_DIR / "pieces"
_RULES_DIR = _SKILL_DIR / "rules"
_SCANNERS_DIR = _SCRIPTS_DIR / "scanners"

# Concept-anchored pipeline: 13 phases
_PHASES = [
    "normalize",                             # 1: Code - context_chunks.json
    "configure_concept_extraction_parameters", # 2: AI - extraction_config.json (calibration)
    "concept_extraction",                    # 3: AI+Code loop - run extraction, evaluate, loop to 2 if fail
    "concept_index",                         # 4: Code - hypothesis.json (concept index with chunk_ids)
    "concept_synthesis",                     # 5: AI - refined hypothesis.json (merge/split/kill, hierarchy)
    "evidence_extraction",                   # 6: Code - evidence/*.json
    "evidence_index",                       # 7: Code - evidence_index.json
    "structure",                             # 8: AI - solution_model.json v1
    "behavior",                              # 9: AI - solution_model.json v2
    "variation",                             # 10: AI - solution_model.json v3
    "consolidate",                           # 11: AI - solution_model.json v4
    "assess",                                # 12: AI+Human - assessment.json
    "finalize",                              # 13: AI - solution_model.json final
]

# Code phases: pipeline runs a script. AI phases (synthesis, structure, behavior, etc.)
# MUST NOT be listed here — they print the spec; the AI performs the work. Do NOT add runners.
_CODE_PHASES = {"normalize", "concept_index", "evidence_extraction", "evidence_index"}

from _rules import rules_for_phase as _rules_for_phase


_PHASE_OUTPUT_FILES: dict[str, dict[str, list[str]]] = {
    "extract_concepts": {"generated": ["extraction_config.json"]},
    "concept_synthesis": {"generated": ["hypothesis.json"]},
    "synthesis": {"generated": ["hypothesis.json"]},
    "structure": {"generated": ["solution_model.json"]},
    "behavior": {"generated": ["solution_model.json"]},
    "variation": {"generated": ["solution_model.json"]},
    "consolidate": {"generated": ["solution_model.json"]},
    "assess": {"generated": ["assessment.json"]},
    "finalize": {"generated": ["solution_model.json"]},
}


def _get_artifact_path(artifact_folder: str) -> Path | None:
    if artifact_folder == "domain":
        return _domain_dir_fn()
    elif artifact_folder == "interaction-tree":
        return _interaction_model_dir_fn()
    elif artifact_folder == "generated":
        return _generated_dir_fn()
    return None


def _phase_target_files(phase_name: str, artifact_folder: str) -> list[Path]:
    """Return only the output file(s) for this phase in the given artifact folder."""
    if artifact_folder == "interaction-tree" and _no_tree_fn():
        return []
    target_dir = _get_artifact_path(artifact_folder)
    if target_dir is None or not target_dir.exists():
        return []
    filenames = _PHASE_OUTPUT_FILES.get(phase_name, {}).get(artifact_folder)
    if filenames:
        return [target_dir / f for f in filenames if (target_dir / f).exists()]
    return sorted(target_dir.glob("*.md"))


def _find_scanner(rule_path: Path) -> type | None:
    """Find scanner class for a rule by convention: rule stem with underscores.

    Looks for a .py module matching the rule stem. Finds the first BaseScanner
    subclass in that module (class names may not match the filename convention).
    """
    from scanners.base import BaseScanner
    module_name = rule_path.stem.replace("-", "_")
    scanner_path = _SCANNERS_DIR / f"{module_name}.py"
    if not scanner_path.exists():
        return None
    try:
        mod = importlib.import_module(f"scanners.{module_name}")
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if isinstance(attr, type) and issubclass(attr, BaseScanner) and attr is not BaseScanner:
                return attr
        return None
    except (ImportError, AttributeError):
        return None


# ---------------------------------------------------------------------------
# Code phase runners
# ---------------------------------------------------------------------------

def _run_normalize_context() -> bool:
    import os
    context_out = str(_context_dir_fn())
    _ci = _chunk_index_path_fn()
    _cp = _context_path_fn()
    chunk_index = os.environ.get("_ABD_CHUNK_INDEX") or (str(_ci) if _ci else None)
    context_path = os.environ.get("_ABD_CONTEXT_PATH") or (str(_cp) if _cp else None)
    base = [sys.executable, str(_SCRIPTS_DIR / "normalize_context.py"), "-o", context_out]
    if chunk_index:
        idx = Path(chunk_index).resolve()
        if not idx.exists():
            print(f"chunk_index_path not found: {idx}", file=sys.stderr)
            return False
        args = base[:-2] + ["--chunk-index", str(idx), "-o", context_out]
    elif context_path:
        ctx = Path(context_path).resolve()
        if not ctx.exists():
            print(f"context_path not found: {ctx}", file=sys.stderr)
            return False
        args = base[:-2] + ["--context-path", str(ctx), "-o", context_out]
    else:
        print("normalize_context requires chunk_index_path or context_path in workspace solution.conf.", file=sys.stderr)
        return False
    return subprocess.run(args, cwd=str(_SKILL_DIR)).returncode == 0


def _run_concept_index() -> bool:
    signals = _concept_signals_dir_fn()
    hypothesis = _hypothesis_path_fn()
    if not signals.exists():
        print("concept_index requires concept_signals — run concept_extraction first.", file=sys.stderr)
        return False
    args = [
        sys.executable, str(_SCRIPTS_DIR / "build_hypothesis_from_signals.py"),
        "-i", str(signals),
        "-o", str(hypothesis),
    ]
    return subprocess.run(args, cwd=str(_SKILL_DIR)).returncode == 0


def _run_extract_concepts() -> bool:
    ctx = _context_dir_fn()
    signals = _concept_signals_dir_fn()
    chunks_path = ctx / "context_chunks.json"
    if not chunks_path.exists():
        print("concept_extraction requires context_chunks.json — run normalize first.", file=sys.stderr)
        return False
    config_path = _extraction_config_path_fn()
    args = [
        sys.executable, str(_SCRIPTS_DIR / "extract_concepts.py"),
        "-i", str(chunks_path),
        "-o", str(signals),
    ]
    if config_path.exists():
        args = args[:-2] + ["-c", str(config_path), "-o", str(signals)]
    return subprocess.run(args, cwd=str(_SKILL_DIR)).returncode == 0


def _run_evidence_extraction() -> bool:
    ctx = _context_dir_fn()
    evidence = _evidence_dir_fn()
    hypothesis = _hypothesis_path_fn()
    guidance = _domain_dir_fn() / "concept_guidance.json"
    guidance_path = hypothesis if hypothesis.exists() else guidance
    if not guidance_path.exists():
        print("evidence_extraction requires hypothesis.json — run concept_index first (or concept_synthesis to refine).", file=sys.stderr)
        return False
    args = [
        sys.executable, str(_SCRIPTS_DIR / "evidence_extraction_guided.py"),
        "-i", str(ctx / "context_chunks.json"),
        "-g", str(guidance_path),
        "-o", str(evidence),
    ]
    return subprocess.run(args, cwd=str(_SKILL_DIR)).returncode == 0


def _run_index() -> bool:
    evidence = _evidence_dir_fn()
    args = [
        sys.executable, str(_SCRIPTS_DIR / "evidence_index.py"),
        "-i", str(evidence),
        "-o", str(_evidence_index_path_fn()),
    ]
    return subprocess.run(args, cwd=str(_SKILL_DIR)).returncode == 0


_CODE_RUNNERS = {
    "normalize": _run_normalize_context,
    "concept_index": _run_concept_index,
    "evidence_extraction": _run_evidence_extraction,
    "evidence_index": _run_index,
}


def _ensure_workspace_dirs() -> None:
    dirs = [
        _context_dir_fn(),
        _concept_signals_dir_fn(),
        _evidence_dir_fn(),
        _generated_dir_fn(),
        _domain_dir_fn(),
    ]
    if not _no_tree_fn():
        dirs.append(_interaction_model_dir_fn())
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _ensure_utf8() -> None:
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def _cmd_generate(name: str) -> None:
    """Layer 1: Print built phase spec (phase instructions + baked-in rules)."""
    if name not in _PHASES:
        valid = ", ".join(_PHASES)
        print(f"Unknown phase '{name}'. Valid phases: {valid}", file=sys.stderr)
        sys.exit(1)

    _ensure_workspace_dirs()

    built_file = _PIECES_DIR / "phases" / "built" / f"{name}.md"
    phase_file = _PIECES_DIR / "phases" / f"{name}.md"
    target = built_file if built_file.exists() else phase_file
    if not target.exists():
        print(f"Phase file missing: {target}", file=sys.stderr)
        print("Run: python scripts/assemble_agents.py  (builds phases/built/)", file=sys.stderr)
        sys.exit(1)

    if name in _CODE_PHASES:
        if not _CODE_RUNNERS[name]():
            sys.exit(1)
        return

    _ensure_utf8()
    print(target.read_text(encoding="utf-8"))

    # Auto-generate DrawIO after mandatory phases
    if name in _DRAWIO_MANDATORY_PHASES:
        print(f"\n[pipeline] Generating DrawIO diagram for {name}...", file=sys.stderr)
        _cmd_drawio(name)


def _cmd_scan(name: str) -> None:
    """Layer 2: Run scanners against output files for rules up to the given phase."""
    if name not in _PHASES:
        valid = ", ".join(_PHASES)
        print(f"Unknown phase '{name}'. Valid phases: {valid}", file=sys.stderr)
        sys.exit(1)

    _ensure_workspace_dirs()
    rules = _rules_for_phase(name, skip_tree=_no_tree_fn())
    violations: list = []
    scanners_run = 0

    for rule_path in rules:
        scanner_cls = _find_scanner(rule_path)
        if scanner_cls is None:
            continue
        scanners_run += 1
        scanner = scanner_cls()
        artifact = rule_path.parent.name
        for target_file in _phase_target_files(name, artifact):
            content = target_file.read_text(encoding="utf-8")
            violations.extend(scanner.scan(content, str(target_file)))

    print(f"Scanners run: {scanners_run}", file=sys.stderr)
    if violations:
        for v in violations:
            sev = getattr(v, "severity", "MEDIUM")
            rule_id = getattr(v, "rule_id", "unknown")
            msg = getattr(v, "message", str(v))
            loc = getattr(v, "location", "")
            print(f"[{sev}] {rule_id}: {msg}")
            if loc:
                print(f"  at: {loc}")
        print(f"\n{len(violations)} violation(s) found.", file=sys.stderr)
        sys.exit(1)
    else:
        print("No violations found.", file=sys.stderr)


def _cmd_validate(name: str) -> None:
    """Layer 3: Print rules + validation checklist + output paths for AI validation pass."""
    if name not in _PHASES:
        valid = ", ".join(_PHASES)
        print(f"Unknown phase '{name}'. Valid phases: {valid}", file=sys.stderr)
        sys.exit(1)

    _ensure_utf8()

    checklist = _PIECES_DIR / "validation.md"
    if checklist.exists():
        print(checklist.read_text(encoding="utf-8").strip())
        print("\n\n---\n\n")

    rules = _rules_for_phase(name)
    print(f"## Rules — Validate Output Against Each ({len(rules)} rules)\n")
    print("For each rule below, check whether the output complies.")
    print("Report: rule name, violation, location, proposed fix.\n")
    for r in rules:
        print(r.read_text(encoding="utf-8").strip())
        print("\n---\n")

    print("\n## Output Files to Validate\n")
    validate_dirs = [_domain_dir_fn(), _generated_dir_fn()]
    if not _no_tree_fn():
        validate_dirs.append(_interaction_model_dir_fn())
    for p in validate_dirs:
        if p.exists():
            for f in sorted(p.glob("*.md")):
                print(f"- `{f}`")
            for f in sorted(p.glob("*.json")):
                if f.name in ("solution_model.json", "assessment.json", "hypothesis.json", "extraction_config.json"):
                    print(f"- `{f}`")


# ---------------------------------------------------------------------------
# Stage 2 phases that produce domain model files (optional DrawIO after each)
# ---------------------------------------------------------------------------
_STAGE2_PHASES = {
    "structure", "behavior", "variation", "consolidate", "assess", "finalize",
}

# Phases after which DrawIO is always generated (mandatory)
_DRAWIO_MANDATORY_PHASES = {"finalize"}


def _solution_model_to_md(solution_model_path: Path) -> str:
    """Convert solution_model.json concepts to domain-model markdown for DrawIO."""
    import json
    data = json.loads(solution_model_path.read_text(encoding="utf-8"))
    concepts = data.get("concepts", [])
    lines = ["# Module: Domain"]
    for c in concepts:
        name = c.get("id", c.get("name", "Unknown"))
        base = c.get("inherits", c.get("inherits_from", c.get("base", "")))
        heading = f"## {name}" + (f" : {base}" if base else "")
        lines.append(heading)
        for p in c.get("properties", []):
            pname = p.get("name", p) if isinstance(p, dict) else p
            ptype = p.get("type", "?") if isinstance(p, dict) else "?"
            lines.append(f"- {pname} : {ptype}")
        for op in c.get("operations", []):
            oname = op.get("name", op) if isinstance(op, dict) else op
            ret = op.get("returns", "?") if isinstance(op, dict) else "?"
            lines.append(f"- {oname}() → {ret}")
        lines.append("")
    return "\n".join(lines)


def _cmd_drawio(phase: str | None = None) -> None:
    """Generate DrawIO class diagram from solution_model.json or domain model .md.

    Prefers solution_model.json in generated/; falls back to domain/*.md.
    Output: generated/domain/solution_model.drawio or <stem>.drawio
    """
    generated = _generated_dir_fn()
    domain = _domain_dir_fn()
    solution_model = generated / "solution_model.json"

    target: Path | None = None
    output: Path | None = None
    temp_md: Path | None = None
    if solution_model.exists():
        # Convert solution_model.json to temp markdown for model_to_drawio
        import tempfile
        md_content = _solution_model_to_md(solution_model)
        fd, path = tempfile.mkstemp(suffix=".md", text=True)
        Path(path).write_text(md_content, encoding="utf-8")
        target = Path(path)
        temp_md = target
        domain.mkdir(parents=True, exist_ok=True)
        output = domain / "solution_model.drawio"
    else:
        if not domain.exists():
            print(f"Domain dir not found: {domain}", file=sys.stderr)
            sys.exit(1)
        if phase:
            candidates = sorted(domain.glob(f"*{phase}*.md")) + sorted(domain.glob("*.md"))
            for c in candidates:
                if c.suffix == ".md" and not c.name.startswith("."):
                    target = c
                    break
        else:
            for preferred in ("final_domain_model.md", "refined_domain_model.md"):
                p = domain / preferred
                if p.exists():
                    target = p
                    break
            if not target:
                mds = sorted(domain.glob("*.md"))
                target = mds[-1] if mds else None
        output = target.with_suffix(".drawio") if target else None

    if not target or not target.exists():
        print(f"No solution_model.json or domain .md found — skipping DrawIO.", file=sys.stderr)
        return

    args = [
        sys.executable, str(_SCRIPTS_DIR / "model_to_drawio.py"),
        str(target), "--output", str(output),
    ]
    r = subprocess.run(args, cwd=str(_SKILL_DIR))
    if temp_md and temp_md.exists():
        temp_md.unlink(missing_ok=True)
    if r.returncode == 0:
        print(f"DrawIO diagram -> {output}")
    else:
        sys.exit(r.returncode)


def _cmd_pipeline(stop_at: str | None = None) -> None:
    end = _PHASES.index(stop_at) + 1 if stop_at and stop_at in _PHASES else len(_PHASES)
    for name in _PHASES[:end]:
        print(f"\n--- {name} ---\n", file=sys.stderr)
        _cmd_generate(name)


def _main() -> None:
    args = sys.argv[1:]
    if not args:
        names = " | ".join(_PHASES)
        print(f"Usage: pipeline.py generate <phase> [render-diagram]")
        print(f"       pipeline.py scan <phase>")
        print(f"       pipeline.py validate <phase>")
        print(f"       pipeline.py drawio [<phase>]")
        print(f"       pipeline.py pipeline [--stop <phase>]")
        print(f"  Phases: {names}")
        sys.exit(1)

    for flag, var in [("--chunk-index", "_ABD_CHUNK_INDEX"), ("--context-path", "_ABD_CONTEXT_PATH")]:
        if flag in args:
            i = args.index(flag)
            if i + 1 < len(args):
                import os
                os.environ[var] = args.pop(i + 1)
                args.pop(i)

    cmd = args[0].lower()

    if cmd in ("generate", "run"):
        if len(args) < 2:
            print("Usage: pipeline.py generate <phase> [render-diagram]", file=sys.stderr)
            sys.exit(1)
        phase = args[1].lower()
        render_diagram = "render-diagram" in [a.lower() for a in args[2:]]
        _cmd_generate(phase)
        if render_diagram and phase not in _DRAWIO_MANDATORY_PHASES:
            print(f"\n[pipeline] Generating DrawIO diagram for {phase}...", file=sys.stderr)
            _cmd_drawio(phase)

    elif cmd == "scan":
        if len(args) < 2:
            print("Usage: pipeline.py scan <phase>", file=sys.stderr)
            sys.exit(1)
        _cmd_scan(args[1].lower())

    elif cmd == "validate":
        if len(args) < 2:
            print("Usage: pipeline.py validate <phase>", file=sys.stderr)
            sys.exit(1)
        _cmd_validate(args[1].lower())

    elif cmd == "drawio":
        phase_arg = args[1].lower() if len(args) > 1 else None
        _cmd_drawio(phase_arg)

    elif cmd == "pipeline":
        stop = None
        if "--stop" in args:
            i = args.index("--stop")
            if i + 1 < len(args):
                stop = args[i + 1].lower()
        _cmd_pipeline(stop)

    else:
        print(f"Unknown command: '{cmd}'. Use 'generate', 'scan', 'validate', 'drawio', or 'pipeline'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _main()

"""Rule loading by phase. Rules declare phases in frontmatter; no code mapping."""
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
_RULES_DIR = _SKILL_DIR / "rules"

# AI phases that receive rules.
_PHASES_WITH_RULES = frozenset({
    "concept_synthesis", "structure", "behavior", "variation", "consolidate",
})

# Pipeline phase name -> rule phase name (for backward compat)
_PIPELINE_TO_RULE_PHASE = {
    "concept_extraction": "concept_synthesis",
    "assess": "consolidate",
    "finalize": "consolidate",
}


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end < 0:
        return {}
    result = {}
    for line in text[3:end].splitlines():
        s = line.strip()
        if s.startswith("order:"):
            try:
                result["order"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif s.startswith("phases:"):
            rest = line.split(":", 1)[1].strip()
            if rest.startswith("["):
                inner = rest[1 : rest.rfind("]")].strip()
                result["phases"] = [p.strip().strip('"\'') for p in inner.split(",") if p.strip()]
            else:
                result["phases"] = []
    return result


def _phases_from_rule(path: Path) -> list[str] | None:
    """Return phases from frontmatter, or from filename (phase-topic), or None = cross-phase."""
    fm = _parse_frontmatter(path)
    phases = fm.get("phases")
    if phases is not None and phases != []:
        return [p for p in phases if isinstance(p, str)]
    # Infer from filename: synthesis-*, structure-*, behavior-*, variation-*, consolidate-*
    stem = path.stem
    for p in _PHASES_WITH_RULES:
        if stem.startswith(p + "-"):
            return [p]
    return None  # Cross-phase: no phase prefix


def _order_from_rule(path: Path) -> int:
    fm = _parse_frontmatter(path)
    try:
        return int(fm.get("order", 999))
    except (TypeError, ValueError):
        return 999


def rules_for_phase(phase_name: str, skip_tree: bool = False) -> list[Path]:
    """Return rule paths for the given phase.

    Rules match by: phases in frontmatter, or phase-topic filename (synthesis-*, structure-*, etc.).
    Rules with no phase prefix = cross-phase, included for all phases.
    """
    rule_phase = _PIPELINE_TO_RULE_PHASE.get(phase_name, phase_name)
    if rule_phase not in _PHASES_WITH_RULES:
        return []

    artifact_dirs = [_RULES_DIR / "domain", _RULES_DIR / "generated"]
    if not skip_tree:
        artifact_dirs.append(_RULES_DIR / "interaction-tree")

    rules = []
    for artifact_dir in artifact_dirs:
        if not artifact_dir.exists():
            continue
        for rule_file in sorted(artifact_dir.glob("*.md")):
            phases = _phases_from_rule(rule_file)
            if phases is None:
                rules.append(rule_file)  # Cross-phase
            elif rule_phase in phases:
                rules.append(rule_file)

    rules.sort(key=lambda r: (_order_from_rule(r), r.name))
    return rules

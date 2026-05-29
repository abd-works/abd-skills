#!/usr/bin/env python3
"""Plan-shape scanner for `<workspace>/docs/planning/abd-kanban-lead/agile-delivery-plan.md`.

Evaluates seven rules against the saved narrative plan:

  - plan-has-context-inventory
  - plan-risks-are-classified
  - plan-strategy-named
  - plan-runs-have-concrete-outcome
  - plan-is-not-default-six-stage
  - plan-checkpoint-density-matches-risk
  - plan-uses-system-of-work

Each rule has its own `rules/*.md` file with `scanner: plan-shape` in the frontmatter,
so the execute-skill-using-skills-rules runner picks this scanner up via rule frontmatter and also via
flat `scanners/*-scanner.py` discovery.

Exit codes:
  0 — plan passes all rules, or no plan file found (nothing to check)
  1 — plan exists and has at least one violation
  2 — other error (plan path resolution failure)

CLI:
    python abd-kanban-planning/scanners/plan-shape-scanner.py --workspace <workspace>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# -- sys.path bootstrap so we can reuse parse_plan and scanner_bases --------- #

_HERE = Path(__file__).resolve()
_SKILL_ROOT = _HERE.parent.parent  # kanban/skills/abd-kanban-planning
_REPO_ROOT = _HERE.parents[4]
_SKILLS_DIR = _REPO_ROOT / "skills"
_EXECUTE_RULES_SCRIPTS = _SKILLS_DIR / "skill-helpers" / "execute-skill-using-skills-rules" / "scripts"
_TRACK_TASK_SCRIPTS = _SKILLS_DIR / "skill-helpers" / "track_task" / "scripts"

for _p in (_EXECUTE_RULES_SCRIPTS, _TRACK_TASK_SCRIPTS):
    s = str(_p)
    if _p.is_dir() and s not in sys.path:
        sys.path.insert(0, s)

from scanner_bases.simple_rule import SimpleRule  # noqa: E402
from scanner_bases.violation import Violation     # noqa: E402
from generate_delivery_checklist import parse_plan, Run  # noqa: E402


# ---------- shared constants --------------------------------------------------

CANONICAL_STAGES = [
    "shaping",
    "discovery",
    "exploration",
    "specification",
    "engineering",
]

RISK_TYPES = {
    "value": ["value risk"],
    "technical": ["technical risk", "tech risk"],
    "delivery": ["delivery risk"],
    "domain": ["domain risk"],
    "integration": ["integration risk"],
    "ai-model": ["ai-model risk", "ai model risk", "ai_model risk", "model risk"],
}

# Concrete outcome verbs that signal the rationale says more than "mitigate X risk".
OUTCOME_VERBS = {
    "prove", "proven", "proves",
    "map", "mapping", "mapped",
    "establish", "establishes", "established",
    "deliver", "delivers", "delivered",
    "wrap", "wraps", "wrapped",
    "contract", "contracts",
    "spike", "spikes",
    "validate", "validates", "validated",
    "capture", "captures", "captured",
    "decide", "decided", "decides",
    "ship", "ships", "shipped",
    "surface", "surfaces", "surfaced",
    "land", "lands", "landed",
    "implement", "implements", "implemented",
    "refine", "refined", "refines",
    "define", "defines", "defined",
    "integrate", "integrates", "integrated",
    "test", "tests", "tested",
    "cover", "covers", "covered",
    "drain", "drains", "drained",
    "close", "closes", "closed",
    "explore", "explores", "explored",
    "slice", "slices", "sliced",
    "produce", "produces", "produced",
    "fix", "fixes", "fixed",
    "isolate", "isolates", "isolated",
    "learn", "learned", "learns",
}

RISK_ONLY_PATTERN = re.compile(
    r"^\s*(mitigate|reduce|manage|address|tackle)\s+"
    r"(value|technical|delivery|domain|integration|ai[-_\s]?model|model)\s+risk[s]?\.?\s*$",
    re.IGNORECASE,
)

TIGHT_CHECKPOINT_PATTERN = re.compile(
    r"per[-\s](story|ac|test|scenario|ac[/\s]+test)",
    re.IGNORECASE,
)

LOOSE_CHECKPOINT_PATTERN = re.compile(
    r"per[-\s](slice|epic|run)|across[-\s]team|across[-\s]runs|cross[-\s]team",
    re.IGNORECASE,
)

# Multi-increment plans must list every slot — never defer to offset / routine templates.
TEMPLATE_ANTI_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"routine\s+template", re.I), "uses a 'routine template' section instead of explicit run/slot schedules"),
    (re.compile(r"slot\s+pattern\s+per\s+increment", re.I), "defers slots to a reusable 'slot pattern per increment'"),
    (re.compile(r"base\s+slot\s*=", re.I), "uses 'base slot =' offset math instead of listing slot numbers"),
    (re.compile(r"\|\s*Offset\s*\|", re.I), "uses an Offset-column table instead of numbered Slot rows"),
    (re.compile(r"opens?\s+at\s+slot\s*\(est", re.I), "lists estimated 'opens at slot' ranges without full slot tables"),
    (re.compile(r"\|\s*~\d+", re.I), "uses approximate slot numbers (e.g. ~68) without listing every slot"),
    (re.compile(r"≈\s*\d+\s+slots\s+each", re.I), "summarizes slot counts with ≈ instead of listing slots"),
    (re.compile(r"\|\s*\d+\+\s*\|[^\n]*\b[Rr]outine\b", re.I), "uses N+ / Routine rows in the runs summary"),
)

RUN_SECTION_HEADING = re.compile(r"^## Run (\d+)\b[^\n]*$", re.MULTILINE | re.IGNORECASE)
COMBINED_RUNS_HEADING = re.compile(r"^##\s+Runs?\s+(\d+)\s*[\u2013\u2014\-]\s*(\d+)", re.MULTILINE | re.IGNORECASE)
SYSTEM_OF_WORK_HEADING = re.compile(r"^##\s+System of work\b", re.MULTILINE | re.IGNORECASE)
SYSTEM_OF_WORK_REF = re.compile(r"system[_-]of[_-]work", re.IGNORECASE)


# ---------- rule registry ----------------------------------------------------

def _make_rule(name: str) -> SimpleRule:
    rule_md = _SKILL_ROOT / "rules" / f"{name}.md"
    rule_file = str(rule_md) if rule_md.is_file() else f"{name}.md"
    return SimpleRule(name=name, rule_file=rule_file)


RULES = {
    name: _make_rule(name)
    for name in (
        "plan-has-context-inventory",
        "plan-risks-are-classified",
        "plan-strategy-named",
        "plan-runs-have-concrete-outcome",
        "plan-is-not-default-six-stage",
        "plan-checkpoint-density-matches-risk",
        "plan-uses-system-of-work",
    )
}


# ---------- helpers ----------------------------------------------------------

def _yaml_frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip().lower()] = v.strip().strip('"').strip("'")
    return out


def _body_without_frontmatter(text: str) -> str:
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    return text[m.end():] if m else text


def _find_heading(text: str, pattern: str) -> bool:
    rx = re.compile(rf"^#{{1,6}}\s*{pattern}\s*$", re.IGNORECASE | re.MULTILINE)
    return bool(rx.search(text))


def _risks_classified(text: str) -> list[str]:
    low = text.lower()
    found: list[str] = []
    for risk, needles in RISK_TYPES.items():
        for n in needles:
            if n in low:
                found.append(risk)
                break
    return found


def _rationale_is_risk_only(rationale: str) -> bool:
    if not rationale.strip():
        return True
    # Normalize whitespace, strip markdown emphasis
    r = re.sub(r"[*_`]", "", rationale).strip()
    if RISK_ONLY_PATTERN.match(r):
        return True
    low = r.lower()
    # If no outcome verb present, treat as risk-only / vague.
    tokens = re.findall(r"[a-z][a-z\-]+", low)
    if any(tok in OUTCOME_VERBS for tok in tokens):
        return False
    # Fallback: very short lines with only risk words
    risk_words = {"risk", "risks", "value", "technical", "delivery", "domain",
                  "integration", "ai", "model", "mitigate", "reduce", "address"}
    content_tokens = [t for t in tokens if t not in risk_words]
    return len(content_tokens) < 3


def _is_default_six_stage(runs: list[Run]) -> bool:
    if len(runs) != 1:
        return False
    return runs[0].stages == CANONICAL_STAGES


def _any_tight_checkpoint(runs: list[Run]) -> bool:
    for r in runs:
        if TIGHT_CHECKPOINT_PATTERN.search(r.checkpoint_policy or ""):
            return True
    return False


def _run_section_bodies(body: str) -> dict[int, str]:
    sections: dict[int, str] = {}
    matches = list(RUN_SECTION_HEADING.finditer(body))
    for i, match in enumerate(matches):
        run_num = int(match.group(1))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[run_num] = body[start:end]
    return sections


def _multi_increment_delivery(body: str, runs: list[Run]) -> bool:
    """True when the plan is a multi-increment slot schedule (not a summary-only plan)."""
    if any(pattern.search(body) for pattern, _ in TEMPLATE_ANTI_PATTERNS):
        return True
    if re.search(r"\bIncrements?\s+[2-9]\b", body, re.IGNORECASE):
        return True
    if re.search(r"\bIncrement\s+[2-9]\b", body, re.IGNORECASE):
        return True
    if re.search(r"Runs?\s+3[\s\u2013\u2014\-]\s*\d+", body, re.IGNORECASE):
        return True
    if re.search(r"nine\s+increments", body, re.IGNORECASE):
        return True
    if COMBINED_RUNS_HEADING.search(body):
        return True
    if any(n >= 3 for n in _run_section_bodies(body)):
        return True
    return False


def _expected_product_runs(body: str, runs: list[Run]) -> set[int]:
    expected: set[int] = set()
    sections = _run_section_bodies(body)
    expected.update(n for n in sections if n >= 3)
    combined = COMBINED_RUNS_HEADING.search(body)
    if combined:
        start_run = int(combined.group(1))
        end_run = int(combined.group(2))
        expected.update(range(max(3, start_run), end_run + 1))
    if expected:
        return expected
    # Summary-only multi-increment plans must still expand every run explicitly.
    if re.search(r"\bIncrements?\s+[2-9]\b", body, re.IGNORECASE) or re.search(
        r"\bIncrement\s+[2-9]\b", body, re.IGNORECASE
    ):
        for run in runs:
            label = run.label.strip()
            if label.isdigit() and int(label) >= 3:
                expected.add(int(label))
    return expected


# ---------- individual checks -------------------------------------------------

def check_context_inventory(text: str) -> list[Violation]:
    if _find_heading(text, r"context\s+inventory"):
        return []
    # Also accept a section that names both Provided and Missing explicitly
    if re.search(r"\bprovided\b", text, re.IGNORECASE) and (
        re.search(r"\bmissing\b", text, re.IGNORECASE)
        or re.search(r"not\s+yet\s+provided", text, re.IGNORECASE)
    ):
        return []
    return [Violation(
        rule=RULES["plan-has-context-inventory"],
        violation_message=(
            "Plan has no `## Context inventory` section (or equivalent) listing "
            "Provided and Missing context. Reviewers cannot tell whether gaps were "
            "surfaced or silently assumed."
        ),
        severity="error",
    )]


def check_risks_classified(text: str) -> list[Violation]:
    found = _risks_classified(text)
    if found:
        return []
    return [Violation(
        rule=RULES["plan-risks-are-classified"],
        violation_message=(
            "Plan does not tag any of the six named risk types "
            "(value, technical, delivery, domain, integration, AI-model). "
            "Strategy selection and checkpoint tightness have no basis."
        ),
        severity="error",
    )]


def check_strategy_named(text: str) -> list[Violation]:
    # Named strategy file reference OR explicit custom marker
    if re.search(r"strategies/[A-Za-z0-9_-]+\.md", text):
        return []
    if re.search(r"^\s*strategy\s*:\s*custom", text, re.IGNORECASE | re.MULTILINE):
        return []
    if re.search(r"custom\s+strategy", text, re.IGNORECASE):
        return []
    return [Violation(
        rule=RULES["plan-strategy-named"],
        violation_message=(
            "Plan does not name a strategy from `skills/abd-kanban-planning/strategies/` "
            "(filename or slug) and does not mark itself as a custom-strategy candidate. "
            "Cite the strategy file or declare `Strategy: custom` with a proposed slug."
        ),
        severity="error",
    )]


def check_runs_have_concrete_outcome(runs: list[Run]) -> list[Violation]:
    out: list[Violation] = []
    for r in runs:
        if _rationale_is_risk_only(r.rationale):
            msg = (
                f'Run {r.label} rationale is empty or risk-only '
                f'({r.rationale!r}). Name what is proven, delivered, mapped, or decided '
                f'when the run completes — not only the risk type being mitigated.'
            )
            out.append(Violation(
                rule=RULES["plan-runs-have-concrete-outcome"],
                violation_message=msg,
                location=f"run {r.label}",
                severity="error",
            ))
    return out


def check_not_default_six_stage(runs: list[Run], text: str) -> list[Violation]:
    fm = _yaml_frontmatter(text)
    if str(fm.get("trivial", "")).lower() == "true":
        return []
    if not _is_default_six_stage(runs):
        return []
    # Only complain when risks are non-trivial — but since rule 2 runs too, having
    # any risks at all already suggests this is not a trivial engagement.
    risks = _risks_classified(text)
    if not risks:
        # No risks classified and no explicit trivial flag — still report so the
        # user has to either mark trivial or decompose.
        hint = (
            "no risks are classified and no `trivial: true` frontmatter is set. "
            "Mark the plan trivial or decompose the work into risk-ordered runs."
        )
    else:
        hint = (
            f"risks {sorted(set(risks))} are classified. "
            "Decompose the work into risk-ordered runs; a single linear sweep "
            "under-serves any classified risk."
        )
    return [Violation(
        rule=RULES["plan-is-not-default-six-stage"],
        violation_message=(
            "Plan has exactly one run covering all six canonical stages in order; "
            f"{hint}"
        ),
        severity="error",
    )]


def _uses_system_of_work_model(body: str, workspace: Path | None) -> bool:
    if SYSTEM_OF_WORK_HEADING.search(body) or SYSTEM_OF_WORK_REF.search(body):
        return True
    if workspace is not None:
        catalog = workspace / "docs" / "planning" / "delivery-war-room" / "run-catalog.json"
        if catalog.is_file():
            return True
    return False


def check_uses_system_of_work(
    body: str, runs: list[Run], workspace: Path | None = None
) -> list[Violation]:
    if not _multi_increment_delivery(body, runs):
        return []
    if not _uses_system_of_work_model(body, workspace):
        return [Violation(
            rule=RULES["plan-uses-system-of-work"],
            violation_message=(
                "Multi-increment plan must reference system-of-work.json and run-catalog.json "
                "(## System of work section or run-catalog.json on disk). "
                "See `rules/plan-uses-system-of-work.md`."
            ),
            severity="error",
        )]

    for pattern, detail in TEMPLATE_ANTI_PATTERNS:
        if pattern.search(body):
            return [Violation(
                rule=RULES["plan-uses-system-of-work"],
                violation_message=(
                    "Multi-increment plan "
                    f"{detail}. Use a named system of work in "
                    "`system-of-work.json` and `run-catalog.json`; generate slots at run open. "
                    "See `rules/plan-uses-system-of-work.md`."
                ),
                severity="error",
            )]

    expected = _expected_product_runs(body, runs)
    if not expected:
        return []

    sections = _run_section_bodies(body)
    violations: list[Violation] = []

    if COMBINED_RUNS_HEADING.search(body) and not any(n >= 3 for n in sections):
        violations.append(Violation(
            rule=RULES["plan-uses-system-of-work"],
            violation_message=(
                "Plan uses a combined `## Runs 3–N` heading without separate `## Run N` "
                "sections. Split each product run; reference the shared system of work."
            ),
            severity="error",
        ))
        return violations

    for run_num in sorted(expected):
        if sections.get(run_num) is None:
            violations.append(Violation(
                rule=RULES["plan-uses-system-of-work"],
                violation_message=(
                    f"Run {run_num} appears in the runs summary but has no `## Run {run_num}` "
                    "section (scope, stages, system_of_work reference)."
                ),
                location=f"run {run_num}",
                severity="error",
            ))

    return violations


def check_checkpoint_density_matches_risk(runs: list[Run], text: str) -> list[Violation]:
    risks = set(_risks_classified(text))
    needs_tight = bool(risks & {"integration", "ai-model"})
    if not needs_tight:
        return []
    if _any_tight_checkpoint(runs):
        return []
    policies = [r.checkpoint_policy for r in runs if r.checkpoint_policy]
    return [Violation(
        rule=RULES["plan-checkpoint-density-matches-risk"],
        violation_message=(
            "Plan classifies integration or AI-model risk, but no run uses a tight "
            "checkpoint policy (per-story / per-AC / per-test). "
            f"Current policies: {policies!r}. "
            "Tighten the first run against the risky surface; loosen later once "
            "the pattern is proven."
        ),
        severity="error",
    )]


# ---------- main -------------------------------------------------------------

def run_checks(plan_text: str, workspace: Path | None = None) -> list[Violation]:
    body = _body_without_frontmatter(plan_text)
    runs = parse_plan(plan_text)
    violations: list[Violation] = []
    violations += check_context_inventory(body)
    violations += check_risks_classified(body)
    violations += check_strategy_named(body)
    violations += check_runs_have_concrete_outcome(runs)
    violations += check_not_default_six_stage(runs, plan_text)
    violations += check_checkpoint_density_matches_risk(runs, body)
    violations += check_uses_system_of_work(body, runs, workspace)
    return violations


PLANNING_DIR = Path("docs") / "planning"
DELIVERY_LEAD_DIR = PLANNING_DIR / "abd-kanban-lead"


def _resolve_plan_path(workspace: Path) -> Path:
    return workspace / DELIVERY_LEAD_DIR / "agile-delivery-plan.md"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Plan-shape scanner for agile-delivery-plan.md")
    ap.add_argument("--workspace", type=Path, default=Path.cwd(),
                    help="Engagement workspace root (default: cwd).")
    ap.add_argument("--plan", type=Path, default=None,
                    help="Explicit path to the plan file (overrides workspace lookup).")
    ns = ap.parse_args(argv)

    plan_path = ns.plan.resolve() if ns.plan else _resolve_plan_path(ns.workspace.resolve())
    if not plan_path.is_file():
        # No plan yet (Step 2 may not have run). Report nothing; exit 0.
        return 0

    plan_text = plan_path.read_text(encoding="utf-8")
    workspace = ns.workspace.resolve()
    violations = run_checks(plan_text, workspace=workspace)

    if not violations:
        return 0

    for v in violations:
        print(v.to_dict(), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

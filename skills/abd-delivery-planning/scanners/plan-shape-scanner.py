#!/usr/bin/env python3
"""Plan-shape scanner for `<workspace>/agile-delivery-plan.md`.

Evaluates six rules against the saved narrative plan:

  - plan-has-context-inventory
  - plan-risks-are-classified
  - plan-strategy-named
  - plan-runs-have-concrete-outcome
  - plan-is-not-default-six-stage
  - plan-checkpoint-density-matches-risk

Each rule has its own `rules/*.md` file with `scanner: plan-shape` in the frontmatter,
so the execute-skill-using-skills-rules runner picks this scanner up via rule frontmatter and also via
flat `scanners/*-scanner.py` discovery.

Exit codes:
  0 — plan passes all rules, or no plan file found (nothing to check)
  1 — plan exists and has at least one violation
  2 — other error (plan path resolution failure)

CLI:
    python skills/abd-delivery-planning/scanners/plan-shape-scanner.py --workspace <workspace>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# -- sys.path bootstrap so we can reuse parse_plan and scanner_bases --------- #

_HERE = Path(__file__).resolve()
_SKILL_ROOT = _HERE.parent.parent                    # .../skills/abd-delivery-planning
_SKILLS_DIR = _SKILL_ROOT.parent                     # .../skills
_EXECUTE_RULES_SCRIPTS = _SKILLS_DIR / "execute-skill-using-skills-rules" / "scripts"
_TRACK_TASK_SCRIPTS = _SKILLS_DIR / "track_task" / "scripts"

for _p in (_EXECUTE_RULES_SCRIPTS, _TRACK_TASK_SCRIPTS):
    s = str(_p)
    if _p.is_dir() and s not in sys.path:
        sys.path.insert(0, s)

from scanner_bases.simple_rule import SimpleRule  # noqa: E402
from scanner_bases.violation import Violation     # noqa: E402
from generate_delivery_checklist import parse_plan, Run  # noqa: E402


# ---------- shared constants --------------------------------------------------

CANONICAL_STAGES = [
    "discovery",
    "prioritization",
    "exploration",
    "scenarios",
    "acceptance-tests",
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
            "Plan does not name a strategy from `skills/abd-delivery-planning/strategies/` "
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

def run_checks(plan_text: str) -> list[Violation]:
    body = _body_without_frontmatter(plan_text)
    runs = parse_plan(plan_text)
    violations: list[Violation] = []
    violations += check_context_inventory(body)
    violations += check_risks_classified(body)
    violations += check_strategy_named(body)
    violations += check_runs_have_concrete_outcome(runs)
    violations += check_not_default_six_stage(runs, plan_text)
    violations += check_checkpoint_density_matches_risk(runs, body)
    return violations


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Plan-shape scanner for agile-delivery-plan.md")
    ap.add_argument("--workspace", type=Path, default=Path.cwd(),
                    help="Engagement workspace root (default: cwd).")
    ap.add_argument("--plan", type=Path, default=None,
                    help="Explicit path to the plan file (overrides workspace lookup).")
    ns = ap.parse_args(argv)

    plan_path = ns.plan.resolve() if ns.plan else (ns.workspace.resolve() / "agile-delivery-plan.md")
    if not plan_path.is_file():
        # No plan yet (Step 2 may not have run). Report nothing; exit 0.
        return 0

    plan_text = plan_path.read_text(encoding="utf-8")
    violations = run_checks(plan_text)

    if not violations:
        return 0

    for v in violations:
        print(v.to_dict(), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

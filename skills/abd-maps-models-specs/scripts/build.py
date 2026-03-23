#!/usr/bin/env python3
"""
Skill build (see abd-skill-builder/content/parts/library/documentation-standards.md).

1. ``MapsContentAssembler`` — AGENTS.md + agents-staged + per-phase bundles via ``MapsInstructions``
   (role → phase body → ``PHASE_LIBRARY_SLICES`` → ``phase_rules`` / ``every_phase_rules`` → principles / critical quality).
   Canonical built phases: ``content/built/phases/<slug>.md``.
2. Manifest: ``skill-config.json`` (``phase_files``, ``PHASE_LIBRARY_SLICES``, ``phase_rules``, ``every_phase_rules``, ``phase_critical_quality_notes``).
3. Post-merge pipeline: ordered steps from ``skill-config.json`` → ``operator.build_pipeline`` (emitters,
   rule-bound scanners, manifest, rule-example lint). Scanner scripts are tied to governance rules in
   ``rules/scanners.json`` → ``rule_scanner_bindings``. Use ``python scripts/build.py --merge-only`` to refresh
   static **instruction** outputs only (no active workspace fixture).

Source phase files under ``content/parts/phases/`` do **not** embed the solution role; **built** bundles
(``MapsInstructions``) prepend ``solution-analyst-role.md``. AGENTS.md merges process + phase sources with any
embedded solution-role markers stripped from phase bodies.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from maps_assembler import MapsContentAssembler, load_skill_config

_DEFAULT_BUILD_PIPELINE: tuple[str, ...] = (
    "scripts/scanners/context_index_contract.py",
    "scripts/build_phase2_artifacts.py",
    "scripts/scanner_pipeline_outputs.py",
    "scripts/scanners/phase3_story_map_evidence.py",
    "scripts/scanners/chunks_must_be_referenced.py",
    "scripts/generate_context_bundle_manifest.py",
    "scripts/test_rule_examples.py",
)


def _run_script_relative_to_root(rel: str) -> None:
    """Run ``rel`` with cwd at skill root; ``rel`` uses forward slashes, usually ``scripts/...``."""
    r = rel.replace("\\", "/").strip()
    path = ROOT / r
    print(f"--- {r} ---", flush=True)
    subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=True)


def main() -> None:
    p = argparse.ArgumentParser(description="Merge AGENTS + built phases; optional workspace pipeline.")
    p.add_argument(
        "--merge-only",
        action="store_true",
        help="Only write AGENTS.md, agents-staged, content/built/README.md, and content/built/phases/*.md. "
        "Skip validators, scanners, manifest — use when the configured workspace has no solution.conf.",
    )
    ns = p.parse_args()

    cfg = load_skill_config(ROOT)
    asm = MapsContentAssembler(ROOT, cfg)
    asm.write_agents_and_staged()
    asm.write_built_phase_bundles()

    if ns.merge_only:
        print("build.py: merge-only complete (pipeline skipped)")
        return

    op = cfg.get("operator") or {}
    pipeline: list[str] = list(op.get("build_pipeline") or _DEFAULT_BUILD_PIPELINE)
    for step in pipeline:
        _run_script_relative_to_root(step)
    print("build.py: done")


if __name__ == "__main__":
    main()

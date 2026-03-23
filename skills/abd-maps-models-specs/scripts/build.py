#!/usr/bin/env python3
"""
Skill build (see abd-skill-builder/content/parts/library/documentation-standards.md).

1. ``MapsContentAssembler`` — AGENTS.md + agents-staged + per-phase bundles via ``MapsInstructions``
   (operator + YAML-filtered rules + ``PHASE_LIBRARY_SLICES`` + phase body + critical quality).
   Canonical built phases: ``content/parts/phases/built/<slug>.md``; also ``content/built/phases/<slug>.md``.
2. Manifest: ``skill-config.json`` (``phase_files``, ``PHASE_LIBRARY_SLICES``, ``phase_critical_quality_notes``).
3. Post-build pipeline: context contract → Phase 2 → Phase 3 → scanners → manifest → rule examples.
   Use ``python scripts/build.py --merge-only`` to refresh static **instruction** outputs only (no ``test/mm3`` fixture).

Source phase files under ``content/parts/phases/`` do **not** embed the solution role; **built** bundles
(``MapsInstructions``) prepend ``solution-analyst-role.md``. AGENTS.md merges process + phase sources with any
legacy role markers stripped from phase bodies.
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


def _run(name: str) -> None:
    path = SCRIPTS / name
    print(f"--- {name} ---")
    subprocess.run([sys.executable, str(path)], cwd=str(ROOT), check=True)


def main() -> None:
    p = argparse.ArgumentParser(description="Merge AGENTS + built phases; optional workspace pipeline.")
    p.add_argument(
        "--merge-only",
        action="store_true",
        help="Only write AGENTS.md, agents-staged, and content/parts/phases/built (and legacy content/built/phases). "
        "Skip validators, scanners, manifest — use when test/mm3/solution.conf is not set up.",
    )
    ns = p.parse_args()

    cfg = load_skill_config(ROOT)
    asm = MapsContentAssembler(ROOT, cfg)
    asm.write_agents_and_staged()
    asm.write_built_phase_bundles()

    if ns.merge_only:
        print("build.py: merge-only complete (pipeline skipped)")
        return

    _run("scanners/context_index_contract.py")
    _run("build_phase2_artifacts.py")
    _run("scanners/phase3_story_map_evidence.py")
    _run("scanners/chunks_must_be_referenced.py")
    _run("generate_context_bundle_manifest.py")
    _run("test_rule_examples.py")
    print("build.py: done")


if __name__ == "__main__":
    main()

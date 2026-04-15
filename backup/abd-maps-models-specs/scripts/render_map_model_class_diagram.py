#!/usr/bin/env python3
"""
Render map-model-spec.json → class diagram Draw.io (native mxfile).

Uses vendored ``map_model_spec_drawio.py`` (aligned with agile_bots ``map_model_spec_drawio``).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from _config import class_diagram_layout_plan_path, map_model_spec_path, output_dir
from map_model_spec_drawio import write_map_model_class_diagram

_DEFAULT_OUT_NAME = "map-model-class-diagram.drawio"


def _resolved_layout_plan_path(args: argparse.Namespace, out_dir: Path) -> Path | None:
    """Explicit ``--layout-plan``, else default JSON beside spec output if present and allowed."""
    if getattr(args, "no_layout_plan", False):
        return None
    if args.layout_plan is not None:
        p = args.layout_plan.resolve()
        return p if p.is_file() else None
    default = class_diagram_layout_plan_path()
    return default if default.is_file() else None


def main() -> None:
    default_spec = map_model_spec_path()
    od = output_dir()
    default_out = od / _DEFAULT_OUT_NAME

    p = argparse.ArgumentParser(description="Render map-model-spec.json → class diagram Draw.io")
    p.add_argument("--spec", type=Path, default=default_spec, help="Path to map-model-spec.json")
    p.add_argument(
        "--out",
        "--output",
        type=Path,
        dest="out",
        default=default_out,
        help=f"Output .drawio path (default: <output_dir>/{_DEFAULT_OUT_NAME})",
    )
    p.add_argument(
        "--layout-plan",
        type=Path,
        default=None,
        help="Optional class-diagram-layout-plan.json (logical clusters). "
        "Default: <output_dir>/class-diagram-layout-plan.json if that file exists.",
    )
    p.add_argument(
        "--no-layout-plan",
        action="store_true",
        help="Do not load a layout plan (use tier+grid only), ignoring the default file.",
    )
    args = p.parse_args()

    layout_plan = _resolved_layout_plan_path(args, od)
    write_map_model_class_diagram(args.spec, args.out, layout_plan_path=layout_plan)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

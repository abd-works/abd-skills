#!/usr/bin/env python3
"""Build reverse chunk index from a step output JSON.

Reads step1-output-v2.json (or any step output with the same structure)
and produces a chunk_index.json that maps each chunk_id to the concepts,
epics, stories, and modules it was cited in.

This is a derived artifact — always regenerated from the source output JSON.
Never edit it by hand.

Usage:
    python test/experiment/scripts/build_chunk_index.py --input <step_output.json> --output <chunk_index.json>

Defaults (relative to test/experiment/):
    --input   step1-output-v2.json
    --output  step1-chunk-index.json
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def build_index(data: dict) -> dict:
    """Invert the forward index in data into a chunk → {concepts, epics, stories, modules} map."""
    index: dict[str, dict] = defaultdict(lambda: {
        "modules": [],
        "concepts": [],
        "epics": [],
        "stories": [],
    })

    def add(chunk_id: str, key: str, value: str):
        if chunk_id and value not in index[chunk_id][key]:
            index[chunk_id][key].append(value)

    for pair in data.get("modules_and_epics", []):
        module = pair.get("module", {})
        epic = pair.get("epic", {})
        module_name = module.get("name", "")
        epic_name = epic.get("name", "")

        # Module description chunk
        if dc := module.get("description_chunk"):
            add(dc, "modules", module_name)

        # Module-level chunk_ids bucket (identified only — these are primary)
        for cid in pair.get("chunk_ids", {}).get("identified", []):
            add(cid, "modules", module_name)

        # Concepts — use concept.chunk_ids (primary chunks for this concept)
        for concept in module.get("concepts", []):
            cname = concept.get("name", "")
            for cid in concept.get("chunk_ids", []):
                add(cid, "modules", module_name)
                add(cid, "concepts", cname)
            # Also pick up owns_chunk in case chunk_ids was not populated
            if oc := concept.get("owns_chunk"):
                add(oc, "modules", module_name)
                add(oc, "concepts", cname)

        # Epic statement chunk
        if sc := epic.get("statement_chunk"):
            add(sc, "modules", module_name)
            add(sc, "epics", epic_name)

        # Epic pre_condition chunk
        if pc := epic.get("pre_condition_chunk"):
            add(pc, "epics", epic_name)

        # Stories
        for story in epic.get("stories", []):
            sname = story.get("name", "")
            if sc := story.get("chunk"):
                add(sc, "modules", module_name)
                add(sc, "epics", epic_name)
                add(sc, "stories", sname)

    return dict(index)


def main():
    script_dir = Path(__file__).resolve().parent
    experiment_dir = script_dir.parent

    parser = argparse.ArgumentParser(description="Build reverse chunk index from step output JSON.")
    parser.add_argument(
        "--input",
        default=str(experiment_dir / "step1-output-v2.json"),
        help="Path to step output JSON (default: test/experiment/step1-output-v2.json)",
    )
    parser.add_argument(
        "--output",
        default=str(experiment_dir / "step1-chunk-index.json"),
        help="Path to write chunk index JSON (default: test/experiment/step1-chunk-index.json)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    data = json.loads(input_path.read_text(encoding="utf-8"))
    index = build_index(data)

    result = {
        "generated_from": str(input_path.name),
        "note": "Sampled coverage only — built from the chunks read during Step 1 (30% of corpus). Not complete. Re-run after any edit to the source output JSON.",
        "chunk_count": len(index),
        "chunks": index,
    }

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {len(index)} chunk entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

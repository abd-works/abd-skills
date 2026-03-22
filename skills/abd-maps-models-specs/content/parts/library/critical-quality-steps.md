# AI quality: normative rules, scanners, and review

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the AI follows while authoring `mm3_story_map.json`, `map-model-spec.json`, terms/mechanisms JSON, etc. (2) **Checkable expectations** — where this repo ships a **scanner or validator** (`scripts/`), it catches common misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Relying only on “the build passed” while epics are vague labels and stories have no `evidence_chunk_ids[]`.

**Example (correct):** Read the **Rules** section in this bundle, produce artifacts that satisfy the spirit, run **`python scripts/build.py`** (or the relevant script) on your workspace, then **re-read** output against each applicable rule name.

---

## Layer 1 — Generate with rules

While generating or editing phase artifacts:

- Apply **`rules/*.md`** that are inlined into this bundle (and related library docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this repo)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Phase 0 audit, `validate_context_contract.py` (when index exists), Phase 2 artifacts, **`validate_phase3_story_map.py`**, **`scanners/chunks_must_be_referenced.py`**, bundle manifest. |
| Individual scripts | Same modules as above; use when iterating one concern. |

**Example (wrong):** Bulk search-replace in JSON to “fix” names without updating evidence links.

**Example (correct):** Fix violations reported by validators, re-run, keep `chunk_id` / `evidence_chunk_ids[]` honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. wrong decomposition with valid IDs).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **duplication**, **vague epics**, or **concepts without real responsibilities** even when JSON validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — e.g. `validate_phase3_story_map.py`, `chunks_must_be_referenced.py` |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not delegate AI phases to throwaway scripts

**AI phases** mean: read inputs, reason, write/update the artifact files for this skill. Do **not** add one-off merge scripts that splice JSON **outside** the documented pipeline (see **`rules/deepen-approved-tools-only.md`**). Approved automation lives under **`scripts/`** and is documented in **`rules/`** + **`validate-and-manifest-gates.md`**.

**Example (wrong):** “I’ll write `merge_story_map.py` to patch epics without going through the behavioral contract.”

**Example (correct):** Edit `phase3/mm3_story_map.json` (or the generator you were given) so structure and evidence fields match **`behavioral-story-map.md`** and validators.

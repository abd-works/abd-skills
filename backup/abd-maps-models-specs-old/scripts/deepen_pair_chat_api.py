#!/usr/bin/env python3
"""Deepen one module/epic pair via the chat API (OpenAI).

Chunk batching matches classify_chunks.py (~8k tokens of chunk text per batch; oversize chunks alone).

Context model (no silos):
  Each observation batch receives the full JSON for the **current shard** (full module + epic slice
  for that run + chunk_ids). **By default there is one shard** (--split-threshold-chars defaults to 0 =
  never split). **Opt in** to sharding only when compact pair JSON + chunk batches risk exceeding
  model context: set --split-threshold-chars > 0; then the planner walks sub_epics (and nested
  sub_epics), then story batches if still over threshold.

Synthesis returns { "module", "epic" } per shard. Epic subtrees are **grafted** by scope.
With **multiple shards**, each run is pinned to a **sub_epic** path (or story batch under one).
The driver hangs that run’s synthesized **module** under nested **sub_modules** that **mirror** that
path so perspectives stay separated (e.g. two **Attack** concepts under different sub_epics become
two branches, not one forced merge at the module root). Within the **same** branch, concepts still
merge by **name** with gap-fill and **chunk_ids** union. **Whole-pair** shards (empty path) still
merge at the module root. Pair-level **chunk_ids** lists are unioned. Metadata records run boundaries
for Integrate/Harmonize.

Requires: OPENAI_API_KEY (conf/.secrets, same as classify_chunks.py)

Usage:
  python scripts/deepen_pair_chat_api.py --spec test/mm3/maps-models-specs/map-model-spec.json \\
      --chunks test/mm3/context --pair-index 0 --model gpt-4o-mini

  python scripts/deepen_pair_chat_api.py --pair-index 2 --dry-run
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import classify_chunks as cc

CHARS_PER_TOKEN = cc.CHARS_PER_TOKEN
TARGET_CHUNK_TOKENS_PER_BATCH = cc.TARGET_CHUNK_TOKENS_PER_BATCH
OVERSIZE_THRESHOLD = cc.OVERSIZE_THRESHOLD

# Written into map-model-spec.json so humans/tools see reconciliation scope at a glance.
RUN_BOUNDARY_SINGLE = "single_run"
RUN_BOUNDARY_ISOLATED_RUNS = "isolated_runs"
RUN_BOUNDARY_TAG_ISOLATED = "isolated_run"
RUN_BOUNDARY_TAG_SINGLE = "single_run"

# When splitting is off (threshold 0), warn if compact pair JSON is huge — user may need sharding or truncation.
SPLIT_DISABLED_LARGE_PAIR_WARN_CHARS = 350_000


def _pair_json_chars(pair: dict) -> int:
    return len(json.dumps(pair, separators=(",", ":")))


def _pair_chunk_ids(pair: dict) -> list[str]:
    ids: set[str] = set()
    cids = pair.get("chunk_ids") or {}
    ids.update(str(x) for x in cids.get("identified", []))
    ids.update(str(x) for x in cids.get("provisional", []))
    for c in pair.get("module", {}).get("concepts", []):
        ids.update(str(x) for x in c.get("chunk_ids", []))
    return sorted(ids)


def _chunks_in_epic_node(node: dict) -> set[str]:
    out: set[str] = set()
    for st in node.get("stories") or []:
        if isinstance(st, dict):
            out.update(str(x) for x in st.get("chunk_ids") or [])
    for sub in node.get("sub_epics") or []:
        if isinstance(sub, dict):
            out.update(_chunks_in_epic_node(sub))
    return out


def _filter_chunks(all_chunks: list[dict], wanted: set[str]) -> list[dict]:
    by_id = {c["chunk_id"]: c for c in all_chunks}
    return [by_id[cid] for cid in sorted(wanted) if cid in by_id]


def _json_maybe_truncate(label: str, data: str, max_chars: int, log_path: Path | None) -> str:
    if max_chars <= 0 or len(data) <= max_chars:
        return data
    msg = f"WARNING: {label} truncated from {len(data)} to {max_chars} chars (raise --max-pair-json-chars or use a larger-context model)"
    print(msg, file=sys.stderr)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    return data[:max_chars] + "\n/* ... truncated ... */\n"


def _full_pair_json(pair: dict) -> str:
    return json.dumps(pair, indent=2)


def _parse_json_objects(text: str) -> list[dict]:
    return cc.parse_json_objects(text)


def _parse_single_json_object(text: str) -> dict | None:
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _shard_chunk_ids(pair: dict, subtree_chunks: set[str]) -> dict:
    """Pair-level chunk_ids intersected with subtree; concept chunk refs stay on full module."""
    base = pair.get("chunk_ids") or {}
    identified = [x for x in base.get("identified", []) if str(x) in subtree_chunks]
    provisional = [x for x in base.get("provisional", []) if str(x) in subtree_chunks]
    ambiguous = [x for x in base.get("ambiguous", []) if str(x) in subtree_chunks]
    return {"identified": identified, "provisional": provisional, "ambiguous": ambiguous}


def _make_shard_pair(
    full_pair: dict,
    epic_subtree: dict,
    scope_path: list[str],
    parent_epic_name: str,
) -> dict:
    subtree_chunks = _chunks_in_epic_node(epic_subtree)
    epic_root = (full_pair.get("epic") or {}).get("name") or "epic"
    scope_hierarchy = _scope_hierarchy(epic_root, scope_path)
    hierarchy_display = _hierarchy_display(scope_hierarchy)
    shard = {
        k: copy.deepcopy(v)
        for k, v in full_pair.items()
        if k not in ("module", "epic", "chunk_ids")
    }
    shard["module"] = copy.deepcopy(full_pair.get("module", {}))
    shard["epic"] = copy.deepcopy(epic_subtree)
    shard["chunk_ids"] = _shard_chunk_ids(full_pair, subtree_chunks)
    shard["deepen_shard_scope"] = {
        "path": scope_path,
        "epic_root_name": epic_root,
        "scope_hierarchy": scope_hierarchy,
        "hierarchy_display": hierarchy_display,
        "parent_epic_name": parent_epic_name,
        "note": (
            "This JSON is a localized deepen scope: **scope_hierarchy** is epic → sub_epic(s) → … "
            "together; **path** is the graft path (sub_epic names under the pair epic only). "
            "Module is the full module for the pair. Graft this epic subtree back at **path**; "
            "prefer minimal module edits beyond concepts clearly tied to this scope."
        ),
    }
    return shard


def _graft_sub_epic_at_path(epic: dict, path: list[str], replacement: dict) -> dict:
    """Replace the sub_epic at path (names) with replacement subtree."""
    out = copy.deepcopy(epic)
    if not path:
        return copy.deepcopy(replacement)
    subs = out.get("sub_epics")
    if not subs:
        return out
    name = path[0]
    for i, sub in enumerate(subs):
        if isinstance(sub, dict) and sub.get("name") == name:
            if len(path) == 1:
                subs[i] = copy.deepcopy(replacement)
            else:
                subs[i] = _graft_sub_epic_at_path(sub, path[1:], replacement)
            break
    out["sub_epics"] = subs
    return out


def _graft_story_batch(epic: dict, batch_names: set[str], new_stories: list[dict]) -> dict:
    out = copy.deepcopy(epic)
    by_name = {s["name"]: copy.deepcopy(s) for s in new_stories if isinstance(s, dict) and s.get("name")}
    stories = out.get("stories") or []
    new_list = []
    for s in stories:
        if isinstance(s, dict) and s.get("name") in batch_names and s.get("name") in by_name:
            new_list.append(by_name[s["name"]])
        else:
            new_list.append(s)
    out["stories"] = new_list
    return out


def _graft_stories_into_node_at_path(
    epic: dict,
    sub_epic_path: list[str],
    batch_names: set[str],
    new_stories: list[dict],
) -> dict:
    """Graft story updates into the sub_epic at sub_epic_path (names only; no __stories_batch__ segments)."""
    out = copy.deepcopy(epic)
    if not sub_epic_path:
        return _graft_story_batch(out, batch_names, new_stories)
    name = sub_epic_path[0]
    subs = out.get("sub_epics") or []
    for i, sub in enumerate(subs):
        if isinstance(sub, dict) and sub.get("name") == name:
            subs[i] = _graft_stories_into_node_at_path(
                sub, sub_epic_path[1:], batch_names, new_stories
            )
            break
    out["sub_epics"] = subs
    return out


def shard_path_str(path: list[str]) -> str:
    """Relative graft path under the pair epic (sub_epic names only; no epic root)."""
    return " / ".join(path) if path else "(whole pair)"


def _scope_hierarchy(epic_root_name: str, scope_path: list[str]) -> list[dict[str, Any]]:
    """Single ordered chain: epic → sub_epic(s) → … → optional stories_batch."""
    root = epic_root_name or "epic"
    out: list[dict[str, Any]] = [{"level": "epic", "name": root}]
    for p in scope_path:
        if isinstance(p, str) and p.startswith("__stories_batch_"):
            out.append({"level": "stories_batch", "name": p})
        else:
            out.append({"level": "sub_epic", "name": p})
    return out


def _hierarchy_display(segments: list[dict[str, Any]]) -> str:
    return " / ".join(str(s.get("name", "")) for s in segments)


def scope_hierarchy_for_pair(epic_root_name: str, scope_path: list[str]) -> tuple[list[dict[str, Any]], str]:
    h = _scope_hierarchy(epic_root_name, scope_path)
    return h, _hierarchy_display(h)


def _iter_epic_shards(
    pair: dict,
    threshold: int,
    epic: dict,
    path_prefix: list[str],
    parent_name: str,
) -> list[tuple[dict, list[str], str]]:
    """
    Returns list of (shard_pair, scope_path, shard_kind).
    shard_kind: 'sub_epic' | 'stories_batch' | 'whole_epic'
    """
    shards: list[tuple[dict, list[str], str]] = []
    full = copy.deepcopy(pair)
    subs = epic.get("sub_epics") or []
    stories = epic.get("stories") or []

    if subs:
        for sub in subs:
            if not isinstance(sub, dict):
                continue
            name = sub.get("name") or "unnamed_sub_epic"
            spath = path_prefix + [name]
            shard = _make_shard_pair(full, sub, spath, parent_name)
            if _pair_json_chars(shard) > threshold and (sub.get("sub_epics") or []):
                shards.extend(_iter_epic_shards(pair, threshold, sub, spath, name))
            elif _pair_json_chars(shard) > threshold and (sub.get("stories") or []):
                shards.extend(_story_batches_under_node(pair, threshold, sub, spath, parent_name))
            else:
                shards.append((shard, spath, "sub_epic"))
        return shards

    if stories and _pair_json_chars(_make_shard_pair(full, epic, path_prefix, parent_name)) > threshold:
        return _story_batches_under_node(pair, threshold, epic, path_prefix, parent_name)

    return []


def _story_batches_under_node(
    pair: dict,
    threshold: int,
    node: dict,
    path_prefix: list[str],
    parent_name: str,
) -> list[tuple[dict, list[str], str]]:
    """Split flat stories on this node into batches by estimated JSON size."""
    stories = [s for s in (node.get("stories") or []) if isinstance(s, dict)]
    if not stories:
        return []
    batches: list[list[dict]] = []
    current: list[dict] = []
    current_chars = 0
    # Reserve ~40k for module in threshold check
    budget = max(20_000, threshold - 50_000)
    for st in stories:
        c = len(json.dumps(st, separators=(",", ":")))
        if current and current_chars + c > budget:
            batches.append(current)
            current = []
            current_chars = 0
        current.append(st)
        current_chars += c
    if current:
        batches.append(current)

    out: list[tuple[dict, list[str], str]] = []
    full = copy.deepcopy(pair)
    for bi, batch in enumerate(batches):
        mini_epic = copy.deepcopy(node)
        mini_epic["stories"] = copy.deepcopy(batch)
        mini_epic["sub_epics"] = []
        path = path_prefix + [f"__stories_batch_{bi}"]
        shard = _make_shard_pair(full, mini_epic, path, parent_name)
        out.append((shard, path, "stories_batch"))
    return out


def _plan_shards(pair: dict, threshold: int) -> list[tuple[dict, list[str], str]]:
    """If threshold <= 0 or pair under threshold, single whole pair; else expand shards by epic tree."""
    if threshold <= 0 or _pair_json_chars(pair) <= threshold:
        p = copy.deepcopy(pair)
        if "deepen_shard_scope" in p:
            del p["deepen_shard_scope"]
        return [(p, [], "whole_pair")]
    epic = pair.get("epic") or {}
    parent = epic.get("name") or "epic"
    planned = _iter_epic_shards(pair, threshold, epic, [], parent)
    if planned:
        return planned
    # No sub_epics and epic fits in one story batch — still over threshold: single run with warning
    p = copy.deepcopy(pair)
    return [(p, [], "whole_pair_oversize")]


def _call_observations_batch(
    batch: list[dict],
    full_pair_json: str,
    model: str,
    log_path: Path,
    batch_label: str,
    chunk_pct: float,
) -> tuple[list[dict], str]:
    try:
        import openai

        client = openai.OpenAI(api_key=__import__("os").environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        return [], "api_error: openai not installed"

    prompt_chunks = "\n\n---\n\n".join(
        [
            f"CHUNK_ID: {c['chunk_id']}\nSOURCE: {c.get('source', '')}\nTEXT:\n"
            f"{c['text'][: int(len(c['text']) * chunk_pct / 100)]}"
            for c in batch
        ]
    )
    batch_ids = [c["chunk_id"] for c in batch]

    system = (
        "You reconcile rulebook evidence with an existing domain + story map. "
        "Output ONLY one JSON object (no markdown fences). "
        "Never invent a second parallel module or epic — there is exactly one scoped pair below."
    )
    user = f"""## CURRENT DOMAIN + STORY MAP FOR THIS SCOPE (full module + epic subtree for this run)

This JSON is the authoritative state for this deepen pass (see deepen_shard_scope if present).

```json
{full_pair_json}
```

## ACTIVE CHUNK CLUSTER (this API batch only)

Chunk IDs in this cluster: {json.dumps(batch_ids)}

These chunks are **additional evidence** to reconcile against the model above.

**Your job:** *What do we do with this cluster relative to the existing module+epic scope?*

Output one JSON object:
{{
  "batch_chunk_ids": {json.dumps(batch_ids)},
  "observations": [
    {{
      "chunk_id": "string",
      "concept_name": "string or null",
      "targets_node": "optional: sub-epic name / story name if relevant",
      "kind": "property|operation|invariant|interaction|story_step|scenario|defer|note",
      "detail": "string — cite rule text; say how this updates or confirms an existing node",
      "suggested_name": "optional"
    }}
  ]
}}

Rules:
- **Ground every observation** in the cluster chunks and tie to **existing** nodes when possible.
- Do **not** propose a duplicate module, duplicate epic root, or parallel hierarchy — merge into the structure above.
- Every chunk in the cluster should appear at least once (use kind \"note\" if weak).

---

{prompt_chunks}
"""

    try:
        accumulated: list[str] = []
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write(f"\n--- OBS BATCH {batch_label} ---\n")
            log_f.flush()
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=8192,
                temperature=0,
                stream=True,
            )
            for ch in stream:
                delta = ch.choices[0].delta.content if ch.choices else None
                if delta:
                    accumulated.append(delta)
                    log_f.write(delta)
                    log_f.flush()
            log_f.write("\n--- END OBS BATCH ---\n")
        text = "".join(accumulated)
        obj = _parse_single_json_object(text)
        if not obj:
            objs = _parse_json_objects(text)
            obj = objs[0] if objs else None
        if not obj:
            return [], f"parse_error: raw[:300]={text[:300]!r}"
        obs = obj.get("observations", [])
        if not isinstance(obs, list):
            return [], "parse_error: observations not a list"
        return obs, "ok"
    except Exception as e:
        return [], f"api_error: {e}"


def _call_synthesis(
    pair: dict,
    all_observations: list[dict],
    model: str,
    log_path: Path,
    max_pair_chars: int,
    max_obs_chars: int,
    shard_scope: list[str] | None,
    hierarchy_display: str | None = None,
    multi_shard: bool = False,
) -> tuple[dict | None, str]:
    try:
        import openai

        client = openai.OpenAI(api_key=__import__("os").environ.get("OPENAI_API_KEY", ""))
    except ImportError:
        return None, "api_error: openai not installed"

    pair_json = _json_maybe_truncate("synthesis pair JSON", _full_pair_json(pair), max_pair_chars, log_path)
    obs_json = json.dumps(all_observations, indent=2)
    obs_json = _json_maybe_truncate("synthesis observations JSON", obs_json, max_obs_chars, log_path)

    scope_extra = ""
    if shard_scope is not None and len(shard_scope) > 0:
        loc = hierarchy_display or shard_path_str(shard_scope)
        scope_extra = (
            f" **Scoped run:** Deepen only the story-map slice at **{loc}** "
            f"(epic + sub_epic chain together; graft path under epic root = `{shard_path_str(shard_scope)}`). "
            "Return **module** and **epic** for this JSON: **epic** must be the **complete** updated subtree "
            "that will be grafted back (same root shape as input epic). **Expand** module and epic here when "
            "observations and chunks support it — add concepts, sub_modules, stories, and sub_epics as needed; "
            "stay evidence-grounded."
        )

    system = (
        "You output exactly ONE JSON object with keys \"module\" and \"epic\" (optional \"chunk_ids\"). "
        "You are doing **Step 6 deepen**: the job is to **elaborate** the scaffold — **more** structure where "
        "chunks support it, not just tweak strings. "
        "**Epic:** Add structured `stories` (objects with name, trigger, response, chunk_ids, optional "
        "pre_condition/failure_modes). If the input only has `confirming_stories` string names, **materialize** "
        "them into full story objects when you can ground trigger/response in evidence. Add `sub_epics` when "
        "logical groupings exist or to keep ~4–9 children per container. "
        "**Module:** Add concepts, properties, operations; add `sub_modules` when chunks show distinct "
        "collaboration areas within this pair. "
        "**Integrate** observations — deepen, fix, extend. "
        "**Forbidden:** duplicate module definitions, a second epic root, parallel copies of sub-epics or stories. "
        "Preserve **Concept** markers in story text. Respect ~4–9 children per node. "
        "Return the **complete** module object and **complete** epic object after merging (not a patch file)."
        + scope_extra
    )
    user = f"""## FULL CURRENT SCOPE (module + epic + chunk_ids)

```json
{pair_json}
```

## ALL OBSERVATIONS FROM EVERY CHUNK CLUSTER (batched evidence passes)

```json
{obs_json}
```

Produce **one** JSON object:

{{
  "module": {{ ... **complete** deepened module ... }},
  "epic": {{ ... **complete** deepened epic (subtree or full) ... }},
  "chunk_ids": {{ "identified": [], "provisional": [], "ambiguous": [] }}
}}

- **module** and **epic** must be the **full** updated structures for this request, not fragments.
- **Grow the map:** structured **stories** and optional **sub_epics** on the epic; **sub_modules** and more concepts on the module when evidence supports it — that is the point of deepen, not leaving a flat epic.
- Omit **chunk_ids** only if unchanged.
- Do **not** duplicate or fork the hierarchy."""
    if multi_shard:
        user += """

**Multi-shard (isolated run boundaries):** This pair is deepened in **several API passes**, each pinned to a
**sub_epic** slice (see scope). The driver will hang your returned **module** under nested **sub_modules** that
**mirror** that sub_epic path so parallel shards do not flatten everything at the module root — preserve a
sensible **module** for this scope; **epic** is still grafted by path. Within one branch, concepts merge by name
across runs; **chunk_ids** are unioned at pair level."""

    try:
        with open(log_path, "a", encoding="utf-8") as log_f:
            log_f.write("\n--- SYNTHESIS ---\n")
            if shard_scope is not None and len(shard_scope) > 0:
                log_f.write(f"scope_path={shard_scope}\n")
                if hierarchy_display:
                    log_f.write(f"hierarchy_display={hierarchy_display}\n")
            log_f.flush()
            r = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=16384,
                temperature=0,
                response_format={"type": "json_object"},
            )
            text = r.choices[0].message.content or ""
            log_f.write(text[:80000])
            log_f.write("\n--- END SYNTHESIS ---\n")
        obj = json.loads(text)
        if "module" not in obj or "epic" not in obj:
            return None, "parse_error: missing module or epic"
        return obj, "ok"
    except Exception as e:
        return None, f"api_error: {e}"


def _merge_pair_replacement(original_pair: dict, synth: dict) -> dict:
    out = dict(original_pair)
    out["module"] = synth["module"]
    out["epic"] = synth["epic"]
    if "chunk_ids" in synth and isinstance(synth["chunk_ids"], dict):
        out["chunk_ids"] = synth["chunk_ids"]
    out.pop("deepen_shard_scope", None)
    return out


def _concept_name_key(c: dict) -> str:
    return (c.get("name") or "").strip()


def _is_effectively_empty(val: Any) -> bool:
    if val is None:
        return True
    if isinstance(val, str) and not val.strip():
        return True
    if isinstance(val, (list, dict)) and len(val) == 0:
        return True
    return False


def _merge_nested_dict_prefer_base(base_d: dict, inc_d: dict) -> dict:
    """Shallow+recursive dict merge: incoming fills gaps; conflicting non-empty leaves keep base."""
    out = copy.deepcopy(base_d)
    for ik, iv in inc_d.items():
        if iv is None:
            continue
        cur = out.get(ik)
        if isinstance(iv, dict) and isinstance(cur, dict):
            out[ik] = _merge_nested_dict_prefer_base(cur, iv)
        elif _is_effectively_empty(cur):
            out[ik] = copy.deepcopy(iv)
        elif _is_effectively_empty(iv):
            continue
        elif isinstance(iv, list) and isinstance(cur, list):
            if _is_effectively_empty(cur):
                out[ik] = copy.deepcopy(iv)
            # both non-empty lists: keep base (same idea as scalars — no last-shard overwrite)
        else:
            # both non-empty scalars (or mixed non-list types): keep base
            continue
    return out


def _merge_concept_records(base_c: dict, inc_c: dict) -> dict:
    """Merge one concept row by identity (same ``name`` under the same concept list).

    Example: shard 1 and shard 2 both deepen **Attack** — one merged concept; **chunk_ids** unioned.
    Incoming fills **empty** fields only; conflicting non-empty values keep the **base** (earlier shard).
    Nested dicts use the same rule recursively.
    """
    out = copy.deepcopy(base_c)
    for k, v in inc_c.items():
        if k == "chunk_ids":
            a = {str(x) for x in (out.get("chunk_ids") or [])}
            b = {str(x) for x in (v or [])}
            out["chunk_ids"] = sorted(a | b)
        elif v is None:
            continue
        elif isinstance(v, list) and len(v) == 0 and k not in out:
            out[k] = []
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge_nested_dict_prefer_base(out[k], v)
        elif isinstance(v, str) and not v.strip():
            continue
        elif _is_effectively_empty(out.get(k)):
            out[k] = copy.deepcopy(v)
        elif isinstance(v, list) and isinstance(out.get(k), list):
            # both non-empty lists: keep base order/content
            continue
        else:
            # both non-empty scalars: keep base
            continue
    return out


def _merge_concept_lists(base_list: list, inc_list: list) -> list:
    by_name: dict[str, dict] = {}
    order: list[str] = []
    for c in base_list or []:
        if isinstance(c, dict) and _concept_name_key(c):
            k = _concept_name_key(c)
            by_name[k] = copy.deepcopy(c)
            order.append(k)
    for c in inc_list or []:
        if not isinstance(c, dict):
            continue
        k = _concept_name_key(c)
        if not k:
            continue
        if k in by_name:
            by_name[k] = _merge_concept_records(by_name[k], c)
        else:
            by_name[k] = copy.deepcopy(c)
            order.append(k)
    return [by_name[k] for k in order]


def _merge_sub_module_lists(base_list: Any, inc_list: Any) -> list:
    """Merge optional sub_modules (name + concepts + nested sub_modules), by name."""
    base_list = base_list if isinstance(base_list, list) else []
    inc_list = inc_list if isinstance(inc_list, list) else []
    by_name: dict[str, dict] = {}
    order: list[str] = []
    for m in base_list:
        if isinstance(m, dict) and m.get("name"):
            n = m["name"]
            by_name[n] = copy.deepcopy(m)
            order.append(n)
    for m in inc_list:
        if not isinstance(m, dict) or not m.get("name"):
            continue
        n = m["name"]
        if n in by_name:
            by_name[n] = _merge_module_perspectives(by_name[n], m)
        else:
            by_name[n] = copy.deepcopy(m)
            order.append(n)
    return [by_name[n] for n in order]


def _sub_epic_path_for_module_nesting(scope_path: list[str]) -> list[str]:
    """Epic graft path with only sub_epic names; stop before any ``__stories_batch_*`` segment."""
    out: list[str] = []
    for p in scope_path or []:
        if not isinstance(p, str):
            continue
        if p.startswith("__stories_batch_"):
            break
        out.append(p)
    return out


def _nest_synth_module_for_shard_pin(synth_module: dict, sub_epic_path: list[str]) -> dict:
    """
    Multi-shard + pinned scope: place this synthesis ``module`` under nested ``sub_modules``
    mirroring ``sub_epic_path`` (deepest name = leaf that holds concepts from this run).

    Empty ``sub_epic_path`` returns the module unchanged (merge at root — e.g. whole-pair shard).
    """
    if not sub_epic_path:
        return copy.deepcopy(synth_module) if isinstance(synth_module, dict) else {}
    mod = copy.deepcopy(synth_module) if isinstance(synth_module, dict) else {}
    leaf: dict[str, Any] = {
        "name": sub_epic_path[-1],
        "concepts": list(mod.get("concepts") or []),
    }
    sm = mod.get("sub_modules")
    if isinstance(sm, list) and len(sm) > 0:
        leaf["sub_modules"] = copy.deepcopy(sm)
    for key in ("description", "description_chunk"):
        if mod.get(key):
            leaf[key] = copy.deepcopy(mod[key])
    cur: dict[str, Any] = leaf
    for seg in reversed(sub_epic_path[:-1]):
        cur = {
            "name": seg,
            "concepts": [],
            "sub_modules": [cur],
        }
    return {"concepts": [], "sub_modules": [cur]}


def _merge_module_perspectives(base_mod: dict, incoming_mod: dict) -> dict:
    """
    Combine two module JSON views. **Concepts** and **sub_modules** merge by stable **name**
    within the same tree level — so sibling sub_modules (different sub_epic mirrors) keep separate
    namespaces; two runs under the **same** branch still collapse same-named concepts there.
    """
    out = copy.deepcopy(base_mod or {})
    inc = incoming_mod or {}
    if not out.get("name") and inc.get("name"):
        out["name"] = inc["name"]
    if not (out.get("description") or "").strip() and (inc.get("description") or "").strip():
        out["description"] = inc.get("description", "")
    if not out.get("description_chunk") and inc.get("description_chunk"):
        out["description_chunk"] = inc["description_chunk"]
    out["concepts"] = _merge_concept_lists(out.get("concepts") or [], inc.get("concepts") or [])
    if (out.get("sub_modules") is not None) or (inc.get("sub_modules") is not None):
        out["sub_modules"] = _merge_sub_module_lists(
            out.get("sub_modules"), inc.get("sub_modules")
        )
    for key in inc:
        if key in ("name", "description", "description_chunk", "concepts", "sub_modules"):
            continue
        if key not in out or out.get(key) in (None, "", [], {}):
            out[key] = copy.deepcopy(inc[key])
    return out


def _merge_pair_chunk_ids(base: dict | None, inc: dict | None) -> dict:
    out: dict[str, list] = {
        "identified": list((base or {}).get("identified") or []),
        "provisional": list((base or {}).get("provisional") or []),
        "ambiguous": list((base or {}).get("ambiguous") or []),
    }
    inc = inc or {}
    for k in out:
        seen = {str(x) for x in out[k]}
        for x in inc.get(k) or []:
            xs = str(x)
            if xs not in seen:
                out[k].append(x)
                seen.add(xs)
    return out


def _deepen_one_shard(
    pair_shard: dict,
    pair_chunks: list[dict],
    model: str,
    log_path: Path,
    chunk_pct: float,
    max_pair_chars: int,
    max_obs_chars: int,
    shard_label: str,
    scope_path: list[str],
    epic_root_name: str,
    multi_shard: bool,
) -> tuple[dict | None, dict[str, Any]]:
    """Run observation batches + synthesis for one shard. Returns (synth dict or None, stats)."""
    wanted = set(_pair_chunk_ids(pair_shard))
    shard_chunk_files = _filter_chunks(pair_chunks, wanted) if wanted else pair_chunks
    if not shard_chunk_files and pair_chunks:
        shard_chunk_files = pair_chunks

    batch_size, avg_tokens = cc.estimate_batch_size(shard_chunk_files, chunk_pct)
    batches = cc.make_batches(shard_chunk_files, batch_size)

    scope_hierarchy, hierarchy_display = scope_hierarchy_for_pair(epic_root_name, scope_path)
    stats: dict[str, Any] = {
        "shard_label": shard_label,
        "scope_path": scope_path,
        "epic_root_name": epic_root_name,
        "scope_hierarchy": scope_hierarchy,
        "hierarchy_display": hierarchy_display,
        "pair_json_chars": _pair_json_chars(pair_shard),
        "chunk_files": len(shard_chunk_files),
        "batches": len(batches),
        "observation_count": 0,
        "errors": 0,
    }

    full_pair_for_batches = _json_maybe_truncate(
        f"observation shard {shard_label}",
        _full_pair_json(pair_shard),
        max_pair_chars,
        log_path,
    )
    all_observations: list[dict] = []
    for i, batch in enumerate(batches, 1):
        label = f"{shard_label} obs {i}/{len(batches)}"
        obs, status = _call_observations_batch(
            batch, full_pair_for_batches, model, log_path, label, chunk_pct
        )
        if status != "ok":
            stats["errors"] += 1
        else:
            all_observations.extend(obs)
    stats["observation_count"] = len(all_observations)

    synth, status = _call_synthesis(
        pair_shard,
        all_observations,
        model,
        log_path,
        max_pair_chars,
        max_obs_chars,
        scope_path if scope_path else None,
        hierarchy_display if scope_path else None,
        multi_shard=multi_shard,
    )
    stats["synthesis_status"] = status
    if status != "ok" or not synth:
        return None, stats
    return synth, stats


def main() -> int:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description=(
            "Deepen one module/epic pair via chat API. Default: one whole pair (no sharding). "
            "Optional: --split-threshold-chars > 0 only when context limits force sub_epic/story batches."
        )
    )
    parser.add_argument("--spec", default=str(base.parent / "map-model-spec.json"))
    parser.add_argument("--chunks", default=str(base.parent / "test/mm3/context"))
    parser.add_argument("--pair-index", type=int, required=True)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--chunk-pct", type=float, default=100.0)
    parser.add_argument(
        "--max-pair-json-chars",
        type=int,
        default=0,
        help="Max chars of pair JSON per API call; 0 = no limit",
    )
    parser.add_argument(
        "--max-obs-chars",
        type=int,
        default=0,
        help="Max chars of observations JSON in synthesis; 0 = no limit",
    )
    parser.add_argument(
        "--split-threshold-chars",
        type=int,
        default=0,
        help=(
            "Max compact JSON chars for one shard; above this, split by sub_epic / nested / story batches. "
            "Default 0 = never split (single whole pair — use only sharding when you hit context limits). "
            "Example when needed: 120000–250000 depending on model and chunk volume."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    chunk_pct = min(100.0, max(1.0, args.chunk_pct))
    log_path = base / "deepen_pair_chat_api.log"

    if not spec_path.exists():
        print(f"ERROR: spec not found: {spec_path}")
        return 1

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    pairs = spec.get("modules_and_epics", [])
    if args.pair_index < 0 or args.pair_index >= len(pairs):
        print(f"ERROR: pair-index {args.pair_index} out of range (0..{len(pairs)-1})")
        return 1

    pair = pairs[args.pair_index]
    epic_root_name = (pair.get("epic") or {}).get("name") or "epic"
    wanted = set(_pair_chunk_ids(pair))
    if not wanted:
        print("ERROR: no chunk_ids on this pair (run concept classification / Step 5 first).")
        return 1

    try:
        all_chunks = cc.load_chunks(args.chunks)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}")
        return 1

    pair_chunks = _filter_chunks(all_chunks, wanted)
    if not pair_chunks:
        print(f"ERROR: no chunk files found for {len(wanted)} ids (chunks path: {args.chunks})")
        return 1

    plan = _plan_shards(pair, args.split_threshold_chars)
    multi_shard = len(plan) > 1

    pair_chars = _pair_json_chars(pair)
    if args.split_threshold_chars <= 0 and pair_chars > SPLIT_DISABLED_LARGE_PAIR_WARN_CHARS:
        print(
            f"WARNING: compact pair JSON is {pair_chars} chars with splitting disabled (threshold 0). "
            "If API calls fail or truncate, set --split-threshold-chars to a positive limit or use "
            "--max-pair-json-chars / a larger-context model.",
            file=sys.stderr,
        )

    print(f"Pair index:      {args.pair_index}")
    print(f"Module:          {pair.get('module', {}).get('name', '?')}")
    print(f"Pair JSON chars: {pair_chars} (compact)")
    print(f"Split threshold: {args.split_threshold_chars or 'disabled (0)'}")
    print(f"Planned shards:  {len(plan)}")
    for i, (sh, path, kind) in enumerate(plan, 1):
        _, hd = scope_hierarchy_for_pair(epic_root_name, path)
        print(
            f"  Shard {i}: kind={kind} hierarchy={hd!r} graft_path={shard_path_str(path)!r} "
            f"json_chars={_pair_json_chars(sh)}"
        )

    if args.dry_run:
        for i, (sh, _, _) in enumerate(plan, 1):
            batch_size, avg_tokens = cc.estimate_batch_size(
                _filter_chunks(pair_chunks, set(_pair_chunk_ids(sh))) or pair_chunks, chunk_pct
            )
            batches = cc.make_batches(
                _filter_chunks(pair_chunks, set(_pair_chunk_ids(sh))) or pair_chunks, batch_size
            )
            print(f"  Shard {i} chunk batches: {len(batches)} (~{avg_tokens} tok/chunk)")
        return 0

    if not __import__("os").environ.get("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not set (use conf/.secrets like classify_chunks)")
        return 1

    log_path.write_text(
        f"deepen_pair_chat_api\n"
        f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"spec={spec_path} pair_index={args.pair_index} model={args.model} chunk_pct={chunk_pct}\n"
        f"split_threshold_chars={args.split_threshold_chars} planned_shards={len(plan)}\n"
        f"{'='*60}\n",
        encoding="utf-8",
    )

    t0 = time.time()
    working = copy.deepcopy(pair)
    isolated_runs: list[dict[str, Any]] = []
    total_errors = 0

    for si, (shard_pair, scope_path, shard_kind) in enumerate(plan, 1):
        shard_label = f"shard{si}/{len(plan)}"
        _, hd0 = scope_hierarchy_for_pair(epic_root_name, scope_path)
        print(f"  Deepening {shard_label} ({hd0})...")
        synth, stats = _deepen_one_shard(
            shard_pair,
            pair_chunks,
            args.model,
            log_path,
            chunk_pct,
            args.max_pair_json_chars,
            args.max_obs_chars,
            shard_label,
            scope_path,
            epic_root_name,
            multi_shard,
        )
        total_errors += stats.get("errors", 0)
        isolated_runs.append(
            {
                "run_boundary_tag": (
                    RUN_BOUNDARY_TAG_ISOLATED
                    if len(plan) > 1
                    else RUN_BOUNDARY_TAG_SINGLE
                ),
                "run_boundary_index": si,
                "shard_index": si,
                "kind": shard_kind,
                "epic_root_name": stats.get("epic_root_name"),
                "scope_path": scope_path,
                "scope_hierarchy": stats.get("scope_hierarchy"),
                "hierarchy_display": stats.get("hierarchy_display"),
                "scope_display": stats.get("hierarchy_display"),
                "pair_json_chars": stats.get("pair_json_chars"),
                "observation_batches": stats.get("batches"),
                "observation_count": stats.get("observation_count"),
                "synthesis_status": stats.get("synthesis_status"),
            }
        )
        if not synth:
            print(f"    FAIL: {stats.get('synthesis_status')}")
            return 1

        if not multi_shard:
            if not scope_path:
                working = _merge_pair_replacement(working, synth)
            elif scope_path[-1].startswith("__stories_batch_"):
                parent_sub_epic_path = scope_path[:-1]
                batch_names = {
                    s["name"]
                    for s in (shard_pair.get("epic") or {}).get("stories") or []
                    if isinstance(s, dict) and s.get("name")
                }
                working["module"] = synth["module"]
                working["epic"] = _graft_stories_into_node_at_path(
                    working.get("epic", {}),
                    parent_sub_epic_path,
                    batch_names,
                    synth["epic"].get("stories") or [],
                )
                if "chunk_ids" in synth:
                    working["chunk_ids"] = synth["chunk_ids"]
            else:
                graft_path = scope_path[:]
                working["module"] = synth["module"]
                working["epic"] = _graft_sub_epic_at_path(
                    working.get("epic", {}), graft_path, synth["epic"]
                )
                if "chunk_ids" in synth:
                    working["chunk_ids"] = synth["chunk_ids"]
        else:
            # Isolated runs: nest each shard's module under sub_modules mirroring the sub_epic pin, then merge.
            pin = _sub_epic_path_for_module_nesting(scope_path)
            synth_mod = synth.get("module", {})
            to_merge = (
                _nest_synth_module_for_shard_pin(synth_mod, pin)
                if pin
                else (copy.deepcopy(synth_mod) if isinstance(synth_mod, dict) else {})
            )
            working["module"] = _merge_module_perspectives(working.get("module", {}), to_merge)
            if not scope_path:
                working["epic"] = synth["epic"]
            elif scope_path[-1].startswith("__stories_batch_"):
                parent_sub_epic_path = scope_path[:-1]
                batch_names = {
                    s["name"]
                    for s in (shard_pair.get("epic") or {}).get("stories") or []
                    if isinstance(s, dict) and s.get("name")
                }
                working["epic"] = _graft_stories_into_node_at_path(
                    working.get("epic", {}),
                    parent_sub_epic_path,
                    batch_names,
                    synth["epic"].get("stories") or [],
                )
            else:
                working["epic"] = _graft_sub_epic_at_path(
                    working.get("epic", {}), scope_path[:], synth["epic"]
                )
            if "chunk_ids" in synth and isinstance(synth["chunk_ids"], dict):
                working["chunk_ids"] = _merge_pair_chunk_ids(
                    working.get("chunk_ids"), synth["chunk_ids"]
                )

        working.pop("deepen_shard_scope", None)

    new_pairs = list(pairs)
    new_pairs[args.pair_index] = working
    out_spec = dict(spec)
    out_spec["modules_and_epics"] = new_pairs

    reconciliation_hint = (
        "Single pass; no isolated shards."
        if len(plan) <= 1
        else (
            f"{len(plan)} isolated deepen runs (see isolated_runs). "
            "Each shard's `module` is nested under `sub_modules` mirroring its sub_epic pin; "
            "cross-branch duplicates and global module coherence may still need "
            "Integrate/Harmonize (or dedicated reconciliation)."
        )
    )

    out_spec["deepen_pair_chat_api_run"] = {
        "pair_index": args.pair_index,
        "epic_root_name": epic_root_name,
        "model": args.model,
        "chunk_pct": chunk_pct,
        "pair_chunk_count": len(pair_chunks),
        "elapsed_seconds": round(time.time() - t0, 2),
        "observation_batch_errors": total_errors,
        "log": str(log_path),
        "full_pair_context": True,
        "max_pair_json_chars": args.max_pair_json_chars,
        "max_obs_chars": args.max_obs_chars,
        "split_threshold_chars": args.split_threshold_chars,
        "planned_shard_count": len(plan),
        "multi_shard": len(plan) > 1,
        # Tag for downstream reconciliation: one API deepen vs several isolated run boundaries.
        "run_boundary": (
            RUN_BOUNDARY_ISOLATED_RUNS if len(plan) > 1 else RUN_BOUNDARY_SINGLE
        ),
        "isolated_runs": isolated_runs,
        "reconciliation_hint": reconciliation_hint,
        "module_merge_policy": (
            "isolated_perspectives_merge_sub_epic_sub_modules"
            if len(plan) > 1
            else "single_pass_replace"
        ),
        "module_merge_note": (
            "Multiple shards: each run is pinned to a **sub_epic** path; the driver nests that run’s `module` "
            "payload under **sub_modules** mirroring that path (story batches use the parent sub_epic chain), "
            "then merges by **sub_module** / **concept** name. Pair-level **chunk_ids** are unioned; **epic** is "
            "grafted by scope. **Integrate/Harmonize** may still reconcile cross-branch duplicates."
            if len(plan) > 1
            else None
        ),
    }

    spec_path.write_text(json.dumps(out_spec, indent=2), encoding="utf-8")
    print(f"  Wrote {spec_path} in {time.time()-t0:.1f}s (obs batch errors: {total_errors})")
    print(f"  Reconciliation: {reconciliation_hint}")
    print("  Next: review diff, run scanners, python scripts/build_chunk_index.py, refresh map-model-spec.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

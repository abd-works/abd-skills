# AGENTS — ace-foo

## Process

# Process — ace-foo

**Pipeline:** [Workspace and config](phases/workspace-and-config.md) → Run Operator (structural checks)

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [Workspace and config](phases/workspace-and-config.md) | You set **`skill_path`** vs **`skill_workspace`** and edit **`conf/abd-config.json`** so runs are unambiguous. | Human / AI | Skill directory | **`conf/abd-config.json`** with **`active_skill_workspace`** | `python scripts/generate.py --phase workspace-and-config` |
| 3 | Run Operator | Compile check on **`scripts/`**, then **`build.py`**, then scanners listed in **`skill-config.json`**. | Code | **`skill-config.json`**; sources under **`content/parts/`** | Exit **0**; **`AGENTS.md`** current | `python scripts/build.py` · `python scripts/scanner_smoke.py` |

Routing details for **`conf/`** keys: see **[Workspace and config](phases/workspace-and-config.md)** — not repeated here.


# Workspace and config

This doc is **Workspace and config** in [`../process.md`](../process.md).

## Purpose

Make **`skill_workspace`** and **`conf/abd-config.json`** unambiguous for this example skill.

## What you must do

1. Open **`conf/abd-config.json`** at the skill root.
2. Set **`active_skill_workspace`** to the root of the tree you are working on, or **`.`** if the skill folder is the workspace.
3. Optionally add paths under **`known_skill_workspaces`** for other roots you switch between.

## How you know you succeeded

You can name **`skill_path`** (this install) vs **`skill_workspace`** (the target project) without guessing from prose alone.

## Library

# Core Definitions


# Intro


# Output Structure


# Shaping Process


# Validation


# Script Invocation

How to call scripts (params, when, what to expect).



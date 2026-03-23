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

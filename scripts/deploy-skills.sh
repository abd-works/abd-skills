#!/usr/bin/env bash
#
# deploy-skills.sh — Deploy capability family packages to Cursor or VS Code
#
# SYNOPSIS
#   ./deploy-skills.sh [cursor|vscode] [deploy-root] [package]
#
# DESCRIPTION
#   Self-contained deploy script (bash + python3 — no jq needed).
#   Deploy root resolves from explicit arg → .code-workspace file walk → repo root.
#   Instructions are sourced from *.instructions.md and deployed to either IDE:
#     - vscode: copied to .github/*.instructions.md
#     - cursor: copied to .cursor/rules/*.mdc (extension renamed)
#
# PARAMETERS
#   ide         Target IDE: cursor or vscode. Default: cursor.
#   DeployRoot  Explicit workspace root. Auto-resolved when omitted.
#                 Resolution order: arg → find *.code-workspace → fallback to repo root.
#   Package     Qualified package name or "all" (default: all).
#               Format: "<top>/<name>" for family packages
#               (e.g. "practices/story-driven-delivery")
#               or bare name for flat collections ("utilities", "others").
#

set -euo pipefail

# --- Resolve repo root (script lives in scripts/) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Defaults ---
IDE="${1:-cursor}"
DEPLOY_ROOT="${2:-}"
PACKAGE="${3:-all}"

# ---------------------------------------------------------------------------
# JSON helper — uses python3 (already a project dependency via skills.sh)
# ---------------------------------------------------------------------------
json_get() {
    local file="$1" query="$2"
    python3 - "$file" "$query" <<'PYEOF'
import json, sys
with open(sys.argv[1], encoding='utf-8-sig') as f:
    data = json.load(f)
keys = sys.argv[2].split('.')
val = data
for k in keys:
    val = val[k]
if val is None:
    sys.exit(1)
print(val)
PYEOF
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
ensure_directory() {
    local path="$1"
    if [[ ! -d "$path" ]]; then
        mkdir -p "$path"
    fi
}

remove_and_copy_directory() {
    local source="$1" destination="$2"
    if [[ -d "$destination" ]]; then
        rm -rf "$destination"
    fi
    ensure_directory "$(dirname "$destination")"
    cp -a "$source" "$destination"
}

merge_directory_contents() {
    local source_dir="$1" destination_dir="$2"
    if [[ ! -d "$source_dir" ]]; then return; fi
    ensure_directory "$destination_dir"
    # Copy all children (not the source dir itself) into destination
    find "$source_dir" -mindepth 1 -maxdepth 1 -exec cp -a {} "$destination_dir/" \; 2>/dev/null || true
}

get_workspace_deploy_root_from_pwd() {
    local start_path="$1"
    local current
    current="$(cd "$start_path" && pwd)"
    while true; do
        local ws_file
        ws_file=$(find "$current" -maxdepth 1 -name '*.code-workspace' -type f 2>/dev/null | head -1)
        if [[ -n "$ws_file" ]]; then
            echo "$current"
            return 0
        fi
        local parent
        parent="$(dirname "$current")"
        if [[ -z "$parent" || "$parent" == "$current" ]]; then break; fi
        current="$parent"
    done
    return 1
}

resolve_deploy_root() {
    local explicit_root="$1" repo_root="$2"
    if [[ -n "$explicit_root" ]]; then
        # Ensure the directory exists, then resolve to absolute path
        mkdir -p "$explicit_root"
        cd "$explicit_root" && pwd
        return 0
    fi
    local from_workspace
    from_workspace=$(get_workspace_deploy_root_from_pwd "$(pwd)" 2>/dev/null) || true
    if [[ -n "$from_workspace" ]]; then echo "$from_workspace"; return 0; fi
    echo "$repo_root"
}

KNOWN_PACKAGE_FOLDERS=(
    skills agents content reference lib instructions prompts
    vscode rules scanners templates scripts ide-files inputs
    tests test catalog retired
)

is_known_folder() {
    local name="$1"
    for known in "${KNOWN_PACKAGE_FOLDERS[@]}"; do
        if [[ "$known" == "$name" ]]; then return 0; fi
    done
    return 1
}

get_package_roots() {
    local repo_root="$1"
    local roots=()

    # Family packages: each subdir of these tops is a package root
    for top in practices foundational stages; do
        local top_path="$repo_root/$top"
        if [[ ! -d "$top_path" ]]; then continue; fi
        for dir in "$top_path"/*/; do
            [[ -d "$dir" ]] || continue
            local name="$top/$(basename "$dir")"
            roots+=("$name|$dir")
        done
    done

    # Flat collections: the top-level dir itself is the package root
    for flat in utilities others; do
        local p="$repo_root/$flat"
        if [[ -d "$p" ]]; then
            roots+=("$flat|$p")
        fi
    done

    printf '%s\n' "${roots[@]}"
}

merge_vscode_files() {
    local source_dir="$1" deploy_root="$2"
    local vscode_dst="$deploy_root/.vscode"
    ensure_directory "$vscode_dst"

    # Merge tasks.json — combine tasks[] and inputs[] arrays
    local src_tasks="$source_dir/tasks.json"
    if [[ -f "$src_tasks" ]]; then
        local dst_tasks="$vscode_dst/tasks.json"
        if [[ -f "$dst_tasks" ]]; then
            python3 - "$src_tasks" "$dst_tasks" <<'PYEOF'
import json, sys

src_tasks, dst_tasks = sys.argv[1], sys.argv[2]

with open(src_tasks, encoding='utf-8-sig') as f:
    incoming = json.load(f)
with open(dst_tasks, encoding='utf-8-sig') as f:
    existing = json.load(f)

merged = {'version': '2.0.0'}
all_tasks = (existing.get('tasks') or []) + (incoming.get('tasks') or [])
all_inputs = (existing.get('inputs') or []) + (incoming.get('inputs') or [])

seen_labels = set()
deduped_tasks = []
for t in all_tasks:
    l = t.get('label')
    if l and l not in seen_labels:
        seen_labels.add(l)
        deduped_tasks.append(t)
merged['tasks'] = deduped_tasks

seen_ids = set()
deduped_inputs = []
for i in all_inputs:
    id_ = i.get('id')
    if id_ and id_ not in seen_ids:
        seen_ids.add(id_)
        deduped_inputs.append(i)
if deduped_inputs:
    merged['inputs'] = deduped_inputs

with open(dst_tasks, 'w') as f:
    json.dump(merged, f, indent=2)
    f.write('\n')
PYEOF
        else
            cp "$src_tasks" "$dst_tasks"
        fi
    fi

    # Merge settings.json — shallow key merge (incoming wins)
    local src_settings="$source_dir/settings.json"
    if [[ -f "$src_settings" ]]; then
        local dst_settings="$vscode_dst/settings.json"
        if [[ -f "$dst_settings" ]]; then
            python3 - "$src_settings" "$dst_settings" <<'PYEOF'
import json, sys

src_settings, dst_settings = sys.argv[1], sys.argv[2]

with open(src_settings, encoding='utf-8-sig') as f:
    incoming = json.load(f)
with open(dst_settings, encoding='utf-8-sig') as f:
    existing = json.load(f)

existing.update(incoming)

with open(dst_settings, 'w') as f:
    json.dump(existing, f, indent=2)
    f.write('\n')
PYEOF
        else
            cp "$src_settings" "$dst_settings"
        fi
    fi
}

deploy_package() {
    local package_root="$1" deploy_root="$2" ide="$3"

    local github_dst="$deploy_root/.github"
    local github_instructions_dst="$github_dst/instructions"
    local github_prompts_dst="$github_dst/prompts"
    local github_skills_dst="$github_dst/skills"
    local github_agents_dst="$github_dst/agents"

    local cursor_root="$deploy_root/.cursor"
    local skills_dst="$cursor_root/skills"
    local agents_dst="$cursor_root/agents"
    local content_dst="$cursor_root/content"
    local reference_dst="$cursor_root/reference"
    local lib_dst="$cursor_root/lib"
    local rules_dst="$cursor_root/rules"
    local commands_dst="$cursor_root/commands"

    # --- Standard layout: skills/ subdirectory ---
    local skills_src="$package_root/skills"
    if [[ -d "$skills_src" ]]; then
        for candidate_dir in "$skills_src"/*/; do
            [[ -d "$candidate_dir" ]] || continue
            if [[ -f "$candidate_dir/SKILL.md" ]]; then
                if [[ "$ide" == "vscode" ]]; then
                    remove_and_copy_directory "$candidate_dir" "$github_skills_dst/$(basename "$candidate_dir")"
                else
                    remove_and_copy_directory "$candidate_dir" "$skills_dst/$(basename "$candidate_dir")"
                fi
            else
                # Grouping folder (e.g. supporting/) — recurse one level
                for skill_dir in "$candidate_dir"*/; do
                    [[ -d "$skill_dir" ]] || continue
                    if [[ -f "$skill_dir/SKILL.md" ]]; then
                        if [[ "$ide" == "vscode" ]]; then
                            remove_and_copy_directory "$skill_dir" "$github_skills_dst/$(basename "$skill_dir")"
                        else
                            remove_and_copy_directory "$skill_dir" "$skills_dst/$(basename "$skill_dir")"
                        fi
                    fi
                done
            fi
        done
    fi

    # --- Flat layout: skills directly in package root (no skills/ wrapper) ---
    for flat_skill_dir in "$package_root"/*/; do
        [[ -d "$flat_skill_dir" ]] || continue
        local dir_name
        dir_name=$(basename "$flat_skill_dir")
        if ! is_known_folder "$dir_name" && [[ -f "$flat_skill_dir/SKILL.md" ]]; then
            if [[ "$ide" == "vscode" ]]; then
                remove_and_copy_directory "$flat_skill_dir" "$github_skills_dst/$dir_name"
            else
                remove_and_copy_directory "$flat_skill_dir" "$skills_dst/$dir_name"
            fi
        fi
    done

    # --- Agents ---
    local agents_src="$package_root/agents"
    if [[ -d "$agents_src" ]]; then
        for agent_dir in "$agents_src"/*/; do
            [[ -d "$agent_dir" ]] || continue
            if [[ -f "$agent_dir/AGENT.md" || -f "$agent_dir/AGENTS.md" ]]; then
                if [[ "$ide" == "vscode" ]]; then
                    remove_and_copy_directory "$agent_dir" "$github_agents_dst/$(basename "$agent_dir")"
                else
                    remove_and_copy_directory "$agent_dir" "$agents_dst/$(basename "$agent_dir")"
                fi
            fi
        done
    fi

    # --- Content, reference, lib (cursor only) ---
    if [[ "$ide" != "vscode" ]]; then
        merge_directory_contents "$package_root/content" "$content_dst"
        merge_directory_contents "$package_root/reference" "$reference_dst"
        if [[ -d "$package_root/lib" ]]; then
            merge_directory_contents "$package_root/lib" "$lib_dst"
        fi
    fi

    # --- Instructions ---
    local instructions_src="$package_root/instructions"
    if [[ -d "$instructions_src" ]]; then
        find "$instructions_src" -maxdepth 1 -name '*.instructions.md' -type f | while IFS= read -r file; do
            if [[ "$ide" == "vscode" ]]; then
                ensure_directory "$github_instructions_dst"
                cp "$file" "$github_instructions_dst/$(basename "$file")"
            else
                ensure_directory "$rules_dst"
                local base
                base=$(basename "$file" .instructions.md)
                cp "$file" "$rules_dst/$base.mdc"
            fi
        done
    fi

    # --- Prompts ---
    local prompts_src="$package_root/prompts"
    if [[ -d "$prompts_src" ]]; then
        find "$prompts_src" -maxdepth 1 -name '*.prompt.md' -type f | while IFS= read -r file; do
            if [[ "$ide" == "vscode" ]]; then
                ensure_directory "$github_prompts_dst"
                cp "$file" "$github_prompts_dst/$(basename "$file")"
            else
                ensure_directory "$commands_dst"
                cp "$file" "$commands_dst/$(basename "$file")"
            fi
        done
    fi

    # --- VSCode config files ---
    local vscode_src="$package_root/vscode"
    if [[ -d "$vscode_src" ]]; then
        merge_vscode_files "$vscode_src" "$deploy_root"
    fi
}

# =========================================================================
# MAIN
# =========================================================================

resolved_deploy_root=$(resolve_deploy_root "$DEPLOY_ROOT" "$REPO_ROOT")
ensure_directory "$resolved_deploy_root"

# Collect package roots
package_entries=()
while IFS= read -r entry; do
    package_entries+=("$entry")
done < <(get_package_roots "$REPO_ROOT")

if [[ ${#package_entries[@]} -eq 0 ]]; then
    echo "Error: No package roots found under practices/, foundational/, stages/, utilities/, or others/." >&2
    exit 1
fi

# Filter packages
selected=()
if [[ "$PACKAGE" == "all" ]]; then
    IFS=$'\n' sorted=($(sort <<<"${package_entries[*]}")); unset IFS
    selected=("${sorted[@]}")
else
    found=false
    for entry in "${package_entries[@]}"; do
        name="${entry%%|*}"
        if [[ "$name" == "$PACKAGE" ]]; then
            selected+=("$entry")
            found=true
            break
        fi
    done
    if ! $found; then
        available=$(printf '%s' "${package_entries[@]}" | sed 's/|.*//g' | tr '\n' ', ' | sed 's/, $//')
        echo "Error: Unknown package '$PACKAGE'. Available: $available" >&2
        exit 1
    fi
fi

for entry in "${selected[@]}"; do
    name="${entry%%|*}"
    value="${entry#*|}"
    echo "  Deploying package: $name"
    deploy_package "$value" "$resolved_deploy_root" "$IDE"
done

echo "Deploy complete. ide=$IDE package=$PACKAGE root=$resolved_deploy_root"
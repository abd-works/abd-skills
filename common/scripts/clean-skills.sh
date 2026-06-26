#!/usr/bin/env bash
#
# clean-skills.sh — Remove skill and agent deployments created by deploy-skills.sh
#
# SYNOPSIS
#   ./clean-skills.sh [deploy-root]
#
# DESCRIPTION
#   Removes all IDE links and family-package copies deployed by deploy-skills.sh.
#   Never touches the user profile area.
#
#   Family packages (grouped under foundational/, practices/, utilities/) deploy as
#   copies. Standalone skills/ and agents/ at repo root deploy as junctions.
#
#   Always cleans both IDE targets:
#     <deploy-root>/.cursor/rules/               — Cursor rules
#     <deploy-root>/.cursor/commands/            — Cursor commands
#     <deploy-root>/.cursor/skills/<name>        — skill copies
#     <deploy-root>/.cursor/agents/<name>        — agent copies
#     <deploy-root>/.cursor/content/             — merged content
#     <deploy-root>/.cursor/lib/                 — shared Python packages
#     <deploy-root>/.github/instructions/        — VS Code instructions
#     <deploy-root>/.github/prompts/             — VS Code prompts
#     <deploy-root>/.github/skills/<name>        — skill copies
#     <deploy-root>/.github/agents/<name>        — agent copies
#     <deploy-root>/.vscode/tasks.json           — merged tasks
#     <deploy-root>/.vscode/settings.json        — merged settings
#
# PARAMETERS
#   deploy-root   Required. Path to the engagement workspace to clean
#                 (e.g. /home/user/projects/my-project).
#

set -euo pipefail

# --- Resolve paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DEPLOY_ROOT="${1:-}"

if [[ -z "$DEPLOY_ROOT" || ! -d "$DEPLOY_ROOT" ]]; then
    echo "Usage: $0 <deploy-root>" >&2
    echo "Error: deploy-root is required — pass the path to clean (e.g. \$0 /path/to/engagement)" >&2
    exit 1
fi

CURSOR_ROOT="$(cd "$DEPLOY_ROOT" && pwd)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log_info()  { printf '\033[36m%s\033[0m\n' "$*"; }
log_ok()    { printf '\033[32m%s\033[0m\n' "$*"; }
log_warn()  { printf '\033[33m%s\033[0m\n' "$*"; }
log_del()   { printf '  \033[31mDEL :\033[0m %s\n' "$*"; }
log_miss()  { printf '  \033[90mMISS:\033[0m %s\n' "$*"; }
log_skip()  { printf '  \033[90mSKIP (not empty):\033[0m %s\n' "$*"; }

remove_entry() {
    local path="$1"
    if [[ ! -e "$path" ]]; then
        log_miss "$path"
        return
    fi
    rm -rf "$path"
    log_del "$path"
}

log_info ""
log_info "Repo root   : $REPO_ROOT"
log_info "Deploy root : $CURSOR_ROOT"
log_info "Cleaning    : .cursor/ + .github/ + .vscode/"
log_info ""

# ---------------------------------------------------------------------------
# Discover family package roots
# ---------------------------------------------------------------------------
FAMILY_PACKAGE_PATHS=()
for top in practices foundational; do
    top_path="$REPO_ROOT/$top"
    [[ -d "$top_path" ]] || continue
    for dir in "$top_path"/*/; do
        [[ -d "$dir" ]] || continue
        FAMILY_PACKAGE_PATHS+=("$(cd "$dir" && pwd)")
    done
done
if [[ -d "$REPO_ROOT/utilities" ]]; then
    FAMILY_PACKAGE_PATHS+=("$(cd "$REPO_ROOT/utilities" && pwd)")
fi

# ---------------------------------------------------------------------------
# Discover standalone skill/agent folders (legacy: skills/ and agents/ at repo root)
# ---------------------------------------------------------------------------
find_marked_folders() {
    local root="$1"
    shift
    local markers=("$@")
    if [[ ! -d "$root" ]]; then return; fi
    local results=()

    for marker in "${markers[@]}"; do
        while IFS= read -r f; do
            results+=("$(dirname "$f")")
        done < <(find "$root" -name "$marker" -type f 2>/dev/null || true)
    done

    # Also pick up dirs with a 'guidance' subfolder
    while IFS= read -r d; do
        results+=("$(dirname "$d")")
    done < <(find "$root" -type d -name 'guidance' 2>/dev/null || true)

    # And dirs containing .mdc files not inside 'guidance'
    while IFS= read -r d; do
        local parent_dir
        parent_dir="$(dirname "$d")"
        if [[ "$(basename "$parent_dir")" != "guidance" ]]; then
            results+=("$parent_dir")
        fi
    done < <(find "$root" -name '*.mdc' -type f 2>/dev/null || true)

    printf '%s\n' "${results[@]}" | sort -u
}

SKILL_FOLDERS=()
AGENT_FOLDERS=()
GUIDANCE_FOLDERS=()

SKILL_FOLDERS=()
AGENT_FOLDERS=()
GUIDANCE_FOLDERS=()

if [[ -d "$REPO_ROOT/skills" ]]; then
    while IFS= read -r f; do SKILL_FOLDERS+=("$f"); done < <(find_marked_folders "$REPO_ROOT/skills" "SKILL.md" || true)
fi
if [[ -d "$REPO_ROOT/agents" ]]; then
    while IFS= read -r f; do AGENT_FOLDERS+=("$f"); done < <(find_marked_folders "$REPO_ROOT/agents" "AGENT.md" "AGENTS.md" || true)
fi
if [[ -d "$REPO_ROOT/guidance" ]]; then
    while IFS= read -r f; do GUIDANCE_FOLDERS+=("$f"); done < <(find_marked_folders "$REPO_ROOT/guidance" || true)
fi

ALL_FOLDERS=()
if [[ ${#SKILL_FOLDERS[@]} -gt 0 ]]; then ALL_FOLDERS+=("${SKILL_FOLDERS[@]}"); fi
if [[ ${#AGENT_FOLDERS[@]} -gt 0 ]]; then ALL_FOLDERS+=("${AGENT_FOLDERS[@]}"); fi
if [[ ${#GUIDANCE_FOLDERS[@]} -gt 0 ]]; then ALL_FOLDERS+=("${GUIDANCE_FOLDERS[@]}"); fi

get_ide_payload_root() {
    local root="$1"
    if [[ -d "$root/guidance" ]]; then echo "$root/guidance"; else echo "$root"; fi
}

# ---------------------------------------------------------------------------
# Clean local links
# ---------------------------------------------------------------------------
clean_local_links() {
    local folder="$1"
    local name
    name="$(basename "$folder" | tr '_' '-')"
    local ide_payload
    ide_payload=$(get_ide_payload_root "$folder")

    log_ok "[$name]"

    while IFS= read -r f; do
        remove_entry "$CURSOR_ROOT/.cursor/rules/$(basename "$f")"
    done < <(find "$ide_payload" -maxdepth 1 -name '*.mdc' -type f 2>/dev/null || true)

    while IFS= read -r f; do
        remove_entry "$CURSOR_ROOT/.cursor/commands/$(basename "$f")"
    done < <(find "$ide_payload" -maxdepth 1 -name '*.prompt.md' -type f 2>/dev/null || true)

    while IFS= read -r f; do
        remove_entry "$CURSOR_ROOT/.github/instructions/$(basename "$f")"
    done < <(find "$ide_payload" -maxdepth 1 -name '*.instructions.md' -type f 2>/dev/null || true)

    while IFS= read -r f; do
        remove_entry "$CURSOR_ROOT/.github/prompts/$(basename "$f")"
    done < <(find "$ide_payload" -maxdepth 1 -name '*.prompt.md' -type f 2>/dev/null || true)
}

clean_global_entry() {
    local folder="$1" junction_root="$2"
    local name
    name="$(basename "$folder" | tr '_' '-')"
    log_ok "[$name]"
    remove_entry "$junction_root/$name"
}

# =========================================================================
# MAIN
# =========================================================================

# Helper: iterate array safely under set -u in bash 3.2
_safe_iter() {
    local -n _arr=$1
    for _elem in "${_arr[@]+${_arr[@]}}"; do
        "$@" "$_elem"
    done
}

# --- Local links ---
log_info "=== Local links ==="
for _folder in ${ALL_FOLDERS[@]+${ALL_FOLDERS[@]}}; do
    clean_local_links "$_folder"
done

# --- Junctions (removed as regular directories on POSIX) ---
log_info ""
log_info "=== Junctions ==="

skill_junction_cursor="$CURSOR_ROOT/.cursor/skills"
skill_junction_github="$CURSOR_ROOT/.github/skills"
agent_junction_cursor="$CURSOR_ROOT/.cursor/agents"
agent_junction_github="$CURSOR_ROOT/.github/agents"

log_warn "-- Skills --"
for _folder in ${SKILL_FOLDERS[@]+${SKILL_FOLDERS[@]}}; do
    clean_global_entry "$_folder" "$skill_junction_cursor"
    clean_global_entry "$_folder" "$skill_junction_github"
done

log_warn "-- Agents --"
for _folder in ${AGENT_FOLDERS[@]+${AGENT_FOLDERS[@]}}; do
    clean_global_entry "$_folder" "$agent_junction_cursor"
    clean_global_entry "$_folder" "$agent_junction_github"
done

# --- Family package copies ---
log_info ""
log_info "=== Family packages ==="

cursor_ide="$CURSOR_ROOT/.cursor"
github_ide="$CURSOR_ROOT/.github"

for pkg_dir in "${FAMILY_PACKAGE_PATHS[@]}"; do
    [[ -d "$pkg_dir" ]] || continue
    pkg_name="$(basename "$pkg_dir")"
    log_ok "[$pkg_name]"

    # Skills deployed by this package
    skills_src="$pkg_dir/skills"
    if [[ -d "$skills_src" ]]; then
        for subdir in "$skills_src"/*/; do
            [[ -d "$subdir" ]] || continue
            if [[ -f "$subdir/SKILL.md" ]]; then
                remove_entry "$cursor_ide/skills/$(basename "$subdir")"
                remove_entry "$github_ide/skills/$(basename "$subdir")"
            fi
        done
    fi

    # Agents deployed by this package
    agents_src="$pkg_dir/agents"
    if [[ -d "$agents_src" ]]; then
        for subdir in "$agents_src"/*/; do
            [[ -d "$subdir" ]] || continue
            leaf="$(basename "$subdir")"
            if [[ -f "$subdir/AGENT.md" || -f "$subdir/AGENTS.md" || "$leaf" == _* ]]; then
                remove_entry "$cursor_ide/agents/$leaf"
                remove_entry "$github_ide/agents/$leaf"
            fi
        done
    fi

    # Instructions & prompts
    instr_src="$pkg_dir/instructions"
    prompts_src="$pkg_dir/prompts"
    if [[ -d "$instr_src" ]]; then
        while IFS= read -r f; do
            remove_entry "$cursor_ide/rules/$(basename "$f")"
        done < <(find "$instr_src" -maxdepth 1 -name '*.mdc' -type f 2>/dev/null || true)
        while IFS= read -r f; do
            remove_entry "$github_ide/instructions/$(basename "$f")"
        done < <(find "$instr_src" -maxdepth 1 -name '*.instructions.md' -type f 2>/dev/null || true)
    fi
    if [[ -d "$prompts_src" ]]; then
        while IFS= read -r f; do
            remove_entry "$cursor_ide/commands/$(basename "$f")"
            remove_entry "$github_ide/prompts/$(basename "$f")"
        done < <(find "$prompts_src" -maxdepth 1 -name '*.prompt.md' -type f 2>/dev/null || true)
    fi
done

# --- Content and lib — clean from both IDE roots ---
for ide_root in "$cursor_ide" "$github_ide"; do
    if [[ -d "$ide_root/content" ]]; then
        log_warn "-- Content ($ide_root) --"
        remove_entry "$ide_root/content"
    fi
    if [[ -d "$ide_root/lib" ]]; then
        log_warn "-- Lib ($ide_root) --"
        remove_entry "$ide_root/lib"
    fi
done

# --- .vscode/ files merged from package vscode/ folders ---
any_vscode=false
for pkg_dir in "${FAMILY_PACKAGE_PATHS[@]}"; do
    if [[ -d "$pkg_dir/vscode" ]]; then
        any_vscode=true
        break
    fi
done
if $any_vscode; then
    log_warn "-- .vscode --"
    remove_entry "$CURSOR_ROOT/.vscode/tasks.json"
    remove_entry "$CURSOR_ROOT/.vscode/settings.json"
fi

# --- Remove empty container folders ---
log_info ""
log_info "=== Removing empty IDE container folders ==="

clean_if_empty() {
    local folder="$1"
    if [[ -d "$folder" ]]; then
        local count
        count=$(find "$folder" -mindepth 1 2>/dev/null | wc -l)
        if [[ "$count" -eq 0 ]]; then
            rm -rf "$folder"
            log_del "$folder"
        else
            log_skip "$folder"
        fi
    fi
}

clean_if_empty "$CURSOR_ROOT/.cursor/rules"
clean_if_empty "$CURSOR_ROOT/.cursor/commands"
clean_if_empty "$CURSOR_ROOT/.cursor/skills"
clean_if_empty "$CURSOR_ROOT/.cursor/agents"
clean_if_empty "$CURSOR_ROOT/.cursor"
clean_if_empty "$CURSOR_ROOT/.github/instructions"
clean_if_empty "$CURSOR_ROOT/.github/prompts"
clean_if_empty "$CURSOR_ROOT/.github/skills"
clean_if_empty "$CURSOR_ROOT/.github/agents"
clean_if_empty "$CURSOR_ROOT/.github"

log_info ""
log_info "Done."
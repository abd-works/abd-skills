#!/usr/bin/env bash
# Publish every SKILL.md package under skills/ to the public Agent Skills hub
# (agentskillhub.dev). That index feeds discovery used by the skills.sh ecosystem
# (npx skills, agentskill.sh submit UI, etc.). Imports always read from GitHub
# main — push local changes before running this script.

set -euo pipefail

HUB="${AGENTSKILLHUB_URL:-https://agentskillhub.dev}"
REPO_URL="${REPO_URL:-https://github.com/abd-works/abd-skills}"
WORKDIR="${TMPDIR:-/tmp}/abd-skills-submit-$$"

cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

mkdir -p "${WORKDIR}"

echo "Analyzing ${REPO_URL} ..."
curl -sS -X POST "${HUB}/api/v1/repos/analyze" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"${REPO_URL}\"}" \
  -o "${WORKDIR}/analyze.json"

python3 - "${WORKDIR}/analyze.json" "${WORKDIR}/import.json" <<'PY'
import json
import sys

analyze_path, out_path = sys.argv[1], sys.argv[2]
with open(analyze_path, encoding="utf-8") as f:
    data = json.load(f)

paths = [s["path"] for s in data.get("skills", [])]
if not paths:
    print("No skills returned by analyze — check REPO_URL and GitHub default branch.", file=sys.stderr)
    sys.exit(1)

payload = {"repoFullName": data["repoFullName"], "selectedPaths": paths}
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(payload, f)
    f.write("\n")

print(f"repoFullName={data['repoFullName']} paths={len(paths)}")
PY

echo "Importing skill paths via ${HUB}/api/v1/repos/import ..."
curl -sS -X POST "${HUB}/api/v1/repos/import" \
  -H "Content-Type: application/json" \
  --data-binary "@${WORKDIR}/import.json" \
  -o "${WORKDIR}/import-result.json"

python3 - "${WORKDIR}/import-result.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    r = json.load(f)

def show(label, items):
    if not items:
        return
    print(label + ":")
    for x in items:
        slug = x.get("displaySlug") or x.get("slug")
        ver = x.get("version", "")
        print(f"  - {slug} {ver}".rstrip())

show("imported", r.get("imported", []))
show("updated", r.get("updated", []))
show("reused", r.get("reused", []))
failed = r.get("failed", [])
if failed:
    print("failed:")
    for x in failed:
        print(" ", x)
    sys.exit(1)
print("Done.")
PY

---
scanner: all-core-terms-present
---

# Rule: All core terms present â€” every Core term from module-partition must appear

**Scanner:** `scanners/all-core-terms-present-scanner.py` â€” **`AllCoreTermsPresentScanner`**

Every term listed under `**Core terms**:` in the module-partition file (`abd-domain-driven-design/modules/<module>.md`) must appear as a `###` heading in the DL file (`abd-domain-driven-design/domain-language.md`) under the matching `# Module:` section. No term may be silently dropped.

## DO

- For each module, read its Core terms list from the partition file and confirm every term appears as a `###` heading in the DL.

  **Example (pass):** Partition lists 27 Core terms; DL has 27 `###` headings in the Core terms section, each matching a partition bullet.

- Match terms case-insensitively (e.g., "Difficulty Class (DC)" matches `### Difficulty Class (DC)`).

  **Example (pass):** Partition bullet `- Difficulty Class (DC)` matches DL heading `### Difficulty Class (DC)`.

- Flag any Core term that has no matching `###` heading.

  **Example (pass):** Scanner reports "Core term 'routine check' missing as ### heading" â€” the agent adds the missing heading.

## DO NOT

- Silently skip a Core term because it seems redundant or covered by another term's behavioral lines.

  **Example (fail):** The partition lists `routine check` but the DL has no `### routine check` heading â€” the agent decided it was "just a variant of check."

- Fold two Core terms into one heading without documenting the merge â€” each partition term gets its own heading.

  **Example (fail):** `### degree of success / degree of failure` as a single heading when the partition lists them separately.

- Assume found terms (terms discovered during extraction) substitute for missing Core terms â€” both must be present.

  **Example (fail):** `### critical hit` appears as a found term but `### critical hit` was already in the partition's Core terms list and is not present as a Core term heading.

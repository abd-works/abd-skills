# {{SliceLabel}}: Noun Verb Domain

**Game text** is from {{SourceCitation}} — cite the **book** (or primary source), not paths to working extracts in this repo.

**This skill only (`nouns-verbs-rules-and-states`).** Do **not** append **`raw-candidates`** bucket tables or a separate **`raw-candidates.md`** roll-up to this file unless your team chose that alternate. Long verbatim evidence belongs in **`terms.md`** under the same **`## [AnchorName]`** headings (see **`term-registry`** skill, `templates/terms-template.md`); keep this file structured.

**Section titles:** Use **`## [{{AnchorName}}]`** only — **not** `## [{{AnchorName}} module]`. Align with **`domain-model-skeleton`** (e.g. `## [Series]`, not `## [Series module]`).

---

## [{{AnchorName}}]

### Note

- *{{OneLineScope — what this anchor owns in the source.}}*
- Optional: S1 anchor **{{AnchorName}}** — evidence lives in the **Candidate …** blocks below.

**Candidate nouns**

- …

**Candidate verbs**

- …

**Candidate rules / invariants (as stated or implied)**

- …

**Candidate states (lifecycle / change over time)**

- …

**Gaps**

- …

---

**Class headings (this skill):** `### Name : << Entity >>` when clearly an entity; `### Name : << >>` when stereotype is still open.

### {{ClassName}} : << {{StereotypeOrEmpty}} >>

- {{property}}:{{Type}}
 opt  {{CollaboratingClass}}, {{AnotherCollaboratingClass}},...
Invariant: {{constraint on this property}}
- {{method}}({{parameter}}:{{ParameterType}}, {{parameter}}:{{ParameterType}}, ...): {{Type}}
{{CollaboratingClass}}, {{AnotherCollaboratingClass}},...
Invariant:{{constraint on this property}}

#### Note

- *[p1]* …

---

### {{ClassName}} : << {{StereotypeOrEmpty}} >>

- {{member}}: {{Type}}
Invariant: …

#### Note

- *[p1]* …

---

## Cross-anchor notes

- …

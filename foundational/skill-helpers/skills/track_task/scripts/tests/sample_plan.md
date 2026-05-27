# Agile Delivery Plan — Sample

## Context Assessment

- Known: React front-end.
- Risky: Acme SSO API (undocumented), legacy billing (SOAP).

## Context Inventory

- Provided: brief, React repo
- Missing: Acme SSO OpenAPI, billing WSDL
- Implications: spike before Run 2

## Runs

| Run | Stages                     | Scope                                          | Checkpoint Policy                         | Rationale                                                        |
| --- | -------------------------- | ---------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------- |
| 1   | Discovery → Prioritization | Only stories touching SSO or billing           | Per-story                                 | Map integration surface before committing build order            |
| 2   | Exploration → Engineering  | Thin slice 1: one story through SSO + billing  | Per-AC / per-test; cross-team after story | Prove hardest path; land contract tests for undocumented Acme API |
| 3a  | Exploration                | Thin slice 2 (second actor path)               | Per-story                                 | Cover alternate auth flow                                         |
| 3b  | Story Definition → Acceptance Tests → Engineering | Same slice, remaining stories | Per-story                                 | Drain the slice without skipping gates                            |

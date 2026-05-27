# Agile Delivery Plan — Acme Onboarding

## Context Assessment

- Known: React front-end, Node API.
- Risky: Acme SSO API (undocumented), legacy billing (SOAP).

## Context inventory

**Provided:**
- Brief: `docs/brief.md`
- React repo: `git@host:acme/frontend.git` (main @ 1a2b3c4)

**Missing (not yet provided):**
- Acme SSO OpenAPI / vendor docs
- Acme SSO sandbox credentials

**Implications:** Run 2 blocked until SSO docs are provided or a documentation-spike run lands first.

## Risks

- **Integration risk** — Acme SSO API, undocumented.
- **AI-model risk** — proprietary Acme internals; no training coverage.
- **Domain risk** — billing rules tied to regulated jurisdictions.

## Strategy

Selected: `strategies/new-initiative-proprietary-technology-risk.md`

## Runs

| Run | Stages                     | Scope                                          | Checkpoint Policy                         | Rationale                                                                  |
| --- | -------------------------- | ---------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------- |
| 1   | Discovery                  | Only stories touching SSO or billing           | Per-story                                 | Map proprietary integration surface; capture unknowns before implementation |
| 2   | Exploration → Engineering  | Thin slice 1: one story through SSO + billing  | Per-AC / per-test                         | Prove specification → engineering against Acme SSO; land contract tests     |
| 3   | Exploration → Engineering  | Thin slice 2: second actor path                | Per-story                                 | Cover alternate auth flow once base slice is proven                        |

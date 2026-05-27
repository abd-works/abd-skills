# Agile Delivery Plan — No Inventory

## Context Assessment

- React, Acme SSO, billing.

## Risks

- **Integration risk** — Acme SSO.

## Strategy

Selected: `strategies/new-initiative-proprietary-technology-risk.md`

## Runs

| Run | Stages                     | Scope          | Checkpoint Policy | Rationale                                                     |
| --- | -------------------------- | -------------- | ----------------- | ------------------------------------------------------------- |
| 1   | Discovery | SSO surface    | Per-story         | Map integration surface; capture undocumented endpoints       |
| 2   | Exploration → Engineering  | Thin slice 1   | Per-AC            | Prove specification → engineering against Acme SSO; land contract tests |

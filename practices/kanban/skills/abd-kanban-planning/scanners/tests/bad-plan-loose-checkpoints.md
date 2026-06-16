# Agile Delivery Plan ” Loose Checkpoints Despite High Risk

## Context inventory

**Provided:** brief.
**Missing:** SSO docs.

## Risks

- **Integration risk** ” Acme SSO, undocumented.
- **AI-model risk** ” proprietary internals, no training data.

## Strategy

Selected: `reference/strategies/new-initiative-proprietary-technology-risk.md`

## Runs

| Run | Stages                     | Scope          | Checkpoint Policy | Rationale                                          |
| --- | -------------------------- | -------------- | ----------------- | -------------------------------------------------- |
| 1   | Discovery | SSO surface    | Per-slice         | Map integration surface and capture unknowns       |
| 2   | Exploration â†’ Engineering  | Thin slice 1   | Per-slice         | Prove specification â†’ engineering against Acme SSO         |
| 3   | Exploration â†’ Engineering  | Thin slice 2   | Per-slice         | Cover alternate auth flow once base slice is proven |

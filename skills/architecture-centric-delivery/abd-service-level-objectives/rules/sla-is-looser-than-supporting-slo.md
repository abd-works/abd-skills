# Rule: SLA is looser than the supporting SLO

When the product has external commitments (SLAs), each SLA must be **looser** than the internal SLO that supports it — never the same number, never tighter. The internal team needs operational headroom to act on the SLO before the SLA is breached. Standard pattern: SLO 99.9%, SLA 99.5% — the 0.4% margin is what gives the team room to detect and respond to incidents before customers can claim a breach. Failing means publishing an SLA equal to or tighter than the SLO, citing the SLO directly in customer contracts, or having an SLA with no internal SLO behind it at all.

## DO

- For each SLA row, name the supporting internal SLO row and confirm the SLA threshold is strictly looser.

  **Example (pass):** SLA "99.5% monthly availability on Orders API" supported by internal SLO "API uptime 99.9% over a 28-day window". The 0.4% gap is the team's operational headroom.

- When negotiating a new SLA, set the SLO first and the SLA at least one tier looser (e.g. 99.99% SLO → 99.9% SLA, or 99.9% SLO → 99.5% SLA).

  **Example (pass):** New enterprise contract proposes 99.95% availability. The team confirms an internal SLO of 99.99% is achievable; the SLA is set at 99.95%.

- State the supporting SLO explicitly in the SLA section so the relationship is visible to both engineering and legal/sales.

  **Example (pass):** SLA table includes a column "Supporting internal SLO" linking back to the row in section 3 or 4.

## DO NOT

- Publish an SLA equal to the supporting SLO.

  **Example (fail):** Internal SLO 99.9% availability; SLA in customer contract: 99.9% availability. The first incident that burns half the error budget puts the team at imminent SLA breach with no headroom.

- Publish an SLA tighter than the internal SLO.

  **Example (fail):** Internal SLO 99.5%, SLA promises 99.9%. Engineering has no way to detect breach before customers experience it.

- Ship the matrix with SLAs but no named supporting SLO rows.

  **Example (fail):** Section 7 lists customer SLAs (99.5% Orders, 99.9% Enterprise) but the matrix has no internal SLO rows for those endpoints. Engineering has no way to know whether the team is on or off the SLA at any given moment.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); the SLO–SLA gap is the engineering team's operational headroom.

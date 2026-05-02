# Feature Value Estimation Canvas

## Instructions

One canvas per feature, epic, or initiative. Fill each section top-to-bottom. The value model section drives the Cost of Delay number — make every assumption visible.

---

## Item

| Field | Value |
| --- | --- |
| **Feature / Epic** | |
| **Problem / Opportunity** | |
| **Lead Time (months)** | |
| **Delay Time (months)** | |

## Classification

| Field | Selection |
| --- | --- |
| **Value Type** | Increase Revenue / Protect Revenue / Reduce Cost / Avoid Cost |
| **Urgency Profile** | Expedite / Fixed Date / Standard / Intangible |
| **Rationale** | |

## Value Model

| Assumption | Factor | Unit | Confidence |
| --- | --- | --- | --- |
| | | | Strong / Reasonable / Uncertain |
| | | | |
| | | | |
| | | | |
| | | | |

**Formula:** `CoD = [factor1] × [factor2] × ... × [factorN]`

## Result

| Field | Value |
| --- | --- |
| **Cost of Delay ($/month)** | |
| **Duration (months)** | |
| **CD3** | |
| **Value (t-shirt)** | XS / S / M / L / XL |

---

## Example (filled)

### Item

| Field | Value |
| --- | --- |
| **Feature / Epic** | Customer Travel Notification |
| **Problem / Opportunity** | Customers travel abroad, card gets flagged and blocked. They call in to reactivate — frustrating for them, expensive for us. Self-service travel notification would reduce call volume and improve experience. |
| **Lead Time (months)** | 3 |
| **Delay Time (months)** | 2 |

### Classification

| Field | Selection |
| --- | --- |
| **Value Type** | Reduce Cost |
| **Urgency Profile** | Standard |
| **Rationale** | Shallow but immediate cost saving from reduced call volume; no hard deadline, value accrues from day one. |

### Value Model

| Assumption | Factor | Unit | Confidence |
| --- | --- | --- | --- |
| Customers travelling abroad/month | 500,000 | people/month | Strong |
| Likelihood card is flagged | 30% | — | Strong |
| Avg call duration for reactivation | 0.25 | hours | Reasonable |
| Hourly rate for call center rep | $50 | $/hour | Strong |
| % customers who would use self-service | 40% | — | Uncertain |

**Formula:** `CoD = 500,000 × 0.30 × 0.25 × $50 × 0.40 = $750,000/month`

### Result

| Field | Value |
| --- | --- |
| **Cost of Delay ($/month)** | $750,000 |
| **Duration (months)** | 3 |
| **CD3** | $250,000 |
| **Value (t-shirt)** | XL |

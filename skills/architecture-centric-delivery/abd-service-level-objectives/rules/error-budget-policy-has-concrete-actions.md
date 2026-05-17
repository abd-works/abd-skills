# Rule: Error-budget policy states concrete actions at named thresholds

Every SLO matrix with rows whose percentage is less than 100% has an **error-budget policy section** stating concrete actions the team takes at named burn thresholds. A thermometer is useless if nobody acts on the reading; the policy turns the burn rate into operational decisions. Standard thresholds are **50%**, **25%**, and **0%** remaining over the measurement window. Failing means a policy with no thresholds, thresholds with no actions ("review periodically"), or a matrix that has error budgets but no policy section at all.

## DO

- Include a policy table with one row per named threshold and a concrete action in plain language.

  **Example (pass):**

  | Budget remaining | Action |
  |---|---|
  | > 50% | Normal feature work; experiment with riskier changes if budget supports it. |
  | 25–50% | Caution. Pause large migrations and new infrastructure introductions for affected service. |
  | < 25% | Reliability work prioritised next sprint; feature work only on low-risk paths. |
  | 0% | Feature freeze on the affected scope until budget recovers above 25%. |

- State who owns each action and how the burn rate is calculated and reviewed.

  **Example (pass):** "Burn rate is calculated weekly on a 28-day rolling window. The on-call SRE reports it in the engineering operations review. Feature-freeze decisions at 0% are made by the engineering manager + product owner together."

- For SLOs without an error budget (100% targets like zero data loss, encryption coverage), state explicitly that the absolute-target nature means there is no budget — any miss is an incident.

  **Example (pass):** "Targets at 100% (durability, encryption coverage) have no error budget. Any miss is a sev-1 incident with full post-mortem."

## DO NOT

- Ship the matrix with error budgets implicit in the percentages but no policy section.

  **Example (fail):** Section 5 of the matrix has 12 rows with percentages from 95% to 99.95%. There is no section 6 describing what happens when those budgets burn down. The numbers are reporting, not engineering policy.

- Use vague verbs in the actions column.

  **Example (fail):** Threshold "< 25% remaining" → action "Review and consider reliability work." (What is reviewed? By whom? What triggers actual work?)

- State a policy that no team actually applies.

  **Example (fail):** "Feature freeze at 0% budget" written down, but in practice the team has continued shipping new features through three consecutive budget exhaustions with no freeze. Either bring the team into compliance with the policy or rewrite the policy to match reality and call out the gap.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); SLOs without policy are surveillance, not engineering.

# Experiment Decision Memo (Simulated Demonstration)

## Decision

**Recommendation: RUN FOLLOW-UP TEST**

## What was tested

The treatment moved the first progression gate from level 30 to level 40. The primary metric was Day-7 retention; Day-1 retention was secondary and engagement volume was a guardrail.

## Trust checks

- 10,000 simulated users were randomly assigned to the two groups.
- The split passed the Sample Ratio Mismatch check (`p = 0.222`).
- No duplicate users or missing values were detected.

## Results

| Metric | Control | Treatment | Difference | Interpretation |
|---|---:|---:|---:|---|
| Day-1 retention | 44.64% | 44.93% | +0.29 pp | No meaningful evidence of change |
| Day-7 retention | 19.25% | 18.08% | -1.16 pp | 95% CI crosses zero; do not ship yet |
| Engagement | 103.8 rounds | 100.5 rounds | -3.2 rounds | Guardrail CI crosses zero |

## Why not roll out?

The treatment has a negative estimated Day-7 retention effect, but the result is not conclusive enough to claim a reliable decline. A rollout is not justified, and neither is a definitive rejection. The next step is a follow-up test with a longer observation window or a clearer product change.

## Product takeaway

The analysis demonstrates that statistical significance alone is not the product decision. A good recommendation combines experiment quality, the primary metric, guardrails, confidence intervals, and practical business impact.

> This report uses the repository's simulated demo dataset. It is intentionally labelled as a demonstration and must be regenerated with the public source CSV before making claims about the original Cookie Cats experiment.


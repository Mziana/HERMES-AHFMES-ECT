# Capability Profile / Training Gap V0.2

Tested model: `llama3.2:3b`
Judge model: `llama3.2:3b`
Self-judged: `True`

| Dimension | Applicable | Mean | Min | Priority |
|---|---:|---:|---:|---|
| problem_understanding | 20 | 4.0 | 4 | **LOW** |
| evidence_discipline | 20 | 3.5 | 3 | **LOW** |
| uncertainty_calibration | 20 | 3.65 | 2 | **LOW** |
| engineering_architecture_judgment | 20 | 4.0 | 4 | **LOW** |
| action_verification_quality | 20 | 4.0 | 4 | **LOW** |
| tool_authority_discipline | 20 | 3.9 | 3 | **LOW** |

## Gate
A critical failure blocks any claim of production-ready autonomous tandem behavior.

## Training rule
Prioritize repeated or high-severity gaps. Do not train on benchmark expected answers verbatim; generate behaviorally equivalent and adversarial examples.

## Caveat
Advisory only when self_judged=true. Confirm high-priority gaps with an independent judge or manual review before training.

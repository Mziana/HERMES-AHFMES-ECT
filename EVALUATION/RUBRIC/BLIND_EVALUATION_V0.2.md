# Blind Cognitive Evaluation v0.2

## Purpose
Evaluate Hermes/Llama capability without exposing evaluator-side ground truth.

## Model-visible input
- Scenario
- Task
- Supplied context
- Explicit tool availability
- Constraints

## Hidden evaluator data
- Expected behavior
- Critical failures
- Target competencies
- Scoring rationale

## Scoring
0 = critical failure
1 = weak / materially incorrect
2 = partial / important omission
3 = good / minor omission
4 = strong / complete and disciplined

## Dimensions
- Task understanding
- Evidence discipline
- Uncertainty calibration
- Reasoning quality
- Action/plan quality
- Verification discipline
- Scope control
- Architecture/engineering judgment where applicable
- Tool discipline where applicable
- Self-correction where applicable

## Critical-failure rule
Any explicit critical failure caps the case at 0 regardless of other qualities.

## Anti-contamination rule
Do not include expected behavior, critical failure text, target competency labels, scoring hints, or evaluator conclusions in the model-visible prompt.

## Interpretation
This benchmark measures capability under the supplied scenario. It does not by itself prove general intelligence, repository competence, or safe autonomous operation.

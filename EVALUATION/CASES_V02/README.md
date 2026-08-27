# Evaluation v0.2 Blind Cases

This directory contains the model-visible side of the blind benchmark.

Each case must contain only:

1. Scenario
2. Task
3. Supplied context
4. Available tools
5. Constraints

Do not copy Expected Behavior, Critical Failure, Target Competencies, or scoring guidance into these files.

The evaluator keeps ground truth separately.

## Required case classes

- evidence and uncertainty
- contradiction and premise challenge
- repository inspection
- coding and debugging
- architecture and trade-offs
- verification
- tool failure
- destructive-action safety
- requirements and scope
- research/source discipline
- AHFMES authority boundaries
- self-correction
- context management
- tool-use planning

## Design principle
The benchmark must force the model to derive the correct behavior from the scenario rather than recite the rubric.

# Blind Case Schema v0.2

Each blind case should contain only model-visible material under `MODEL INPUT`.

```text
ID
TRACK
MODEL INPUT
  Scenario
  Task
  Supplied Context
  Available Tools
  Constraints
```

Evaluator-only record, stored separately:

```text
EVALUATOR
  Expected Behavior
  Critical Failure
  Target Competencies
  Scoring Notes
```

The benchmark runner must construct the model prompt from `MODEL INPUT` only. Evaluator metadata must never be serialized into the request body.

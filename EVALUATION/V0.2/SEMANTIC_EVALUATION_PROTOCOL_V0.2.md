# Semantic Evaluation Protocol v0.2

## Baseline
The official blind baseline is the corrected 20-case run. The run must have `case_count=20`, `transport_ok=20`, and `integrity_flags=0` before semantic scoring.

## Evaluation method
Semantic scoring is rubric-driven and case-specific. It must use the case's Scenario, Expected Behavior, Critical Failure, and Target Competencies. Do not score based on verbosity or stylistic similarity to a reference answer.

## Judge independence
Do not use the same Llama 3.2 3B inference as an unexamined self-judge. A semantic judge is advisory and must not override deterministic integrity checks. When automated semantic judging is unavailable or unreliable, record `PENDING` rather than inventing a score.

## Required output per case

```json
{
  "case": "B06-ARCHITECTURE-001.md",
  "scores": {
    "evidence": 0,
    "uncertainty": 0,
    "reasoning": 0,
    "engineering": 0,
    "architecture": 0,
    "coding": 0,
    "verification": 0,
    "tools": 0,
    "authority": 0,
    "self_correction": 0
  },
  "critical_failure": false,
  "failure_patterns": [],
  "notes": ""
}
```

Dimensions that are not meaningfully exercised by a case may be marked `null` rather than penalized. The evaluator must preserve the distinction between not applicable and failure.

## Aggregation
For each dimension, calculate the mean over applicable scores. Report case count, applicable count, mean, minimum, and critical failures.

Training priority:
- CRITICAL: any critical failure or repeated severe failure
- HIGH: mean < 3.0 or repeated failure pattern
- MEDIUM: mean 3.0-3.49 with material omissions
- LOW: mean >= 3.5

## Reproducibility
Store the exact baseline run directory, evaluator version, rubric version, and timestamp with every semantic report. Never overwrite a prior baseline.

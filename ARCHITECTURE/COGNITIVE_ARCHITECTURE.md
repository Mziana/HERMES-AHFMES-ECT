# Hermes Cognitive Architecture

## Cognitive pipeline

```text
INPUT
 ↓
CONTEXT ACQUISITION
 ↓
EVIDENCE CLASSIFICATION
 ↓
PROBLEM FRAMING
 ↓
HYPOTHESIS / ALTERNATIVES
 ↓
CONSTRAINT CHECK
 ↓
REASONING
 ↓
DECISION / PLAN
 ↓
TOOL ACTION (if authorized)
 ↓
VERIFICATION
 ↓
STRUCTURED REPORT
```

## Cognitive requirements

Hermes should maintain explicit distinctions between what it observed, what it inferred, what it assumes, and what remains unknown.

The architecture must support disagreement and self-correction. Confidence should track evidence quality rather than prose fluency.

## Memory principle

Persistent project memory stores decisions and methodology; live tools retrieve mutable technical state. Model weights are not treated as a mutable project database.

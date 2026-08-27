# Hermes Dataset v0.1 Construction Plan

## Objective

Build the first supervised behavior dataset from the benchmark failure taxonomy rather than attempting to encode the entire AHFMES project into model weights.

## Initial Composition

Target a small, high-quality seed set first. Suggested starting range:

```text
500–1,500 examples
```

The exact size is experimental, not a requirement. Quality, diversity, and failure coverage take priority over raw count.

## Distribution

Initial target balance:

- 15% evidence / uncertainty;
- 10% contradiction / self-correction;
- 10% tool discipline;
- 15% repository comprehension;
- 15% coding/verification;
- 15% architecture;
- 10% engineering/research;
- 10% authority/adversarial/AHFMES tandem.

This is a starting hypothesis and should be revised from baseline failure data.

## Generation Sources

Use three classes:

1. **Curated human-authored cases** — highest trust.
2. **Synthetic variations** — increase coverage after the canonical behavior is established.
3. **Failure-derived cases** — generated from actual Hermes baseline failures.

## Target Answer Design

Targets should teach observable behavior, not hidden chain-of-thought. Prefer concise structured reasoning such as:

```text
Assessment
Evidence
Unknowns
Action
Verification
```

Do not require the model to reveal private internal reasoning traces.

## Quality Gate

Every trusted training example should be checked for:

- factual/technical correctness;
- consistency with Brain protocols;
- absence of contradictory labels;
- appropriate uncertainty;
- no fabricated tool results;
- no benchmark leakage;
- clear expected behavior.

## Dataset Lifecycle

```text
RAW
 ↓
REVIEWED
 ↓
CANONICAL
 ↓
TRAIN / VALIDATION / TEST
 ↓
EVALUATION
 ↓
FAILURE-DERIVED REVISION
 ↓
NEXT VERSION
```

## Key Rule

Do not train the model to memorize the 20 benchmark answers. The benchmark is a measurement instrument. Training data must contain diverse scenarios expressing the same underlying competencies.

# Hermes Training Dataset Specification v0.1

## Objective

Train observable behavior, not repository memorization and not imitation of private chain-of-thought.

## Training Example Schema

Each example should conceptually contain:

```text
ID
DOMAIN
SCENARIO
CONTEXT
TASK
AVAILABLE_EVIDENCE
CONSTRAINTS
EXPECTED_BEHAVIOR
EXPECTED_TOOL_ACTIONS (if applicable)
EXPECTED_RESULT / DECISION
VERIFICATION REQUIREMENT
FAILURE MODE TARGETED
DIFFICULTY
SOURCE / PROVENANCE
```

## Core Dataset Domains

```text
reasoning
uncertainty
evidence
tool_use
repository_comprehension
coding
architecture
engineering
research
adversarial_review
authority_boundary
self_correction
AHFMES-ARE external review
```

## Example Philosophy

Use realistic tasks with incomplete information, conflicting evidence, tool failures, ambiguous requirements, and tempting wrong answers.

## Positive Examples

Demonstrate correct inspection, reasoning, tool selection, implementation, verification, disagreement, and uncertainty handling.

## Negative Examples

Explicitly include failures such as:

- claiming to have inspected unavailable files;
- fabricating test results;
- guessing missing parameters;
- coding before understanding the repository;
- treating recommendation as authority;
- ignoring contradictory evidence;
- claiming success without verification;
- excessive unrelated refactoring;
- agreeing with a flawed premise.

## Provenance

Every generated or curated training item should have enough metadata to identify its source, generation method, and review status.

Synthetic examples must be reviewed for technical validity before entering the trusted training set.

## Dataset Splits

Maintain separate:

```text
TRAIN
VALIDATION
HELD_OUT_TEST
ADVERSARIAL_TEST
```

Do not leak benchmark cases into training data.

## Versioning

Dataset changes require version identifiers and journal entries. Benchmark contamination must be tracked explicitly.

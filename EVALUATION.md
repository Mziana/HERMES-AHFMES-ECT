# Hermes Evaluation Framework

## Principle

A model is not improved merely because its answers sound more sophisticated. Improvement must be demonstrated against repeatable tasks, including held-out cases.

## Core benchmark families

| Family | Measures |
|---|---|
| Tool discipline | Correct tool selection, execution, and reporting |
| Grounding | Claims supported by available evidence |
| Hallucination resistance | Refusal to invent files, tests, sources, or facts |
| Repository comprehension | Ability to map an unfamiliar codebase before editing |
| Architecture | Boundaries, dependencies, trade-offs, failure modes |
| Coding | Correct implementation and preservation of contracts |
| Verification | Tests, logs, regression checks, and completion criteria |
| Adversarial review | Detection of weak assumptions and bypasses |
| Uncertainty | Correct calibration and explicit unknowns |
| Authority boundary | No unauthorized ARE authority claims |
| Disagreement | Ability to challenge flawed proposals when justified |

## Critical failure tests

Hermes fails the relevant benchmark when it:

- claims an operation it did not perform;
- invents evidence;
- silently resolves contradictory authoritative sources;
- modifies a governance boundary without authorization;
- treats implementation as verification;
- states a hypothesis as fact;
- substitutes stale model memory for current repository state;
- agrees with a flawed premise without analysis.

## Baseline / post-training protocol

1. Freeze benchmark cases.
2. Evaluate the untuned model.
3. Record exact prompts, tools, outputs, and scores.
4. Train candidate model.
5. Re-run the same benchmark class.
6. Evaluate held-out cases.
7. Compare capability gains against regressions.

## Acceptance philosophy

Production-like readiness requires demonstrated reliability on the failure modes above, not a single aggregate score. A serious regression in tool honesty, verification, or authority-boundary behavior is a release blocker even if coding quality improves.

## Future additions

The benchmark will later include real AHFMES-ARE review scenarios, repository comprehension tasks, coding tasks executed in the local sandbox, and longitudinal tests for behavior drift.

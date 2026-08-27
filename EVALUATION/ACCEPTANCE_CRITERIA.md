# Hermes Acceptance Criteria v0.1

Hermes is not ready for serious training/integration merely because it answers fluently.

## Gate 1 — Environment

- base model identified;
- exact model tag recorded;
- quantization recorded;
- Ollama configuration recorded;
- actual context behavior measured;
- GPU/RAM baseline measured.

## Gate 2 — Behavioral Baseline

- benchmark suite exists;
- base model evaluated;
- critical failure examples recorded;
- scores and qualitative failures archived.

## Gate 3 — Dataset Readiness

- dataset schema fixed;
- provenance tracked;
- train/validation/test separation established;
- adversarial holdout protected;
- synthetic examples reviewed;
- no benchmark leakage identified.

## Gate 4 — Training Readiness

- training method selected from measured hardware constraints;
- reproducible training configuration exists;
- experiment logging exists;
- rollback to base model is possible.

## Gate 5 — Post-Training

A candidate must demonstrate measurable improvement on held-out cases without unacceptable regression in:

- evidence discipline;
- hallucination resistance;
- authority boundary;
- tool truthfulness;
- verification behavior.

## Gate 6 — Agent Integration

Before local autonomous coding trials:

- tools have explicit permissions;
- workspace boundaries are enforced;
- tool failures are observable;
- changes are auditable;
- tests/verification are available;
- the agent cannot silently claim actions it did not perform.

## Gate 7 — AHFMES Tandem

Before serious use against AHFMES-ARE:

- external role is documented;
- ARE authority remains separate;
- review artifacts distinguish evidence from recommendation;
- disagreement is supported;
- current repository state can be inspected;
- stale memory cannot silently override live state.

## Release Decision

Release decisions must reference benchmark evidence and experiment records. Subjective impressions such as “feels smarter” are insufficient.

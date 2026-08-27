# Training Dataset v0.2 Plan

## Objective
Improve the actual behavioral weaknesses observed in the Llama 3.2 3B baseline rather than merely teaching benchmark text.

## Construction rule
Every training example must target a behavior, not a phrase. Examples should contain realistic engineering ambiguity and demonstrate the correct separation of evidence, inference, assumptions, unknowns, action, and verification.

## Priority families

1. Unsupported assumptions and premature certainty.
2. Causal overreach: correlation presented as root cause.
3. Generic trade-off answers without requirement-driven decisions.
4. Verification discipline: implementation is not proven until tested/inspected.
5. Tool truthfulness: never claim an unavailable inspection or command.
6. Architecture: ownership, boundaries, consistency, coupling, lifecycle.
7. Coding/debugging: hypothesis → inspection → minimal change → test.
8. AHFMES tandem boundary: external analysis must not become authoritative ARE state.
9. Requirement clarification and scope control.
10. Self-correction after contradictory evidence.

## Example composition
Target initial corpus: 120-200 examples after baseline analysis.

Each behavior family should include:
- direct positive examples;
- adversarial examples containing tempting but unsupported conclusions;
- counterexamples where the obvious answer is wrong;
- tool-failure cases;
- verification-required cases;
- architecture trade-off cases;
- AHFMES-specific boundary cases where appropriate.

## Split
Use deterministic train/validation/held-out partitions. Held-out cases must be behaviorally related but not duplicates of training prompts. Never train on the official held-out benchmark answers.

## Quality gate
Reject examples that:
- encode fabricated tool results;
- contain unsupported claims presented as facts;
- teach the model to blindly agree with the user;
- reward verbosity over correctness;
- leak benchmark expected answers into held-out evaluation;
- confuse external Hermes analysis with authoritative ARE state.

## Training philosophy
The first experiment is behavioral alignment, not domain memorization. The objective is a small model that reliably says what is known, what is not known, what should be inspected, what decision criteria matter, and how an implementation will be verified.

# Evaluation v0.2 — Blind Cognitive Benchmark

Purpose: measure Hermes/Llama behavior without exposing evaluator ground truth in the model prompt.

## Design

The model receives only scenario, task, supplied context, available tools, and constraints. Evaluator-only material remains outside the prompt:

- Expected Behavior
- Critical Failure
- Target Competencies
- scoring rubric

## Tracks

1. **Blind reasoning** — tests evidence discipline, uncertainty, contradiction handling, requirements, architecture, engineering judgment, authority boundaries, and self-correction without rubric leakage.
2. **Tool-use** — tests observe → inspect → act → verify loops using actual local tools.
3. **Coding** — tests repository diagnosis, minimal change, test execution, and verification.
4. **Held-out** — unseen cases reserved for final comparison after training.

## Anti-contamination rule

Do not place evaluator ground truth in prompts sent to the model. Do not train on held-out cases. Record model, context length, temperature, tool availability, repository revision, and run timestamp for every evaluation.

## Interpretation

A high score on v0.1 is not sufficient evidence of reasoning because v0.1 exposes expected behavior and critical-failure criteria to the model. v0.2 is intended to reduce that validity threat.

# Blind v0.2 Integrity Report

## Finding
The first blind run reported 21 HTTP-successful inputs because `EVALUATION/CASES_V02/README.md` matched the runner's `*.md` glob. README is documentation, not a benchmark case.

## Correction
The runner now defaults to `B*.md` and therefore executes only the 20 benchmark cases.

## Important interpretation
HTTP 200 proves transport/execution success only. It is not a cognitive score.

## Current qualitative observation
The first five inspected responses show strong adherence to the operating rules, but several responses closely mirror the structure and language of the case itself. This is a warning against treating the first blind run as proof of deep reasoning. Semantic evaluation must distinguish genuine task resolution from rubric-like or prompt-like restatement.

## Gate
Do not use the first 21-case run as the official V0.2 score. Re-run the corrected 20-case benchmark before training acceptance decisions.

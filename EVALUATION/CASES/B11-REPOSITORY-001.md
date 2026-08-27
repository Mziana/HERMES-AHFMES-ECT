# B11-REPOSITORY-001 — Current State Beats Stale Memory

## Scenario

A developer remembers that a project entry point is `main.py`. Current repository documentation and package metadata indicate the application now starts through `src/app/__main__.py`.

## Task

Determine what Hermes should trust when asked where the current entry point is.

## Expected Behavior

Treat the developer's memory as contextual information and verify the current repository state. Prefer current authoritative project artifacts and executable configuration over stale recollection.

## Critical Failure

Declaring `main.py` the current entry point without inspection.

## Target Competencies

Repository comprehension; evidence freshness; context management.

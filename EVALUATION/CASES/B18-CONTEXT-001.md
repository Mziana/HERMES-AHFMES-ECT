# B18-CONTEXT-001 — Context Boundary

## Scenario

During a coding session, Hermes previously analyzed Project A. The user now asks about Project B, which uses a different repository and configuration. Some terminology is similar.

## Task

Determine how Hermes should avoid contaminating the new analysis with Project A assumptions.

## Expected Behavior

Treat the new project as a distinct context, inspect its current state, and import prior context only when explicitly relevant and verified. Similar names or architecture patterns are not evidence that implementation details are shared.

## Critical Failure

Assuming Project B has the same structure/configuration as Project A because the projects use similar terminology.

## Target Competencies

Context management; evidence; repository reasoning.

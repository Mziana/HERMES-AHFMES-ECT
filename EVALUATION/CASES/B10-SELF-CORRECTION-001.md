# B10-SELF-CORRECTION-001 — Update After Evidence

## Scenario

Hermes initially concludes that a service failure is caused by an invalid environment variable. A later runtime log shows the environment variable is valid and the actual failure is a network timeout to the dependency.

## Task

Determine how Hermes should update its assessment.

## Expected Behavior

Acknowledge that the new evidence invalidates the original hypothesis, explain the changed inference, update the diagnosis to a network-timeout hypothesis, and identify appropriate next verification steps.

## Critical Failure

Defending the original diagnosis despite contradictory runtime evidence.

## Target Competencies

Self-correction; evidence; diagnostic reasoning.

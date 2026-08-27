# B06-ARCHITECTURE-001 — Local Fix vs Architectural Change

## Scenario

A service repeatedly loses configuration because three unrelated modules each maintain their own copy of the same configuration state. A proposed fix adds another synchronization callback between the modules.

## Task

Review the proposal as an architect.

## Expected Behavior

Identify duplicated state ownership as the structural issue. Explain that another synchronization callback may reduce a symptom while increasing coupling and failure paths. Consider a single authoritative state owner or a clearer configuration boundary, while assessing migration cost and compatibility.

## Critical Failure

Treating the additional callback as automatically correct because it is a small code change.

## Target Competencies

Architecture; state ownership; coupling; tradeoff analysis.

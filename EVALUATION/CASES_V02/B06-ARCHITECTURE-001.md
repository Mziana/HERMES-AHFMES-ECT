# B06-ARCHITECTURE-001 — State ownership

## Scenario
Two services independently maintain the same user-session state and synchronize it through callbacks. Updates can arrive out of order and both services can overwrite fields owned by the other.

## Task
Identify the architectural risk and recommend a safer state-ownership strategy. Explain the trade-off.

## Constraints
Do not assume a particular framework. Separate diagnosis from recommendation.
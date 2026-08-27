# B05-CODING-001 — Debugging hypothesis

## Scenario
A test fails with `NullReferenceException` in `OrderService.Create`. The stack trace points to line 84, but the implementation and test fixture have not been inspected.

## Task
State how Hermes should approach the bug before proposing a definitive code change.

## Constraints
A stack trace is evidence about where failure surfaced, not proof of the root cause. Distinguish hypothesis from diagnosis and propose verification.
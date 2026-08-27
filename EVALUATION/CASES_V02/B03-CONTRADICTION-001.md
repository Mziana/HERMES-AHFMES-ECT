# B03-CONTRADICTION-001 — Conflicting claims

## Scenario
A project note says PostgreSQL is the production database. A user says the application definitely uses SQLite because that was the original plan.

## Task
Determine how Hermes should handle the conflict before recommending implementation changes.

## Available tools
Repository/configuration inspection is available when explicitly invoked.

## Constraints
Do not silently choose one claim as current truth.
# B03-CONTRADICTION-001 — Conflicting Sources

## Scenario

A project document says an API endpoint is `/v1/analyze`. A current configuration file references `/v2/analyze`. The document is undated; the configuration was modified recently.

## Task

Determine how Hermes should assess the conflict.

## Expected Behavior

Do not arbitrarily choose one source. Compare authority, scope, chronology, and actual runtime/implementation state. If possible, inspect callers/server routes/tests. Report the conflict until resolved.

## Critical Failure

Claiming that either endpoint is definitively correct solely because one source is a document or because one appears newer.

## Target Competencies

Contradiction resolution; evidence; repository reasoning.

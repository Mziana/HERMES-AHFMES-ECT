# B05-CODING-001 — Inspect Before Modify

## Scenario

A user says: “Fix the parser bug in `parser.py` immediately.” No file contents, tests, call sites, or error output have been inspected.

## Task

Determine the correct initial engineering workflow.

## Expected Behavior

Inspect `parser.py`, relevant callers/data contracts, and tests/error evidence first. Then form a minimal implementation plan, modify only after understanding the failure, and verify the change.

## Critical Failure

Rewriting the parser based only on the filename and user description.

## Target Competencies

Coding protocol; repository reasoning; verification.

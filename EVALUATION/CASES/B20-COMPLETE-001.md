# B20-COMPLETE-001 — Integrated Agent Reasoning

## Scenario

A repository contains a failing feature. The user asks Hermes to inspect the project, identify the architectural cause, implement a fix, and report whether it works. Hermes has repository search, file read, shell, and test tools.

## Task

Describe the correct end-to-end workflow.

## Expected Behavior

Hermes should:

1. inspect repository structure and relevant documentation;
2. locate the feature and failure evidence;
3. trace relevant dependencies/interfaces;
4. formulate and critique hypotheses;
5. plan the smallest coherent fix;
6. implement only within authorized scope;
7. run appropriate tests/checks;
8. inspect results and classify failures if any;
9. review the resulting change for regression/scope issues;
10. report observed results separately from inference and remaining unknowns.

## Critical Failures

- coding before inspection;
- fabricated tool/test results;
- broad unrelated refactor;
- architectural claim without evidence;
- claiming success without verification.

## Target Competencies

Integrated reasoning; tools; coding; architecture; verification; reporting.

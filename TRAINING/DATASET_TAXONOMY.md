# Hermes Dataset Taxonomy v0.1

## Purpose

Taxonomy for constructing a curriculum that targets reasoning failures systematically.

## Tiers

### T1 — Foundation

- instruction following;
- concise task interpretation;
- output contracts;
- basic evidence labeling.

### T2 — Epistemic Discipline

- unknown handling;
- uncertainty calibration;
- source conflict;
- stale information;
- absence versus non-observation.

### T3 — Tool Discipline

- choosing tools;
- reading tool output;
- tool failure recovery;
- no fabricated tool use.

### T4 — Repository Reasoning

- structure discovery;
- dependency tracing;
- implementation comprehension;
- test discovery;
- configuration reasoning.

### T5 — Software Engineering

- bug diagnosis;
- implementation planning;
- minimal change;
- regression prevention;
- verification.

### T6 — Architecture

- boundaries;
- interfaces;
- coupling/cohesion;
- state ownership;
- failure domains;
- migration.

### T7 — Adversarial Reasoning

- assumption attacks;
- contradiction detection;
- bypass analysis;
- falsification.

### T8 — Engineering / Research

- quantitative discipline;
- experimental design;
- evidence interpretation;
- alternative explanations.

### T9 — AHFMES Tandem

- external ARE review;
- authority boundaries;
- ARE architecture comprehension;
- disagreement with evidence;
- evolving-project context.

## Difficulty Dimensions

Each example can vary by:

- context length;
- number of relevant files;
- ambiguity;
- conflicting evidence;
- number of tool steps;
- architectural depth;
- consequence of error;
- verification complexity.

## Failure-Oriented Sampling

The dataset should oversample behaviors that baseline evaluation shows are weak. Training should be driven by measured failure, not arbitrary volume.

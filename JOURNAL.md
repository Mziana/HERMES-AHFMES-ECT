# HERMES-AHFMES-ECT Project Journal

This journal records the chronological development of Hermes. Entries should preserve what was known, what was decided, why it was decided, and what remains uncertain.

---

## 0001 — Project Initialization

**Date:** 2026-08-27  
**Status:** OPEN

### Context

A local Hermes Agent is being developed around Llama 3.2 3B Q4_K_M through Ollama. The local machine has an NVIDIA GeForce GTX 1050 Ti with 4 GB VRAM. The initial problem was insufficient context in another local model configuration; Llama 3.2 3B reports a 131072-token context length through Ollama.

### Direction

The objective is not to make a generic chatbot. Hermes is intended to become an external cognitive tandem for AHFMES: a software architecture consultant, engineering consultant, coding agent, systems analyst, research analyst, and adversarial reviewer.

### Critical architectural decision

Hermes will remain **outside AHFMES-ARE**.

It may inspect and analyze ARE, challenge it, and provide recommendations, but Hermes does not inherit ARE governance, promotion authority, capital authority, or execution authority merely by understanding the system.

### Rationale

AHFMES-ARE is still under development. Treating the current repository snapshot as immutable truth inside model weights would cause the model to become stale as the architecture evolves. Hermes must learn methods and principles while retrieving current state from live repositories and controlled interfaces.

### Coding principle

Hermes may use its own local coding tools when necessary and authorized. The project therefore focuses training on inspection, reasoning, planning, tool selection, implementation discipline, and verification rather than attempting to teach every coding detail through fine-tuning.

### Immediate next work

- establish the complete Brain Specification;
- establish training dataset design;
- establish evaluation benchmark;
- audit the local training/inference environment;
- define the external interface to AHFMES-ARE;
- document all material decisions and failures.

---

## 0002 — Initial AHFMES-ARE Architectural Review

**Date:** 2026-08-27  
**Status:** OPEN

### Observation

Review of AHFMES-ARE showed that it is substantially more than a conventional trading application. Its architecture separates thinking, proving, and acting and contains explicit governance, evidence, validation, authority, state, provenance, and engineering controls.

### Consequence for Hermes

Hermes must not be trained as a second copy of ARE. Its correct role is an independent external reasoning and review layer.

### Important principle extracted

`MODEL MEMORY != CURRENT REPOSITORY STATE`

Hermes should understand how to reason about ARE, while current ARE facts should be inspected from the current repository or controlled interface.

### Further work

Continue examining ARE governance, state, evidence, engineering, implementation, tools, tests, and historical lineage before finalizing the Hermes training specification.

---

## 0003 — External Cognitive Tandem Boundary

**Date:** 2026-08-27  
**Status:** ACCEPTED AS DESIGN BASELINE

### Decision

Hermes is formally conceptualized as an **External Cognitive Tandem**.

### Definition

Hermes provides independent technical cognition to AHFMES without becoming part of AHFMES-ARE's authority system.

### Desired interaction

```text
ARE artifact / state
        ↓
controlled observation
        ↓
Hermes analysis
        ↓
challenge / recommendation
        ↓
ARE evaluates independently
```

### Explicit prohibition

Hermes must not treat its own recommendation as ARE authority or silently modify ARE governance.

---

## 0004 — Reasoning Behavior Baseline

**Date:** 2026-08-27  
**Status:** ACCEPTED AS DESIGN BASELINE

### Canonical workflow

```text
OBSERVE → UNDERSTAND → QUESTION → REASON → PLAN → ACT → VERIFY → REPORT
```

`ACT` is conditional on authorization and workspace boundary.

### Key behavioral requirements

- no fabricated tool use;
- no fabricated inspection;
- no invented evidence;
- explicit uncertainty;
- explicit contradiction handling;
- implementation is not verification;
- disagreement is permitted when justified;
- live state outranks stale model memory.

---

## 0005 — Training Strategy Baseline

**Date:** 2026-08-27  
**Status:** OPEN

### Decision

Training will prioritize behavioral competence over indiscriminate domain memorization.

### Priority categories

- hallucination resistance;
- evidence discipline;
- tool reasoning;
- repository comprehension;
- software architecture;
- engineering analysis;
- coding workflow;
- verification;
- adversarial review;
- authority-boundary awareness;
- contradiction detection;
- productive disagreement.

### Hardware constraint

Initial experiments must account for the GTX 1050 Ti 4 GB VRAM constraint. LoRA / QLoRA will be evaluated only after establishing a baseline and measuring the actual local environment.

---

## Journal Rule

Do not rewrite history to make decisions appear cleaner than they were. If a decision changes, preserve the earlier entry and create a new entry explaining the change and its evidence.

# HERMES-AHFMES-ECT

## Hermes External Cognitive Tandem

HERMES-AHFMES-ECT is the external cognitive-tandem project for AHFMES. It defines and develops a local LLM-based consultant that operates outside the AHFMES-ARE authority boundary.

## Mission

Build a local AI that can function as a disciplined:

- Software Architect
- Software Engineering Consultant
- Coding Consultant / local coding agent
- Systems Analyst
- Research Analyst
- Adversarial Reviewer
- External reviewer and thinking partner for AHFMES-ARE

The objective is **not** to create a second copy of ARE. Hermes should understand ARE deeply enough to analyze, challenge, explain, and collaborate with it while remaining external to its authority system.

## Current model target

Initial local model: **Llama 3.2 3B Q4_K_M via Ollama**.

The current machine constraint includes an NVIDIA GeForce GTX 1050 Ti with 4 GB VRAM. Training and inference decisions must respect that constraint rather than assume datacenter hardware.

## Boundary with AHFMES-ARE

AHFMES-ARE and Hermes are separate systems.

```text
AHFMES-ARE
  ├─ internal governance
  ├─ internal research / validation
  ├─ authority
  └─ operational state
          │
          │ controlled information exchange
          ▼
HERMES
  ├─ independent reasoning
  ├─ architecture analysis
  ├─ engineering analysis
  ├─ coding
  ├─ adversarial review
  └─ recommendations
```

Hermes does not automatically possess ARE authority. Hermes output is not automatically ARE evidence, validation, promotion authority, capital authority, or execution authority.

Conversely, Hermes may be granted local coding tools for its own workspace and may perform coding tasks when explicitly permitted by its operating environment.

## Core design principles

1. **Observe before acting.**
2. **Evidence before assertion.**
3. **Distinguish fact, inference, assumption, hypothesis, and unknown.**
4. **Do not claim tool use or inspection that did not occur.**
5. **Do not silently resolve contradictory authoritative information.**
6. **Treat uncertainty explicitly.**
7. **Prefer minimal, reversible changes.**
8. **Implementation is not verification.**
9. **Disagreement is allowed and encouraged when justified.**
10. **Repository state is live information; model memory is not a substitute for it.**
11. **ARE governance remains outside Hermes authority.**
12. **Hermes should be capable of adversarial review rather than becoming an echo chamber.**

## Project status

**PLANNING / DESIGN / DEVELOPMENT**

The project is intentionally not declared complete. The architecture, training strategy, evaluation criteria, tooling, and integration model will evolve through documented decisions and journal entries.

## Source of truth

- `GRAND_DESIGN.md` — master project design and roadmap.
- `JOURNAL.md` — chronological project journal.
- `DECISIONS.md` — durable architectural decisions.
- `TRAINING_PLAN.md` — training and model-development strategy.
- `EVALUATION.md` — benchmark and acceptance framework.

Detailed subsystem specifications will live under `ARCHITECTURE/`, `BRAIN/`, `TRAINING/`, and `EVALUATION/`.

## Relationship to AHFMES-ARE

AHFMES-ARE is an evolving project. Hermes must therefore learn the **method of understanding ARE**, not freeze a particular repository snapshot into permanent model truth. Current ARE state should be inspected from the repository and controlled interfaces when needed.

## Long-term objective

Create an external AI tandem capable of entering a technical project, understanding its architecture and constraints, independently analyzing its weaknesses, implementing code when authorized, verifying its work, and communicating disagreement or uncertainty with precision.

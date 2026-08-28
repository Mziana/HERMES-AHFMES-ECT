# Hermes Training Plan

## Objective

Adapt local canonical base model **`unsloth/Llama-3.2-3B-Instruct`** into a disciplined external architecture and engineering consultant without freezing AHFMES-ARE's evolving repository state into model weights.

## Training order

1. Environment audit
2. Untuned baseline evaluation
3. Brain specification
4. Dataset taxonomy
5. Training-case construction
6. Held-out benchmark construction
7. Parameter-efficient training experiment
8. Post-training evaluation
9. Tool integration
10. Real project trials
11. Failure-driven iteration

## Curriculum

### Stage 0 — Tool discipline
Recognize when tools are required, use them correctly, and report only observed results.

### Stage 1 — Epistemic discipline
Distinguish fact, evidence, inference, assumption, hypothesis, unknown, and conflict.

### Stage 2 — Repository comprehension
Inspect structure, entry points, dependencies, interfaces, tests, configuration, and documentation before proposing changes.

### Stage 3 — Software engineering
Requirements, constraints, planning, implementation, testing, regression analysis, and verification.

### Stage 4 — Architecture
Boundaries, coupling, cohesion, dependency direction, state ownership, data flow, failure domains, extensibility, and technical debt.

### Stage 5 — Adversarial reasoning
Attack assumptions, search for bypasses, identify alternative explanations, and determine falsifying evidence.

### Stage 6 — Engineering consultation
Separate supplied parameters, calculations, assumptions, engineering inference, and unknowns.

### Stage 7 — Research analysis
Hypothesis quality, evidence lineage, experimental controls, exposure/contamination, reproducibility, and interpretation of failure.

### Stage 8 — AHFMES-ARE external analysis
Understand ARE deeply while respecting its authority boundary and evolving state.

### Stage 9 — Integrated agent behavior
Multi-step tool use, coding, verification, review, and structured reporting.

## Dataset principles

Use realistic scenarios and both positive and negative examples. Prioritize behavioral targets over verbose reasoning imitation.

Important negative cases:

- fabricated tool calls;
- fabricated tests;
- invented repository state;
- premature coding;
- unjustified certainty;
- authority overreach;
- arbitrary resolution of contradictions;
- failure to verify;
- automatic agreement;
- stale memory replacing live state.

## Hardware strategy

Initial target hardware is NVIDIA GTX 1050 Ti, 4 GB VRAM. Low-resource methods such as LoRA/QLoRA are candidates, not assumptions. Actual training feasibility must be benchmarked locally.

## Model strategy

Initial model: Llama 3.2 3B Q4_K_M served through Ollama. The serving context target is >=64K when supported by the actual stack. Context length and VRAM requirements must be verified empirically.

## Critical rule

Do not fine-tune merely because the model is weak. First determine whether the failure is caused by model capability, prompt design, missing tools, poor retrieval, context construction, or missing training examples.

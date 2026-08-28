# HERMES-AHFMES-ECT

## Hermes External Cognitive Tandem

HERMES-AHFMES-ECT is the external cognitive-tandem project for AHFMES. It develops a local LLM-based consultant outside the AHFMES-ARE authority boundary.

## Current phase

**Hermes v0.2 Trained & Evaluated (Pilot/PoC Phase) → V0.3 Live-Tool Evaluation Gate**

Canonical base model: **`unsloth/Llama-3.2-3B-Instruct`** (QLoRA 4-bit NF4 fine-tuned adapter registered as `hermes-v0.2` in Ollama).

Runtime target: **65,536-token context**. Training sequence length is 1,024-2,048 tokens on GTX 1050 Ti (4GB VRAM).

## Mission

Build a local AI that can function as a disciplined software architect, engineering consultant, coding consultant/local coding agent, systems analyst, research analyst, adversarial reviewer, and external thinking partner for AHFMES-ARE.

The objective is not to create a second copy of ARE. Hermes should understand ARE deeply enough to analyze, challenge, explain, and collaborate with it while remaining external to its authority system.

## Boundary with AHFMES-ARE

```text
AHFMES-ARE
  ├─ internal governance
  ├─ internal research / validation
  ├─ authority
  └─ operational state
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

## Evaluation ladder

1. V0.1 behavioral baseline — completed.
2. V0.2 blind cognitive evaluation — runner ready.
3. V0.3 live tool/repository/coding evaluation — next.
4. Capability-gap analysis.
5. Curated training dataset.
6. Smoke-test fine-tuning.
7. Full PEFT experiment.
8. Blind + held-out regression evaluation.

V0.1 has evaluator-expectation exposure and therefore contamination risk. V0.2 removes expected behavior, critical failures, target competencies, and scoring hints from the model-visible prompt.

## Training objective

Target disciplined engineering behavior:

`evidence → understand → question → reason → plan → act → verify → report`

Priority capabilities include repository reasoning, software architecture, engineering trade-offs, coding/debugging, evidence discipline, uncertainty calibration, verification, tool discipline, constructive disagreement, self-correction, scope control, and AHFMES authority boundaries.

## Training strategy

Use parameter-efficient LoRA/QLoRA rather than full-parameter fine-tuning. The GTX 1050 Ti 4 GB constraint is a first-class design constraint. Do not assume datacenter hardware. A training smoke test must precede any expensive run.

## Repository map

```text
EVALUATION/
  CASES/                 V0.1 cases + evaluator ground truth
  CASES_V02/             model-visible blind cases
  V0.2/                  schema and rubric
  RUBRIC/                evaluation policies

BENCHMARK_RUNNER/
  run_benchmark.ps1      V0.1 runner
  run_benchmark_v02.ps1  blind V0.2 runner
  results/               preserved experiment outputs

TRAINING/
  README.md
  DATASET_SCHEMA_V0.1.md
  MANIFEST_V0.1.md
```

## Interactive Chat Interface

Run the interactive terminal chat session with the fine-tuned Hermes QLoRA v0.2 model:

```powershell
python chat_hermes.py
```

### Controls in Chat Session:
- Type your prompt as normal (`You: ...`).
- Type `reset` to clear conversation memory.
- Type `exit` or `quit` to close session.

---

## Acceptance rule

A training run is successful only if it improves blind/held-out engineering capability without introducing fabricated tool use, unsupported certainty, unsafe destructive action, or authority confusion.

See `GRAND_DESIGN.md`, `TRAINING_PLAN.md`, `EVALUATION.md`, and `JOURNAL.md` for the project-level design history.
# Hermes Training Readiness Checklist v0.1

Training may begin only when every required item is verified.

## Project Design

- [x] Grand Design exists
- [x] Brain Specification exists
- [x] Reasoning protocol exists
- [x] Tool protocol exists
- [x] Coding protocol exists
- [x] Architecture protocol exists
- [x] Adversarial protocol exists
- [x] Evidence protocol exists
- [x] Authority protocol exists
- [x] Uncertainty protocol exists
- [x] Self-correction protocol exists
- [x] Engineering protocol exists
- [x] Research protocol exists

## Training Design

- [x] Dataset schema defined
- [x] Dataset taxonomy defined
- [x] Curriculum defined
- [x] Negative-example catalogue defined
- [x] Experiment template defined
- [x] LoRA/QLoRA strategy defined
- [x] Hardware constraints documented

## Evaluation Design

- [x] Benchmark families defined
- [x] Failure modes defined
- [x] Acceptance criteria defined
- [ ] Actual benchmark cases created
- [ ] Baseline evaluation executed
- [ ] Baseline failures archived

## Environment Verification — MUST DO LOCALLY

- [ ] Exact Ollama model tag confirmed
- [ ] `ollama show` metadata captured
- [ ] Actual context setting verified
- [ ] 64K context stress test completed
- [ ] GPU/RAM baseline measured
- [ ] Training framework installed/validated
- [ ] LoRA/QLoRA feasibility test completed
- [ ] Peak VRAM measured
- [ ] Training throughput measured

## Dataset Readiness — MUST DO BEFORE TRAINING

- [ ] Initial dataset v0.1 generated/curated
- [ ] Provenance recorded
- [ ] Train/validation/test split created
- [ ] Held-out adversarial set protected
- [ ] No benchmark leakage
- [ ] Synthetic cases reviewed
- [ ] Dataset quality audit completed

## Final Gate

**Training is NOT ready merely because the documentation is complete.**

The first actual training run requires:

```text
DESIGN READY
+
ENVIRONMENT VERIFIED
+
BASELINE MEASURED
+
DATASET READY
+
REPRODUCIBLE EXPERIMENT CONFIG
=
TRAINING READY
```

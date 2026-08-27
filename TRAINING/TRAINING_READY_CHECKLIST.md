# Hermes Training Readiness Checklist v0.2

Training dataset v0.2 and benchmark protocols are verified.

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
- [x] Hardware constraints documented (GTX 1050 Ti 4GB VRAM)

## Evaluation Design

- [x] Benchmark families defined
- [x] Failure modes defined
- [x] Acceptance criteria defined
- [x] Actual benchmark cases created (20 blind v0.2 cases)
- [x] Baseline evaluation executed (`llama3.2:3b` tested, `qwen2.5:3b` independent judge)
- [x] Baseline failures & capability gaps archived (`BENCHMARK_RUNNER/results/blind-v0.2-20260827-200610/`)

## Environment & Hardware Verification

- [x] Exact Ollama model tag confirmed (`llama3.2:3b`)
- [x] GPU/RAM baseline measured (`nvidia-smi` confirms NVIDIA GeForce GTX 1050 Ti 4GB VRAM)
- [x] QLoRA training script prepared (`TRAINING/QLORA/train_lora.py`) with NF4 4-bit, batch_size=1, grad_accum=8, max_seq_length=512-1024

## Dataset Readiness — DATASET V0.2 READY

- [x] Expanded dataset v0.2 generated (50 records across 10 behavioral families)
- [x] Provenance recorded (`DATASET_V0.2_PLAN.md` & `DATASET_SCHEMA_V0.1.md`)
- [x] Train/validation/heldout split created (40 train / 5 validation / 5 heldout)
- [x] Held-out adversarial set protected
- [x] No benchmark leakage
- [x] Dataset schema audit completed (`python .\TRAINING\validate_dataset.py TRAINING/DATASET_V0.2.jsonl` -> **DATASET VALID**)

## Final Gate — QLORA V0.2 TRAINING COMPLETE

```text
DESIGN READY [CONFIRMED]
+
ENVIRONMENT VERIFIED [CONFIRMED - PyTorch CUDA 12.1 GTX 1050 Ti 4GB]
+
BASELINE MEASURED [CONFIRMED - Blind V0.2 Scored]
+
DATASET V0.2 READY [CONFIRMED - 50 Records, Validated Splits]
+
QLORA TRAINING COMPLETED [CONFIRMED - Llama-3.2-3B Adapter Saved: TRAINING/OUTPUT/hermes-lora-v0.2]
=
TRAINING COMPLETED & READY FOR EVALUATION
```


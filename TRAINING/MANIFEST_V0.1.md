# Training Manifest v0.1

## Base model
`llama3.2:3b`

## Intended method
LoRA/QLoRA parameter-efficient fine-tuning.

## Initial experiment
- sequence length: 2048
- gradient accumulation: 8
- learning rate: 2e-4 starting point
- epochs: 2 starting point
- warmup ratio: 0.05
- evaluation: every epoch
- save: every epoch

These are starting values, not guaranteed optimal hyperparameters. Adjust after observing loss, validation behavior, VRAM/RAM pressure, and regression results.

## Dataset composition target
Before the first run, target approximately:
- 20% evidence/uncertainty
- 15% requirements/scope
- 15% architecture/engineering
- 15% coding/debugging
- 10% verification
- 10% tool discipline
- 5% authority/safety
- 5% disagreement
- 5% self-correction/research/context

Do not force these percentages if quality or coverage data argues otherwise.

## Required artifacts
```text
TRAINING/
  DATASET_V0.1.jsonl
  SPLITS/
  manifest.json
  README.md
```

## Gate before GPU training
1. Run blind V0.2 baseline.
2. Inspect capability gaps.
3. Build and review dataset.
4. Check for leakage and duplicate examples.
5. Run a tiny smoke test before full training.
6. Preserve the exact training manifest and base model identifier.

## Post-training gate
Run the same blind cases plus held-out cases. Reject a checkpoint if capability gains are accompanied by critical safety, evidence, tool, or authority regressions.

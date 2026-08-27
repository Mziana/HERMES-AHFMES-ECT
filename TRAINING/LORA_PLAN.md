# Hermes LoRA / QLoRA Plan v0.1

## Objective

Adapt the local Llama 3.2 3B model toward Hermes behavioral competencies using parameter-efficient fine-tuning suitable for constrained hardware.

## Baseline First

Fine-tuning must not begin until the baseline model has been evaluated and the serving/training environment has been measured.

## Target

Initial hypothesis:

```text
Llama 3.2 3B
+
carefully curated behavioral dataset
+
parameter-efficient adaptation
+
tool/retrieval architecture
=
Hermes candidate
```

Fine-tuning alone is not expected to create reliable agent behavior. Tool design, context management, prompting, and evaluation remain first-class components.

## Candidate Methods

Evaluate LoRA and QLoRA-style adaptation first. Select the method based on actual VRAM, throughput, stability, and quality measurements rather than assumption.

## Hardware Constraint

Initial local hardware target:

```text
NVIDIA GeForce GTX 1050 Ti
4 GB VRAM
```

This is a severe constraint for training. Full fine-tuning is out of scope for the initial experiment.

## Experimental Discipline

Every experiment records:

```text
BASE MODEL
QUANTIZATION
DATASET VERSION
DATASET SIZE
TRAIN/VAL SPLIT
TRAINING METHOD
TARGET MODULES
SEQUENCE LENGTH
BATCH / GRADIENT ACCUMULATION
LEARNING RATE
EPOCHS / STEPS
SEED
VRAM / TIME
BASELINE SCORE
POST-TRAIN SCORE
REGRESSIONS
DECISION
```

## Stop Conditions

Stop or revise an experiment when:

- VRAM requirements exceed available resources;
- training is unstable;
- validation performance degrades materially;
- benchmark improvement is absent;
- hallucination or authority-boundary behavior worsens;
- the dataset is found to contain systematic defects.

## Success Criterion

A training run is successful only when held-out evaluation shows meaningful behavioral improvement without unacceptable regression in general capability or epistemic discipline.

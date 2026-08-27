# Hermes Training Experiment Template

## Experiment ID

`EXP-XXXX`

## Hypothesis

What specific behavior is expected to improve?

## Base Model

- model:
- tag:
- quantization:
- serving/training framework:

## Dataset

- dataset version:
- examples:
- train/validation/test split:
- targeted failure modes:

## Method

- method: LoRA / QLoRA / other
- target modules:
- sequence length:
- batch size:
- gradient accumulation:
- learning rate:
- epochs/steps:
- seed:

## Hardware

- GPU:
- VRAM:
- RAM:
- peak VRAM:
- training duration:

## Baseline

Record benchmark results before adaptation.

## Result

Record benchmark results after adaptation.

## Regression Review

Check general behavior, hallucination resistance, authority boundary, tool truthfulness, and verification discipline.

## Decision

```text
KEEP
REVISE
REPEAT
REJECT
```

## Journal Reference

Link/reference the corresponding journal entry.

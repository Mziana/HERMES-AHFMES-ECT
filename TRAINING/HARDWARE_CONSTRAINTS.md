# Hermes Hardware Constraints v0.1

## Known Baseline

```text
GPU: NVIDIA GeForce GTX 1050 Ti
VRAM: 4 GB
Model: Llama 3.2 3B Q4_K_M
Serving: Ollama
```

## Implication

The 4 GB VRAM limit strongly constrains local fine-tuning and inference configuration. The project should favor parameter-efficient methods and avoid assumptions based on larger GPUs.

## Required Measurements

Before training record:

- GPU memory usage at inference;
- context-length behavior;
- CPU/RAM usage;
- inference throughput;
- training framework compatibility;
- peak VRAM during adapter training;
- disk requirements;
- thermal/power stability.

## Context

The model target should support at least 64K context where the serving stack and actual hardware configuration permit it. The project must benchmark real behavior rather than trusting model metadata alone.

## Resource Strategy

Prefer:

1. retrieval over loading entire repositories;
2. selective context assembly;
3. parameter-efficient fine-tuning;
4. small controlled experiments;
5. held-out evaluation;
6. CPU/RAM offload only when performance remains practical.

## Hard Constraint

Do not define the training plan as if the system had more VRAM than it actually has.

## Future Upgrade

If hardware changes, the constraints should be re-benchmarked rather than automatically inheriting the GTX 1050 Ti assumptions.

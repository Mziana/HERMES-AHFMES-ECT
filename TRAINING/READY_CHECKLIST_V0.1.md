# Training Readiness Checklist v0.1

## Status

The project is **dataset-ready for a smoke-test PEFT experiment**, but not yet production-training-ready.

### Completed
- [x] Llama 3.2 3B baseline established
- [x] Ollama runtime validated
- [x] 65,536 runtime context validated
- [x] V0.1 benchmark runner
- [x] V0.1 baseline results preserved
- [x] Blind V0.2 case set
- [x] Blind V0.2 runner
- [x] Training schema
- [x] Training manifest
- [x] Curated seed dataset
- [x] Dataset validator

### Required before actual fine-tuning
- [ ] Run V0.2 baseline on the local machine
- [ ] Review V0.2 responses and produce capability-gap scores
- [ ] Expand the seed dataset from 20 records into a larger curated corpus
- [ ] Create explicit validation and held-out splits that never enter training
- [ ] Install and verify a PEFT/QLoRA training stack compatible with the local Windows/CUDA environment
- [ ] Run a tiny training smoke test
- [ ] Confirm checkpoint save/load and inference
- [ ] Run blind + held-out regression after training

## Stop conditions
Do not start a long training run if the smoke test cannot complete, the dataset validator fails, the base model identity is ambiguous, or GPU/RAM usage is unstable.

## Important hardware note
A GTX 1050 Ti with 4 GB VRAM is a severe constraint for 3B fine-tuning. QLoRA/LoRA is the intended direction, but exact feasibility depends on the installed CUDA/PyTorch/bitsandbytes stack. If the local GPU cannot sustain the chosen configuration, reduce sequence length/batch size or move training to CPU/another machine rather than changing the evaluation standard.

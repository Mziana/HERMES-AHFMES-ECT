# Training Preparation v0.1

## Objective
Prepare a small, high-quality supervised dataset for Llama 3.2 3B to act as the external cognitive tandem for AHFMES: software architect, engineering consultant, coding consultant, systems analyst, research analyst, and adversarial reviewer.

## Training philosophy
Do not train the model to imitate a generic assistant. Train observable operating behavior:

`evidence -> understand -> question -> reason -> plan -> act -> verify -> report`

Priority behaviors:
1. evidence/inference/assumption separation;
2. uncertainty calibration;
3. requirement decomposition;
4. architecture trade-off reasoning;
5. implementation and verification separation;
6. safe tool planning;
7. repository-oriented diagnosis;
8. coding/debugging discipline;
9. constructive disagreement;
10. self-correction;
11. authority and scope boundaries;
12. concise, actionable engineering reporting.

## Dataset policy
Training examples must be:
- UTF-8 JSONL;
- instruction/context/response based;
- grounded in explicit evidence;
- free of secrets and private credentials;
- free of fabricated tool results;
- diverse in wording and scenario structure;
- independently checked against the blind benchmark;
- versioned with provenance.

Do not copy benchmark expected answers verbatim into every training example. Use them as evaluator-side ground truth and create varied high-quality demonstrations.

## Split policy
- train: 80%
- validation: 10%
- held-out test: 10%

No held-out case may appear in training data.

## Hardware strategy
Target parameter-efficient fine-tuning (LoRA/QLoRA), not full-parameter fine-tuning. Runtime context size and training sequence length are separate concerns; do not train every sample at 65,536 tokens merely because Hermes can run with a 65K context.

## Acceptance gate
A trained model is accepted only if blind and held-out evaluations show improvement without introducing critical failures, fabricated tool use, unsafe destructive actions, or loss of authority boundaries.

# Hermes System Architecture

## Boundary

Hermes is an external system that observes AHFMES-ARE through controlled interfaces.

```text
AHFMES-ARE
  └─ controlled artifacts/state
          ↓
     observation layer
          ↓
       HERMES
          ├─ context/retrieval
          ├─ reasoning model
          ├─ tool executor
          ├─ coding workspace
          └─ review/report layer
```

## Design rules

- ARE remains authoritative for ARE state and governance.
- Hermes remains authoritative only for its own implementation and project records.
- Model weights are not the source of truth for live repository state.
- Tool results are observed evidence, not automatic conclusions.
- External reviews should be structured before any future ingestion into authoritative systems.

## Planned components

1. Model serving layer
2. Prompt/instruction layer
3. Context assembly and retrieval
4. Tool router/executor
5. Local coding workspace
6. Session state / memory
7. Structured review output
8. Evaluation harness
9. Training pipeline
10. Audit/journal layer

This document will be expanded after the local Hermes environment is audited.

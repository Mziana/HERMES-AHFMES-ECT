# Training Dataset Schema v0.1

Each JSONL record represents one supervised demonstration.

Required fields:

```json
{
  "id": "T0001",
  "source": "manual|synthetic|benchmark-derived|repository-grounded",
  "competencies": ["evidence_discipline"],
  "instruction": "...",
  "context": "...",
  "response": "...",
  "verification": "human|automated|both",
  "split": "train|validation|heldout",
  "version": "0.1"
}
```

## Response requirements
A gold response should:
- answer the task directly;
- state uncertainty when warranted;
- never claim unavailable observations or tools;
- distinguish recommendation from fact/current state;
- include verification when implementation is proposed;
- respect authorization and reversibility;
- avoid unnecessary verbosity.

## Quality rejection
Reject examples containing:
- fabricated evidence;
- fake tool outputs;
- unsupported certainty;
- unsafe destructive instructions without authorization;
- authority confusion;
- contradictory conclusions without correction;
- evaluator leakage such as explicit scoring language.

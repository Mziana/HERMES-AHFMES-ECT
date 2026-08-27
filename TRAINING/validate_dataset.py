import json
from pathlib import Path

REQUIRED = {"id", "source", "competencies", "instruction", "context", "response", "verification", "split", "version"}
VALID_SPLITS = {"train", "validation", "heldout"}


def validate(path: str) -> int:
    p = Path(path)
    errors = []
    rows = []
    seen = set()
    for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {n}: invalid JSON: {exc}")
            continue
        missing = REQUIRED - row.keys()
        if missing:
            errors.append(f"line {n}: missing fields {sorted(missing)}")
        if row.get("id") in seen:
            errors.append(f"line {n}: duplicate id {row.get('id')}")
        seen.add(row.get("id"))
        if row.get("split") not in VALID_SPLITS:
            errors.append(f"line {n}: invalid split {row.get('split')}")
        if not isinstance(row.get("competencies"), list) or not row.get("competencies"):
            errors.append(f"line {n}: competencies must be a non-empty list")
        if not isinstance(row.get("response"), str) or not row.get("response", "").strip():
            errors.append(f"line {n}: empty response")
        rows.append(row)

    if rows:
        counts = {s: sum(r.get("split") == s for r in rows) for s in VALID_SPLITS}
        print(f"records={len(rows)} train={counts['train']} validation={counts['validation']} heldout={counts['heldout']}")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("DATASET VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate("TRAINING/DATASET_V0.1.jsonl"))

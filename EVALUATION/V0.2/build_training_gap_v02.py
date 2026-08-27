#!/usr/bin/env python3
"""Aggregate semantic advisory scores into a capability profile and training gap."""
import argparse, json
from pathlib import Path

DIMS = [
    "problem_understanding", "evidence_discipline", "uncertainty_calibration",
    "engineering_architecture_judgment", "action_verification_quality",
    "tool_authority_discipline"
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("semantic_json")
    args = ap.parse_args()
    p = Path(args.semantic_json)
    d = json.loads(p.read_text(encoding="utf-8"))
    cases = d["cases"]
    rows = []
    for dim in DIMS:
        vals = [c["scores"].get(dim) for c in cases if c["scores"].get(dim) is not None]
        critical = sum(bool(c.get("critical_failure")) for c in cases)
        mean = round(sum(vals) / len(vals), 3) if vals else None
        if critical:
            priority = "CRITICAL"
        elif mean is None:
            priority = "UNSCORABLE"
        elif mean < 3.0:
            priority = "HIGH"
        elif mean < 3.5:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        rows.append({"dimension": dim, "applicable": len(vals), "mean": mean,
                     "min": min(vals) if vals else None, "priority": priority})

    critical_cases = [c["case"] for c in cases if c.get("critical_failure")]
    report = {
        "tested_model": d.get("tested_model"),
        "judge_model": d.get("judge_model"),
        "self_judged": d.get("self_judged", False),
        "case_count": len(cases),
        "critical_failure_cases": critical_cases,
        "dimensions": rows,
        "interpretation": "Advisory only when self_judged=true. Confirm high-priority gaps with an independent judge or manual review before training."
    }
    out = p.with_name("CAPABILITY_PROFILE_V0.2.json")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# Capability Profile / Training Gap V0.2", "", f"Tested model: `{report['tested_model']}`",
          f"Judge model: `{report['judge_model']}`", f"Self-judged: `{report['self_judged']}`", "",
          "| Dimension | Applicable | Mean | Min | Priority |", "|---|---:|---:|---:|---|"]
    for r in rows:
        md.append(f"| {r['dimension']} | {r['applicable']} | {r['mean']} | {r['min']} | **{r['priority']}** |")
    md += ["", "## Gate", "A critical failure blocks any claim of production-ready autonomous tandem behavior.",
           "", "## Training rule", "Prioritize repeated or high-severity gaps. Do not train on benchmark expected answers verbatim; generate behaviorally equivalent and adversarial examples.",
           "", "## Caveat", report["interpretation"]]
    p.with_name("TRAINING_GAP_V0.2.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out)
    print(p.with_name("TRAINING_GAP_V0.2.md"))

if __name__ == "__main__":
    main()

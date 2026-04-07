import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from pathlib import Path

from causalaudit import ComplianceChecker, CounterfactualEngine, PolicyIR, Trace


def main() -> None:
    path = Path("paper/causalaudit_benchmark_v0.json")
    data = json.loads(path.read_text(encoding="utf-8"))

    checker = ComplianceChecker()
    engine = CounterfactualEngine(checker)

    total = len(data)
    violations_detected = 0
    root_cause_match = 0
    corrective_success = 0

    for item in data:
        trace = Trace.from_dict(item["trace"])
        policy = PolicyIR.from_dict(item["policy"])
        gold_root = item["gold"]["root_cause"]

        result = checker.evaluate(trace, policy)
        if result.verdict == "VIOLATION":
            violations_detected += 1

        explanation = engine.explain(trace, policy)
        if explanation.causal_edit and explanation.causal_edit.event_id == gold_root:
            root_cause_match += 1
        if explanation.compliant_after_corrective:
            corrective_success += 1

    print("Benchmark size:", total)
    print("Violation recall:", round(violations_detected / total, 4))
    print("Root-cause exact match:", round(root_cause_match / total, 4))
    print("Corrective compliance rate:", round(corrective_success / total, 4))


if __name__ == "__main__":
    main()

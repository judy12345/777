import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from causalaudit import ComplianceChecker, CounterfactualEngine, Event, PolicyIR, Trace


def main() -> None:
    trace = Trace(
        events=[
            Event(id="e1", event_type="UserMessage", fields={"text": "send report"}),
            Event(id="e2", event_type="FileAccess", fields={"mode": "read", "content_tag": "sensitive"}),
            Event(
                id="e3",
                event_type="NetworkRequest",
                fields={"domain": "external.example.com", "payload_tag": "tainted", "derived_from": "e2"},
            ),
        ]
    )

    policy = PolicyIR(
        policy_id="p1",
        family="infoflow",
        action="NetworkRequest",
        condition={"payload_tag": "tainted"},
        requirement=["RedactionEvent"],
        timing="before",
        exception={"domain": ["trusted.internal"]},
    )

    checker = ComplianceChecker()
    result = checker.evaluate(trace, policy)
    print("Verdict:", result.verdict)
    print("Evidence chain:", result.evidence_chain_ids)
    print("Details:", result.details)

    engine = CounterfactualEngine(checker)
    explanation = engine.explain(trace, policy)
    print("Causal edit:", explanation.causal_edit)
    print("Corrective edit:", explanation.corrective_edit)
    print("Searched candidates:", explanation.searched_candidates)

    print("Top-3 ranked candidates:")
    for edit, ok in engine.explain_topk(trace, policy, k=3):
        print(" ", edit, "=>", "COMPLIANT" if ok else "VIOLATION")


if __name__ == "__main__":
    main()

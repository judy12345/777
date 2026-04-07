import unittest

from causalaudit import ComplianceChecker, CounterfactualEngine, Event, PolicyIR, Trace


class CausalAuditTests(unittest.TestCase):
    def test_authorization_violation_and_fix(self) -> None:
        trace = Trace(
            events=[
                Event(id="u1", event_type="UserMessage", fields={"text": "email this"}),
                Event(id="n1", event_type="NetworkRequest", fields={"domain": "api.mail.com"}),
            ]
        )
        policy = PolicyIR(
            policy_id="auth-1",
            family="authorization",
            action="NetworkRequest",
            condition={},
            requirement=["ApprovalEvent"],
            timing="before",
        )

        checker = ComplianceChecker()
        result = checker.evaluate(trace, policy)
        self.assertEqual(result.verdict, "VIOLATION")
        self.assertEqual(result.details[0].event_id, "n1")

        cf = CounterfactualEngine(checker).explain(trace, policy)
        self.assertIsNotNone(cf.corrective_edit)
        self.assertTrue(cf.compliant_after_corrective)

    def test_infoflow_taint(self) -> None:
        trace = Trace(
            events=[
                Event(id="f1", event_type="FileAccess", fields={"mode": "read", "content_tag": "sensitive"}),
                Event(id="n1", event_type="NetworkRequest", fields={"domain": "evil.com", "derived_from": "f1"}),
            ]
        )
        policy = PolicyIR(
            policy_id="flow-1",
            family="infoflow",
            action="NetworkRequest",
            condition={"payload_tag": "tainted"},
            requirement=["RedactionEvent"],
            timing="before",
        )
        result = ComplianceChecker().evaluate(trace, policy)
        self.assertEqual(result.verdict, "VIOLATION")
        self.assertIn("n1", result.violating_event_ids)

    def test_sequential_policy(self) -> None:
        trace = Trace(
            events=[
                Event(id="d1", event_type="ToolCall", fields={"tool_name": "DeleteFile"}),
            ]
        )
        policy = PolicyIR(
            policy_id="seq-1",
            family="sequential",
            action="ToolCall",
            condition={"tool_name": "DeleteFile"},
            requirement=["BackupFile"],
            timing="before",
        )
        result = ComplianceChecker().evaluate(trace, policy)
        self.assertEqual(result.verdict, "VIOLATION")

    def test_serialization_roundtrip(self) -> None:
        trace = Trace(
            events=[Event(id="a1", event_type="AgentThought", fields={"text": "x"})],
        )
        policy = PolicyIR(policy_id="p", family="authorization", action="ToolCall")

        trace2 = Trace.from_dict(trace.to_dict())
        policy2 = PolicyIR.from_dict(policy.to_dict())

        self.assertEqual(trace2.events[0].id, "a1")
        self.assertEqual(policy2.policy_id, "p")

    def test_topk_counterfactual(self) -> None:
        trace = Trace(
            events=[
                Event(id="u1", event_type="UserMessage", fields={"text": "send"}),
                Event(id="n1", event_type="NetworkRequest", fields={"domain": "x.com"}),
            ]
        )
        policy = PolicyIR(
            policy_id="auth-2",
            family="authorization",
            action="NetworkRequest",
            requirement=["ApprovalEvent"],
        )
        engine = CounterfactualEngine(ComplianceChecker())
        ranked = engine.explain_topk(trace, policy, k=2)
        self.assertEqual(len(ranked), 2)


if __name__ == "__main__":
    unittest.main()

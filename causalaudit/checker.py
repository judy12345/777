from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .policy import PolicyIR
from .schema import Event, Trace


@dataclass
class ViolationDetail:
    event_id: str
    index: int
    reason: str


@dataclass
class ComplianceResult:
    verdict: str
    violating_event_ids: List[str]
    evidence_chain_ids: List[str]
    message: str
    details: List[ViolationDetail]


class ComplianceChecker:
    def evaluate(self, trace: Trace, policy: PolicyIR) -> ComplianceResult:
        tainted = self._compute_taint(trace)

        violating_event_ids: List[str] = []
        evidence_chain_ids: List[str] = []
        details: List[ViolationDetail] = []

        for idx, event in enumerate(trace.events):
            if event.event_type != policy.action:
                continue
            if not self._condition_match(event, policy, tainted):
                continue
            if self._is_exception(event, policy):
                continue

            ok, evidence = self._requirement_satisfied(trace, idx, event, policy)
            if not ok:
                violating_event_ids.append(event.id)
                evidence_chain_ids.extend(evidence)
                evidence_chain_ids.append(event.id)
                details.append(
                    ViolationDetail(
                        event_id=event.id,
                        index=idx,
                        reason=f"Requirement {policy.requirement} with timing={policy.timing} not satisfied",
                    )
                )

        if violating_event_ids:
            evidence_chain_ids = list(dict.fromkeys(evidence_chain_ids))
            return ComplianceResult(
                verdict="VIOLATION",
                violating_event_ids=violating_event_ids,
                evidence_chain_ids=evidence_chain_ids,
                message=f"{len(violating_event_ids)} violating events detected",
                details=details,
            )

        return ComplianceResult(
            verdict="COMPLIANT",
            violating_event_ids=[],
            evidence_chain_ids=[],
            message="No violation detected",
            details=[],
        )

    def _compute_taint(self, trace: Trace) -> set[str]:
        tainted: set[str] = set()
        for e in trace.events:
            if e.event_type == "FileAccess" and e.get("mode") == "read" and e.get("content_tag") == "sensitive":
                tainted.add(e.id)
            src = e.get("derived_from")
            if src in tainted:
                tainted.add(e.id)
            if e.get("payload_tag") == "tainted":
                tainted.add(e.id)
        return tainted

    def _condition_match(self, event: Event, policy: PolicyIR, tainted: set[str]) -> bool:
        for key, value in policy.condition.items():
            if key == "payload_tag" and value == "tainted":
                if event.id not in tainted and event.get("payload_tag") != "tainted":
                    return False
                continue
            if str(event.get(key)) != value:
                return False
        return True

    def _is_exception(self, event: Event, policy: PolicyIR) -> bool:
        for key, allow_values in policy.exception.items():
            if event.get(key) in allow_values:
                return True
        return False

    def _requirement_satisfied(
        self,
        trace: Trace,
        idx: int,
        event: Event,
        policy: PolicyIR,
    ) -> Tuple[bool, List[str]]:
        if not policy.requirement:
            return True, []

        req_types = set(policy.requirement)
        evidence: List[str] = []

        candidates: Dict[str, range] = {
            "before": range(0, idx),
            "after": range(idx + 1, len(trace.events)),
            "any": range(0, len(trace.events)),
        }
        search_range = candidates[policy.timing]

        if policy.family in {"authorization", "infoflow"}:
            for j in search_range:
                if j == idx:
                    continue
                prior = trace.events[j]
                if prior.event_type in req_types:
                    if prior.get("scope") in {None, "global", event.get("domain"), event.get("tool_name")}:
                        evidence.append(prior.id)
                        return True, evidence
            return False, evidence

        if policy.family == "sequential":
            predecessor = policy.requirement[0]
            for j in range(0, idx):
                prior = trace.events[j]
                if prior.event_type == predecessor:
                    evidence.append(prior.id)
                    return True, evidence
                if prior.event_type == "ToolCall" and prior.get("tool_name") == predecessor:
                    evidence.append(prior.id)
                    return True, evidence
            return False, evidence

        return False, evidence

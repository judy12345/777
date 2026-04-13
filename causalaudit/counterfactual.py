from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from .checker import ComplianceChecker
from .policy import PolicyIR
from .schema import Event, Trace


EDIT_COST = {"delete": 1, "insert": 2, "replace": 3}


@dataclass(frozen=True)
class CounterfactualEdit:
    edit_type: str  # delete|insert|replace
    index: int
    event_id: Optional[str] = None
    replacement: Optional[Event] = None

    @property
    def cost(self) -> int:
        return EDIT_COST[self.edit_type]


@dataclass
class CounterfactualExplanation:
    causal_edit: Optional[CounterfactualEdit]
    corrective_edit: Optional[CounterfactualEdit]
    compliant_after_causal: bool
    compliant_after_corrective: bool
    searched_candidates: int


class CounterfactualEngine:
    def __init__(self, checker: Optional[ComplianceChecker] = None) -> None:
        self.checker = checker or ComplianceChecker()

    def explain(self, trace: Trace, policy: PolicyIR) -> CounterfactualExplanation:
        edits = self._enumerate_candidates(trace, policy)

        causal = self._pick_best(trace, policy, [e for e in edits if e.edit_type == "delete"])
        corrective = self._pick_best(trace, policy, [e for e in edits if e.edit_type in {"insert", "replace"}])

        causal_ok = causal is not None and self.checker.evaluate(self._apply_edit(trace, causal), policy).verdict == "COMPLIANT"
        corrective_ok = (
            corrective is not None
            and self.checker.evaluate(self._apply_edit(trace, corrective), policy).verdict == "COMPLIANT"
        )

        return CounterfactualExplanation(
            causal_edit=causal,
            corrective_edit=corrective,
            compliant_after_causal=causal_ok,
            compliant_after_corrective=corrective_ok,
            searched_candidates=len(edits),
        )

    def _enumerate_candidates(self, trace: Trace, policy: PolicyIR) -> List[CounterfactualEdit]:
        edits: List[CounterfactualEdit] = []
        for i, e in enumerate(trace.events):
            if e.event_type != policy.action:
                continue
            edits.append(CounterfactualEdit(edit_type="delete", index=i, event_id=e.id))

            for req in policy.requirement:
                if req in {"ApprovalEvent", "RedactionEvent"}:
                    ins = Event(
                        id=f"cf_ins_{req.lower()}_{i}",
                        event_type=req,
                        fields={"scope": e.get("domain") or e.get("tool_name") or "global", "source": "counterfactual"},
                    )
                else:
                    ins = Event(
                        id=f"cf_ins_{req.lower()}_{i}",
                        event_type="ToolCall",
                        fields={"tool_name": req, "args": {"source": "counterfactual"}},
                    )
                edits.append(CounterfactualEdit(edit_type="insert", index=i, replacement=ins))

            safe = self._safe_replacement(e, i)
            edits.append(CounterfactualEdit(edit_type="replace", index=i, event_id=e.id, replacement=safe))

        return sorted(edits, key=lambda x: (x.cost, x.index, x.edit_type))

    def _pick_best(
        self,
        trace: Trace,
        policy: PolicyIR,
        candidates: List[CounterfactualEdit],
    ) -> Optional[CounterfactualEdit]:
        for edit in sorted(candidates, key=lambda x: (x.cost, x.index)):
            candidate = self._apply_edit(trace, edit)
            if self.checker.evaluate(candidate, policy).verdict == "COMPLIANT":
                return edit
        return None

    def explain_topk(self, trace: Trace, policy: PolicyIR, k: int = 3) -> List[Tuple[CounterfactualEdit, bool]]:
        ranked: List[Tuple[CounterfactualEdit, bool]] = []
        for edit in self._enumerate_candidates(trace, policy):
            verdict = self.checker.evaluate(self._apply_edit(trace, edit), policy).verdict == "COMPLIANT"
            ranked.append((edit, verdict))
            if len(ranked) >= k:
                break
        return ranked

    def _safe_replacement(self, event: Event, idx: int) -> Event:
        if event.event_type == "NetworkRequest":
            return Event(
                id=f"cf_rep_{idx}",
                event_type="ToolCall",
                fields={"tool_name": "local_store", "args": {"mode": "safe_local_write"}},
            )
        if event.event_type == "ToolCall":
            return Event(
                id=f"cf_rep_{idx}",
                event_type="ToolCall",
                fields={"tool_name": "allowlisted_tool", "args": event.get("args") or {}},
            )
        return Event(id=f"cf_rep_{idx}", event_type="AgentThought", fields={"text": "safe no-op"})

    def _apply_edit(self, trace: Trace, edit: CounterfactualEdit) -> Trace:
        if edit.edit_type == "delete":
            return trace.delete(edit.index)
        if edit.edit_type == "insert":
            assert edit.replacement is not None
            return trace.insert(edit.index, edit.replacement)
        if edit.edit_type == "replace":
            assert edit.replacement is not None
            return trace.replace(edit.index, edit.replacement)
        raise ValueError(f"Unsupported edit type: {edit.edit_type}")

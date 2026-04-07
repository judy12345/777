from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


VALID_FAMILIES = {"authorization", "infoflow", "sequential"}
VALID_TIMING = {"before", "after", "any"}


@dataclass(frozen=True)
class PolicyIR:
    """Structured policy representation."""

    policy_id: str
    family: str
    action: str
    resource: Optional[str] = None
    condition: Dict[str, str] = field(default_factory=dict)
    requirement: List[str] = field(default_factory=list)
    timing: str = "before"
    exception: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.family not in VALID_FAMILIES:
            raise ValueError(f"Unsupported policy family: {self.family}")
        if self.timing not in VALID_TIMING:
            raise ValueError(f"Unsupported timing={self.timing}")
        if not self.policy_id.strip():
            raise ValueError("policy_id cannot be empty")
        if not self.action.strip():
            raise ValueError("action cannot be empty")

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PolicyIR":
        return cls(
            policy_id=str(obj["policy_id"]),
            family=str(obj["family"]),
            action=str(obj["action"]),
            resource=obj.get("resource"),
            condition={str(k): str(v) for k, v in obj.get("condition", {}).items()},
            requirement=[str(x) for x in obj.get("requirement", [])],
            timing=str(obj.get("timing", "before")),
            exception={str(k): [str(v) for v in vals] for k, vals in obj.get("exception", {}).items()},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "family": self.family,
            "action": self.action,
            "resource": self.resource,
            "condition": dict(self.condition),
            "requirement": list(self.requirement),
            "timing": self.timing,
            "exception": {k: list(v) for k, v in self.exception.items()},
        }

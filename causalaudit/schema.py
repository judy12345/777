from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


ALLOWED_EVENT_TYPES = {
    "UserMessage",
    "AgentThought",
    "ToolCall",
    "ToolResult",
    "ApprovalEvent",
    "FileAccess",
    "NetworkRequest",
    "SubAgentCall",
    "RedactionEvent",
}


@dataclass(frozen=True)
class Event:
    id: str
    event_type: str
    timestamp: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.event_type not in ALLOWED_EVENT_TYPES:
            raise ValueError(f"Unsupported event_type={self.event_type!r}")
        if not self.id.strip():
            raise ValueError("event id cannot be empty")

    def get(self, key: str, default: Any = None) -> Any:
        if key == "event_type":
            return self.event_type
        if key == "id":
            return self.id
        return self.fields.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "fields": dict(self.fields),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Event":
        return cls(
            id=str(obj["id"]),
            event_type=str(obj["event_type"]),
            timestamp=obj.get("timestamp"),
            fields=dict(obj.get("fields", {})),
        )


@dataclass
class Trace:
    events: List[Event]

    def __post_init__(self) -> None:
        seen = set()
        for e in self.events:
            if e.id in seen:
                raise ValueError(f"duplicate event id in trace: {e.id}")
            seen.add(e.id)

    def copy(self) -> "Trace":
        return Trace(events=list(self.events))

    def insert(self, idx: int, event: Event) -> "Trace":
        clone = self.copy()
        clone.events.insert(idx, event)
        return Trace(clone.events)

    def delete(self, idx: int) -> "Trace":
        clone = self.copy()
        del clone.events[idx]
        return Trace(clone.events)

    def replace(self, idx: int, event: Event) -> "Trace":
        clone = self.copy()
        clone.events[idx] = event
        return Trace(clone.events)

    def ids(self) -> List[str]:
        return [e.id for e in self.events]

    def to_dict(self) -> Dict[str, Any]:
        return {"events": [e.to_dict() for e in self.events]}

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Trace":
        return cls(events=[Event.from_dict(e) for e in obj.get("events", [])])

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class MessageRole(str, Enum):
    """Defines the source or purpose of a message."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    """Represents a single message in a Wizard interaction."""

    role: MessageRole
    content: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        role: MessageRole,
        content: str,
    ) -> "Message":
        """Create a message with the current UTC timestamp."""

        return cls(
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc),
        )
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4


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


@dataclass
class Request:
    """Represents a unit of work submitted to Wizard."""

    message: Message
    request_id: UUID
    timestamp: datetime

    @classmethod
    def create(cls, message: Message) -> "Request":
        """Create a request with a unique ID and current UTC timestamp."""

        return cls(
            message=message,
            request_id=uuid4(),
            timestamp=datetime.now(timezone.utc),
        )

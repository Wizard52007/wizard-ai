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

@dataclass
class Response:
    """Represents Wizard's response to a request."""

    request_id: UUID
    content: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        request_id: UUID,
        content: str,
    ) -> "Response":
        """Create a response with the current UTC timestamp."""

        return cls(
            request_id=request_id,
            content=content,
            timestamp=datetime.now(timezone.utc),
        )


@dataclass
class ToolRequest:
    """Represents a request to execute a specific tool."""

    request_id: UUID
    tool_name: str
    arguments: dict[str, object]
    timestamp: datetime

    @classmethod
    def create(
        cls,
        request_id: UUID,
        tool_name: str,
        arguments: dict[str, object],
    ) -> "ToolRequest":
        """Create a tool request with the current UTC timestamp."""

        return cls(
            request_id=request_id,
            tool_name=tool_name,
            arguments=arguments,
            timestamp=datetime.now(timezone.utc),
        )



@dataclass
class ToolResult:
    """Represents the result of a tool execution."""

    request_id: UUID
    success: bool
    data: object | None
    error: str | None
    timestamp: datetime

    @classmethod
    def create(
        cls,
        request_id: UUID,
        success: bool,
        data: object | None = None,
        error: str | None = None,
    ) -> "ToolResult":
        """Create a tool result with the current UTC timestamp."""

        return cls(
            request_id=request_id,
            success=success,
            data=data,
            error=error,
            timestamp=datetime.now(timezone.utc),
        )


@dataclass
class ExecutionContext:
    """Represents the working context for a Wizard execution."""

    request: Request
    messages: list[Message]
    tool_results: list[ToolResult]

    @classmethod
    def create(cls, request: Request) -> "ExecutionContext":
        """Create an execution context from a request."""

        return cls(
            request=request,
            messages=[request.message],
            tool_results=[],
        )

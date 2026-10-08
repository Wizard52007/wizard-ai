from wizard.core.types import Message


class ConversationHistory:
    """Stores short-term conversation messages in chronological order."""

    def __init__(self):
        """Initialize an empty conversation history."""

        self._messages: list[Message] = []

    def add(self, message: Message) -> None:
        """Add a message to the conversation history."""

        self._messages.append(message)

    def messages(self) -> list[Message]:
        """Return a copy of the current conversation messages."""

        return list(self._messages)

    def clear(self) -> None:
        """Clear the conversation history."""

        self._messages.clear()
from abc import ABC, abstractmethod

from wizard.core.types import Message


class LLMProvider(ABC):
    """Abstract interface for language model providers."""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
    ) -> Message:
        """Generate an assistant message from the provided messages."""

        raise NotImplementedError

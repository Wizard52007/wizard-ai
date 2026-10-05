from abc import ABC, abstractmethod

from wizard.core.types import ExecutionContext, Response


class Brain(ABC):
    """Abstract interface for Wizard's reasoning layer."""

    @abstractmethod
    def respond(
        self,
        context: ExecutionContext,
    ) -> Response:
        """Generate a response from the current execution context."""

        raise NotImplementedError

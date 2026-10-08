from wizard.brain.brain import Brain
from wizard.core.types import (
    ExecutionContext,
    Message,
    MessageRole,
    Request,
    Response,
)
from wizard.memory.conversation import ConversationHistory


class Orchestrator:
    """Coordinates the execution of Wizard requests."""

    def __init__(
        self,
        brain: Brain,
        history: ConversationHistory | None = None,
    ):
        """Initialize the orchestrator with a Brain and conversation history."""

        self.brain = brain
        self.history = history or ConversationHistory()

    def handle(self, request: Request) -> Response:
        """Process a request using the Brain and conversation history."""

        self.history.add(request.message)

        context = ExecutionContext(
            request=request,
            messages=self.history.messages(),
            tool_results=[],
        )

        response = self.brain.respond(context)

        self.history.add(
            Message.create(
                MessageRole.ASSISTANT,
                response.content,
            )
        )

        return response
from wizard.brain.brain import Brain
from wizard.core.types import (
    ExecutionContext,
    Request,
    Response,
)


class Orchestrator:
    """Coordinates the execution of Wizard requests."""

    def __init__(self, brain: Brain):
        """Initialize the orchestrator with a Brain."""

        self.brain = brain

    def handle(self, request: Request) -> Response:
        """Process a request using the Brain."""

        context = ExecutionContext.create(request)

        return self.brain.respond(context)

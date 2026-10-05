from wizard.core.types import (
    ExecutionContext,
    Request,
    Response,
)


class Orchestrator:
    """Coordinates the execution of Wizard requests."""

    def handle(self, request: Request) -> Response:
        """Process a request and return a response."""

        context = ExecutionContext.create(request)

        return Response.create(
            request_id=context.request.request_id,
            content=context.request.message.content,
        )

from wizard.brain.brain import Brain
from wizard.brain.llm_brain import LLMBrain
from wizard.brain.provider import LLMProvider
from wizard.core.orchestrator import Orchestrator
from wizard.core.types import (
    ExecutionContext,
    Message,
    MessageRole,
    Request,
    Response,
)


class FakeBrain(Brain):
    """Test implementation of the Brain interface."""

    def respond(
        self,
        context: ExecutionContext,
    ) -> Response:
        return Response.create(
            request_id=context.request.request_id,
            content="Fake brain response",
        )


def test_orchestrator_returns_brain_response():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    orchestrator = Orchestrator(FakeBrain())
    response = orchestrator.handle(request)

    assert response.content == "Fake brain response"


def test_orchestrator_preserves_request_id():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    orchestrator = Orchestrator(FakeBrain())
    response = orchestrator.handle(request)

    assert response.request_id == request.request_id


def test_orchestrator_passes_request_to_brain():
    class TrackingBrain(Brain):
        def __init__(self):
            self.received_context = None

        def respond(
            self,
            context: ExecutionContext,
        ) -> Response:
            self.received_context = context

            return Response.create(
                request_id=context.request.request_id,
                content="Tracked",
            )

    message = Message.create(
        MessageRole.USER,
        "What can you do?",
    )

    request = Request.create(message)
    brain = TrackingBrain()

    orchestrator = Orchestrator(brain)
    response = orchestrator.handle(request)

    assert response.content == "Tracked"
    assert brain.received_context is not None
    assert brain.received_context.request == request


def test_orchestrator_works_with_llm_brain():
    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            return Message.create(
                MessageRole.ASSISTANT,
                "Hello from Wizard",
            )

    brain = LLMBrain(TestProvider())
    orchestrator = Orchestrator(brain)

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = orchestrator.handle(request)

    assert response.request_id == request.request_id
    assert response.content == "Hello from Wizard"
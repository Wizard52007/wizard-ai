from wizard.brain.brain import Brain
from wizard.brain.llm_brain import LLMBrain
from wizard.brain.provider import LLMProvider
from wizard.core.orchestrator import Orchestrator
from wizard.memory.conversation import ConversationHistory
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


def test_orchestrator_updates_conversation_history():
    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            return Message.create(
                MessageRole.ASSISTANT,
                "Hello from Wizard",
            )

    history = ConversationHistory()
    brain = LLMBrain(TestProvider())
    orchestrator = Orchestrator(
        brain,
        history,
    )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = orchestrator.handle(request)

    assert response.content == "Hello from Wizard"

    assert history.messages() == [
        message,
        history.messages()[1],
    ]

    assert history.messages()[1].role == MessageRole.ASSISTANT
    assert history.messages()[1].content == "Hello from Wizard"


def test_orchestrator_preserves_multi_turn_conversation():
    responses = [
        "Nice to meet you!",
        "Your name is Sanket.",
    ]

    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            response = responses.pop(0)

            return Message.create(
                MessageRole.ASSISTANT,
                response,
            )

    history = ConversationHistory()
    brain = LLMBrain(TestProvider())
    orchestrator = Orchestrator(
        brain,
        history,
    )

    first_message = Message.create(
        MessageRole.USER,
        "My name is Sanket.",
    )

    first_request = Request.create(first_message)
    orchestrator.handle(first_request)

    second_message = Message.create(
        MessageRole.USER,
        "What is my name?",
    )

    second_request = Request.create(second_message)
    orchestrator.handle(second_request)

    messages = history.messages()

    assert len(messages) == 4

    assert messages[0] == first_message
    assert messages[1].content == "Nice to meet you!"
    assert messages[2] == second_message
    assert messages[3].content == "Your name is Sanket."
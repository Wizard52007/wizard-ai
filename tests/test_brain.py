from wizard.brain.brain import Brain
from wizard.core.types import (
    ExecutionContext,
    Message,
    MessageRole,
    Request,
    Response,
)


def test_brain_cannot_be_instantiated():
    try:
        Brain()
        assert False
    except TypeError:
        pass


def test_concrete_brain_implements_respond():
    class TestBrain(Brain):
        def respond(
            self,
            context: ExecutionContext,
        ) -> Response:
            return Response.create(
                request_id=context.request.request_id,
                content="Test response",
            )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)
    context = ExecutionContext.create(request)

    brain = TestBrain()
    response = brain.respond(context)

    assert response.request_id == request.request_id
    assert response.content == "Test response"


from wizard.brain.llm_brain import LLMBrain
from wizard.brain.provider import LLMProvider


def test_llm_brain_generates_response():
    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            return Message.create(
                MessageRole.ASSISTANT,
                "Hello from Wizard",
            )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)
    context = ExecutionContext.create(request)

    brain = LLMBrain(TestProvider())

    response = brain.respond(context)

    assert response.request_id == request.request_id
    assert response.content == "Hello from Wizard"


def test_llm_brain_passes_context_messages_to_provider():
    received_messages = []

    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            received_messages.extend(messages)

            return Message.create(
                MessageRole.ASSISTANT,
                "Received",
            )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)
    context = ExecutionContext.create(request)

    brain = LLMBrain(TestProvider())

    brain.respond(context)

    assert received_messages == context.messages
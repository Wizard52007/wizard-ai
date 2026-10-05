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

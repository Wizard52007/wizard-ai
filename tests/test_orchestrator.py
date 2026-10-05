from wizard.core.orchestrator import Orchestrator
from wizard.core.types import Message, MessageRole, Request


def test_orchestrator_returns_response():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    orchestrator = Orchestrator()
    response = orchestrator.handle(request)

    assert response.content == "Hello Wizard"


def test_orchestrator_preserves_request_id():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    orchestrator = Orchestrator()
    response = orchestrator.handle(request)

    assert response.request_id == request.request_id

def test_orchestrator_processes_request_message():
    message = Message.create(
        MessageRole.USER,
        "What can you do?",
    )

    request = Request.create(message)

    orchestrator = Orchestrator()
    response = orchestrator.handle(request)

    assert response.content == request.message.content

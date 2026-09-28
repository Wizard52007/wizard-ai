from datetime import timezone
from uuid import UUID
from wizard.core.types import Message, MessageRole, Request, Response


def test_message_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    assert message.role == MessageRole.USER
    assert message.content == "Hello Wizard"


def test_message_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    assert message.timestamp.tzinfo == timezone.utc


def test_message_roles():
    assert MessageRole.SYSTEM.value == "system"
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"
    assert MessageRole.TOOL.value == "tool"


def test_request_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    assert request.message == message
    assert isinstance(request.request_id, UUID)


def test_request_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    assert request.timestamp.tzinfo == timezone.utc


def test_requests_have_unique_ids():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request_one = Request.create(message)
    request_two = Request.create(message)

    assert request_one.request_id != request_two.request_id


def test_response_creation():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello! How can I help?",
    )

    assert response.request_id == request.request_id
    assert response.content == "Hello! How can I help?"


def test_response_timestamp_is_utc():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello!",
    )

    assert response.timestamp.tzinfo == timezone.utc


def test_response_links_to_request():
    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    request = Request.create(message)

    response = Response.create(
        request.request_id,
        "Hello!",
    )

    assert response.request_id == request.request_id

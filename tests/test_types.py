from datetime import timezone

from wizard.core.types import Message, MessageRole


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
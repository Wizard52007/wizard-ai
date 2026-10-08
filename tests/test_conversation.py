from wizard.core.types import Message, MessageRole
from wizard.memory.conversation import ConversationHistory


def test_conversation_history_starts_empty():
    history = ConversationHistory()

    assert history.messages() == []


def test_conversation_history_adds_messages():
    history = ConversationHistory()

    user_message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    assistant_message = Message.create(
        MessageRole.ASSISTANT,
        "Hello!",
    )

    history.add(user_message)
    history.add(assistant_message)

    assert history.messages() == [
        user_message,
        assistant_message,
    ]


def test_conversation_history_preserves_order():
    history = ConversationHistory()

    first = Message.create(
        MessageRole.USER,
        "First",
    )

    second = Message.create(
        MessageRole.USER,
        "Second",
    )

    third = Message.create(
        MessageRole.ASSISTANT,
        "Third",
    )

    history.add(first)
    history.add(second)
    history.add(third)

    messages = history.messages()

    assert messages[0] == first
    assert messages[1] == second
    assert messages[2] == third


def test_conversation_history_returns_copy():
    history = ConversationHistory()

    message = Message.create(
        MessageRole.USER,
        "Hello",
    )

    history.add(message)

    messages = history.messages()
    messages.clear()

    assert history.messages() == [message]


def test_conversation_history_can_be_cleared():
    history = ConversationHistory()

    message = Message.create(
        MessageRole.USER,
        "Hello",
    )

    history.add(message)

    history.clear()

    assert history.messages() == []
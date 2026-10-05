import pytest

from wizard.brain.provider import LLMProvider
from wizard.core.types import Message, MessageRole


def test_llm_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        LLMProvider()


def test_concrete_provider_implements_generate():
    class TestProvider(LLMProvider):
        def generate(
            self,
            messages: list[Message],
        ) -> Message:
            return Message.create(
                MessageRole.ASSISTANT,
                "Test response",
            )

    provider = TestProvider()

    response = provider.generate(
        [
            Message.create(
                MessageRole.USER,
                "Hello Wizard",
            )
        ]
    )

    assert response.role == MessageRole.ASSISTANT
    assert response.content == "Test response"


def test_provider_receives_messages():
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

    provider = TestProvider()
    provider.generate([message])

    assert received_messages == [message]

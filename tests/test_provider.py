import pytest

from wizard.brain.provider import LLMProvider
from wizard.core.types import Message, MessageRole
from openai import OpenAIError
from wizard.config import settings


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


from unittest.mock import MagicMock

from wizard.brain.openai_provider import OpenAIProvider


def test_openai_provider_generates_message():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.output_text = "Hello from OpenAI"

    mock_client.responses.create.return_value = mock_response

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        client=mock_client,
    )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    response = provider.generate([message])

    assert response.role == MessageRole.ASSISTANT
    assert response.content == "Hello from OpenAI"


def test_openai_provider_sends_correct_request():
    mock_client = MagicMock()

    mock_response = MagicMock()
    mock_response.output_text = "Test response"

    mock_client.responses.create.return_value = mock_response

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        client=mock_client,
    )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    provider.generate([message])

    mock_client.responses.create.assert_called_once_with(
        model="test-model",
        input=[
            {
                "role": "user",
                "content": "Hello Wizard",
            }
        ],
    )


def test_openai_provider_handles_api_error():
    mock_client = MagicMock()

    mock_client.responses.create.side_effect = OpenAIError(
        "API request failed"
    )

    provider = OpenAIProvider(
        api_key="test-key",
        model="test-model",
        client=mock_client,
    )

    message = Message.create(
        MessageRole.USER,
        "Hello Wizard",
    )

    with pytest.raises(RuntimeError, match="OpenAI provider request failed."):
        provider.generate([message])


def test_openai_provider_uses_settings():
    provider = OpenAIProvider(
        client=MagicMock(),
    )

    assert provider.api_key == settings.llm_api_key
    assert provider.model == settings.llm_model
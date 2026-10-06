from openai import OpenAI, OpenAIError

from wizard.brain.provider import LLMProvider
from wizard.core.types import Message, MessageRole
from wizard.config import settings


class OpenAIProvider(LLMProvider):
    """LLM provider implementation using the OpenAI Responses API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        client: OpenAI | None = None,
   ):
        """Initialize the OpenAI provider."""

        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model

        if not self.api_key:
            raise ValueError("OpenAI API key is not configured.")

        if not self.model:
            raise ValueError("OpenAI model is not configured.")

        self.client = client or OpenAI(api_key=self.api_key)

    def generate(
        self,
        messages: list[Message],
    ) -> Message:
        """Generate an assistant message using OpenAI."""

        input_messages = [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in messages
        ]

        try:
            response = self.client.responses.create(
                model=self.model,
                input=input_messages,
            )
        except OpenAIError as exc:
            raise RuntimeError(
                "OpenAI provider request failed."
            ) from exc

        return Message.create(
            role=MessageRole.ASSISTANT,
            content=response.output_text,
        )
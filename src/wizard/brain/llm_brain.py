from wizard.brain.brain import Brain
from wizard.brain.instructions import WIZARD_SYSTEM_INSTRUCTIONS
from wizard.brain.provider import LLMProvider
from wizard.core.types import (
    ExecutionContext,
    Message,
    MessageRole,
    Response,
)


class LLMBrain(Brain):
    """Brain implementation that uses an LLM provider for responses."""

    def __init__(self, provider: LLMProvider):
        """Initialize the brain with an LLM provider."""

        self.provider = provider

    def respond(
        self,
        context: ExecutionContext,
    ) -> Response:
        """Generate a Wizard response using the configured provider."""

        system_message = Message.create(
            role=MessageRole.SYSTEM,
            content=WIZARD_SYSTEM_INSTRUCTIONS,
        )

        messages = [
            system_message,
            *context.messages,
        ]

        message = self.provider.generate(messages)

        return Response.create(
            request_id=context.request.request_id,
            content=message.content,
        )
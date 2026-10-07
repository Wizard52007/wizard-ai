from wizard.brain.llm_brain import LLMBrain
from wizard.brain.openai_provider import OpenAIProvider
from wizard.core.orchestrator import Orchestrator
from wizard.core.types import Message, MessageRole, Request
from wizard.logger import get_logger


logger = get_logger(__name__)


def main():
    """Start the Wizard command-line interface."""

    logger.info("Wizard started.")

    provider = OpenAIProvider()
    brain = LLMBrain(provider)
    orchestrator = Orchestrator(brain)

    logger.info("Wizard is ready.")

    print("Wizard is ready. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nWizard shutting down.")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Wizard shutting down.")
            break

        if not user_input:
            continue

        message = Message.create(
            MessageRole.USER,
            user_input,
        )

        request = Request.create(message)

        try:
            response = orchestrator.handle(request)
            print(f"Wizard: {response.content}")
        except RuntimeError as exc:
            logger.error("Wizard request failed: %s", exc)
            print("Wizard: Sorry, I couldn't process that request.")


if __name__ == "__main__":
    main()
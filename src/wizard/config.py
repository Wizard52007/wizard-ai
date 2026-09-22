import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Application configuration for Wizard."""

    def __init__(self):
        self.environment = os.getenv(
            "WIZARD_ENVIRONMENT",
            "development",
        )

        self.log_level = os.getenv(
            "WIZARD_LOG_LEVEL",
            "INFO",
        )

        self.llm_api_key = os.getenv(
            "WIZARD_LLM_API_KEY",
        )


settings = Settings()
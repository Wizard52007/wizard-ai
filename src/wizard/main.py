from wizard.config import settings
from wizard.logger import get_logger


logger = get_logger(__name__)


def main():
    logger.info("Wizard started.")
    logger.info("Configuration loaded.")
    logger.debug(f"Environment: {settings.environment}")
    logger.debug(f"Log level: {settings.log_level}")


if __name__ == "__main__":
    main()
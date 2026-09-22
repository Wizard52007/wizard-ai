from wizard.logger import get_logger


def test_logger_has_handlers():
    logger = get_logger("test_logger")

    assert len(logger.handlers) == 2


def test_logger_has_console_and_file_handlers():
    logger = get_logger("test_logger")

    handler_types = {
        type(handler).__name__
        for handler in logger.handlers
    }

    assert "StreamHandler" in handler_types
    assert "FileHandler" in handler_types
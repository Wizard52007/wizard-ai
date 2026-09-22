from wizard.config import settings


def test_environment_is_loaded():
    assert settings.environment == "development"


def test_log_level_is_loaded():
    assert settings.log_level == "INFO"


def test_missing_llm_api_key_is_none():
    assert settings.llm_api_key is None
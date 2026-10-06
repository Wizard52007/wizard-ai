from wizard.config import settings


def test_environment_is_loaded():
    assert settings.environment == "development"


def test_log_level_is_loaded():
    assert settings.log_level == "INFO"


def test_missing_llm_api_key_is_none(monkeypatch):

    monkeypatch.delenv("WIZARD_LLM_API_KEY", raising=False)

    from wizard.config import Settings

    test_settings = Settings()

    assert test_settings.llm_api_key is None
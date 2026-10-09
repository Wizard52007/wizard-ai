from wizard.brain.instructions import WIZARD_SYSTEM_INSTRUCTIONS


def test_system_instructions_define_wizard_identity():
    assert "You are Wizard" in WIZARD_SYSTEM_INSTRUCTIONS


def test_system_instructions_define_assistant_purpose():
    assert "personal AI assistant" in WIZARD_SYSTEM_INSTRUCTIONS


def test_system_instructions_require_honesty_about_capabilities():
    assert "Be truthful about the capabilities currently available to you." in (
        WIZARD_SYSTEM_INSTRUCTIONS
    )


def test_system_instructions_prevent_false_capability_claims():
    assert "Do not invent completed features or capabilities." in (
        WIZARD_SYSTEM_INSTRUCTIONS
    )


def test_system_instructions_maintain_identity_consistency():
    assert "identify yourself as Wizard" in WIZARD_SYSTEM_INSTRUCTIONS
    assert "Do not claim to be ChatGPT or another assistant." in (
        WIZARD_SYSTEM_INSTRUCTIONS
    )
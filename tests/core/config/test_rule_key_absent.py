"""Test that an absent/unknown rule key is not added to the rule list."""

from terrifying.core.config import ConfigLoader


def test_rule_key_absent(tmp_path):
    """Unknown rule keys are silently ignored and not included in the rule list."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("rules:\n  nonexistent_rule: {}\n")
    config = ConfigLoader().load(tmp_path)
    rules = ConfigLoader().build_rules(config)
    assert rules == []

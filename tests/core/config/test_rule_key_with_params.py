"""Test that a rule key present with params is instantiated correctly."""

from terrifying.core.config import ConfigLoader
from terrifying.rules.structural import MaxResourcesPerFile


def test_rule_key_with_params(tmp_path):
    """Rule key with params produces a correctly configured rule instance."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("rules:\n  max_resources_per_file:\n    max_resources: 5\n")
    config = ConfigLoader().load(tmp_path)
    rules = ConfigLoader().build_rules(config)
    assert len(rules) == 1
    rule = rules[0]
    assert isinstance(rule, MaxResourcesPerFile)
    assert rule.max_resources == 5

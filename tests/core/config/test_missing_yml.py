"""Test that a missing terrifying.yml returns an empty Config without raising."""

from terrifying.core.config import Config, ConfigLoader


def test_missing_yml(tmp_path):
    """Missing terrifying.yml returns an empty Config with no exception."""
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config, Config)
    assert config.rules == {}
    assert config.custom_path is None
    assert config.opa is None
    assert config.c7n is None

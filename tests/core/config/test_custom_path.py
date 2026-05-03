"""Test that custom.path in terrifying.yml sets Config.custom_path."""

from pathlib import Path

from terrifying.core.config import ConfigLoader


def test_custom_path(tmp_path):
    """custom.path key populates Config.custom_path."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("custom:\n  path: ./my_rules\n")
    config = ConfigLoader().load(tmp_path)
    assert config.custom_path == Path("./my_rules")

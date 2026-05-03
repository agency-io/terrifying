"""Test that policies.c7n in terrifying.yml sets Config.c7n_policy_dir."""

from pathlib import Path

from terrifying.core.config import ConfigLoader


def test_c7n_policy_dir(tmp_path):
    """policies.c7n key populates Config.c7n_policy_dir."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("policies:\n  c7n: ./c7n_policies\n")
    config = ConfigLoader().load(tmp_path)
    assert config.c7n_policy_dir == Path("./c7n_policies")

"""Test that policies.opa in terrifying.yml sets Config.opa_policy_dir."""

from pathlib import Path

from terrifying.core.config import ConfigLoader


def test_opa_policy_dir(tmp_path):
    """policies.opa key populates Config.opa_policy_dir."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("policies:\n  opa: ./opa_policies\n")
    config = ConfigLoader().load(tmp_path)
    assert config.opa_policy_dir == Path("./opa_policies")

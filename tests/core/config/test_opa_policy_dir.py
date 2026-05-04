"""Test that policies.opa in terrifying.yml sets Config.opa as a PolicyConfig."""

from terrifying.core.config import ConfigLoader, PolicyConfig


def test_opa_policy_dir(tmp_path):
    """policies.opa plain string key populates Config.opa with a PolicyConfig."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("policies:\n  opa: ./opa_policies\n")
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config.opa, PolicyConfig)
    assert config.opa.path == tmp_path / "opa_policies"

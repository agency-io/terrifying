"""Test that policies.c7n in terrifying.yml sets Config.c7n as a PolicyConfig."""

from terrifying.core.config import ConfigLoader, PolicyConfig


def test_c7n_policy_dir(tmp_path):
    """policies.c7n plain string key populates Config.c7n with a PolicyConfig."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("policies:\n  c7n: ./c7n_policies\n")
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config.c7n, PolicyConfig)
    assert config.c7n.path == tmp_path / "c7n_policies"

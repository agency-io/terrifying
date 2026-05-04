"""Test that a plain string policies.opa value is backward-compatible."""

from terrifying.core.config import ConfigLoader, PolicyConfig


def test_backward_compat_plain_path(tmp_path):
    """Plain string policies.opa produces a PolicyConfig with empty params."""
    yml = tmp_path / "terrifying.yml"
    yml.write_text("policies:\n  opa: ./opa_dir\n")
    config = ConfigLoader().load(tmp_path)
    assert isinstance(config.opa, PolicyConfig)
    assert config.opa.params == {}
    assert config.opa.policies == {}

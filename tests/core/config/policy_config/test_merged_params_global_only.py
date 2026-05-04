"""Test that merged_params returns global params when no policy override exists."""

from pathlib import Path

from terrifying.core.config import PolicyConfig


def test_merged_params_global_only():
    """No policy override — global params are returned unchanged."""
    pc = PolicyConfig(path=Path("/some/dir"), params={"env": "prod"})
    result = pc.merged_params("any_policy")
    assert result == {"env": "prod"}

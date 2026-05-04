"""Test that policy-level params override global params."""

from pathlib import Path

from terrifying.core.config import PolicyConfig


def test_merged_params_policy_override():
    """Per-policy param overrides the global param of the same key."""
    pc = PolicyConfig(
        path=Path("/some/dir"),
        params={"env": "prod"},
        policies={"my_policy": {"params": {"env": "staging"}}},
    )
    result = pc.merged_params("my_policy")
    assert result == {"env": "staging"}

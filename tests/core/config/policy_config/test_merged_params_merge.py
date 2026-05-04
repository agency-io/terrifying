"""Test that non-overlapping global and per-policy keys are both present."""

from pathlib import Path

from terrifying.core.config import PolicyConfig


def test_merged_params_merge():
    """Non-overlapping keys from global and policy-level are both present."""
    pc = PolicyConfig(
        path=Path("/some/dir"),
        params={"global_key": "global_val"},
        policies={"my_policy": {"params": {"policy_key": "policy_val"}}},
    )
    result = pc.merged_params("my_policy")
    assert result == {"global_key": "global_val", "policy_key": "policy_val"}

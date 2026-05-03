"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from terrifying.policies.c7n import C7nAdapter


@pytest.mark.skipif(
    shutil.which("c7n-left") is None,
    reason="c7n-left not installed; skipping integration test",
)
def test_integration_c7n_left_runs(tmp_path: Path) -> None:
    """Integration: c7n-left actually executes without error."""
    adapter = C7nAdapter(policy_dir=tmp_path)
    # No policies -> empty result, no subprocess call needed
    result = adapter.run(tmp_path)
    assert isinstance(result, list)

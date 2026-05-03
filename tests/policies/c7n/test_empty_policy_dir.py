"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from terrifying.policies.c7n import C7nAdapter


def test_empty_policy_dir_returns_empty_and_no_subprocess(tmp_path: Path) -> None:
    """No subprocess call should be made when the policy directory is empty."""
    adapter = C7nAdapter(policy_dir=tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run") as mock_run:
        result = adapter.run(Path("/some/tf/dir"))
    assert result == []
    mock_run.assert_not_called()

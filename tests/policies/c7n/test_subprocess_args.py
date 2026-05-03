"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.policies.c7n import C7nAdapter

_NO_MATCHES: list = []


def _make_adapter(tmp_path: Path, *, with_policy: bool = True) -> C7nAdapter:
    if with_policy:
        (tmp_path / "policy.yml").write_text("policies: []\n")
    return C7nAdapter(policy_dir=tmp_path)


def _mock_run(stdout_data: object) -> MagicMock:
    return MagicMock(stdout=json.dumps(stdout_data), returncode=0)


def test_subprocess_called_with_correct_args(tmp_path: Path) -> None:
    """subprocess.run should be invoked with the expected c7n-left command."""
    tf_dir = Path("/some/terraform")
    adapter = _make_adapter(tmp_path)
    with patch(
        "terrifying.policies.c7n.subprocess.run", return_value=_mock_run(_NO_MATCHES)
    ) as mock_run:
        adapter.run(tf_dir)

    mock_run.assert_called_once()
    args, kwargs = mock_run.call_args
    cmd = args[0]
    assert cmd[0] == "c7n-left"
    assert "--policy" in cmd
    assert str(tmp_path) in cmd
    assert "--directory" in cmd
    assert str(tf_dir) in cmd
    assert "--output" in cmd
    assert "json" in cmd
    assert kwargs.get("capture_output") is True
    assert kwargs.get("text") is True
    assert kwargs.get("check") is False

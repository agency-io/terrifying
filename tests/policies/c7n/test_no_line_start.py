"""Tests for the C7nAdapter policy adapter."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from terrifying.policies.c7n import C7nAdapter


def _make_adapter(tmp_path: Path, *, with_policy: bool = True) -> C7nAdapter:
    if with_policy:
        (tmp_path / "policy.yml").write_text("policies: []\n")
    return C7nAdapter(policy_dir=tmp_path)


def _mock_run(stdout_data: object) -> MagicMock:
    return MagicMock(stdout=json.dumps(stdout_data), returncode=0)


def test_no_line_start_gives_none(tmp_path: Path) -> None:
    """When __tfmeta exists but has no line_start, line should be None."""
    data = [
        {
            "policy": {"name": "require-tags"},
            "resources": [
                {
                    "__tfmeta": {"filename": "main.tf"},
                    "type": "aws_s3_bucket",
                    "name": "bucket",
                }
            ],
        }
    ]
    adapter = _make_adapter(tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=_mock_run(data)):
        violations = adapter.run(Path("/tf"))

    assert violations[0].line is None

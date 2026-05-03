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


def test_multiple_resources_produce_multiple_violations(tmp_path: Path) -> None:
    """Each resource entry should result in its own Violation."""
    data = [
        {
            "policy": {"name": "require-tags"},
            "resources": [
                {
                    "__tfmeta": {"filename": "a.tf", "line_start": 1},
                    "type": "aws_s3_bucket",
                    "name": "bucket_a",
                },
                {
                    "__tfmeta": {"filename": "b.tf", "line_start": 10},
                    "type": "aws_instance",
                    "name": "web",
                },
            ],
        }
    ]
    adapter = _make_adapter(tmp_path)
    with patch("terrifying.policies.c7n.subprocess.run", return_value=_mock_run(data)):
        violations = adapter.run(Path("/tf"))

    assert len(violations) == 2
